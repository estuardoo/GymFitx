"""Comparador sin DTW: remuestrea la repeticion al largo de la plantilla y compara cuadro a cuadro.

Sirve de control para medir cuanto aporta el DTW."""

from __future__ import annotations

import numpy as np

from src.evaluacion.comparadores.dtw import zscore
from src.nucleo.tipos import Score, Segment


def _resample(data: np.ndarray, n: int) -> np.ndarray:
    """(T,F) -> (n,F) por interpolacion lineal en el indice de tiempo."""
    t_src = np.linspace(0.0, 1.0, data.shape[0])
    t_dst = np.linspace(0.0, 1.0, n)
    return np.stack(
        [np.interp(t_dst, t_src, data[:, f]) for f in range(data.shape[1])], axis=1
    )


def _angulos_directo(segment: Segment, template) -> Score:
    """Arquitectura 2 del documento de referencia: distancia angular directa,
    sin DTW. Remuestrea la repeticion a la duracion de la plantilla y compara
    frame a frame."""
    rep = _resample(segment.data, template.data.shape[0])
    A, B = zscore(rep, template.mu, template.sigma), zscore(template.data, template.mu, template.sigma)
    with np.errstate(invalid="ignore"):
        err_z = float(np.nanmean(np.abs(A - B)))
        per_feature = np.nanmean(np.abs(rep - template.data), axis=0)
    total = 100.0 * float(np.exp(-err_z / max(template.tau, 1e-6)))
    return Score(
        total=float(np.clip(total, 0.0, 100.0)),
        error_z=err_z,
        per_feature=per_feature.astype(np.float32),
        feature_names=list(template.names),
        duration_ms=segment.duration_ms,
    )
