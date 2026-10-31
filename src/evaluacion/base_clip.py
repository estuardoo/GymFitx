"""Base (plantilla) a partir de UN clip ya cortado: el primer clip "bien" del ejercicio (o el que se indique).

Sirve para que el ejercicio cuente repeticiones en vivo sin tener que grabar una base aparte.
Los umbrales salen del propio clip: a = P10 y b = P90 de la señal; low = a + 0.3 (b - a), high = a + 0.5 (b - a)
(la banda es estrecha y esta en el medio del recorrido, asi cada ciclo se cuenta una sola vez); la rep se cuenta al volver
a `fin` = 70 % del recorrido, o sea en la posicion inicial y no a mitad de la subida.
tau (severidad del puntaje) sale del error DTW contra los demas clips "bien" si los hay."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import numpy as np

from src.evaluacion.comparadores.dtw import pairwise_errors
from src.evaluacion.plantilla import LN_090, Template, template_path
from src.nucleo import inputs as INP
from src.nucleo.config import CLIPS_DIR, TEMPLATES_DIR, params
from src.nucleo.landmarks import es_landmark, resolve
from src.procesamiento.medidas.features import FeatureExtractor

_B = params("base_clip")   # parameters/config.json; FIN: la rep se cuenta al volver al inicio
FRAC_LOW, FRAC_HIGH, FRAC_FIN = _B["frac_low"], _B["frac_high"], _B["frac_fin"]
TAU_DEFECTO = 0.5 / LN_090   # ponytail: sin otros clips no hay forma de medir la dispersion; se afina al re-hacer la base con mas clips
MAX_OTROS = 12


def _valores(ex, ext: FeatureExtractor, npz: Path) -> np.ndarray:
    """(T, F) features crudas del clip, medidas con la misma matematica del vivo."""
    z = np.load(npz, allow_pickle=False)
    pts = np.asarray(z["points"], dtype=np.float32)
    if len(z["point_names"]) != 33:   # el clip guarda solo sus kpoints (12, 23...): se llevan a los 33 por nombre
        completo = np.full((len(pts), 33, pts.shape[2]), np.nan, dtype=np.float32)
        for i, n in enumerate(z["point_names"]):
            if es_landmark(str(n), ext.source):
                completo[:, resolve(str(n), ext.source)] = pts[:, i]
        pts = completo
    return np.array([ext.from_points(P) for P in pts], dtype=np.float32)


def _originales(slug: str, clase: str) -> list[Path]:
    """.npz de los clips de esa clase en orden de id, sin las copias si hay originales."""
    filas = sorted((r for r in INP.filas() if r["exercise"] == slug and r["clase"] == clase), key=lambda r: r["id"])
    todos = [CLIPS_DIR / Path(r["clip"]).parent / r["npz"] for r in filas]
    sin_copias = [CLIPS_DIR / Path(r["clip"]).parent / r["npz"] for r in filas if not r["copia"]]
    return [p for p in (sin_copias or todos) if p.exists()]


def primer_clip(slug: str, clase: str = "bien") -> Path | None:
    return next(iter(_originales(slug, clase)), None)


def plantilla_de_clip(ex, npz: Path, otros: list[Path] | None = None) -> Template:
    ext = FeatureExtractor(ex)
    vals = _valores(ex, ext, npz)
    señal = ext.signal(vals)
    finitos = señal[np.isfinite(señal)]
    if finitos.size < 10:
        raise ValueError("el clip no tiene suficientes cuadros medibles")
    a, b = float(np.percentile(finitos, 10)), float(np.percentile(finitos, 90))
    if b - a < 1e-6:
        raise ValueError("la señal del clip no varia: revisa signal.features de la definicion")
    low, high, fin = (a + f * (b - a) for f in (FRAC_LOW, FRAC_HIGH, FRAC_FIN))

    with np.errstate(invalid="ignore"):
        mu = np.nan_to_num(np.nanmean(vals, axis=0), nan=0.0).astype(np.float32)
        sigma = np.nanstd(vals, axis=0)
    sigma = np.where(np.isfinite(sigma) & (sigma > 1e-3), sigma, 1.0).astype(np.float32)

    tau = TAU_DEFECTO
    reps = [vals]
    for p in (otros or [])[:MAX_OTROS]:
        try:
            reps.append(_valores(ex, ext, p))
        except Exception:   # noqa: BLE001 - un clip ilegible solo se salta (tau se calcula con los demas)
            continue
    if len(reps) >= 2:
        M = pairwise_errors(reps, mu, sigma, 0.15)
        tau = max(float(np.median(M[0, 1:])) / LN_090, 1e-3)

    t = np.load(npz, allow_pickle=False)["t_ms"]
    return Template(exercise=ex.slug, names=list(ext.names), units=list(ext.units), data=vals, mu=mu, sigma=sigma,
                    low=low, high=high, fin=fin, origen="clip", tau=tau, n_reps=len(reps), created_at=datetime.now().isoformat(timespec="seconds"),
                    duration_ms=int(t[-1] - t[0]) if len(t) > 1 else 0)


def base_desde_clip(ex, clip: str | None = None, clase: str = "bien") -> dict:
    """Crea parameters/plantillas/<slug>.npz desde `clip` (nombre o ruta; por defecto el primero de la clase)."""
    if clip:   # ruta a un .npz, '1/000123.mp4' o solo el id '000123'
        c = Path(clip)
        npz = c if c.is_file() else (CLIPS_DIR / c.with_suffix(".npz") if c.parent.name else
                                     CLIPS_DIR / str(INP.asegurar_ejercicio(ex.slug)) / (c.stem + ".npz"))
    else:
        npz = primer_clip(ex.slug, clase)
    if npz is None or not npz.exists():
        raise ValueError(f"no hay clips '{clase}' del ejercicio '{ex.slug}'")
    otros = [p for p in _originales(ex.slug, clase) if p != npz]
    otros = otros[::max(1, len(otros) // MAX_OTROS)]   # repartidos, para que tau no dependa de uno solo
    tpl = plantilla_de_clip(ex, npz, otros)
    ruta = template_path(TEMPLATES_DIR, ex.slug)
    tpl.save(ruta)
    return {"clip": npz.stem, "ruta": str(ruta), "low": round(tpl.low, 1), "high": round(tpl.high, 1),
            "tau": round(tpl.tau, 3), "frames": int(tpl.data.shape[0])}
