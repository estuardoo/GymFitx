"""Carga y validacion del ejercicio declarado en YAML.

Un ejercicio NO es codigo: es un archivo de datos que declara que articulaciones
mirar y como reconocer una repeticion. Agregar manguito rotador o flexion de
tobillo es escribir un YAML, nunca tocar el motor.

Todo lo que se puede validar se valida al cargar. Un error de dedo en un nombre
de landmark revienta antes de encender la camara, no a mitad de la serie.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from .landmarks import resolve

VALID_SOURCES = {"hands", "pose"}
VALID_HANDS = {"left", "right", "any"}
VALID_TYPES = {"angle", "distance_ratio"}
VALID_REDUCE = {"mean", "min", "max"}
VALID_DIRECTION = {"down_up", "up_down"}


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
    hand: str = "any"
    manos_detalle: bool = False  # arranca con dedos articulados de verdad (ver Pipeline.set_manos_detalle)
    description: str = ""
    path: Path | None = None

    @property
    def feature_names(self) -> list[str]:
        return [f["name"] for f in self.features]

    def unit_of(self, name: str) -> str:
        for f in self.features:
            if f["name"] == name:
                return "deg" if f["type"] == "angle" else "ratio"
        return ""

    def to_dict(self) -> dict:
        return {
            "slug": self.slug,
            "name": self.name,
            "source": self.source,
            "hand": self.hand,
            "manos_detalle": self.manos_detalle,
            "description": self.description.strip(),
            "features": self.feature_names,
            "units": [self.unit_of(n) for n in self.feature_names],
        }


def load_exercise(path: str | Path) -> Exercise:
    path = Path(path)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))

    for key in ("name", "source", "features"):
        if key not in data:
            raise ValueError(f"{path.name}: falta la clave obligatoria '{key}'")

    source = data["source"]
    if source not in VALID_SOURCES:
        raise ValueError(f"{path.name}: source debe ser uno de {sorted(VALID_SOURCES)}")

    hand = data.get("hand", "any")
    if hand not in VALID_HANDS:
        raise ValueError(f"{path.name}: hand debe ser uno de {sorted(VALID_HANDS)}")

    nombres: list[str] = []
    for spec in data["features"]:
        for key in ("name", "type", "points"):
            if key not in spec:
                raise ValueError(f"{path.name}: feature sin '{key}': {spec}")
        if spec["type"] not in VALID_TYPES:
            raise ValueError(f"{path.name}: tipo invalido {spec['type']!r}")
        if spec["name"] in nombres:
            raise ValueError(f"{path.name}: feature duplicada {spec['name']!r}")
        nombres.append(spec["name"])

        n_esperado = 3 if spec["type"] == "angle" else 2
        if len(spec["points"]) != n_esperado:
            raise ValueError(
                f"{path.name}: '{spec['name']}' de tipo {spec['type']} "
                f"necesita exactamente {n_esperado} puntos"
            )
        if spec["type"] == "distance_ratio" and len(spec.get("reference", [])) != 2:
            raise ValueError(f"{path.name}: '{spec['name']}' necesita 'reference' con 2 puntos")

        for p in list(spec["points"]) + list(spec.get("reference", [])):
            resolve(p, source)

    signal = data.get("signal", {})
    signal_features = signal.get("features") or nombres
    faltantes = [n for n in signal_features if n not in nombres]
    if faltantes:
        raise ValueError(f"{path.name}: signal.features desconocidas: {faltantes}")

    reduce = signal.get("reduce", "mean")
    if reduce not in VALID_REDUCE:
        raise ValueError(f"{path.name}: signal.reduce debe ser uno de {sorted(VALID_REDUCE)}")

    seg = data.get("segmentation", {})
    direction = seg.get("direction", "down_up")
    if direction not in VALID_DIRECTION:
        raise ValueError(
            f"{path.name}: segmentation.direction debe ser uno de {sorted(VALID_DIRECTION)}"
        )

    return Exercise(
        slug=path.stem,
        name=data["name"],
        source=source,
        features=data["features"],
        signal_features=list(signal_features),
        signal_reduce=reduce,
        direction=direction,
        min_duration_ms=int(seg.get("min_duration_ms", 600)),
        max_duration_ms=int(seg.get("max_duration_ms", 8000)),
        hand=hand,
        manos_detalle=bool(data.get("manos_detalle", False)),
        description=data.get("description", ""),
        path=path,
    )


def load_all(directory: str | Path) -> dict[str, Exercise]:
    """Todos los ejercicios de la carpeta, indexados por slug."""
    directory = Path(directory)
    out: dict[str, Exercise] = {}
    for p in sorted(directory.glob("*.yaml")):
        out[p.stem] = load_exercise(p)
    return out
