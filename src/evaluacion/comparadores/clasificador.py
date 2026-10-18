"""Comparador con el modelo entrenado (datos/entrenamientos/run_N/modelo.joblib).

Convierte los kpoints de la repeticion en el MISMO vector que vio al entrenar
(procesamiento/puntos/vectorizar.py); el puntaje es P(bien) 0-100."""

from __future__ import annotations

import json
from collections import deque
from pathlib import Path

import numpy as np

from src.nucleo.config import ENTRENAMIENTOS_DIR
from src.nucleo.tipos import Score, Segment
from src.procesamiento.puntos import vectorizar


class Clasificador:
    """Modelo de datos/entrenamientos/run_N cargado para puntuar en vivo."""

    def __init__(self, ruta: Path) -> None:
        import joblib
        datos = joblib.load(ruta)
        if "spec" not in datos:
            raise ValueError(f"{ruta.parent.name}: modelo entrenado antes de guardar su 'spec'; "
                             "vuelve a entrenar para usarlo en vivo")
        self.ruta = Path(ruta)
        self.run = self.ruta.parent.name
        self.modelo = datos["modelo"]
        self.clases = list(datos["clases"])
        self.nombre = datos.get("nombre", "?")
        self.spec = datos["spec"]
        self.point_names = self.spec.get("point_names") or [kp["nombre"] for kp in self.spec.get("kpoints", [])]

    def puntuar(self, segment: Segment, template) -> Score:
        names = list(template.names) if template is not None else []
        vacio = np.full(len(names), np.nan, dtype=np.float32)
        vec = None
        if segment.kpoints is not None and len(segment.kpoints):
            vec = vectorizar.vector_de_clip(segment.kpoints, self.point_names, self.spec)
        if vec is None or vec.size != self.spec.get("n_features", vec.size):
            # sin kpoints en esta rep (puntos fuera de cuadro): no se inventa un puntaje
            return Score(total=float("nan"), error_z=float("nan"), per_feature=vacio,
                         feature_names=names, duration_ms=segment.duration_ms, clase="")
        if hasattr(self.modelo, "predict_proba"):
            proba = self.modelo.predict_proba(vec[None, :])[0]
            clase = self.clases[int(np.argmax(proba))]
            total = 100.0 * float(proba[self.clases.index("bien")]) if "bien" in self.clases else 100.0 * float(np.max(proba))
        else:
            clase = self.clases[int(self.modelo.predict(vec[None, :])[0])]
            total = 100.0 if clase == "bien" else 0.0
        return Score(total=total, error_z=float("nan"), per_feature=vacio, feature_names=names,
                     duration_ms=segment.duration_ms, clase=clase)

    def to_dict(self) -> dict:
        return {"run": self.run, "modelo": self.nombre, "clases": self.clases,
                "exercise": self.spec.get("exercise")}


class DetectorCiclos:
    """Cuenta ciclos solo con el modelo: ventana deslizante del largo de un ciclo (spec['ventana_ms']) sobre los
    kpoints en vivo. P(ciclo) = 1 - P(fuera); un ciclo se cuenta cuando sube de ALTO y vuelve a bajar de BAJO."""
    ALTO, BAJO, PASO_MS = 0.6, 0.4, 150   # ponytail: umbrales fijos; subir ALTO si cuenta de mas, bajarlo si se salta ciclos

    def __init__(self, clf: Clasificador) -> None:
        self.clf, self.W = clf, int(clf.spec["ventana_ms"])
        self.i_fuera = clf.clases.index("fuera")
        self.buf: deque = deque()
        self.activo, self.mejor, self._t = False, None, float("-inf")

    def update(self, t_ms: int, kp) -> dict | None:
        """kp = kpoints (K,3) de este cuadro. Devuelve {"clase","p_bien","p_ciclo"} al cerrar un ciclo, o None."""
        self.buf.append((t_ms, kp))
        while self.buf[0][0] < t_ms - self.W:
            self.buf.popleft()
        if t_ms - self.buf[0][0] < 0.9 * self.W or t_ms - self._t < self.PASO_MS:
            return None
        self._t = t_ms
        clf = self.clf
        vec = vectorizar.vector_de_clip(np.stack([k for _, k in self.buf]), clf.point_names, clf.spec)
        if vec is None or vec.size != clf.spec.get("n_features", vec.size):
            return None
        if hasattr(clf.modelo, "predict_proba"):
            proba = clf.modelo.predict_proba(vec[None, :])[0]
        else:
            proba = np.eye(len(clf.clases))[int(clf.modelo.predict(vec[None, :])[0])]
        p = 1.0 - float(proba[self.i_fuera])
        if not self.activo:
            if p >= self.ALTO:
                self.activo, self.mejor = True, (p, proba)
            return None
        if p > self.mejor[0]:
            self.mejor = (p, proba)
        if p >= self.BAJO:
            return None
        self.activo, (pico, proba) = False, self.mejor
        otras = [i for i, c in enumerate(clf.clases) if c in ("bien", "mal")] or [i for i in range(len(proba)) if i != self.i_fuera]
        i = max(otras, key=lambda j: proba[j])
        pb = float(proba[clf.clases.index("bien")]) if "bien" in clf.clases else pico
        return {"clase": clf.clases[i], "p_bien": pb, "p_ciclo": pico}


def buscar_clasificador(exercise: str, base_dir: Path = ENTRENAMIENTOS_DIR) -> Path | None:
    """El modelo.joblib mas reciente entrenado con clips de 'exercise' y con
    spec (los entrenados antes de esta version no la tienen)."""
    if not base_dir.exists():
        return None
    runs = sorted((p for p in base_dir.glob("run_*") if p.name[4:].isdigit()),
                  key=lambda p: int(p.name[4:]), reverse=True)
    for run in runs:
        meta, modelo = run / "meta.json", run / "modelo.joblib"
        if not (meta.exists() and modelo.exists()):
            continue
        try:
            m = json.loads(meta.read_text("utf-8"))
        except Exception:
            continue
        if m.get("exercise") == exercise and m.get("criterio"):   # 'criterio' = version con spec
            return modelo
    return None


def cargar_clasificador(exercise: str) -> Clasificador | None:
    ruta = buscar_clasificador(exercise)
    if ruta is None:
        return None
    try:
        return Clasificador(ruta)
    except Exception:
        return None
