"""Orquestacion. El corazon del diseño: UN pipeline, sumideros intercambiables.

Grabar la plantilla y evaluar una serie recorren exactamente las mismas capas
1 a 5. Lo unico que cambia es el sumidero del final. Es lo que garantiza que la
plantilla grabada y la repeticion evaluada se midan con la misma vara: no hay
dos rutas que puedan desincronizarse porque no hay dos rutas.

En modo grabacion no hay segmentador: todavia no existen umbrales. La toma se
segmenta despues, offline, con los umbrales que la propia toma produce.

Pausa: la camara sigue entregando cuadros mientras el usuario tiene la sesion
en pausa (no se puede pausar el sensor), pero esos cuadros no llegan a ningun
lado: no se trackean, no se archivan y no cuentan repeticiones. El tiempo que
dura la pausa se resta de la linea de tiempo que ven el filtro, el segmentador
y el archivador (`_pause_offset_ms`), asi que al reanudar todo continua como
si la pausa nunca hubiera existido -- sin saltos en el video archivado ni
sobresaltos en el filtro por un dt gigante.
"""

from __future__ import annotations

import threading
import time
from collections import deque
from collections.abc import Callable

import numpy as np

from . import overlay
from .features import FeatureExtractor, angle_deg
from .filters import OneEuroFilter
from .landmarks import HAND_LANDMARKS, region_indices
from .segmenter import RepSegmenter

# Los sumideros y el bus viven en core/sinks.py (no importan mediapipe).
# Se reexportan aqui para que `from core.pipeline import Evaluator` siga siendo valido.
from .sinks import Evaluator, EventBus, Evento, MultiSink, Recorder, Sink  # noqa: E402,F401
from .template import Template
from .tracker import HandTracker, build_tracker
from .types import FeatureVec, Frame

# Gesto de control: abrir y cerrar la mano izquierda en la esquina superior
# izquierda de la imagen inicia/detiene la grabacion sin tocar el mouse, para
# cuando las manos estan ocupadas en el ejercicio. Corre SIEMPRE (sea el
# ejercicio de pose o de manos) con su propio HandTracker chico, recortado a
# esa esquina -- recortar antes de trackear abarata la deteccion en vez de
# correrla sobre el cuadro entero.
_DEDOS = (
    ("INDEX_FINGER_MCP", "INDEX_FINGER_PIP", "INDEX_FINGER_DIP"),
    ("MIDDLE_FINGER_MCP", "MIDDLE_FINGER_PIP", "MIDDLE_FINGER_DIP"),
    ("RING_FINGER_MCP", "RING_FINGER_PIP", "RING_FINGER_DIP"),
    ("PINKY_MCP", "PINKY_PIP", "PINKY_DIP"),
)
_IDX_DEDOS = tuple(tuple(HAND_LANDMARKS.index(n) for n in dedo) for dedo in _DEDOS)

GESTO_RECORTE = 0.318         # esquina superior izquierda. El area es frac^2 del
                               # cuadro: 0.318 =~ 0.45 / sqrt(2), la mitad de area
                               # que el 0.45 original (a pedido: "50% menor en area")
# ponytail: umbrales de curl fijos (no calibrados por persona/camara), con
# zona muerta entre medio para no parpadear entre abierta/cerrada cuadro a
# cuadro. Si en la practica no distinguen bien, calibrar por sesion como ya
# se hace con la plantilla de cada ejercicio (Template.low/high).
GESTO_UMBRAL_ABIERTA = 130.0  # grados promedio de curl por encima = mano abierta
GESTO_UMBRAL_CERRADA = 90.0   # por debajo = puño cerrado


