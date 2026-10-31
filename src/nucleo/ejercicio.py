"""Carga y validacion del ejercicio (su definicion vive en parameters/<n>/, ver nucleo/definicion.py).

Un ejercicio NO es codigo: es un dato que declara que articulaciones
mirar y como reconocer una repeticion. Agregar manguito rotador o flexion de
tobillo es crear su definicion, nunca tocar el motor.

Todo lo que se puede validar se valida al cargar. Un error de dedo en un nombre
de landmark revienta antes de encender la camara, no a mitad de la serie.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.nucleo import definicion as DEF
from src.nucleo.landmarks import resolve

VALID_SOURCES = {"pose"}
VALID_TYPES = {"angle", "distance_ratio", "proporcion"}
VALID_REDUCE = {"mean", "min", "max"}
VALID_DIRECTION = {"down_up", "up_down"}
UNIDAD_POR_TIPO = {"angle": "deg", "distance_ratio": "ratio", "proporcion": "%"}


@dataclass
class Exercise:
    slug: str
    name: str
    source: str
    features: list[dict]
    signal_features: list[str]
    signal_reduce: str = "mean"
    direction: str = "down_up"
    min_duration_ms: int = 600
    max_duration_ms: int = 8000
    description: str = ""
    # catalogo de kpoints (editor de Puntos / cortador): que puntos se usan
    # para el dataset y para el clasificador en vivo
    kpoints: list[dict] | None = None
    # de que ejercicio se toma el clasificador entrenado (output/models):
    # por defecto el propio slug. Permite puntuar en vivo con un modelo
    # entrenado con clips de otro ejercicio que usa el MISMO catalogo de puntos.
    clasificador: str | None = None
    # reglas de postura (angulo entre dos puntos, color verde/rojo en el video): ver nucleo/reglas.py
    reglas: list[dict] = field(default_factory=list)
    # clase de clips ('bien') de la que se crea la base sola si no hay una grabada: ver evaluacion/base_clip.py
    base_clip: str = ""

    @property
    def feature_names(self) -> list[str]:
        return [f["name"] for f in self.features]

    def unit_of(self, name: str) -> str:
        for f in self.features:
            if f["name"] == name:
                return UNIDAD_POR_TIPO.get(f["type"], "ratio")
        return ""

    def to_dict(self) -> dict:
        return {
            "slug": self.slug,
            "name": self.name,
            "source": self.source,
            "description": self.description.strip(),
            "features": self.feature_names,
            "units": [self.unit_of(n) for n in self.feature_names],
            "kpoints": len(self.kpoints or []),
            "clasificador": self.clasificador or self.slug,
            "direction": self.direction,
            "min_duration_ms": self.min_duration_ms,
            "max_duration_ms": self.max_duration_ms,
        }


def _reglas(slug, data):
    from src.nucleo import reglas as REGLAS
    try:
        return REGLAS.validar(data.get("reglas"))
    except ValueError as e:
        raise ValueError(f"{slug}: {e}") from None


def load_exercise(slug: str) -> Exercise:
    data = DEF.leer(slug)
    if data is None:
        raise FileNotFoundError(f"No existe el ejercicio '{slug}'")
    return construir(slug, data)


def construir(slug: str, data: dict) -> Exercise:
    """Valida una definicion (leida o por guardar) y arma el Exercise."""

    for key in ("name", "source", "features"):
        if key not in data:
            raise ValueError(f"{slug}: falta la clave obligatoria '{key}'")

    source = data["source"]
    if source not in VALID_SOURCES:
        raise ValueError(f"{slug}: source debe ser uno de {sorted(VALID_SOURCES)}")

    # las features con activo:false se guardan en la definicion (el editor de Puntos
    # las sigue mostrando para poder reactivarlas) pero no entran a Exercise.features
    # -- ni el pipeline en vivo ni el entrenamiento offline las calculan.
    features_activas = [f for f in data["features"] if f.get("activo", True)]

    nombres_kp = {kp["nombre"] for kp in data.get("kpoints") or []}
    nombres: list[str] = []
    for spec in features_activas:
        for key in ("name", "type", "points"):
            if key not in spec:
                raise ValueError(f"{slug}: feature sin '{key}': {spec}")
        if spec["type"] not in VALID_TYPES:
            raise ValueError(f"{slug}: tipo invalido {spec['type']!r}")
        if spec["name"] in nombres:
            raise ValueError(f"{slug}: feature duplicada {spec['name']!r}")
        nombres.append(spec["name"])

        n_esperado = {"angle": 3, "distance_ratio": 2, "proporcion": 2}[spec["type"]]
        if len(spec["points"]) != n_esperado:
            raise ValueError(
                f"{slug}: '{spec['name']}' de tipo {spec['type']} "
                f"necesita exactamente {n_esperado} puntos"
            )
        if spec["type"] == "distance_ratio" and len(spec.get("reference", [])) != 2:
            raise ValueError(f"{slug}: '{spec['name']}' necesita 'reference' con 2 puntos")
        if spec["type"] == "proporcion":
            cadena = spec.get("cadena") or []
            if len(cadena) < 3:
                raise ValueError(f"{slug}: '{spec['name']}' necesita 'cadena' con 3+ puntos")
            if list(spec["points"]) not in [[a, b] for a, b in zip(cadena, cadena[1:])]:
                raise ValueError(
                    f"{slug}: '{spec['name']}': 'points' debe ser un tramo consecutivo de 'cadena'"
                )

        for p in list(spec["points"]) + list(spec.get("reference", [])) + list(spec.get("cadena", [])):
            if p not in nombres_kp:   # un nombre puede ser un landmark crudo o un kpoint del catalogo
                resolve(p, source)

    signal = data.get("signal", {})
    signal_features = signal.get("features") or nombres
    faltantes = [n for n in signal_features if n not in nombres]
    if faltantes:
        raise ValueError(f"{slug}: signal.features desconocidas: {faltantes}")

    reduce = signal.get("reduce", "mean")
    if reduce not in VALID_REDUCE:
        raise ValueError(f"{slug}: signal.reduce debe ser uno de {sorted(VALID_REDUCE)}")

    seg = data.get("segmentation", {})
    direction = seg.get("direction", "down_up")
    if direction not in VALID_DIRECTION:
        raise ValueError(
            f"{slug}: segmentation.direction debe ser uno de {sorted(VALID_DIRECTION)}"
        )

    return Exercise(
        slug=slug,
        name=data["name"],
        source=source,
        features=features_activas,
        signal_features=list(signal_features),
        signal_reduce=reduce,
        direction=direction,
        min_duration_ms=int(seg.get("min_duration_ms", 600)),
        max_duration_ms=int(seg.get("max_duration_ms", 8000)),
        description=data.get("description", ""),
        kpoints=data.get("kpoints") or [],
        clasificador=data.get("clasificador"),
        reglas=_reglas(slug, data),
        base_clip=str(data.get("base_clip") or ""),
    )


def load_all() -> dict[str, Exercise]:
    """Todos los ejercicios activos, indexados por slug."""
    return {slug: load_exercise(slug) for slug in DEF.slugs()}


# --- catalogo de puntos del ejercicio (lo leen deteccion offline y el dataset) ---

def leer_def(exercise):
    """La definicion del ejercicio (dict) o None."""
    try:
        return DEF.leer(exercise)
    except Exception:
        return None


def kpoints_de_ejercicio(exercise):
    """El catalogo 'kpoints' de la definicion (lista vacia si no tiene)."""
    return (leer_def(exercise) or {}).get("kpoints") or []


def resolver_features(features, kpoints):
    """Un feature de la definicion puede nombrar un landmark crudo (LEFT_ELBOW) aunque el ejercicio tenga catalogo de
    kpoints con otro nombre: se traduce al nombre del kpoint que lo representa.
    Sin esto, esos angulos no se encuentran en los datos."""
    if not kpoints:
        return [dict(f) for f in features]
    nombres = {k["nombre"] for k in kpoints}
    por_lm = {}
    for k in kpoints:
        o = k.get("origen") or {}
        if o.get("tipo") == "landmark":
            por_lm.setdefault(o.get("landmark"), k["nombre"])

    def traducir(p):
        if p in nombres or p not in por_lm:
            return p
        return por_lm[p]

    out = []
    for f in features:
        g = dict(f)
        for clave in ("points", "reference", "cadena"):
            if g.get(clave):
                g[clave] = [traducir(p) for p in g[clave]]
        out.append(g)
    return out


def features_de_ejercicio(exercise):
    """Los angulos y proporciones ACTIVADOS de la definicion, con sus puntos ya traducidos a kpoints (lista vacia si no tiene)."""
    data = leer_def(exercise) or {}
    activos = [f for f in data.get("features") or [] if f.get("activo", True) is not False]
    return resolver_features(activos, data.get("kpoints") or [])


def puntos_de_ejercicio(exercise: str) -> list[str] | None:
    """Los puntos que le importan a este ejercicio, en orden. Si la definicion ya
    tiene catalogo de 'kpoints' (editor de Puntos), son ESOS nombres -- es lo
    que src/procesamiento/offline.py guarda en el .npz. Si no, los landmarks que aparecen en
    'points'/'reference' de sus features, en orden de aparicion.
    None si no se pudo leer la definicion -- quien llama debe caer entonces a la
    lista completa que trae el .npz (mejor eso que perder datos)."""
    data = leer_def(exercise)
    if data is None:
        return None
    if data.get("kpoints"):
        return [kp["nombre"] for kp in data["kpoints"]]
    vistos, orden = set(), []
    for feat in data.get("features") or []:
        for n in [*(feat.get("points") or []), *(feat.get("reference") or [])]:
            if n not in vistos:
                vistos.add(n)
                orden.append(n)
    return orden or None
