"""Capa 3: landmarks -> vector de features invariantes.

Dos reglas que sostienen todo el proyecto:

1. Nunca comparamos coordenadas crudas. Comparamos angulos articulares
   (invariantes a posicion, escala y distancia a la camara) y razones de
   distancia divididas por un segmento del propio cuerpo.
2. Los angulos salen de los *world landmarks* (metros, origen en la entidad),
   no de las coordenadas de pantalla: eso elimina la perspectiva.

Optimizacion: el YAML se compila UNA vez a arrays de indices. En caliente no
hay lookups de diccionario ni bucles de Python, solo operaciones numpy sobre
todas las features a la vez.
"""

from __future__ import annotations

import numpy as np

from src.nucleo.ejercicio import UNIDAD_POR_TIPO
from src.nucleo.landmarks import es_landmark, resolve
from src.nucleo.tipos import FeatureVec, Landmarks
from src.procesamiento.medidas.angulos import angulo_interior
from src.procesamiento.puntos import kpoints as KP

# --- Formas escalares, para tests y uso puntual ---------------------------

def angle_deg(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
    """Angulo interior A-B-C en grados, con vertice en B."""
    return float(angulo_interior(a, b, c))


def distance(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b))


# --- Extractor compilado --------------------------------------------------

def _nombres_de(spec: dict) -> list[str]:
    return [*spec["points"], *spec.get("reference", []), *spec.get("cadena", [])]


def _angulos_deg(P: np.ndarray, idx: np.ndarray) -> np.ndarray:
    """(K,3) indices de A-B-C -> (K,) angulos en grados. NaN si A o C caen sobre B."""
    a, b, c = P[idx[:, 0]], P[idx[:, 1]], P[idx[:, 2]]
    ba, bc = a - b, c - b
    den = np.linalg.norm(ba, axis=1) * np.linalg.norm(bc, axis=1)
    seguro = den > 1e-9
    cos = np.einsum("ij,ij->i", ba, bc) / np.where(seguro, den, 1.0)
    ang = np.degrees(np.arccos(np.clip(cos, -1.0, 1.0)))
    return np.where(seguro, ang, np.nan)


class _Banco:
    """Un grupo de features del YAML compilado a arrays de indices. 'indice' traduce el nombre
    de un punto a su fila en P: los landmarks crudos de una fuente, o los kpoints del catalogo."""

    def __init__(self, entradas, indice) -> None:
        ang_out, ang_idx, rat_out, rat_idx, self._pro = [], [], [], [], []
        for pos, spec in entradas:
            if spec["type"] == "angle":
                ang_out.append(pos)
                ang_idx.append([indice(p) for p in spec["points"]])
            elif spec["type"] == "distance_ratio":
                rat_out.append(pos)
                rat_idx.append([indice(p) for p in spec["points"]] + [indice(p) for p in spec["reference"]])
            else:  # "proporcion": tramo (2 puntos) / suma de todos los tramos de 'cadena', x100
                self._pro.append((pos, [indice(p) for p in spec["points"]], [indice(p) for p in spec["cadena"]]))
        self._ang_out = np.array(ang_out, dtype=np.intp)
        self._ang_idx = np.array(ang_idx, dtype=np.intp).reshape(-1, 3)
        self._rat_out = np.array(rat_out, dtype=np.intp)
        self._rat_idx = np.array(rat_idx, dtype=np.intp).reshape(-1, 4)

    def medir(self, P: np.ndarray, out: np.ndarray) -> None:
        """P (N,3) -> escribe en 'out' las features de este grupo (NaN = no medible)."""
        if self._ang_idx.size:
            out[self._ang_out] = _angulos_deg(P, self._ang_idx)

        if self._rat_idx.size:
            d = np.linalg.norm(P[self._rat_idx[:, 0]] - P[self._rat_idx[:, 1]], axis=1)
            r = np.linalg.norm(P[self._rat_idx[:, 2]] - P[self._rat_idx[:, 3]], axis=1)
            seguro = r > 1e-9
            out[self._rat_out] = np.where(seguro, d / np.where(seguro, r, 1.0), np.nan)

        # pocas features de este tipo por ejercicio -- un for simple alcanza, no
        # hace falta vectorizar 'cadena' (largo variable, no encaja en un array fijo).
        for pos, (a, b), cadena in self._pro:
            total = sum(distance(P[x], P[y]) for x, y in zip(cadena, cadena[1:]))
            out[pos] = 100.0 * distance(P[a], P[b]) / total if total > 1e-9 else np.nan


