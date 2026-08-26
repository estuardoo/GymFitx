"""Capa 6: comparacion de una repeticion contra la plantilla.

Dos decisiones que definen la calidad del resultado:

1. z-score por feature contra mu/sigma de la plantilla. Sin esto los angulos
   (rango 0-180) aplastarian a las razones de distancia (rango 0-2) en la
   distancia total, y una falla del meñique casi no moveria el puntaje.
2. DTW con banda de Sakoe-Chiba. Alinea en el tiempo dos ejecuciones a
   velocidades distintas (hacerlo mas lento no es hacerlo mal), y la banda
   ademas impide alineamientos degenerados donde un solo cuadro se estira
   sobre media repeticion.
"""

from __future__ import annotations

import numpy as np

from .types import Score, Segment

INF = float("inf")


def zscore(data: np.ndarray, mu: np.ndarray, sigma: np.ndarray) -> np.ndarray:
    return (data - mu) / np.where(sigma > 1e-6, sigma, 1.0)


def cost_matrix(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """(T,S) distancia media absoluta por par de cuadros, ignorando NaN."""
    diff = np.abs(A[:, None, :] - B[None, :, :])
    with np.errstate(invalid="ignore"):
        C = np.nanmean(diff, axis=2)
    return np.nan_to_num(C, nan=0.0)


def dtw_band(C: np.ndarray, radius_frac: float = 0.15) -> tuple[float, list[tuple[int, int]]]:
    """DTW sobre la matriz de costos, restringido a una banda diagonal.

    Devuelve (costo medio por paso, camino). El costo se divide por la
    longitud del camino para que no dependa de cuantos cuadros duro la rep.
    """
    T, S = C.shape
    radius = max(int(round(radius_frac * max(T, S))), abs(T - S) + 1, 2)

    D = np.full((T + 1, S + 1), INF, dtype=np.float64)
    D[0, 0] = 0.0
    # 0=diagonal, 1=arriba (consume A), 2=izquierda (consume B)
    move = np.zeros((T + 1, S + 1), dtype=np.int8)

    for i in range(1, T + 1):
        centro = (i - 1) * S / T
        j_ini = max(1, int(centro - radius) + 1)
        j_fin = min(S, int(centro + radius) + 1)
        fila = C[i - 1]
        for j in range(j_ini, j_fin + 1):
            d = fila[j - 1]
            diag, arriba, izq = D[i - 1, j - 1], D[i - 1, j], D[i, j - 1]
            if diag <= arriba and diag <= izq:
                D[i, j] = d + diag
                move[i, j] = 0
            elif arriba <= izq:
                D[i, j] = d + arriba
                move[i, j] = 1
            else:
                D[i, j] = d + izq
                move[i, j] = 2

    if not np.isfinite(D[T, S]):
        return INF, []

    camino: list[tuple[int, int]] = []
    i, j = T, S
    while i > 0 and j > 0:
        camino.append((i - 1, j - 1))
        m = move[i, j]
        if m == 0:
            i, j = i - 1, j - 1
        elif m == 1:
            i -= 1
        else:
            j -= 1
    camino.reverse()
    return float(D[T, S] / max(len(camino), 1)), camino


def compare(segment: Segment, template) -> Score:
    """Repeticion vs plantilla -> Score 0-100 con desglose por feature."""
    A = zscore(segment.data, template.mu, template.sigma)
    B = zscore(template.data, template.mu, template.sigma)

    C = cost_matrix(A, B)
    err_z, camino = dtw_band(C, template.radius_frac)

    F = A.shape[1]
    per_feature = np.full(F, np.nan, dtype=np.float32)
    if camino:
        ia = np.fromiter((p[0] for p in camino), dtype=np.intp, count=len(camino))
        ib = np.fromiter((p[1] for p in camino), dtype=np.intp, count=len(camino))
        with np.errstate(invalid="ignore"):
            # Desviacion media por feature, devuelta a unidades reales (grados / razon)
            per_feature = np.nanmean(np.abs(segment.data[ia] - template.data[ib]), axis=0)

    total = 100.0 * float(np.exp(-err_z / max(template.tau, 1e-6)))
    return Score(
        total=float(np.clip(total, 0.0, 100.0)),
        error_z=err_z,
        per_feature=per_feature.astype(np.float32),
        feature_names=list(template.names),
        duration_ms=segment.duration_ms,
    )


def pairwise_errors(reps: list[np.ndarray], mu, sigma, radius_frac: float) -> np.ndarray:
    """Matriz (n,n) de error DTW entre repeticiones. Base de la autocalibracion."""
    n = len(reps)
    Z = [zscore(r, mu, sigma) for r in reps]
    M = np.zeros((n, n), dtype=np.float64)
    for i in range(n):
        for j in range(i + 1, n):
            e, _ = dtw_band(cost_matrix(Z[i], Z[j]), radius_frac)
            M[i, j] = M[j, i] = e
    return M