class Pipeline:
    """Capas 1-6 encadenadas. No decide nada: obedece al Exercise y al Sink."""

    ESTADO_CADA = 4  # cuadros entre eventos de estado (evita inundar el WebSocket)

    def __init__(
        self,
        exercise,
        source,
        sink: Sink,
        template: Template | None = None,
        bus: EventBus | None = None,
        annotate: bool = True,
    ) -> None:
        self.exercise = exercise
        self.source = source
        self.sink = sink
        self.template: Template | None = None
        self.bus = bus or EventBus()
        self.annotate = annotate

        self.extractor = FeatureExtractor(exercise)
        self.tracker = build_tracker(exercise)
        self.filter = OneEuroFilter(self.extractor.size, self.extractor.units)
        self.segmenter: RepSegmenter | None = None
        if template is not None:
            self.set_template(template)

        self.fps = 0.0
        self.last_score = float("nan")
        self.frames_vistos = 0
        self._latencias: deque[float] = deque(maxlen=30)
        self._lock = threading.Lock()
        self._sink_lock = threading.Lock()
        self._latest = None  # ultimo cuadro anotado, para el streaming MJPEG

        self._paused = threading.Event()
        self._pause_offset_ms = 0
        self._paused_since: int | None = None

        # Protege tracker/extractor/filter/segmenter contra un cambio de
        # ejercicio en caliente (set_exercise, desde el hilo del servidor)
        # mientras el hilo de captura esta a mitad de un cuadro.
        self._tracker_lock = threading.Lock()

        # Que regiones del cuerpo se dibujan en el overlay (solo aplica a
        # detecciones "pose"; "hands" siempre se dibuja entera). None = todas.
        self.regiones: list[str] | None = None
        self._visibles: set[int] | None = None

        # Tracker de gesto, independiente del de la deteccion principal (ver
        # _revisar_gesto_mano). Se arma siempre, la region que analiza igual
        # queda vacia mientras nadie mueva la mano ahi.
        self._tracker_gesto = HandTracker(num_hands=1)
        self._gesto_mano_estado: str | None = None   # "abierta" | "cerrada" | None

        # "Dedos detallados": HandTracker opcional para ver los dedos de
        # verdad en ejercicios de cuerpo completo (el PoseLandmarker no trae
        # nudillos). Apagado por defecto y armado recien al activarlo -- no
        # siempre se usa, depende de si el usuario prende el boton (ver
        # set_manos_detalle), asi que no tiene sentido pagar el costo de un
        # segundo modelo siempre corriendo.
        self._manos_detalle_activo = False
        self._tracker_manos_detalle: HandTracker | None = None

    def sink_of(self, tipo):
        """El sumidero de este tipo, este solo o dentro de un MultiSink."""
        if isinstance(self.sink, MultiSink):
            return self.sink.find(tipo)
        return self.sink if isinstance(self.sink, tipo) else None

    @property
    def grabando(self) -> bool:
        """True si el sumidero actual ya no es el placeholder de
        previsualizacion. OJO: tiene que ser 'type(...) is Sink', NO
        'isinstance(..., Sink)' -- Recorder/Evaluator/MultiSink heredan de
        Sink, asi que isinstance() da True para TODOS los sumideros
        (grabando o no) y nunca distingue nada.
        """
        return type(self.sink) is not Sink

    def set_template(self, template: Template) -> None:
        """Instala o reemplaza la plantilla de esta sesion sin reabrir la
        camara: reconstruye el segmentador con los nuevos umbrales.

        Es lo que permite, dentro de la MISMA sesion de camara, grabar la
        base de un ejercicio que todavia no tenia y evaluar contra ella acto
        seguido -- sin apagar y volver a prender.
        """
        self.template = template
        self.segmenter = RepSegmenter(
            n_features=self.extractor.size,
            signal_idx=self.extractor.signal_idx,
            reduce=self.extractor.signal_reduce,
            low=template.low,
            high=template.high,
            direction=self.exercise.direction,
            min_duration_ms=self.exercise.min_duration_ms,
            max_duration_ms=self.exercise.max_duration_ms,
        )

    def set_exercise(self, exercise, template: Template | None = None) -> None:
        """Cambia de ejercicio SIN reabrir la camara: reconstruye tracker,
        extractor y filtro para el ejercicio nuevo (puede ser de otra fuente,
        manos o pose). Es lo que permite elegir otro de la lista de rutina
        con la camara ya prendida, sin el corte de apagar/prender.

        El tracker nuevo se arma ANTES de tomar el lock (puede tardar
        milisegundos en crear el landmarker) para no bloquear el hilo de
        captura mientras tanto; el swap de referencias es rapido y atomico
        bajo el lock, y el tracker viejo se cierra DESPUES de soltarlo.
        """
        nuevo_tracker = build_tracker(exercise)
        nuevo_extractor = FeatureExtractor(exercise)
        nuevo_filtro = OneEuroFilter(nuevo_extractor.size, nuevo_extractor.units)
        with self._tracker_lock:
            viejo_tracker = self.tracker
            self.exercise = exercise
            self.tracker = nuevo_tracker
            self.extractor = nuevo_extractor
            self.filter = nuevo_filtro
            self.template = None
            self.segmenter = None
        viejo_tracker.close()
        if template is not None:
            self.set_template(template)

    def set_fps(self, fps: int) -> bool:
        """Delega en la fuente si sabe hacerlo en caliente (solo CameraSource;
        VideoSource no tiene FPS que pedir). Ver CameraSource.set_fps."""
        cambiar = getattr(self.source, "set_fps", None)
        return bool(cambiar(fps)) if cambiar else False

    def set_regiones(self, nombres: list[str] | None) -> None:
        """Cambia en caliente que partes del cuerpo se dibujan en el video,
        sin reabrir la camara ni tocar la deteccion (el modelo pose sigue
        midiendo el cuerpo entero; esto solo filtra el dibujo). None = todas.
        """
        self.regiones = nombres
        self._visibles = region_indices(nombres)

    def set_manos_detalle(self, activo: bool) -> None:
        """Prende/apaga los dedos articulados de verdad (HandLandmarker)
        sobre ejercicios de cuerpo completo. El tracker se arma la primera
        vez que se activa (no en __init__) y despues queda armado para que
        prender/apagar dentro de la misma sesion sea instantaneo; se cierra
        recien en run() al terminar la sesion, junto con los demas trackers.
        """
        if activo and self._tracker_manos_detalle is None:
            self._tracker_manos_detalle = HandTracker(num_hands=2)
        self._manos_detalle_activo = activo

    def swap_sink(self, nuevo: Sink) -> Sink:
        """Cambia el sumidero sin detener la camara ni el hilo del pipeline.

        Cierra el sumidero anterior (on_stop) antes de instalar el nuevo, asi
        que quien llama puede leer sus resultados (plantilla, rutas de video)
        en el valor devuelto. Esto es lo que separa "prender la camara" de
        "grabar": los dos corren el mismo pipeline, solo cambia que hace cada
        sumidero con los cuadros. El lock evita que on_stop() se cruce con un
        on_frame() todavia en marcha en el hilo de captura (p.ej. el
        VideoWriter cerrandose a mitad de una escritura).

        Si el sumidero anterior revienta al cerrar (p.ej. VideoLogger si el
        disco falla a mitad de escritura), el swap AL SUMIDERO NUEVO tiene
        que pasar igual: si no, "detener grabacion" queda trabado en el
        sumidero viejo -- se ve el aviso de "grabando" pero cerrar/guardar
        nunca ocurre, porque la excepcion nunca llega a nadie (el gesto la
        dispara desde el bus, que traga cualquier excepcion del que escucha).
        El error se avisa por el bus en vez de perderse en silencio.
        """
        with self._sink_lock:
            anterior = self.sink
            try:
                anterior.on_stop(self)
            except Exception as e:
                self.bus.emit({"type": "error",
                               "message": f"Error al cerrar la grabacion anterior: {e}"})
            self.sink = nuevo
            nuevo.on_start(self)
            return anterior

    @property
    def latest_frame(self):
        with self._lock:
            return None if self._latest is None else self._latest.copy()

    # -- pausa --
    @property
    def is_paused(self) -> bool:
        return self._paused.is_set()

    def pause(self) -> None:
        self._paused.set()

    def resume(self) -> None:
        self._paused.clear()

    def run(self, should_stop: Callable[[], bool] | None = None) -> None:
        should_stop = should_stop or (lambda: False)
        with self._sink_lock:
            self.sink.on_start(self)
        self.bus.emit({"type": "started", "exercise": self.exercise.slug,
                       "modo": "grabar" if self.segmenter is None else "evaluar"})
        try:
            for frame in self.source.frames():
                if should_stop():
                    break
                self._procesar(frame)
        finally:
            with self._sink_lock:
                self.sink.on_stop(self)
            self.tracker.close()
            self._tracker_gesto.close()
            if self._tracker_manos_detalle is not None:
                self._tracker_manos_detalle.close()
            self.source.close()
            self.bus.emit({"type": "stopped", "exercise": self.exercise.slug,
                           "frames": self.frames_vistos})

    def _procesar(self, frame: Frame) -> None:
        if self._paused.is_set():
            if self._paused_since is None:
                self._paused_since = frame.t_ms
            if self.annotate:
                self._anotar_pausado(frame)
            return

        if self._paused_since is not None:
            # La pausa termino: ese tramo de tiempo real se descuenta de la
            # linea de tiempo que ve el resto del pipeline.
            self._pause_offset_ms += frame.t_ms - self._paused_since
            self._paused_since = None

        frame = Frame(image=frame.image, t_ms=frame.t_ms - self._pause_offset_ms,
                     index=frame.index)

        t0 = time.perf_counter()
        with self._tracker_lock:
            detecciones = self.tracker.detect(frame)
            fv = self.extractor.extract(detecciones, frame.t_ms)

        if fv is not None:
            suave = self.filter.update(fv.values, frame.t_ms)
            fv = FeatureVec(values=suave, valid=~np.isnan(suave), t_ms=frame.t_ms)

        seg = None
        if fv is not None and self.segmenter is not None:
            seg = self.segmenter.update(fv)

        with self._sink_lock:
            self.sink.on_frame(self, frame, fv)
            if seg is not None:
                self.sink.on_rep(self, seg)

        self._revisar_gesto_mano(frame)

        self._latencias.append(time.perf_counter() - t0)
        self.fps = 1.0 / max(sum(self._latencias) / len(self._latencias), 1e-6)
        self.frames_vistos += 1

        if self.annotate:
            self._anotar(frame, detecciones, fv)
        if self.frames_vistos % self.ESTADO_CADA == 0:
            self._emitir_estado(fv, len(detecciones))

    def _revisar_gesto_mano(self, frame: Frame) -> None:
        """Recorta la esquina superior izquierda del cuadro, busca una mano
        ahi y avisa por el bus en cuanto detecta el cierre (dedos hacia la
        palma) -- quien escuche decide que hacer (el panel manda la MISMA
        accion grabar/detener que usan los botones, sin logica propia: ver
        _al_bus_gestos en apps/serve.py). Con una sola vez que cierre el
        puno alcanza, no hace falta que antes se vea la mano abierta.
        """
        h, w = frame.image.shape[:2]
        recorte = frame.image[: int(h * GESTO_RECORTE), : int(w * GESTO_RECORTE)]
        manos = self._tracker_gesto.detect(Frame(image=recorte, t_ms=frame.t_ms, index=frame.index))
        if not manos:
            self._gesto_mano_estado = None
            return

        world = manos[0].world
        curl = float(np.mean([angle_deg(world[a], world[b], world[c]) for a, b, c in _IDX_DEDOS]))
        if self._clasificar_gesto_mano(curl):
            self.bus.emit({"type": "gesto", "gesto": "mano_abrir_cerrar"})

    def _clasificar_gesto_mano(self, curl: float) -> bool:
        """Logica pura del gesto, separada de la deteccion para poder
        probarla sin camara ni tracker: clasifica el curl en abierta/cerrada
        (con zona muerta entre medio, para no parpadear) y devuelve True
        justo en el cuadro donde el puno se acaba de cerrar -- sin exigir
        haber visto la mano abierta antes (alcanza con el cierre, una vez).
        """
        if curl > GESTO_UMBRAL_ABIERTA:
            nuevo_estado = "abierta"
        elif curl < GESTO_UMBRAL_CERRADA:
            nuevo_estado = "cerrada"
        else:
            nuevo_estado = self._gesto_mano_estado

        disparo = self._gesto_mano_estado != "cerrada" and nuevo_estado == "cerrada"
        self._gesto_mano_estado = nuevo_estado
        return disparo

    def _anotar_pausado(self, frame: Frame) -> None:
        """Mientras esta en pausa: se sigue viendo la camara, pero marcada."""
        img = frame.image.copy()
        overlay.draw_panel(img, [
            (self.exercise.name, overlay.COLOR_OK),
            ("PAUSADO", overlay.COLOR_WARN),
            ("nada se esta grabando ni contando", overlay.COLOR_TEXT),
        ])
        with self._lock:
            self._latest = img

    def _anotar(self, frame: Frame, detecciones, fv: FeatureVec | None) -> None:
        img = frame.image.copy()
        # Zona de control por gesto: se tinta solo mientras hay una mano ahi
        # (abierta o cerrada, ver _revisar_gesto_mano), verde si cerrar el
        # puno va a INICIAR la grabacion, rojo si ya se esta grabando y va a
        # DETENERLA. Se dibuja antes del panel de texto para que el panel
        # (que vive en la misma esquina) quede legible encima.
        if self._gesto_mano_estado is not None:
            color = overlay.COLOR_BAD if self.grabando else overlay.COLOR_OK
            overlay.draw_zona_gesto(img, GESTO_RECORTE, color)

        # Dedos detallados: solo tiene sentido en ejercicios de cuerpo
        # completo -- en "hands" la deteccion principal YA es el
        # HandLandmarker de 21 puntos (ver overlay.draw_landmarks).
        dedos_activo = (self._manos_detalle_activo
                        and self._tracker_manos_detalle is not None
                        and self.exercise.source == "pose")
        for d in detecciones:
            vis = self._visibles if d.source == "pose" else None
            omitir_manos = dedos_activo and d.source == "pose"
            overlay.draw_landmarks(img, d, visibles=vis, omitir_manos=omitir_manos)

        if dedos_activo:
            for mano in self._tracker_manos_detalle.detect(frame):
                overlay.draw_landmarks(img, mano)

        # Panel de texto quemado en el video: solo lo esencial (nombre, fps,
        # puntos detectados). Angulos, estado y reps ya se ven en el panel
        # HTML de al lado -- repetirlos aqui solo tapa la imagen.
        n_puntos = sum(len(d.screen) for d in detecciones)
        overlay.draw_panel(img, [
            (self.exercise.name, overlay.COLOR_OK),
            (f"FPS {self.fps:5.1f}", overlay.COLOR_TEXT),
            (f"puntos: {n_puntos}", overlay.COLOR_TEXT),
        ])

        if self.segmenter is not None:
            overlay.draw_signal_bar(img, self.segmenter.last_signal,
                                    self.template.low, self.template.high)
            if not np.isnan(self.last_score):
                overlay.draw_big_score(img, self.last_score, self.segmenter.reps)

        with self._lock:
            self._latest = img

    def _emitir_estado(self, fv: FeatureVec | None, n_det: int) -> None:
        features = {}
        if fv is not None:
            features = {
                n: (None if np.isnan(v) else round(float(v), 1))
                for n, v in zip(self.extractor.names, fv.values)
            }
        self.bus.emit({
            "type": "status",
            "exercise": self.exercise.slug,
            "fps": round(self.fps, 1),
            "detecciones": n_det,
            "features": features,
            "unidades": self.extractor.units,
            "señal": None if (self.segmenter is None or np.isnan(self.segmenter.last_signal))
                     else round(self.segmenter.last_signal, 2),
            "low": None if self.template is None else round(self.template.low, 2),
            "high": None if self.template is None else round(self.template.high, 2),
            "estado": None if self.segmenter is None else self.segmenter.state,
            "reps": 0 if self.segmenter is None else self.segmenter.reps,
            "frames": self.frames_vistos,
        })
