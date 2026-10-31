"""API de la sesion en vivo: camaras, estado, rutina, historial, encender/grabar/detener, video MJPEG y WebSocket."""

from __future__ import annotations

import asyncio
import time
from datetime import date

import cv2
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from src.captura.fuentes.camara import list_cameras, nombres_camaras_windows
from src.evaluacion import comparadores as scorers
from src.evaluacion.plantilla import template_path
from src.interfaz import tunel
from src.interfaz.control import plantilla_valida, sesion, store
from src.nucleo import config as CFG
from src.nucleo.config import TEMPLATES_DIR
from src.nucleo.ejercicio import load_all
from src.nucleo.landmarks import regiones_de_puntos
from src.nucleo.tiempos import medir

router = APIRouter()


# --- puente hilo -> asyncio para el WebSocket ---
# --------------------------------------------------------------------------
# Puente hilo -> asyncio para el WebSocket
# --------------------------------------------------------------------------
_clientes: set[WebSocket] = set()


_cola: asyncio.Queue | None = None


_loop: asyncio.AbstractEventLoop | None = None


def _encolar(evento: dict) -> None:
    if _cola is not None and not _cola.full():   # navegador lento: se descartan estados, no se revienta
        _cola.put_nowait(evento)


def _al_bus(evento: dict) -> None:
    if _loop is not None and _cola is not None:
        _loop.call_soon_threadsafe(_encolar, evento)


sesion.bus.subscribe(_al_bus)


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


def iniciar_difusor():
    """Lo llama el ciclo de vida de la app: crea la cola y la tarea que reparte eventos."""
    global _cola, _loop
    _loop = asyncio.get_running_loop()
    _cola = asyncio.Queue(maxsize=512)
    return asyncio.create_task(_difusor())


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
    droidcam: str | None = None   # IP:puerto; si viene, se usa en vez de la camara `camera`


class PersonaPedido(BaseModel):
    persona: str | None = None   # 'P1'..'Pn'; vacio = sin persona


class OverlayRegiones(BaseModel):
    regiones: list[str] | None = None


class CambiarFps(BaseModel):
    fps: int


class SeleccionarModelo(BaseModel):
    modelo: str


class SeleccionarEntrenamiento(BaseModel):
    run: str


class CambiarEjercicio(BaseModel):
    exercise: str


@router.get("/api/cameras")
def cameras(max: int = 8) -> dict:
    encontradas = list_cameras(max_index=max)
    resultado = {"camaras": encontradas, "droidcams": CFG.droidcams_nombrados()}
    if not encontradas:
        # Distingue "no hay camara" de "hay camara pero no se pudo abrir"
        # (permisos de Windows, en uso por otra app).
        resultado["nombres_windows"] = nombres_camaras_windows()
    return resultado


@router.get("/api/state")
def state() -> dict:   # def (no async): FastAPI lo corre en un hilo y SQL no congela el servidor
    ejercicios = []
    with medir("state:ejercicios"):
        todos = sorted(load_all().items())
    for slug, ex in todos:
        ruta = template_path(TEMPLATES_DIR, slug)
        d = ex.to_dict()
        d["tiene_base"] = ruta.exists()
        if ex.source == "pose":
            puntos = [p for f in ex.features for p in (list(f["points"]) + list(f.get("reference", [])))]
            d["regiones_default"] = sorted({*regiones_de_puntos(puntos), "cabeza"})   # la cabeza siempre activa
        else:
            d["regiones_default"] = []
        clf = scorers.buscar_clasificador(ex.clasificador or slug)
        d["clasificador_run"] = f"{clf.parent.parent.name}/{clf.parent.name}" if clf else None
        if ruta.exists():
            try:
                with medir("state:plantilla"):
                    plantilla, motivo = plantilla_valida(ex, ruta)
                if plantilla is not None:
                    d["base"] = plantilla.to_dict()
                else:
                    d["tiene_base"], d["error_base"] = False, motivo
            except Exception as e:
                d["tiene_base"] = False
                d["error_base"] = str(e)
        ejercicios.append(d)

    with medir("state:sql"):
        hoy = {r["exercise"]: r for r in store.today()}
        rutina, racha = store.routine(), store.streak()
    return {
        "fecha": date.today().isoformat(),
        "ejercicios": ejercicios,
        "rutina": rutina,
        "hoy": hoy,
        "racha": racha,
        "sesion": sesion.estado(),
        "modelos": [{"clave": k, "nombre": v["nombre"]} for k, v in scorers.MODELOS.items()]
                   + [{"clave": scorers.CLAVE_CLASIFICADOR,
                       "nombre": "Clasificador entrenado"}],
        "almacen": store.estado(),
        "publicar": tunel.estado(),
    }


