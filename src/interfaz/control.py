"""Estado del panel: la sesion de camara (una sola, hay una sola camara), el historial y el log de eventos.

Las rutas de interfaz/api/ solo llaman a esto."""

from __future__ import annotations

import threading
from typing import Any

from fastapi import HTTPException

from src.almacenamiento.historial import Storage
from src.captura.fuentes.camara import CameraSource
from src.evaluacion import comparadores as scorers
from src.evaluacion.base_clip import base_desde_clip
from src.evaluacion.plantilla import Template, template_path
from src.nucleo import config as CFG
from src.nucleo.config import DB_PATH, ENTRENAMIENTOS_DIR, EXERCISES_DIR, RECORDINGS_DIR, TEMPLATES_DIR
from src.nucleo.ejercicio import load_all
from src.nucleo.log import logger
from src.procesamiento.medidas.features import FeatureExtractor
from src.sesion.grabacion import VideoLogger
from src.sesion.pipeline import Contador, ContadorModelo, Evaluator, EventBus, MultiSink, Pipeline, Recorder, Sink


def plantilla_valida(ex, ruta):
    """(Template | None, motivo). La base grabada solo sirve si sus features son las del ejercicio, en el mismo
    orden: si se editaron las filas del .yaml (Kpoints), medir contra ella daria puntajes sin sentido."""
    if not ruta.exists():
        return None, None
    plantilla = Template.load(ruta)
    if list(plantilla.names) != FeatureExtractor(ex).names:
        return None, "Cambiaron las filas de angulos/proporciones de este ejercicio: graba la base de nuevo."
    return plantilla, None


store = Storage(DB_PATH)   # no revienta si SQL Server no responde (ver src/almacenamiento/historial.py)


# --------------------------------------------------------------------------
# Log de sesion: un archivo unico, siempre activo, con los eventos que
# importan (se salta "status", que se emite varias veces por segundo).
# --------------------------------------------------------------------------
log = logger()   # gymfitx.log, compartido con el dataset (src/nucleo/log.py)


_LOGEAR = {"started", "stopped", "rep", "grabando", "grabacion_detenida", "grabacion",
           "template_saved", "error", "aviso", "paused", "resumed", "gesto"}


def _al_bus_archivo(evento: dict) -> None:
    tipo = evento.get("type")
    if tipo in _LOGEAR:
        log.info("%s %s", tipo, {k: v for k, v in evento.items() if k != "type"})


