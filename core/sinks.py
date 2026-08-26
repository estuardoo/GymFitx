"""Bus de eventos y sumideros: el extremo final del pipeline.

Viven aparte de pipeline.py por una razon concreta: aqui no se importa
mediapipe. Asi los sumideros, el bus y sus tests se pueden usar sin la pila de
vision instalada, igual que types.py.
"""

from __future__ import annotations

from typing import Callable

import numpy as np

from .compare import compare
from .template import Template
from .types import FeatureVec, Frame, Segment

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
    def on_start(self, pipe: "Pipeline") -> None: ...
    def on_frame(self, pipe: "Pipeline", frame: Frame, fv: FeatureVec | None) -> None: ...
    def on_rep(self, pipe: "Pipeline", seg: Segment) -> None: ...
    def on_stop(self, pipe: "Pipeline") -> None: ...


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

    def on_frame(self, pipe: "Pipeline", frame: Frame, fv: FeatureVec | None) -> None:
        if fv is not None and fv.any_valid:
            self.frames.append(fv)

    def on_stop(self, pipe: "Pipeline") -> None:
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
    """Modo evaluacion: puntua cada repeticion y la registra."""

    def __init__(self, template: Template, storage=None, target_reps: int = 0,
                 session_id: int | None = None) -> None:
        self.template = template
        self.storage = storage
        self.target_reps = target_reps
        self.session_id = session_id
        self.scores: list[float] = []

    def on_rep(self, pipe: "Pipeline", seg: Segment) -> None:
        score = compare(seg, self.template)
        self.scores.append(score.total)
        if self.storage is not None:
            self.storage.log_rep(pipe.exercise.slug, score, self.session_id)
        pipe.last_score = score.total
        pipe.bus.emit({
            "type": "rep",
            "exercise": pipe.exercise.slug,
            "n": len(self.scores),
            "target": self.target_reps,
            "score": score.to_dict(),
            "peor": [{"feature": n, "desvio": v} for n, v in score.worst(2)],
            "promedio": round(float(np.mean(self.scores)), 1),
        })
