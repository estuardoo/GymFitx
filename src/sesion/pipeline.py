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

Rendimiento (camara en vivo). Dos hilos, cada uno a su ritmo:
  captura    lee la camara a sus fps reales, escribe el video (on_raw_frame)
             y pinta la vista previa con la ultima deteccion disponible.
  deteccion  toma SIEMPRE el cuadro mas reciente (descarta los que no alcanza)
             y corre la pose (33 puntos); el gesto de control sale de esa misma pose.
Antes todo era un solo hilo en serie: la grabacion quedaba a ~7 fps con 70 %
de cuadros congelados. Con un video (VideoSource, tests) se sigue procesando
cuadro por cuadro en orden, para que el resultado sea repetible.
"""

from __future__ import annotations

import threading
import time
from collections import deque
from collections.abc import Callable

import numpy as np

from src.captura.deteccion.tracker import build_tracker
from src.evaluacion.plantilla import Template
from src.evaluacion.segmentador import RepSegmenter
from src.nucleo import reglas as REGLAS
from src.nucleo.landmarks import region_indices
from src.nucleo.tipos import FeatureVec, Frame
from src.procesamiento.medidas.features import FeatureExtractor
from src.procesamiento.medidas.filtros import OneEuroFilter
from src.procesamiento.puntos import kpoints as KP
from src.sesion import overlay
from src.sesion.gesto import GESTO_RECORTE, Gesto

# Los sumideros y el bus viven en src/sesion/sumideros.py (no importan mediapipe).
# Se reexportan aqui para que `from src.sesion.pipeline import Evaluator` siga siendo valido.
from src.sesion.sumideros import (  # noqa: E402,F401
    Contador,
    ContadorModelo,
    Evaluator,
    EventBus,
    Evento,
    MultiSink,
    Recorder,
    Sink,
)


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
        self.latest_version = 0   # sube con cada cuadro anotado nuevo (el stream no reenvia repetidos)

        self._paused = threading.Event()
        self._pause_offset_ms = 0
        self._paused_since: int | None = None

        # Protege tracker/extractor/filter/segmenter contra un cambio de
        # ejercicio en caliente (set_exercise, desde el hilo del servidor)
        # mientras el hilo de captura esta a mitad de un cuadro.
        self._tracker_lock = threading.Lock()

        # Que regiones del cuerpo se dibujan en el overlay None = todas.
        self.regiones: list[str] | None = None
        self._visibles: set[int] | None = None

        # Gesto de control (sesion/gesto.py): muneca sostenida en la esquina, sale de la misma pose.
        self.gesto = Gesto(lambda: self.bus.emit({"type": "gesto", "gesto": "muneca_esquina"}))

        # kpoints en vivo (para el clasificador dataset): se arman por cuadro con
        # src.procesamiento.puntos.kpoints.resolver, la misma funcion del dataset offline. Solo se
        # activan cuando hay un clasificador que los usa (set_kpoints_vivo).
        self._kpoints_vivo = False
        self._kpoints_catalogo: list[dict] = []

        # Captura desacoplada (solo fuentes en_vivo)
        self._en_vivo = False
        self._slot_lock = threading.Lock()
        self._pendiente: Frame | None = None
        self._ultimo_resultado: tuple = ([], None)   # (detecciones, fv) para la vista previa
        self._reglas_res: list[dict] = []            # reglas de postura del ultimo cuadro (verde/rojo)
        self.fps_camara = 0.0
        self.frames_camara = 0
        self.frames_descartados = 0
        self._t_camara: deque[float] = deque(maxlen=30)
        self.motivo_fin: str | None = None

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
        return type(self.sink) is not Sink and not self.sink.es_contador

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
            fin=template.fin,
            direction=self.exercise.direction,
            min_duration_ms=self.exercise.min_duration_ms,
            max_duration_ms=self.exercise.max_duration_ms,
        )

    def set_exercise(self, exercise, template: Template | None = None) -> None:
        """Cambia de ejercicio SIN reabrir la camara: reconstruye tracker,
        extractor y filtro para el ejercicio nuevo . Es lo que permite elegir otro de la lista de rutina
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
            self._kpoints_vivo, self._kpoints_catalogo = False, []
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

    def set_kpoints_vivo(self, catalogo: list[dict] | None) -> None:
        """Arma en cada cuadro los kpoints de 'catalogo' (el del modelo
        entrenado, asi el orden de los puntos es el mismo que vio al
        entrenar). None/[] = apagado."""
        self._kpoints_catalogo = list(catalogo or [])
        self._kpoints_vivo = bool(self._kpoints_catalogo)

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
            if getattr(self.source, "en_vivo", False):
                self._run_en_vivo(should_stop)
            else:
                for frame in self.source.frames():
                    if should_stop():
                        break
                    self._procesar(frame)
        except Exception as e:   # nunca terminar en silencio: queda en el log
            self.motivo_fin = f"Error en el pipeline: {e}"
            raise
        finally:
            with self._sink_lock:
                self.sink.on_stop(self)
            self.tracker.close()
            self.gesto.close()
            self.source.close()
            motivo = (self.motivo_fin or getattr(self.source, "motivo_fin", None)
                      or ("detenido desde el panel" if should_stop() else "la fuente termino"))
            self.bus.emit({"type": "stopped", "exercise": self.exercise.slug,
                           "frames": self.frames_vistos, "frames_camara": self.frames_camara,
                           "descartados": self.frames_descartados, "motivo": motivo})

    def _run_en_vivo(self, should_stop: Callable[[], bool]) -> None:
        """Hilo de captura (camara -> video + vista previa) separado del de
        deteccion (este), que siempre toma el cuadro mas reciente."""
        self._en_vivo = True
        hay_nuevo = threading.Event()
        termino = threading.Event()

        def capturar() -> None:
            try:
                for frame in self.source.frames():
                    if should_stop():
                        break
                    ajustado = self._entrada(frame)
                    if ajustado is None:
                        continue
                    with self._slot_lock:
                        if self._pendiente is not None:
                            self.frames_descartados += 1
                        self._pendiente = ajustado
                    hay_nuevo.set()
                    if self.annotate:   # vista previa a los fps de la camara
                        dets, fv = self._ultimo_resultado
                        self._anotar(ajustado, dets, fv)
            except Exception as e:
                self.motivo_fin = f"Error leyendo la camara: {e}"
            finally:
                termino.set()
                hay_nuevo.set()

        hilo = threading.Thread(target=capturar, daemon=True, name="captura")
        hilo.start()
        try:
            while not should_stop():
                hay_nuevo.wait(0.5)
                with self._slot_lock:
                    frame, self._pendiente = self._pendiente, None
                    hay_nuevo.clear()
                if frame is None:
                    if termino.is_set():
                        break
                    continue
                self._detectar(frame)
        finally:
            hilo.join(timeout=3)

    def _entrada(self, frame: Frame) -> Frame | None:
        """Pausa + linea de tiempo + video (on_raw_frame). Devuelve el cuadro
        con el tiempo ya ajustado, o None si la sesion esta en pausa."""
        ahora = time.perf_counter()
        self._t_camara.append(ahora)
        self.frames_camara += 1
        if len(self._t_camara) > 1:
            self.fps_camara = (len(self._t_camara) - 1) / max(self._t_camara[-1] - self._t_camara[0], 1e-6)

        if self._paused.is_set():
            if self._paused_since is None:
                self._paused_since = frame.t_ms
            if self.annotate:
                self._anotar_pausado(frame)
            return None

        if self._paused_since is not None:
            # La pausa termino: ese tramo de tiempo real se descuenta de la
            # linea de tiempo que ve el resto del pipeline.
            self._pause_offset_ms += frame.t_ms - self._paused_since
            self._paused_since = None

        frame = Frame(image=frame.image, t_ms=frame.t_ms - self._pause_offset_ms,
                      index=frame.index)
        with self._sink_lock:
            self.sink.on_raw_frame(self, frame)
        return frame

    def _procesar(self, frame: Frame) -> None:
        """Un paso completo en serie (videos y tests): entrada + deteccion."""
        ajustado = self._entrada(frame)
        if ajustado is not None:
            self._detectar(ajustado)

    def _detectar(self, frame: Frame) -> None:
        t0 = time.perf_counter()
        with self._tracker_lock:
            detecciones = self.tracker.detect(frame)
            fv = self.extractor.extract(detecciones, frame.t_ms)
            kp = (KP.resolver(self._kpoints_catalogo, detecciones)
                  if self._kpoints_vivo else None)

        if fv is not None:
            suave = self.filter.update(fv.values, frame.t_ms)
            fv = FeatureVec(values=suave, valid=~np.isnan(suave), t_ms=frame.t_ms,
                            raw=fv.raw, label=fv.label,
                            kpoints=None if kp is None else kp[0])

        seg = None
        if fv is not None and self.segmenter is not None:
            seg = self.segmenter.update(fv)

        with self._sink_lock:
            self.sink.on_frame(self, frame, fv)
            if seg is not None:
                self.sink.on_rep(self, seg)

        self.gesto.evaluar(detecciones, frame.t_ms)
        self._reglas_res = self._evaluar_reglas(detecciones, frame)

        self._latencias.append(time.perf_counter() - t0)
        self.fps = 1.0 / max(sum(self._latencias) / len(self._latencias), 1e-6)
        self.frames_vistos += 1

        self._ultimo_resultado = (detecciones, fv)
        if self.annotate and not self._en_vivo:
            self._anotar(frame, detecciones, fv)
        if self.frames_vistos % self.ESTADO_CADA == 0:
            self._emitir_estado(fv, len(detecciones))

    def n_conteo(self) -> int:
        """Repeticiones contadas: UNA sola cifra para el video, el contador del panel y el evento de estado."""
        n = getattr(self.sink, "n", None)
        return int(n) if n is not None else (0 if self.segmenter is None else self.segmenter.reps)

    def _evaluar_reglas(self, detecciones, frame: Frame) -> list[dict]:
        pose = next((d for d in detecciones if len(d.screen) >= 33), None)
        if pose is None or not self.exercise.reglas:
            return []
        h, w = frame.image.shape[:2]
        seg, tpl = self.segmenter, self.template
        fases = ["siempre"]   # sin base no hay fases: las reglas "bajando"/"abajo" no se evaluan
        if seg is not None and tpl is not None and seg.last_signal <= tpl.high:
            fases.append("bajando")
            if seg.last_signal <= tpl.low:
                fases.append("abajo")
        return REGLAS.evaluar(self.exercise.reglas, pose.screen, w, h, fases)

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
            self.latest_version += 1

    def _anotar(self, frame: Frame, detecciones, fv: FeatureVec | None) -> None:
        img = frame.image.copy()
        # Zona de control por gesto: se tinta solo mientras hay una muneca ahi
        # (ver sesion/gesto.py), verde si sostenerla va a INICIAR la
        # grabacion, rojo si ya se esta grabando y va a DETENERLA. Se dibuja antes del panel de texto para que el panel
        # (que vive en la misma esquina) quede legible encima.
        if self.gesto.estado is not None:
            color = overlay.COLOR_BAD if self.grabando else overlay.COLOR_OK
            overlay.draw_zona_gesto(img, GESTO_RECORTE, color)

        # el cuadro viene del hilo de captura: la imagen no se toca, se copia
        for d in detecciones:
            overlay.draw_landmarks(img, d, visibles=self._visibles)

        overlay.draw_reglas(img, self._reglas_res)

        # Panel de texto quemado en el video: solo lo esencial (nombre, fps,
        # puntos detectados). Angulos, estado y reps ya se ven en el panel
        # HTML de al lado -- repetirlos aqui solo tapa la imagen.
        n_puntos = sum(len(d.screen) for d in detecciones)
        overlay.draw_panel(img, [
            (self.exercise.name, overlay.COLOR_OK),
            (f"camara {self.fps_camara:4.1f} fps | deteccion {self.fps:4.1f} fps", overlay.COLOR_TEXT),
            (f"puntos: {n_puntos}", overlay.COLOR_TEXT),
        ])

        if self.segmenter is not None:
            overlay.draw_signal_bar(img, self.segmenter.last_signal,
                                    self.template.low, self.template.high)
            if not np.isnan(self.last_score):
                overlay.draw_big_score(img, self.last_score, self.n_conteo())

        with self._lock:
            self._latest = img
            self.latest_version += 1

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
            "fps_camara": round(self.fps_camara, 1),
            "detecciones": n_det,
            "features": features,
            "unidades": self.extractor.units,
            "señal": None if (self.segmenter is None or np.isnan(self.segmenter.last_signal))
                     else round(self.segmenter.last_signal, 2),
            "low": None if self.template is None else round(self.template.low, 2),
            "high": None if self.template is None else round(self.template.high, 2),
            "estado": None if self.segmenter is None else self.segmenter.state,
            "reps": self.n_conteo(),
            "frames": self.frames_vistos,
            "reglas": [{k: r[k] for k in ("nombre", "angulo", "desvio", "ok", "mensaje")} for r in self._reglas_res],
        })
