"""Contratos de datos del pipeline. Cero logica, solo estructura.

Todo lo que viaja entre capas pasa por aqui. Si un modulo necesita un campo
que no esta en estos tipos, la responsabilidad esta mal repartida.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass(frozen=True)
class Frame:
    """Un cuadro crudo de la fuente."""

    image: np.ndarray   # BGR (H, W, 3)
    t_ms: int           # monotono creciente desde el inicio de la captura
    index: int


@dataclass(frozen=True)
class Landmarks:
    """Puntos detectados en un cuadro, de una sola entidad (una mano o el cuerpo)."""

    source: str          # "hands" | "pose"
    world: np.ndarray    # (N, 3) metros, origen en la entidad -> para MEDIR
    screen: np.ndarray   # (N, 3) normalizado 0-1 al frame -> para DIBUJAR
    label: str = ""      # "Left" / "Right" en manos; "" en pose
    score: float = 1.0


@dataclass(frozen=True)
class FeatureVec:
    """El vector de features de un cuadro. Nada aguas abajo conoce los pixeles."""

    values: np.ndarray   # (F,) float32, NaN donde no se pudo medir
    valid: np.ndarray    # (F,) bool
    t_ms: int

    @property
    def any_valid(self) -> bool:
        return bool(self.valid.any())


@dataclass
class Segment:
    """Una repeticion recortada del flujo."""

    start_ms: int
    end_ms: int
    data: np.ndarray     # (T, F)
    valid: np.ndarray    # (T, F) bool

    @property
    def duration_ms(self) -> int:
        return self.end_ms - self.start_ms

    @property
    def n_frames(self) -> int:
        return self.data.shape[0]


@dataclass
class Score:
    """Resultado de comparar una repeticion contra la plantilla."""

    total: float                  # 0-100
    error_z: float                # error medio en desviaciones tipicas
    per_feature: np.ndarray       # (F,) desviacion media por feature, en unidades reales
    feature_names: list[str] = field(default_factory=list)
    duration_ms: int = 0

    def worst(self, n: int = 2) -> list[tuple[str, float]]:
        """Las n features con mayor desviacion. Es lo que el panel muestra como consejo."""
        order = np.argsort(-np.nan_to_num(self.per_feature))
        return [(self.feature_names[i], float(self.per_feature[i])) for i in order[:n]]

    def to_dict(self) -> dict:
        return {
            "total": round(self.total, 1),
            "error_z": round(self.error_z, 3),
            "duration_ms": self.duration_ms,
            "per_feature": {
                n: (None if np.isnan(v) else round(float(v), 1))
                for n, v in zip(self.feature_names, self.per_feature)
            },
        }