# --------------------------------------------------------------------------
# Sesion: una sola a la vez (hay una sola camara)
# --------------------------------------------------------------------------
class Session:
    def __init__(self) -> None:
        self.pipeline: Pipeline | None = None
        self.session_id: int | None = None
        self.thread: threading.Thread | None = None
        self.stop_flag = threading.Event()
        self.info: dict[str, Any] = {}
        self.bus = EventBus()
        self._lock = threading.Lock()
        self._cfg: dict[str, Any] | None = None
        self.modelo = scorers.DEFAULT_MODEL
        self.clasificador: scorers.Clasificador | None = None
        self.conteo: str | None = None   # quien cuenta en vista previa: "modelo" | "base" | None

    def _preparar_clasificador(self, ex) -> None:
        """Carga el ultimo modelo entrenado (pestana Entrenamiento) para este
        ejercicio, si hay, y prende los kpoints en vivo que necesita."""
        self.clasificador = scorers.cargar_clasificador(ex.clasificador or ex.slug)
        if self.pipeline is not None:
            self.pipeline.set_kpoints_vivo(self.clasificador.spec.get("kpoints")
                                           if self.clasificador is not None else None)
        if self.clasificador is not None:
            log.info("clasificador en vivo para %s: %s", ex.slug, self.clasificador.to_dict())
        # por defecto manda el modelo entrenado mas reciente; sin modelo vuelve al puntaje DTW
        self.modelo = scorers.CLAVE_CLASIFICADOR if self.clasificador else (
            scorers.DEFAULT_MODEL if self.modelo == scorers.CLAVE_CLASIFICADOR else self.modelo)
        self._instalar_preview()

    def _instalar_preview(self) -> None:
        """Camara prendida sin grabar. Modelo con clase "fuera": cuenta solo con el modelo (ContadorModelo);
        si no, con base + modelo cuenta por segmentacion y clasifica (Contador); si no, Sink vacio."""
        pipe, clf = self.pipeline, self.clasificador
        if pipe is None or pipe.grabando:
            return
        if clf is not None and "fuera" in clf.clases and clf.spec.get("ventana_ms"):
            self.conteo, sink = "modelo", ContadorModelo(clf)
        elif pipe.template is not None:   # cuenta con la base; clasifica solo si hay modelo
            self.conteo, sink = "base", Contador(pipe.template, clf, self.modelo)
        else:
            self.conteo, sink = None, Sink()
        pipe.swap_sink(sink)
        if pipe.segmenter is not None:
            pipe.segmenter.reps = 0

    def set_clasificador(self, run: str) -> dict:
        """Cambia el entrenamiento (run_N) que clasifica en vivo, sin apagar la camara."""
        import re
        if not self.activa or self.pipeline is None:
            raise HTTPException(409, "Prende la camara primero.")
        if self.pipeline.grabando:
            raise HTTPException(409, "Deten la grabacion antes de cambiar de entrenamiento.")
        if not re.fullmatch(r"run_\d+", run or ""):
            raise HTTPException(400, f"Entrenamiento invalido: {run}")
        ruta = ENTRENAMIENTOS_DIR / run / "modelo.joblib"
        if not ruta.exists():
            raise HTTPException(404, f"{run}: no tiene modelo.joblib")
        try:
            clf = scorers.Clasificador(ruta)
        except Exception as e:
            raise HTTPException(422, str(e)) from None
        esperado = self.pipeline.exercise.clasificador or self.pipeline.exercise.slug
        if clf.spec.get("exercise") != esperado:
            raise HTTPException(422, f"{run} es de '{clf.spec.get('exercise')}', no de '{esperado}'")
        with self._lock:
            self.clasificador, self.modelo = clf, scorers.CLAVE_CLASIFICADOR
            self.pipeline.set_kpoints_vivo(clf.spec.get("kpoints"))
            self._instalar_preview()
        return {"run": run}

    @property
    def activa(self) -> bool:
        return self.thread is not None and self.thread.is_alive()

    def camera_on(self, slug: str, camera: int, mirror: bool, reps: int,
                  archivar: bool, video: bool, fps: int = 30,
                  regiones: list[str] | None = None, droidcam: str | None = None) -> dict:
        """Prende la camara en modo previsualizacion: esqueleto en vivo (y el
        umbral si ya existe una base), nada se guarda todavia. No hace falta
        que el ejercicio ya tenga base -- si no la tiene, 'grabar_iniciar'
        graba la primera toma como base; si ya la tiene, la evalua. La camara
        no se reabre entre un caso y otro.
        """
        with self._lock:
            if self.activa:
                raise HTTPException(409, "Ya hay una sesion en curso. Apaga la camara primero.")

            ejercicios = load_all(EXERCISES_DIR)
            if slug not in ejercicios:
                raise HTTPException(404, f"Ejercicio desconocido: {slug}")
            ex = ejercicios[slug]

            ruta_base = template_path(TEMPLATES_DIR, slug)
            viejo = ruta_base.exists() and ex.base_clip and Template.load(ruta_base).origen == "clip" \
                and Template.load(ruta_base).fin is None   # base automatica de antes de `fin`: se rehace
            if ex.base_clip and (viejo or not ruta_base.exists()):   # sin base grabada: primer clip de esa clase (yaml: base_clip)
                try:
                    log.info("%s: base desde el primer clip: %s", slug, base_desde_clip(ex, clase=ex.base_clip))
                except Exception as e:   # noqa: BLE001 - la base automatica nunca debe impedir prender la camara
                    log.warning("%s: no se pudo crear la base desde un clip (%s)", slug, e)
            plantilla, motivo = plantilla_valida(ex, ruta_base)
            if motivo:
                log.warning("%s: %s", slug, motivo)

            try:
                fuente = CameraSource(index=camera, mirror=mirror, fps=fps,
                                      url=CFG.url_droidcam(droidcam) if droidcam else None)
            except (RuntimeError, ValueError) as e:
                raise HTTPException(400, str(e)) from None

            self.stop_flag.clear()
            try:
                self.pipeline = Pipeline(ex, fuente, Sink(), template=plantilla, bus=self.bus)
            except Exception as e:
                # No dejar la camara abierta y bloqueada si el pipeline no
                # arranco (p.ej. el modelo de deteccion no se pudo
                # descargar): si no, el proximo intento falla igual, pero
                # encima "porque la camara ya esta en uso".
                fuente.close()
                log.error("no se pudo iniciar el pipeline de '%s': %s", slug, e)
                raise HTTPException(
                    502,
                    f"No se pudo iniciar la deteccion para '{ex.name}'. Si es la primera vez "
                    f"que usas este tipo de ejercicio, el modelo se descarga solo -- revisa tu "
                    f"conexion a internet e intenta de nuevo. Detalle: {e}",
                ) from None
            self.pipeline.set_regiones(regiones)
            self._preparar_clasificador(ex)
            self._cfg = {"slug": slug, "reps": reps, "archivar": archivar, "video": video}
            self.info = {"exercise": slug, "name": ex.name, "modo": "preview", "target": reps}
            self.thread = threading.Thread(
                target=self.pipeline.run, args=(self.stop_flag.is_set,), daemon=True
            )
            self.thread.start()
            return self.info

    def grabar_iniciar(self) -> dict:
        with self._lock:
            if not self.activa or self.pipeline is None or self._cfg is None:
                raise HTTPException(409, "Primero prende la camara.")
            if self.pipeline.grabando:
                raise HTTPException(409, "Ya se esta grabando.")
            cfg = self._cfg

            if self.pipeline.template is not None:
                modo = "evaluar"
                self.session_id = store.open_session(cfg["slug"], "serie")
                principal = Evaluator(self.pipeline.template, storage=store,
                                      target_reps=cfg["reps"], session_id=self.session_id,
                                      modelo=self.modelo, clasificador=self.clasificador)
            else:
                modo = "grabar"
                self.session_id = store.open_session(cfg["slug"], "referencia")
                principal = Recorder(template_path(TEMPLATES_DIR, cfg["slug"]))

            sink = (MultiSink(principal, VideoLogger(RECORDINGS_DIR, guardar_video=cfg["video"]))
                    if cfg["archivar"] else principal)
            if self.pipeline.segmenter is not None:
                self.pipeline.segmenter.reps = 0  # no contar las reps de la previsualizacion
            self.pipeline.swap_sink(sink)
            self.info["modo"] = modo
            self.bus.emit({"type": "grabando", "exercise": cfg["slug"], "modo": modo})
            return {"grabando": True, "modo": modo}

    def grabar_detener(self) -> dict:
        """Detiene solo la toma actual: la camara sigue prendida para otra."""
        with self._lock:
            if not self.activa or self.pipeline is None:
                raise HTTPException(409, "No hay ninguna sesion en curso.")
            if not self.pipeline.grabando:
                raise HTTPException(409, "No se esta grabando actualmente.")
            anterior = self.pipeline.swap_sink(Sink())
            resultado = self._resultados_de(anterior)
            vl = anterior.find(VideoLogger) if isinstance(anterior, MultiSink) else None
            if vl is not None and self.session_id is not None and hasattr(vl, "meta"):
                store.close_session(self.session_id, vl.meta, vl.rutas)
            self.session_id = None
            self.info["modo"] = "preview"

            # Si esta toma acaba de crear la base del ejercicio, la proxima
            # 'Grabar' en esta misma sesion de camara ya evalua contra ella
            # en vez de volver a grabar otra base encima.
            grabador = anterior.find(Recorder) if isinstance(anterior, MultiSink) else (
                anterior if isinstance(anterior, Recorder) else None)
            if grabador is not None and grabador.template is not None:
                self.pipeline.set_template(grabador.template)

            self._instalar_preview()
            self.bus.emit({"type": "grabacion_detenida", **resultado})
            return resultado

    @staticmethod
    def _resultados_de(sink) -> dict:
        """Extrae plantilla/puntajes/rutas de un sumidero ya cerrado (on_stop
        llamado), este solo o dentro de un MultiSink. Lo usan tanto apagar la
        camara del todo como detener solo la toma en curso.
        """
        resultado: dict[str, Any] = {}
        hallar = (sink.find if isinstance(sink, MultiSink)
                  else lambda tipo: (sink if isinstance(sink, tipo) else None))
        grabador = hallar(Recorder)
        if grabador is not None:
            resultado["template"] = grabador.template.to_dict() if grabador.template else None
            resultado["error"] = grabador.error
        evaluador = hallar(Evaluator)
        if evaluador is not None:
            resultado["scores"] = [round(s, 1) for s in evaluador.scores]
        vl = hallar(VideoLogger)
        if vl is not None:
            resultado["grabacion"] = vl.rutas
        return resultado

    def stop(self) -> dict:
        """Apaga la camara del todo. Si se estaba grabando, el 'finally' de
        Pipeline.run() ya cerro ese sumidero (lo archivo) antes de que el
        hilo termine: apagar a mitad de una toma no pierde el video.
        """
        self.stop_flag.set()
        if self.thread is not None:
            self.thread.join(timeout=8)
        resultado = dict(self.info)
        pipe = self.pipeline
        if pipe is not None:
            resultado.update(self._resultados_de(pipe.sink))
            vl = pipe.sink_of(VideoLogger)
            if vl is not None and self.session_id is not None and hasattr(vl, "meta"):
                store.close_session(self.session_id, vl.meta, vl.rutas)
        self.session_id = None
        self.pipeline = None
        self.thread = None
        self.info = {}
        self._cfg = None
        return resultado

    def pause(self) -> dict:
        if not self.activa or self.pipeline is None:
            raise HTTPException(409, "No hay ninguna sesion en curso.")
        self.pipeline.pause()
        self.bus.emit({"type": "paused", "exercise": self.info.get("exercise")})
        return {"pausado": True}

    def resume(self) -> dict:
        if not self.activa or self.pipeline is None:
            raise HTTPException(409, "No hay ninguna sesion en curso.")
        self.pipeline.resume()
        self.bus.emit({"type": "resumed", "exercise": self.info.get("exercise")})
        return {"pausado": False}

    def set_fps(self, fps: int) -> dict:
        """Intenta cambiar el FPS en caliente. Si el driver no lo acepta
        (aplicado=False), el panel reabre la camara del lado del navegador."""
        if not self.activa or self.pipeline is None:
            raise HTTPException(409, "No hay ninguna sesion en curso.")
        return {"aplicado": self.pipeline.set_fps(fps)}

    def set_exercise(self, slug: str) -> dict:
        """Cambia de ejercicio con la camara ya prendida, sin reabrirla (ver
        Pipeline.set_exercise). No permitido a mitad de una grabacion: hay
        que detenerla primero, si no la toma quedaria mezclando dos ejercicios.
        """
        with self._lock:
            if not self.activa or self.pipeline is None:
                raise HTTPException(409, "No hay ninguna sesion en curso.")
            if self.pipeline.grabando:
                raise HTTPException(409, "Detén la grabación antes de cambiar de ejercicio.")
            ejercicios = load_all(EXERCISES_DIR)
            if slug not in ejercicios:
                raise HTTPException(404, f"Ejercicio desconocido: {slug}")
            ex = ejercicios[slug]
            plantilla, motivo = plantilla_valida(ex, template_path(TEMPLATES_DIR, slug))
            if motivo:
                log.warning("%s: %s", slug, motivo)
            try:
                self.pipeline.set_exercise(ex, plantilla)
            except Exception as e:
                # set_exercise() arma el tracker nuevo ANTES de tocar el
                # pipeline (ver su docstring): si esto falla, la sesion sigue
                # con el ejercicio de antes, sin la camara comprometida.
                log.error("no se pudo cambiar a '%s': %s", slug, e)
                raise HTTPException(
                    502,
                    f"No se pudo cargar la deteccion para '{ex.name}'. Si es la primera vez "
                    f"que usas este tipo de ejercicio, el modelo se descarga solo -- revisa tu "
                    f"conexion a internet e intenta de nuevo. Detalle: {e}",
                ) from None
            self._preparar_clasificador(ex)
            self._cfg["slug"] = slug
            self.info["exercise"] = slug
            self.info["name"] = ex.name
            return {"exercise": slug, "name": ex.name}

    def overlay_regiones(self, regiones: list[str] | None) -> dict:
        """Cambia en caliente que partes del cuerpo se dibujan, sin apagar
        la camara (ver Pipeline.set_regiones)."""
        if not self.activa or self.pipeline is None:
            raise HTTPException(409, "No hay ninguna sesion en curso.")
        self.pipeline.set_regiones(regiones)
        return {"regiones": regiones}

    def set_modelo(self, modelo: str) -> dict:
        """Elige que modelo de comparacion se usa como puntaje oficial en la
        proxima evaluacion (Evaluator ya en curso no cambia a mitad de toma).
        """
        if modelo not in scorers.MODELOS and modelo != scorers.CLAVE_CLASIFICADOR:
            raise HTTPException(404, f"Modelo desconocido: {modelo}")
        self.modelo = modelo
        return {"modelo": modelo}

    def estado(self) -> dict:
        pausado = bool(self.pipeline is not None and self.pipeline.is_paused)
        grabando = bool(self.pipeline is not None and self.pipeline.grabando)
        pipe = self.pipeline
        return {"activa": self.activa, "pausado": pausado, "grabando": grabando,
                "modelo": self.modelo,
                "clasificador": self.clasificador.to_dict() if self.clasificador else None,
                "contando": self.conteo is not None, "conteo": self.conteo,
                "fps_camara": round(pipe.fps_camara, 1) if pipe else None,
                "fps_deteccion": round(pipe.fps, 1) if pipe else None,
                **self.info}


sesion = Session()


def _al_bus_gestos(evento: dict) -> None:
    """El gesto (muneca en la esquina) alterna grabar/detener, igual que los
    botones: si no se esta grabando, inicia; si ya se esta grabando, detiene
    (y guarda). Corre en el hilo de captura (lo emite sesion/gesto.py
    ahi mismo); EventBus.emit traga cualquier excepcion de aca para que un
    gesto mal disparado nunca tumbe la sesion de camara -- pero eso tambien
    significa que si esto revienta, no se ve en ningun lado: por eso el
    try/except propio, solo para dejar rastro en el log de sesion.
    """
    if evento.get("type") != "gesto" or sesion.pipeline is None:
        return
    try:
        if not sesion.pipeline.grabando:
            sesion.grabar_iniciar()
        else:
            sesion.grabar_detener()
    except Exception as e:
        log.error("gesto: no se pudo iniciar/detener la grabacion: %s", e)


sesion.bus.subscribe(_al_bus_archivo)
sesion.bus.subscribe(_al_bus_gestos)
