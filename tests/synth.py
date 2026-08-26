"""Generador de repeticiones sinteticas: permite probar el motor sin camara."""

from __future__ import annotations

import numpy as np

from core.types import FeatureVec


def rep_sintetica(
    n_frames: int = 45,
    amplitud: float = 90.0,
    ruido: float = 0.0,
    sesgo_menique: float = 0.0,
    semilla: int = 0,
) -> np.ndarray:
    """(n_frames, 6) imitando 'apertura y cierre de mano'.

    Empieza arriba (mano abierta), baja (puño) y vuelve arriba: direction down_up.
    """
    rng = np.random.default_rng(semilla)
    t = np.linspace(0.0, 1.0, n_frames, endpoint=False)
    onda = np.sin(np.pi * t)                       # 0 -> 1 -> 0
    curl = 170.0 - amplitud * onda
    out = np.empty((n_frames, 6), dtype=np.float32)
    out[:, 0] = 150.0 - (amplitud * 0.6) * onda    # curl_pulgar
    out[:, 1] = curl                               # curl_indice
    out[:, 2] = curl
    out[:, 3] = curl
    out[:, 4] = curl + sesgo_menique               # curl_menique
    out[:, 5] = 2.0 - 1.2 * onda                   # apertura_lateral
    if ruido:
        out += rng.normal(scale=ruido, size=out.shape).astype(np.float32)
    return out


def a_framevecs(datos: np.ndarray, fps: float = 30.0, t0: int = 0) -> list[FeatureVec]:
    dt = 1000.0 / fps
    return [
        FeatureVec(values=fila.astype(np.float32), valid=np.ones(fila.size, bool),
                   t_ms=int(t0 + i * dt))
        for i, fila in enumerate(datos)
    ]


def toma(n_reps: int = 6, **kw) -> list[FeatureVec]:
    """Una toma continua de N repeticiones, como la que graba record.py."""
    bloques = [rep_sintetica(semilla=i, **kw) for i in range(n_reps)]
    return a_framevecs(np.vstack(bloques))
