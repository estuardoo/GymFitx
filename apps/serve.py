"""Servidor local del panel de control.

    python apps/serve.py          ->  http://127.0.0.1:8000

Tres canales hacia el navegador, cada uno con un proposito claro:
  REST       estado y configuracion (ejercicios, rutina, historial, camaras)
  WebSocket  eventos del pipeline en vivo (mismo bus que usa la ventana CV2)
  MJPEG      el video anotado (puntos y esqueleto), para no necesitar ventana

El pipeline corre en un hilo aparte; el servidor nunca lo bloquea.
"""

from __future__ import annotations

import argparse
import asyncio
import importlib.metadata as metadata
import logging
import os
import re
import shutil
import subprocess
import sys
import threading
from datetime import date
from typing import Any

import _bootstrap  # noqa: F401
import cv2
import numpy as np
import uvicorn
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from core.config import DB_PATH, EXERCISES_DIR, RECORDINGS_DIR, ROOT, TEMPLATES_DIR, WEB_DIR
from core.exercise import load_all
from core.features import FeatureExtractor
from core.landmarks import regiones_de_puntos
from core.pipeline import Evaluator, EventBus, MultiSink, Pipeline, Recorder, Sink
from core.source import CameraSource, list_cameras, nombres_camaras_windows
from core.storage import Storage
from core.template import Template, build_template, template_path
from core.types import FeatureVec
from core.videolog import VideoLogger, features_a_csv, listar_grabaciones, resolver_json, uso_en_disco

app = FastAPI(title="GYMFITX")
store = Storage(DB_PATH)

# --------------------------------------------------------------------------
# Log de sesion: un archivo unico, siempre activo, con los eventos que
# importan (se salta "status", que se emite varias veces por segundo).
# --------------------------------------------------------------------------
LOG_PATH = ROOT / "gymfitx.log"
log = logging.getLogger("gymfitx")
log.setLevel(logging.INFO)
log.propagate = False
if not log.handlers:
    _handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
    _handler.setFormatter(logging.Formatter("%(asctime)s  %(message)s", "%Y-%m-%d %H:%M:%S"))
    log.addHandler(_handler)

_LOGEAR = {"started", "stopped", "rep", "grabando", "grabacion_detenida", "grabacion",
           "template_saved", "error", "aviso", "paused", "resumed"}


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

    @property
    def activa(self) -> bool:
        return self.thread is not None and self.thread.is_alive()

    def camera_on(self, slug: str, camera: int, mirror: bool, reps: int,
                  archivar: bool, video: bool, fps: int = 30,
                  regiones: list[str] | None = None, manos_detalle: bool = False) -> dict:
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

            ruta = template_path(TEMPLATES_DIR, slug)
            plantilla = Template.load(ruta) if ruta.exists() else None

            try:
                fuente = CameraSource(index=camera, mirror=mirror, fps=fps)
            except RuntimeError as e:
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
            if manos_detalle:
                self.pipeline.set_manos_detalle(True)
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
                                      target_reps=cfg["reps"], session_id=self.session_id)
            else:
                modo = "grabar"
                self.session_id = store.open_session(cfg["slug"], "base")
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
            ruta = template_path(TEMPLATES_DIR, slug)
            plantilla = Template.load(ruta) if ruta.exists() else None
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

    def manos_detalle(self, activo: bool) -> dict:
        """Prende/apaga los dedos articulados de verdad en ejercicios de
        cuerpo completo (ver Pipeline.set_manos_detalle)."""
        if not self.activa or self.pipeline is None:
            raise HTTPException(409, "No hay ninguna sesion en curso.")
        self.pipeline.set_manos_detalle(activo)
        return {"manos_detalle": activo}

    def estado(self) -> dict:
        pausado = bool(self.pipeline is not None and self.pipeline.is_paused)
        grabando = bool(self.pipeline is not None and self.pipeline.grabando)
        return {"activa": self.activa, "pausado": pausado, "grabando": grabando, **self.info}


sesion = Session()


# --------------------------------------------------------------------------
# Puente hilo -> asyncio para el WebSocket
# --------------------------------------------------------------------------
_clientes: set[WebSocket] = set()
_cola: asyncio.Queue | None = None
_loop: asyncio.AbstractEventLoop | None = None