class FeatureExtractor:
    """Compilado desde un Exercise. Inmutable una vez construido.

    Cada feature se mide de una de dos formas:
      - CRUDA: todos sus puntos son landmarks de MediaPipe de la fuente del ejercicio (camino de siempre).
      - DE KPOINTS: algun punto es un kpoint del catalogo (p.ej. un punto derivado). Se mide sobre los
        kpoints resueltos por cuadro con la misma funcion que el dataset (procesamiento/puntos/kpoints.py)."""

    def __init__(self, exercise) -> None:
        self.source = exercise.source
        self.names: list[str] = [f["name"] for f in exercise.features]
        self.units: list[str] = [UNIDAD_POR_TIPO.get(f["type"], "ratio") for f in exercise.features]
        self.size = len(self.names)

        self._kp = list(getattr(exercise, "kpoints", None) or [])
        pos_kp = {kp["nombre"]: i for i, kp in enumerate(self._kp)}

        def indice_kp(nombre: str) -> int:
            if nombre not in pos_kp:
                raise ValueError(f"'{nombre}' no es un landmark de '{self.source}' ni esta en el catalogo de kpoints")
            return pos_kp[nombre]

        crudas, de_kp = [], []
        for pos, spec in enumerate(exercise.features):
            crudo = all(es_landmark(n, self.source) for n in _nombres_de(spec))
            (crudas if crudo else de_kp).append((pos, spec))
        self._crudo = _Banco(crudas, lambda n: resolve(n, self.source))
        self._kbanco = _Banco(de_kp, indice_kp) if de_kp else None

        # Indice de la señal 1-D que usa el segmentador para contar repeticiones.
        self.signal_idx = np.array(
            [self.names.index(n) for n in exercise.signal_features], dtype=np.intp
        )
        self.signal_reduce = exercise.signal_reduce

        self._n_base = self.size

    # -- nucleo vectorizado --
    _angulos_deg = staticmethod(_angulos_deg)

    def from_points(self, P: np.ndarray) -> np.ndarray:
        """P: (N, 3) world landmarks -> (F,) valores de las features CRUDAS. NaN = no medible
        (tambien las de kpoints, que salen de extract())."""
        out = np.full(self._n_base, np.nan, dtype=np.float32)
        self._crudo.medir(P, out)
        return out

    def select(self, detections: list[Landmarks]) -> Landmarks | None:
        """Elige que entidad medir cuando hay varias."""
        candidatos = [d for d in detections if d.source == self.source]
        if not candidatos:
            return None
        return max(candidatos, key=lambda d: d.score)

    def extract(self, detections: list[Landmarks], t_ms: int) -> FeatureVec | None:
        elegido = self.select(detections)
        if elegido is None:
            return None
        vals = np.full(self.size, np.nan, dtype=np.float32)
        vals[: self._n_base] = self.from_points(elegido.world)
        if self._kbanco is not None:
            r = KP.resolver(self._kp, detections)
            if r is not None:
                self._kbanco.medir(r[0], vals[: self._n_base])
        return FeatureVec(values=vals, valid=~np.isnan(vals), t_ms=t_ms,
                           raw=elegido.world, label=elegido.label)

    def signal(self, values: np.ndarray) -> float:
        """Proyeccion 1-D declarada en el YAML. Es lo que cuenta repeticiones."""
        sub = values[..., self.signal_idx]
        fn = np.nanmean if self.signal_reduce == "mean" else (
            np.nanmin if self.signal_reduce == "min" else np.nanmax
        )
        with np.errstate(invalid="ignore"):
            return float(fn(sub)) if sub.ndim == 1 else fn(sub, axis=-1)


# Escala para llevar cada metrica a 0..1 (tabla normalizada): angulo /180, proporcion /100 y razon de
# distancias recortada a 0..4 y /4. La cruda se guarda tal cual sale en table_frames.
ESCALA_TIPO = {"angle": 180.0, "proporcion": 100.0, "distance_ratio": 4.0}


def medibles(nombres, features) -> list[dict]:
    """Los features (activos) cuyos puntos existen todos en 'nombres', en el orden del yaml."""
    ok = set(nombres)
    return [f for f in (features or []) if f.get("activo", True) is not False
            and all(p in ok for p in _nombres_de(f))]


def medir_clip(points, nombres, features):
    """points (T,N,3) + nombres de sus N puntos -> ((T,F) float32 crudo, [nombres de feature], [tipos]).
    Mide EXACTAMENTE los angulos y proporciones activados del ejercicio, tal como salen (sin normalizar)."""
    feats = medibles(nombres, features)
    if not feats:
        return np.zeros((len(points), 0), dtype=np.float32), [], []
    pos = {n: i for i, n in enumerate(nombres)}
    banco = _Banco(list(enumerate(feats)), lambda n: pos[n])
    out = np.full((len(points), len(feats)), np.nan, dtype=np.float32)
    fila = np.empty(len(feats), dtype=np.float32)
    for t, P in enumerate(np.asarray(points, dtype=np.float32)):
        fila[:] = np.nan
        banco.medir(P, fila)
        out[t] = fila
    return out, [f["name"] for f in feats], [f["type"] for f in feats]


def normalizar_metricas(valores, tipos):
    """(n,F) crudo -> (n,F) en 0..1 segun el tipo de cada columna (sin tipos: todo angulo /180)."""
    v = np.asarray(valores, dtype=np.float32)
    if v.shape[1] == 0:
        return v
    esc = np.array([ESCALA_TIPO.get(t, 180.0) for t in (tipos or ["angle"] * v.shape[1])], dtype=np.float32)
    return np.clip(v / esc, 0.0, 1.0)


def compute_features(points: np.ndarray, specs: list[dict], source: str = "pose") -> dict:
    """Camino escalar, usado por los tests. Misma matematica que la version compilada."""
    out: dict[str, float] = {}
    for spec in specs:
        if spec["type"] == "angle":
            a, b, c = (points[resolve(p, source)] for p in spec["points"])
            out[spec["name"]] = angle_deg(a, b, c)
        elif spec["type"] == "distance_ratio":
            p1, p2 = (points[resolve(p, source)] for p in spec["points"])
            r1, r2 = (points[resolve(p, source)] for p in spec["reference"])
            ref = distance(r1, r2)
            out[spec["name"]] = distance(p1, p2) / ref if ref > 1e-9 else float("nan")
        elif spec["type"] == "proporcion":
            cadena = [points[resolve(p, source)] for p in spec["cadena"]]
            total = sum(distance(a, b) for a, b in zip(cadena, cadena[1:]))
            a, b = (points[resolve(p, source)] for p in spec["points"])
            out[spec["name"]] = 100.0 * distance(a, b) / total if total > 1e-9 else float("nan")
        else:
            raise ValueError(f"Tipo de feature no soportado: {spec['type']!r}")
    return out
