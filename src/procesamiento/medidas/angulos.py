"""Geometria de angulos entre vectores/puntos (grados).

VERSION: subirla si cambia la definicion de algun angulo (fuerza a recalcular en SQL)."""

from __future__ import annotations

import numpy as np

VERSION = 2


def angulo_entre(u: np.ndarray, v: np.ndarray) -> np.ndarray:
    """(...,3),(...,3) -> (...) grados entre vectores; NaN si alguno es ~0."""
    u = np.asarray(u, dtype=np.float64)
    v = np.asarray(v, dtype=np.float64)
    nu, nv = np.linalg.norm(u, axis=-1), np.linalg.norm(v, axis=-1)
    den = nu * nv
    ok = den > 1e-9
    cos = np.sum(u * v, axis=-1) / np.where(ok, den, 1.0)
    return np.where(ok, np.degrees(np.arccos(np.clip(cos, -1.0, 1.0))), np.nan)


def angulo_interior(a, b, c) -> np.ndarray:
    """Angulo A-B-C con vertice en B, en grados (acepta lotes (...,3))."""
    return angulo_entre(np.asarray(a) - np.asarray(b), np.asarray(c) - np.asarray(b))
