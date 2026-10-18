"""Bus de eventos y sumideros: el extremo final del pipeline.

Viven aparte de pipeline.py por una razon concreta: aqui no se importa
mediapipe. Asi los sumideros, el bus y sus tests se pueden usar sin la pila de
vision instalada, igual que types.py.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

import numpy as np

from src.evaluacion import comparadores as scorers
from src.evaluacion.plantilla import Template, build_template
from src.nucleo.tipos import FeatureVec, Frame, Segment

if TYPE_CHECKING:   # solo para las anotaciones (evita import circular)
    from src.sesion.pipeline import Pipeline

Evento = dict


class EventBus:
    """Un solo flujo de eventos, consumido por igual por la ventana y el panel web."""

    def __init__(self) -> None:
        self._subs: list[Callable[[Evento], None]] = []

    def subscribe(self, fn: Callable[[Evento], None]) -> None:
        self._subs.append(fn)

    def emit(self, evento: Evento) -> None:
        for fn in list(self._subs):
            try:
                fn(evento)
            except Exception:  # un consumidor caido no puede tumbar la captura
                pass


class Sink:
    es_contador = False   # True = vista previa que cuenta/clasifica reps pero no graba (no cuenta como "grabando")
    n: int | None = None  # repeticiones contadas por este sumidero (None = no cuenta)

    def on_start(self, pipe: Pipeline) -> None: ...
    # TODOS los cuadros de la camara (hilo de captura, a los fps de la camara):
    # lo usa VideoLogger para que el video grabado sea fluido aunque la
    # deteccion vaya mas lenta. on_frame solo recibe los cuadros procesados.
    def on_raw_frame(self, pipe: Pipeline, frame: Frame) -> None: ...
    def on_frame(self, pipe: Pipeline, frame: Frame, fv: FeatureVec | None) -> None: ...
    def on_rep(self, pipe: Pipeline, seg: Segment) -> None: ...
    def on_stop(self, pipe: Pipeline) -> None: ...


class MultiSink(Sink):
    """Reparte los eventos a varios sumideros en orden.

    Es lo que permite que archivar el video sea un sumidero mas y no una rama
    dentro del pipeline: grabar base + archivar, o evaluar + archivar, son la
    misma composicion.
    """

    def __init__(self, *sinks: Sink) -> None:
        self.sinks = [s for s in sinks if s is not None]

    def find(self, tipo):
        for s in self.sinks:
            if isinstance(s, tipo):
                return s
        return None

    def on_start(self, pipe): [s.on_start(pipe) for s in self.sinks]
    def on_raw_frame(self, pipe, frame): [s.on_raw_frame(pipe, frame) for s in self.sinks]
    def on_frame(self, pipe, frame, fv): [s.on_frame(pipe, frame, fv) for s in self.sinks]
    def on_rep(self, pipe, seg): [s.on_rep(pipe, seg) for s in self.sinks]
    def on_stop(self, pipe): [s.on_stop(pipe) for s in self.sinks]


class Recorder(Sink):
    """Modo grabacion: acumula la toma y al cerrar construye la plantilla."""

    def __init__(self, out_path, radius_frac: float = 0.15) -> None:
        self.out_path = out_path
        self.radius_frac = radius_frac
        self.frames: list[FeatureVec] = []
        self.template: Template | None = None
        self.error: str | None = None

    def on_frame(self, pipe: Pipeline, frame: Frame, fv: FeatureVec | None) -> None:
        if fv is not None and fv.any_valid:
            self.frames.append(fv)

    def on_stop(self, pipe: Pipeline) -> None:
        try:
            self.template = build_template(
                self.frames, pipe.exercise, pipe.extractor, self.radius_frac
            )
            self.template.save(self.out_path)
            pipe.bus.emit({
                "type": "template_saved",
                "exercise": pipe.exercise.slug,
                "template": self.template.to_dict(),
            })
        except Exception as e:
            self.error = str(e)
            pipe.bus.emit({"type": "error", "message": str(e)})


class Evaluator(Sink):
    """Modo evaluacion: puntua cada repeticion y la registra.

    Corre TODOS los modelos de src/evaluacion/comparadores/ en cada repeticion (son
    baratos: milisegundos) para poder comparar puntaje y tiempo entre
    arquitecturas con la misma toma. Solo el modelo activo (`modelo`) decide
    el puntaje "oficial" que se guarda y que mueve el semaforo del panel.
    """

    def __init__(self, template: Template, storage=None, target_reps: int = 0,
                 session_id: int | None = None, modelo: str = scorers.DEFAULT_MODEL,
                 clasificador: scorers.Clasificador | None = None) -> None:
        self.template = template
        self.storage = storage
        self.target_reps = target_reps
        self.session_id = session_id
        self.clasificador = clasificador
        validos = set(scorers.MODELOS) | ({scorers.CLAVE_CLASIFICADOR} if clasificador else set())
        self.modelo = modelo if modelo in validos else scorers.DEFAULT_MODEL
        self.scores: list[float] = []

    @property
    def n(self) -> int:
        return len(self.scores)

    def on_rep(self, pipe: Pipeline, seg: Segment) -> None:
        resultados = scorers.comparar_todos(seg, self.template, self.clasificador)
        modelo = self.modelo
        score = resultados[modelo]["score"]
        if not np.isfinite(score.total):   # clasificador sin kpoints en esta rep: cae al DTW
            modelo = scorers.DEFAULT_MODEL
            score = resultados[modelo]["score"]
        self.scores.append(score.total)
        if self.storage is not None:
            self.storage.log_rep(pipe.exercise.slug, score, self.session_id, modelo)
        pipe.last_score = score.total
        pipe.bus.emit({
            "type": "rep",
            "exercise": pipe.exercise.slug,
            "n": len(self.scores),
            "target": self.target_reps,
            "modelo": modelo,
            "score": score.to_dict(),
            "peor": [{"feature": n, "desvio": v} for n, v in score.worst(2)],
            "promedio": round(float(np.mean(self.scores)), 1),
            "clasificador": None if self.clasificador is None else {
                "run": self.clasificador.run,
                "clase": resultados[scorers.CLAVE_CLASIFICADOR]["score"].clase or None},
            "modelos": {
                clave: {"nombre": r["nombre"],
                        "total": None if not np.isfinite(r["score"].total) else round(r["score"].total, 1),
                        "clase": r["score"].clase or None,
                        "latencia_ms": r["latencia_ms"]}
                for clave, r in resultados.items()
            },
        })


class Contador(Evaluator):
    """Vista previa con camara prendida: cuenta cada repeticion (con la base) y, si hay modelo entrenado, la clasifica,
    sin guardar nada (storage=None). Es lo que deja ver en el panel si el modelo esta contando."""
    es_contador = True

    def __init__(self, template: Template, clasificador: scorers.Clasificador | None = None,
                 modelo: str = scorers.CLAVE_CLASIFICADOR) -> None:
        super().__init__(template, storage=None, clasificador=clasificador, modelo=modelo)


class ContadorModelo(Sink):
    """Vista previa que cuenta ciclos SOLO con el modelo entrenado (clase "fuera" + ventana deslizante): no
    necesita base ni umbrales. Emite el mismo evento "rep" que Evaluator."""
    es_contador = True

    def __init__(self, clasificador: scorers.Clasificador) -> None:
        self.clasificador = clasificador
        self.detector = scorers.DetectorCiclos(clasificador)
        self.n, self.scores = 0, []

    def on_frame(self, pipe: Pipeline, frame: Frame, fv: FeatureVec | None) -> None:
        if fv is None or fv.kpoints is None:
            return
        r = self.detector.update(fv.t_ms, fv.kpoints)
        if r is None:
            return
        self.n += 1
        total = 100.0 * r["p_bien"]
        self.scores.append(total)
        pipe.last_score = total
        pipe.bus.emit({
            "type": "rep", "exercise": pipe.exercise.slug, "n": self.n, "target": 0,
            "modelo": scorers.CLAVE_CLASIFICADOR, "contador": "modelo", "score": {"total": total},
            "peor": [{"feature": "", "desvio": 0.0}], "promedio": round(float(np.mean(self.scores)), 1),
            "modelos": {},
            "clasificador": {"run": self.clasificador.run, "clase": r["clase"]},
        })