def _al_bus(evento: dict) -> None:
    if _loop is not None and _cola is not None:
        _loop.call_soon_threadsafe(_cola.put_nowait, evento)


def _al_bus_gestos(evento: dict) -> None:
    """El gesto "manos juntas" alterna grabar/detener, igual que los
    botones: si no se esta grabando, inicia; si ya se esta grabando, detiene
    (y guarda). Corre en el hilo de captura (lo emite Pipeline._revisar_gesto
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
        log.error("gesto de mano: no se pudo iniciar/detener la grabacion: %s", e)


sesion.bus.subscribe(_al_bus)
sesion.bus.subscribe(_al_bus_archivo)
sesion.bus.subscribe(_al_bus_gestos)


async def _difusor() -> None:
    assert _cola is not None
    while True:
        evento = await _cola.get()
        muertos = []
        for ws in list(_clientes):
            try:
                await ws.send_json(evento)
            except Exception:
                muertos.append(ws)
        for ws in muertos:
            _clientes.discard(ws)


@app.on_event("startup")
async def _arranque() -> None:
    global _cola, _loop
    _loop = asyncio.get_running_loop()
    _cola = asyncio.Queue(maxsize=512)
    asyncio.create_task(_difusor())


# --------------------------------------------------------------------------
# API
# --------------------------------------------------------------------------
class RutinaItem(BaseModel):
    exercise: str
    target_reps: int = 10


class EncenderCamara(BaseModel):
    exercise: str
    camera: int = 0
    reps: int = 0
    mirror: bool = True
    archivar: bool = True
    video: bool = True
    fps: int = 30
    regiones: list[str] | None = None
    manos_detalle: bool = False


class OverlayRegiones(BaseModel):
    regiones: list[str] | None = None


class ManosDetalle(BaseModel):
    activo: bool


class CambiarFps(BaseModel):
    fps: int


class CambiarEjercicio(BaseModel):
    exercise: str


class UsarComoBase(BaseModel):
    ruta_relativa: str


class CambiarVersionPython(BaseModel):
    version: str


class ActualizarLibreria(BaseModel):
    nombre: str | None = None   # None = actualizar todo requirements.txt


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(WEB_DIR / "index.html")


@app.get("/api/cameras")
async def cameras(max: int = 8) -> dict:
    encontradas = list_cameras(max_index=max)
    resultado = {"camaras": encontradas}
    if not encontradas:
        # Distingue "no hay camara" de "hay camara pero no se pudo abrir"
        # (permisos de Windows, en uso por otra app).
        resultado["nombres_windows"] = nombres_camaras_windows()
    return resultado


@app.get("/api/state")
async def state() -> dict:
    ejercicios = []
    for slug, ex in sorted(load_all(EXERCISES_DIR).items()):
        ruta = template_path(TEMPLATES_DIR, slug)
        d = ex.to_dict()
        d["tiene_base"] = ruta.exists()
        if ex.source == "pose":
            puntos = [p for f in ex.features for p in (list(f["points"]) + list(f.get("reference", [])))]
            d["regiones_default"] = regiones_de_puntos(puntos)
        else:
            d["regiones_default"] = []
        if ruta.exists():
            try:
                d["base"] = Template.load(ruta).to_dict()
            except Exception as e:
                d["tiene_base"] = False
                d["error_base"] = str(e)
        ejercicios.append(d)

    hoy = {r["exercise"]: r for r in store.today()}
    return {
        "fecha": date.today().isoformat(),
        "ejercicios": ejercicios,
        "rutina": store.routine(),
        "hoy": hoy,
        "racha": store.streak(),
        "sesion": sesion.estado(),
    }


@app.get("/api/history")
async def history(days: int = 14) -> dict:
    return {
        "diario": store.daily(days),
        "por_ejercicio": store.by_exercise(days),
        "recientes": store.recent(20),
    }


@app.post("/api/routine")
async def set_routine(items: list[RutinaItem]) -> dict:
    store.set_routine([i.model_dump() for i in items])
    return {"ok": True, "rutina": store.routine()}


@app.post("/api/session/camera_on")
async def session_camera_on(cfg: EncenderCamara) -> dict:
    return sesion.camera_on(cfg.exercise, cfg.camera, cfg.mirror, cfg.reps,
                            cfg.archivar, cfg.video, cfg.fps, cfg.regiones,
                            cfg.manos_detalle)


@app.post("/api/session/overlay")
async def session_overlay(cfg: OverlayRegiones) -> dict:
    return sesion.overlay_regiones(cfg.regiones)


@app.post("/api/session/manos_detalle")
async def session_manos_detalle(cfg: ManosDetalle) -> dict:
    return sesion.manos_detalle(cfg.activo)


@app.post("/api/session/fps")
async def session_fps(cfg: CambiarFps) -> dict:
    return sesion.set_fps(cfg.fps)


@app.post("/api/session/exercise")
async def session_exercise(cfg: CambiarEjercicio) -> dict:
    return sesion.set_exercise(cfg.exercise)


@app.post("/api/session/grabar")
async def session_grabar() -> dict:
    return sesion.grabar_iniciar()


@app.post("/api/session/grabar_detener")
async def session_grabar_detener() -> dict:
    return sesion.grabar_detener()


@app.post("/api/session/stop")
async def session_stop() -> dict:
    return sesion.stop()


@app.post("/api/session/pause")
async def session_pause() -> dict:
    return sesion.pause()


@app.post("/api/session/resume")
async def session_resume() -> dict:
    return sesion.resume()


@app.get("/api/recordings")
async def recordings(limit: int = 40, exercise: str | None = None) -> dict:
    return {"grabaciones": listar_grabaciones(RECORDINGS_DIR, limit, exercise),
            "disco": uso_en_disco(RECORDINGS_DIR)}


@app.get("/api/recordings/csv")
async def recording_csv(ruta_relativa: str) -> Response:
    """Descarga en CSV las features (movimientos) ya guardadas en el .npz de
    una grabación -- incluye las de mano (curl de cada dedo, apertura, etc.),
    que ya se archivan automáticamente al terminar cada sesión, en cualquier
    ejercicio, sea de manos o de cuerpo completo.
    """
    try:
        json_path = resolver_json(RECORDINGS_DIR, ruta_relativa)
    except ValueError as e:
        raise HTTPException(400, str(e)) from None
    npz_path = json_path.with_suffix(".npz")
    if not npz_path.exists():
        raise HTTPException(404, "No se encontraron las features de esa grabación.")

    return Response(
        content=features_a_csv(npz_path),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{npz_path.stem}.csv"'},
    )


@app.post("/api/recordings/use_as_base")
async def use_as_base(cfg: UsarComoBase) -> dict:
    """Recalibra la plantilla de un ejercicio a partir de una grabacion archivada.

    No hace falta redecodificar el video: las features de cada cuadro ya
    quedaron guardadas en el .npz cuando se archivo la sesion, asi que esto
    corre en milisegundos, sea cual sea el largo del video.
    """
    if sesion.activa:
        raise HTTPException(409, "Detén la sesión en curso antes de recalibrar una base.")

    try:
        json_path = resolver_json(RECORDINGS_DIR, cfg.ruta_relativa)
    except ValueError as e:
        raise HTTPException(400, str(e)) from None
    npz_path = json_path.with_suffix(".npz")
    if not json_path.exists() or not npz_path.exists():
        raise HTTPException(404, "No se encontraron los metadatos o las features de esa grabación.")

    import json
    meta = json.loads(json_path.read_text(encoding="utf-8"))
    slug = meta["exercise"]
    ejercicios = load_all(EXERCISES_DIR)
    if slug not in ejercicios:
        raise HTTPException(404, f"El ejercicio '{slug}' de esa grabación ya no existe.")
    ex = ejercicios[slug]
    extractor = FeatureExtractor(ex)

    z = np.load(npz_path, allow_pickle=False)
    valores, tiempos = z["values"], z["t_ms"]
    if list(z["names"]) != extractor.names:
        raise HTTPException(
            400, "El YAML de este ejercicio cambió desde que se grabó esta sesión "
                 "(las features no coinciden); no se puede recalibrar desde ella.")

    frames = [
        FeatureVec(values=valores[i], valid=~np.isnan(valores[i]), t_ms=int(tiempos[i]))
        for i in range(len(tiempos))
    ]
    try:
        plantilla = build_template(frames, ex, extractor)
    except ValueError as e:
        raise HTTPException(400, str(e)) from None

    plantilla.save(template_path(TEMPLATES_DIR, slug))
    resultado = plantilla.to_dict()
    sesion.bus.emit({"type": "template_saved", "exercise": slug, "template": resultado,
                     "origen": "grabacion"})
    return resultado


@app.get("/api/log")
async def log_tail(lines: int = 200) -> dict:
    if not LOG_PATH.exists():
        return {"lineas": []}
    texto = LOG_PATH.read_text(encoding="utf-8", errors="replace").splitlines()
    return {"lineas": texto[-lines:]}


def _requisitos() -> dict[str, str]:
    """{nombre: linea de requirements.txt tal cual, sin el nombre} -- ej.
    "mediapipe" -> ">=0.10.18,<0.11". Se usa para mostrar la version pedida
    y para saber con que restriccion actualizar cada paquete.
    """
    req_path = ROOT / "requirements.txt"
    salida: dict[str, str] = {}
    if not req_path.exists():
        return salida
    for linea in req_path.read_text(encoding="utf-8").splitlines():
        linea = linea.split("#", 1)[0].strip()
        if not linea:
            continue
        nombre = re.split(r"[<>=!~; ]", linea, maxsplit=1)[0].strip()
        if not nombre:
            continue
        salida[nombre] = linea[len(nombre):].split(";", 1)[0].strip()
    return salida


@app.get("/api/libraries")
async def libraries() -> dict:
    """Lee requirements.txt y busca la version realmente instalada de cada
    paquete (puede diferir de lo que pide el archivo).
    """
    libs = []
    for nombre, requerida in _requisitos().items():
        try:
            version = metadata.version(nombre)
        except metadata.PackageNotFoundError:
            version = None
        libs.append({"nombre": nombre, "version": version, "requerida": requerida or None})
    libs.append({"nombre": "python", "version": sys.version.split()[0], "requerida": None})
    return {"librerias": libs}


@app.post("/api/system/libraries/update")
async def actualizar_libreria(cfg: ActualizarLibreria) -> dict:
    """Actualiza una libreria (o todas, si no se pasa nombre) respetando lo
    que pide requirements.txt. Corre pip en un hilo aparte para no trabar el
    resto del panel mientras baja el paquete.
    """
    if cfg.nombre is None:
        objetivo = ["-r", str(ROOT / "requirements.txt")]
    else:
        requisitos = _requisitos()
        if cfg.nombre not in requisitos:
            raise HTTPException(404, f"'{cfg.nombre}' no esta en requirements.txt.")
        objetivo = [f"{cfg.nombre}{requisitos[cfg.nombre]}"]

    r = await asyncio.to_thread(
        subprocess.run,
        [sys.executable, "-m", "pip", "install", "--upgrade", *objetivo],
        capture_output=True, text=True, timeout=600,
    )
    if r.returncode != 0:
        raise HTTPException(500, f"pip fallo: {r.stderr[-800:]}")
    log.info("libreria(s) actualizada(s): %s", cfg.nombre or "todas (requirements.txt)")
    return {"ok": True, "salida": r.stdout[-800:]}


def _detectar_versiones_python() -> list[str]:
    """Versiones de Python que el lanzador 'py' de Windows encuentra
    instaladas (ej. ["3.12", "3.11"]). Vacio si 'py' no esta disponible
    (Linux/Mac, o Windows sin el lanzador) -- no es un error, el panel
    simplemente no ofrece cambiar de version en ese caso.
    """
    try:
        r = subprocess.run(["py", "-0p"], capture_output=True, text=True, timeout=5)
    except (FileNotFoundError, OSError):
        return []
    if r.returncode != 0:
        return []
    versiones = {m.group(1) for m in re.finditer(r"-(\d+\.\d+)", r.stdout)}
    return sorted(versiones, reverse=True)


@app.get("/api/system/python")
async def python_entorno() -> dict:
    actual = f"{sys.version_info.major}.{sys.version_info.minor}"
    detectadas = _detectar_versiones_python()
    return {"actual": actual, "actual_completa": sys.version.split()[0],
            "detectadas": detectadas}


@app.post("/api/system/python_version")
async def cambiar_version_python(cfg: CambiarVersionPython) -> dict:
    """Recrea el entorno virtual con otra version de Python y reinicia.

    No cambia el interprete de este proceso en caliente (no se puede); en
    su lugar deja la version pedida en un archivo que GYMFITX.bat lee al
    crear el .venv, borra el .venv actual para forzar que se rearme, y
    reinicia -- igual que el boton "Reiniciar panel", pero con la version
    nueva. El primer arranque despues de esto tarda mas: reinstala todo.
    """
    disponibles = _detectar_versiones_python()
    if disponibles and cfg.version not in disponibles:
        raise HTTPException(400, f"Version '{cfg.version}' no detectada en este equipo.")

    (ROOT / "python_version.txt").write_text(cfg.version.strip(), encoding="utf-8")
    shutil.rmtree(ROOT / ".venv", ignore_errors=True)

    if sesion.activa:
        sesion.stop()
    log.info("cambio de version de Python solicitado desde el panel: %s", cfg.version)
    bat = ROOT / "GYMFITX.bat"
    subprocess.Popen(
        ["cmd", "/c", "start", "", str(bat)],
        cwd=str(ROOT), creationflags=getattr(subprocess, "DETACHED_PROCESS", 0), close_fds=True,
    )
    threading.Timer(0.5, lambda: os._exit(0)).start()
    return {"ok": True}


@app.post("/api/system/shutdown")
async def system_shutdown() -> dict:
    """Guarda lo que haya en curso y cierra el proceso del servidor. El
    .bat, al ver que python termino, cierra la ventana de cmd sola.
    """
    if sesion.activa:
        sesion.stop()
    log.info("apagado solicitado desde el panel")
    threading.Timer(0.5, lambda: os._exit(0)).start()
    return {"ok": True}


@app.post("/api/system/restart")
async def system_restart() -> dict:
    """Como apagar, pero antes relanza GYMFITX.bat en una ventana nueva."""
    if sesion.activa:
        sesion.stop()
    log.info("reinicio solicitado desde el panel")
    bat = ROOT / "GYMFITX.bat"
    subprocess.Popen(
        ["cmd", "/c", "start", "", str(bat)],
        cwd=str(ROOT), creationflags=getattr(subprocess, "DETACHED_PROCESS", 0), close_fds=True,
    )
    threading.Timer(0.5, lambda: os._exit(0)).start()
    return {"ok": True}


@app.get("/video")
async def video() -> StreamingResponse:
    async def cuadros():
        vacio = 0
        while True:
            pipe = sesion.pipeline
            img = pipe.latest_frame if pipe is not None else None
            if img is None:
                vacio += 1
                if vacio > 200:      # ~13 s sin nada: cierra el stream
                    return
                await asyncio.sleep(0.066)
                continue
            vacio = 0
            ok, buf = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 75])
            if ok:
                yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n"
                       + buf.tobytes() + b"\r\n")
            await asyncio.sleep(0.05)   # ~20 fps hacia el navegador

    return StreamingResponse(
        cuadros(), media_type="multipart/x-mixed-replace; boundary=frame"
    )


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket) -> None:
    await ws.accept()
    _clientes.add(ws)
    try:
        while True:
            await ws.receive_text()   # el cliente solo manda pings
    except WebSocketDisconnect:
        pass
    finally:
        _clientes.discard(ws)


# Las grabaciones se sirven como archivos estaticos: StaticFiles ya maneja
# peticiones por rango, que es lo que necesita el <video> del navegador para
# saltar dentro de un mp4 sin descargarlo entero.
app.mount("/recordings", StaticFiles(directory=RECORDINGS_DIR), name="recordings")


def main() -> None:
    ap = argparse.ArgumentParser(description="Panel de control GYMFITX")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8000)
    args = ap.parse_args()
    print(f"\n  Panel GYMFITX  ->  http://{args.host}:{args.port}\n")
    uvicorn.run(app, host=args.host, port=args.port, log_level="warning")


if __name__ == "__main__":
    main()
