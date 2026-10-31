"""La plantilla: el movimiento base y TODO lo que se deriva de el.

Aqui vive la autocalibracion, que es lo que elimina los numeros magicos del
sistema. De una sola grabacion de N repeticiones salen:

  mu / sigma    normalizacion de las features        -> compare
  low / high    umbrales de histeresis               -> segmenter
  data          la repeticion de referencia (medoide)-> compare
  tau           severidad del puntaje                -> compare

El medoide (la repeticion mas parecida a todas las demas) es mejor referencia
que el promedio: promediar en el dominio del tiempo emborrona los picos y
produce una plantilla que nadie puede reproducir.

tau se fija para que una repeticion tan buena como tu promedio puntue 90:
    100 * exp(-err/tau) = 90   =>   tau = err / 0.10536
Asi el puntaje es comparable entre dias y entre ejercicios distintos.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import numpy as np

from src.evaluacion.comparadores.dtw import pairwise_errors
from src.evaluacion.segmentador import RepSegmenter
from src.nucleo.tipos import FeatureVec, Segment

LN_090 = 0.105360516  # -ln(0.90)
PCT_BAJO, PCT_ALTO = 20.0, 80.0


@dataclass
class Template:
    exercise: str
    names: list[str]
    units: list[str]
    data: np.ndarray        # (T, F) la repeticion de referencia, unidades reales
    mu: np.ndarray          # (F,)
    sigma: np.ndarray       # (F,)
    low: float
    high: float
    tau: float
    n_reps: int
    radius_frac: float = 0.15
    created_at: str = ""
    duration_ms: int = 0
    fin: float | None = None   # umbral de "volvio al inicio" (la rep se cuenta ahi); None = high
    origen: str = ""          # "clip" = creada sola desde un clip (base_clip.py)

    def save(self, path: str | Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(
            path,
            data=self.data,
            mu=self.mu,
            sigma=self.sigma,
            meta=json.dumps(
                {
                    "exercise": self.exercise,
                    "names": self.names,
                    "units": self.units,
                    "low": self.low,
                    "high": self.high,
                    "tau": self.tau,
                    "n_reps": self.n_reps,
                    "radius_frac": self.radius_frac,
                    "created_at": self.created_at or datetime.now().isoformat(timespec="seconds"),
                    "duration_ms": self.duration_ms,
                    "fin": self.fin,
                    "origen": self.origen,
                }
            ),
        )
        return path

    @classmethod
    def load(cls, path: str | Path) -> Template:
        z = np.load(Path(path), allow_pickle=False)
        m = json.loads(str(z["meta"]))
        return cls(
            exercise=m["exercise"],
            names=m["names"],
            units=m["units"],
            data=z["data"],
            mu=z["mu"],
            sigma=z["sigma"],
            low=m["low"],
            high=m["high"],
            tau=m["tau"],
            n_reps=m["n_reps"],
            radius_frac=m.get("radius_frac", 0.15),
            created_at=m.get("created_at", ""),
            duration_ms=m.get("duration_ms", 0),
            fin=m.get("fin"),
            origen=m.get("origen", ""),
        )

    def to_dict(self) -> dict:
        return {
            "exercise": self.exercise,
            "n_reps": self.n_reps,
            "created_at": self.created_at,
            "duration_ms": self.duration_ms,
            "tau": round(self.tau, 4),
            "low": round(self.low, 3),
            "high": round(self.high, 3),
            "frames": int(self.data.shape[0]),
        }


def template_path(templates_dir: str | Path, slug: str) -> Path:
    return Path(templates_dir) / f"{slug}.npz"


def build_template(
    frames: list[FeatureVec],
    exercise,
    extractor,
    radius_frac: float = 0.15,
) -> Template:
    """De una toma continua de N repeticiones a una plantilla calibrada.

    Se segmenta OFFLINE, con umbrales derivados de la propia toma: en el
    momento de grabar todavia no existen umbrales que aplicar.
    """
    if len(frames) < 30:
        raise ValueError(
            f"Toma demasiado corta ({len(frames)} cuadros con deteccion). "
            f"Graba al menos 5 repeticiones lentas."
        )

    valores = np.vstack([f.values for f in frames])
    señal = np.array([extractor.signal(v) for v in valores], dtype=np.float64)
    finitos = señal[np.isfinite(señal)]
    if finitos.size < 30:
        raise ValueError("La señal no fue medible en suficientes cuadros. Revisa la iluminacion.")

    low = float(np.percentile(finitos, PCT_BAJO))
    high = float(np.percentile(finitos, PCT_ALTO))
    if high - low < 1e-6:
        raise ValueError(
            "La señal no varia: el movimiento no se distingue del reposo. "
            "Revisa que signal.features de la definicion describan el movimiento."
        )

    seg = RepSegmenter(
        n_features=valores.shape[1],
        signal_idx=extractor.signal_idx,
        reduce=extractor.signal_reduce,
        low=low,
        high=high,
        direction=exercise.direction,
        min_duration_ms=exercise.min_duration_ms,
        max_duration_ms=exercise.max_duration_ms,
        capacity=max(len(frames) + 1, 64),
    )
    reps: list[Segment] = []
    for fv in frames:
        s = seg.update(fv)
        if s is not None:
            reps.append(s)

    if len(reps) < 2:
        raise ValueError(
            f"Solo se detectaron {len(reps)} repeticiones completas. "
            f"Necesito al menos 2 (idealmente 5) para calibrar. "
            f"Haz el movimiento completo y regresa siempre al punto de partida."
        )

    datos = [r.data for r in reps]
    apilado = np.vstack(datos)
    with np.errstate(invalid="ignore"):
        mu = np.nanmean(apilado, axis=0).astype(np.float32)
        sigma = np.nanstd(apilado, axis=0).astype(np.float32)
    mu = np.nan_to_num(mu, nan=0.0)
    sigma = np.where(np.isfinite(sigma) & (sigma > 1e-3), sigma, 1.0).astype(np.float32)

    M = pairwise_errors(datos, mu, sigma, radius_frac)
    medoide = int(np.argmin(M.sum(axis=1)))

    fuera_diagonal = M[~np.eye(len(reps), dtype=bool)]
    err_tipico = float(np.median(fuera_diagonal))
    tau = max(err_tipico / LN_090, 1e-3)

    return Template(
        exercise=exercise.slug,
        names=list(extractor.names),
        units=list(extractor.units),
        data=datos[medoide],
        mu=mu,
        sigma=sigma,
        low=low,
        high=high,
        tau=tau,
        n_reps=len(reps),
        radius_frac=radius_frac,
        created_at=datetime.now().isoformat(timespec="seconds"),
        duration_ms=reps[medoide].duration_ms,
    )
