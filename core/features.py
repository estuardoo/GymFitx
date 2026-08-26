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

from .landmarks import resolve
from .types import FeatureVec, Landmarks


# --- Formas escalares, para tests y uso puntual ---------------------------

def angle_deg(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
    """Angulo A-B-C en grados, con vertice en B."""
    ba, bc = a - b, c - b
    na, nc = float(np.linalg.norm(ba)), float(np.linalg.norm(bc))
    if na < 1e-9 or nc < 1e-9:
        return float("nan")
    cos = float(np.dot(ba, bc) / (na * nc))
    return float(np.degrees(np.arccos(np.clip(cos, -1.0, 1.0))))


def distance(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b))


# --- Extractor compilado --------------------------------------------------

class FeatureExtractor:
    """Compilado desde un Exercise. Inmutable una vez construido."""

    def __init__(self, exercise) -> None:
        self.source = exercise.source
        self.hand = exercise.hand
        self.names: list[str] = [f["name"] for f in exercise.features]
        self.units: list[str] = [
            "deg" if f["type"] == "angle" else "ratio" for f in exercise.features
        ]
        self.size = len(self.names)

        ang_out, ang_idx, rat_out, rat_idx = [], [], [], []
        for pos, spec in enumerate(exercise.features):
            if spec["type"] == "angle":
                ang_out.append(pos)
                ang_idx.append([resolve(p, self.source) for p in spec["points"]])
            else:
                rat_out.append(pos)
                rat_idx.append(
                    [resolve(p, self.source) for p in spec["points"]]
                    + [resolve(p, self.source) for p in spec["reference"]]
                )

        self._ang_out = np.array(ang_out, dtype=np.intp)
        self._ang_idx = np.array(ang_idx, dtype=np.intp).reshape(-1, 3)
        self._rat_out = np.array(rat_out, dtype=np.intp)
        self._rat_idx = np.array(rat_idx, dtype=np.intp).reshape(-1, 4)

        # Indice de la señal 1-D que usa el segmentador para contar repeticiones.
        self.signal_idx = np.array(
            [self.names.index(n) for n in exercise.signal_features], dtype=np.intp
        )
        self.signal_reduce = exercise.signal_reduce

    # -- nucleo vectorizado --
    def from_points(self, P: np.ndarray) -> np.ndarray:
        """P: (N, 3) world landmarks -> (F,) valores. NaN = no medible."""
        out = np.full(self.size, np.nan, dtype=np.float32)

        if self._ang_idx.size:
            a = P[self._ang_idx[:, 0]]
            b = P[self._ang_idx[:, 1]]
            c = P[self._ang_idx[:, 2]]
            ba, bc = a - b, c - b
            den = np.linalg.norm(ba, axis=1) * np.linalg.norm(bc, axis=1)
            seguro = den > 1e-9
            cos = np.einsum("ij,ij->i", ba, bc) / np.where(seguro, den, 1.0)
            ang = np.degrees(np.arccos(np.clip(cos, -1.0, 1.0)))
            out[self._ang_out] = np.where(seguro, ang, np.nan)

        if self._rat_idx.size:
            d = np.linalg.norm(P[self._rat_idx[:, 0]] - P[self._rat_idx[:, 1]], axis=1)
            r = np.linalg.norm(P[self._rat_idx[:, 2]] - P[self._rat_idx[:, 3]], axis=1)
            seguro = r > 1e-9
            out[self._rat_out] = np.where(seguro, d / np.where(seguro, r, 1.0), np.nan)

        return out

    def select(self, detections: list[Landmarks]) -> Landmarks | None:
        """Elige que entidad medir cuando hay varias (dos manos en cuadro)."""
        candidatos = [d for d in detections if d.source == self.source]
        if not candidatos:
            return None
        if self.source == "hands" and self.hand != "any":
            candidatos = [d for d in candidatos if d.label.lower() == self.hand]
            if not candidatos:
                return None
        return max(candidatos, key=lambda d: d.score)

    def extract(self, detections: list[Landmarks], t_ms: int) -> FeatureVec | None:
        elegido = self.select(detections)
        if elegido is None:
            return None
        vals = self.from_points(elegido.world)
        return FeatureVec(values=vals, valid=~np.isnan(vals), t_ms=t_ms)

    def signal(self, values: np.ndarray) -> float:
        """Proyeccion 1-D declarada en el YAML. Es lo que cuenta repeticiones."""
        sub = values[..., self.signal_idx]
        fn = np.nanmean if self.signal_reduce == "mean" else (
            np.nanmin if self.signal_reduce == "min" else np.nanmax
        )
        with np.errstate(invalid="ignore"):
            return float(fn(sub)) if sub.ndim == 1 else fn(sub, axis=-1)


def compute_features(points: np.ndarray, specs: list[dict], source: str = "hands") -> dict:
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
        else:
            raise ValueError(f"Tipo de feature no soportado: {spec['type']!r}")
    return out
