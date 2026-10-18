"""Normalizacion de un clip de puntos: caja 100x100 (o punto de referencia) y remuestreo a N cuadros.

La usan igual el dataset (SQL) y el clasificador en vivo."""

from __future__ import annotations

import hashlib

import numpy as np

DEFAULT_CFG = {
    "modo": "rectangulo",       # "rectangulo" (recomendado) o "punto"
    "n_frames_fijo": 30,
    "punto_centro": None, "punto_escala_a": None, "punto_escala_b": None,  # modo "punto"
    "puntos_caja": None,        # modo "rectangulo": subset de nombres para la caja (None = todos)
}


LADO_LIENZO = 100


def cfg_para(point_names, cfg_guardada: dict | None = None) -> dict:
    """Config efectiva con defaults razonables para estos puntos."""
    out = {**DEFAULT_CFG, **(cfg_guardada or {})}
    nombres = list(point_names)
    if out["punto_centro"] not in nombres:
        out["punto_centro"] = "WRIST" if "WRIST" in nombres else nombres[0]
    if out["punto_escala_a"] not in nombres:
        out["punto_escala_a"] = out["punto_centro"]
    if out["punto_escala_b"] not in nombres:
        out["punto_escala_b"] = "MIDDLE_FINGER_MCP" if "MIDDLE_FINGER_MCP" in nombres else nombres[-1]
    validos = [n for n in (out.get("puntos_caja") or []) if n in nombres]
    out["puntos_caja"] = validos or None
    return out


def guia(cfg: dict) -> str:
    """Descriptor corto de la normalizacion (table_file.guia_fix)."""
    if cfg["modo"] == "rectangulo":
        caja = ",".join(cfg["puntos_caja"]) if cfg.get("puntos_caja") else "todos"
        return f"rect:{LADO_LIENZO}|{cfg['n_frames_fijo']}f|caja:{caja}"
    return f"punto:{cfg['punto_centro']}-{cfg['punto_escala_a']}-{cfg['punto_escala_b']}|{cfg['n_frames_fijo']}f"


def firma(nombres, angulos) -> str:
    """Firma corta de QUE puntos/angulos trae el clip."""
    txt = "|".join(nombres) + "#" + "|".join(angulos)
    return hashlib.sha1(txt.encode()).hexdigest()[:8]


def resamplear(fijo: np.ndarray, n_frames_fijo: int) -> np.ndarray:
    """(T,N,C) -> (n,N,C). Interpola solo sobre cuadros con dato (NaN = no detectado)."""
    t_actual = np.linspace(0, 1, len(fijo))
    t_nuevo = np.linspace(0, 1, n_frames_fijo)
    out = np.full((n_frames_fijo, fijo.shape[1], fijo.shape[2]), np.nan, dtype=np.float32)
    for n in range(fijo.shape[1]):
        for c in range(fijo.shape[2]):
            serie = fijo[:, n, c]
            ok = np.isfinite(serie)
            if ok.any():
                out[:, n, c] = np.interp(t_nuevo, t_actual[ok], serie[ok])
    return out


def resamplear_angulos(angulos: np.ndarray, n_frames_fijo: int) -> np.ndarray:
    if angulos.shape[1] == 0:
        return np.zeros((n_frames_fijo, 0), dtype=np.float32)
    return resamplear(angulos[:, :, None], n_frames_fijo)[:, :, 0]


def _normalizar_punto(points, point_names, cfg):
    nombres = list(point_names)
    ic = nombres.index(cfg["punto_centro"])
    ia = nombres.index(cfg["punto_escala_a"])
    ib = nombres.index(cfg["punto_escala_b"])
    centrado = points - points[:, ic:ic + 1, :]
    escala = np.linalg.norm(points[:, ia, :] - points[:, ib, :], axis=-1)
    escala = np.where(escala > 1e-6, escala, 1.0).reshape(-1, 1, 1)
    return centrado / escala


def _normalizar_rectangulo(points, indices_caja=None):
    """Caja envolvente del clip completo -> lienzo fijo de 100x100 con un solo
    factor de escala (no deforma). Si se dan indices_caja, la caja sale solo
    de esos puntos pero la transformacion se aplica a todos."""
    ref = points[:, indices_caja, :] if indices_caja else points
    minimo = np.nanmin(ref, axis=(0, 1))
    ancho = max(np.nanmax(ref[..., 0]) - minimo[0], 1e-6)
    alto = max(np.nanmax(ref[..., 1]) - minimo[1], 1e-6)
    factor = min((LADO_LIENZO - 1) / ancho, (LADO_LIENZO - 1) / alto)
    return (points - minimo) * factor


def normalizar(points, point_names, cfg: dict) -> np.ndarray:
    """(T,N,3) crudo -> (n_frames_fijo,N,3) segun cfg (ya resuelta con cfg_para)."""
    if cfg["modo"] == "rectangulo":
        indices_caja = None
        if cfg.get("puntos_caja"):
            nombres = list(point_names)
            indices_caja = [nombres.index(n) for n in cfg["puntos_caja"] if n in nombres] or None
        fijo = _normalizar_rectangulo(points, indices_caja)
    else:
        fijo = _normalizar_punto(points, point_names, cfg)
    return resamplear(fijo, cfg["n_frames_fijo"])