@router.get("/api/history")
def history(days: int = 14) -> dict:
    return {
        "diario": store.daily(days),
        "por_ejercicio": store.by_exercise(days),
        "recientes": store.recent(20),
    }


@router.post("/api/routine")
def set_routine(items: list[RutinaItem]) -> dict:
    from src.almacenamiento.historial import SQLServerNoDisponible
    try:
        store.set_routine([i.model_dump() for i in items])
    except SQLServerNoDisponible as e:
        raise HTTPException(503, f"No se pudo guardar la rutina: {e}") from None
    return {"ok": True, "rutina": store.routine()}


@router.post("/api/session/camera_on")
def session_camera_on(cfg: EncenderCamara) -> dict:
    return sesion.camera_on(cfg.exercise, cfg.camera, cfg.mirror, cfg.reps,
                            cfg.archivar, cfg.video, cfg.fps, cfg.regiones, cfg.droidcam)


@router.post("/api/session/persona")
def session_persona(cfg: PersonaPedido) -> dict:
    """Con quien se graba (P1, P2...): queda en la tabla `raw` de cada grabacion nueva."""
    return sesion.set_persona(cfg.persona)


@router.get("/api/personas")
def personas() -> dict:
    """Las personas conocidas (de las tablas) mas P1..P5, y la elegida ahora para grabar."""
    from src.nucleo import inputs as INP
    t = INP.tabla()
    usadas = {r.get("persona") for r in t["raw"]} | {c.get("persona") for c in t["clips"]}
    todas = sorted({p for p in usadas if p} | {f"P{i}" for i in range(1, 6)}, key=lambda p: (len(p), p))
    return {"personas": todas, "grabando_con": sesion.persona}


@router.post("/api/session/overlay")
def session_overlay(cfg: OverlayRegiones) -> dict:
    return sesion.overlay_regiones(cfg.regiones)


@router.post("/api/session/fps")
def session_fps(cfg: CambiarFps) -> dict:
    return sesion.set_fps(cfg.fps)


@router.post("/api/session/modelo")
def session_modelo(cfg: SeleccionarModelo) -> dict:
    return sesion.set_modelo(cfg.modelo)


@router.post("/api/session/clasificador")
def session_clasificador(cfg: SeleccionarEntrenamiento) -> dict:
    return sesion.set_clasificador(cfg.run)


@router.post("/api/session/exercise")
def session_exercise(cfg: CambiarEjercicio) -> dict:
    return sesion.set_exercise(cfg.exercise)


@router.post("/api/session/grabar")
def session_grabar() -> dict:
    return sesion.grabar_iniciar()


@router.post("/api/session/grabar_detener")
def session_grabar_detener() -> dict:
    return sesion.grabar_detener()


@router.post("/api/session/stop")
def session_stop() -> dict:
    return sesion.stop()


@router.post("/api/session/pause")
def session_pause() -> dict:
    return sesion.pause()


@router.post("/api/session/resume")
def session_resume() -> dict:
    return sesion.resume()


VIDEO_ANCHO_MAX = 960   # el stream al navegador no necesita 1280: menos CPU y ancho de banda


def _jpeg(img):
    h, w = img.shape[:2]
    if w > VIDEO_ANCHO_MAX:
        img = cv2.resize(img, (VIDEO_ANCHO_MAX, int(h * VIDEO_ANCHO_MAX / w)), interpolation=cv2.INTER_AREA)
    ok, buf = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 75])
    return buf.tobytes() if ok else None


@router.get("/video")
async def video() -> StreamingResponse:
    """MJPEG. El JPEG se codifica en un hilo (antes bloqueaba el event loop
    del servidor en cada cuadro) y solo cuando hay un cuadro NUEVO."""
    async def cuadros():
        ultima, visto = -1, time.monotonic()
        while True:
            pipe = sesion.pipeline
            if pipe is None:
                if time.monotonic() - visto > 13:   # 13 s sin sesion: cierra el stream
                    return
                await asyncio.sleep(0.05)
                continue
            visto = time.monotonic()
            version = pipe.latest_version
            if version == ultima:
                await asyncio.sleep(0.015)
                continue
            img = pipe.latest_frame
            if img is None:
                await asyncio.sleep(0.03)
                continue
            ultima = version
            datos = await asyncio.to_thread(_jpeg, img)
            if datos:
                yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + datos + b"\r\n"
            await asyncio.sleep(0.025)   # tope ~30 fps hacia el navegador

    return StreamingResponse(
        cuadros(), media_type="multipart/x-mixed-replace; boundary=frame"
    )


@router.websocket("/ws")
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
