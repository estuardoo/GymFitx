"""Servidor local del panel de control.

    python -m src.interfaz       ->  http://127.0.0.1:8000

Tres canales hacia el navegador:
  REST       estado y configuracion           interfaz/api/*.py
  WebSocket  eventos del pipeline en vivo      interfaz/api/sesion.py
  MJPEG      el video anotado                  interfaz/api/sesion.py

Este archivo solo arma la app: middleware del tunel, ciclo de vida, routers y carpetas estaticas.
"""

from __future__ import annotations

import argparse
import asyncio
import time
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from src.nucleo import tiempos
from src.nucleo.config import CLIPS_DIR, ENTRENAMIENTOS_DIR, PITCH_DIR, PUERTO_PANEL, RECORDINGS_DIR, WEB_DIR
from src.nucleo.log import logger

with tiempos.medir("import:etiquetado"):
    from src.etiquetado import editor_puntos as etiquetado_puntos
with tiempos.medir("import:interfaz.control (mediapipe, cv2, SQL)"):
    from src.interfaz import control, tunel
with tiempos.medir("import:api.*"):
    from src.interfaz.api import (
        ahpc,
        entrenamiento,
        etiquetado,
        grabaciones,
        publicar,
        sesion,
        sim,
        sistema,
    )

log = logger()


async def _sincronizar_kpoints() -> None:
    """Al arrancar trae de SQL lo que difiera y despues, cada 30 s, sube lo guardado sin conexion."""
    primera = True
    while True:
        with tiempos.medir("sync_kpoints" + (":arranque" if primera else "")):
            await asyncio.to_thread(etiquetado_puntos.reintentar, primera)
        primera = False
        tiempos.escribir()
        await asyncio.sleep(30)


@asynccontextmanager
async def _ciclo_de_vida(_app):
    tarea = sesion.iniciar_difusor()
    sync = asyncio.create_task(_sincronizar_kpoints())
    tiempos.registrar("arranque:listo para atender", tiempos.T0, time.perf_counter() - tiempos.T0)
    tiempos.escribir(forzar=True)
    yield
    tarea.cancel()
    sync.cancel()
    with tiempos.medir("cierre:flush SQL"):
        control.store.flush(timeout=5)       # no perder repeticiones en cola al cerrar
    tiempos.escribir(forzar=True)


app = FastAPI(title="GYMFITX", lifespan=_ciclo_de_vida)
app.add_middleware(tunel.ProteccionTunel)   # usuario/clave para lo que entra por el tunel (lo local pasa)

for modulo in (sesion, grabaciones, etiquetado, entrenamiento, sistema, publicar, ahpc, sim):
    app.include_router(modulo.router)


@app.exception_handler(Exception)
async def _log_error_no_manejado(request: Request, exc: Exception) -> JSONResponse:
    """Sin esto un error de ruta (ej. pyodbc) solo se veia en la consola del .bat,
    nunca en gymfitx.log -- quedaba invisible en cuanto se cerraba esa ventana."""
    log.exception("error no manejado en %s %s", request.method, request.url.path)
    return JSONResponse({"detail": f"Error interno: {exc}"}, status_code=500)


@app.middleware("http")
async def _sin_cache(request: Request, call_next):
    """La interfaz (index y /static) no se cachea: un cambio de JS llega con recargar, sin Ctrl+F5."""
    resp = await call_next(request)
    if request.url.path == "/" or request.url.path.startswith("/static/"):
        resp.headers["Cache-Control"] = "no-cache"
    return resp


@app.middleware("http")
async def _medir_http(request: Request, call_next):
    """Tiempo hasta tener la respuesta de cada ruta (los streams largos se saltan). Ver /api/tiempos."""
    a = time.perf_counter()
    resp = await call_next(request)
    ruta = request.scope.get("route")
    if request.url.path not in ("/video", "/api/tiempos") and ruta is not None:
        tiempos.registrar(f"http:{request.method} {ruta.path}", a, time.perf_counter() - a)
    return resp


@app.get("/api/tiempos")
def tiempos_api() -> dict:
    """Matriz de tiempos por proceso de esta sesion (tambien en datos/logs/tiempos_*.log)."""
    return {"matriz": tiempos.matriz(), "filas": tiempos.filas(), "archivo": tiempos.RUTA.name}


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(WEB_DIR / "index.html")


# Carpetas servidas tal cual: StaticFiles ya maneja Range (lo que necesita el
# <video> para saltar dentro de un mp4) y bloquea path-traversal.
for _d in (RECORDINGS_DIR, CLIPS_DIR, PITCH_DIR, ENTRENAMIENTOS_DIR):
    _d.mkdir(parents=True, exist_ok=True)
app.mount("/recordings", StaticFiles(directory=RECORDINGS_DIR), name="recordings")
app.mount("/dataset", StaticFiles(directory=CLIPS_DIR), name="dataset")
app.mount("/entrenamientos", StaticFiles(directory=ENTRENAMIENTOS_DIR), name="entrenamientos")
app.mount("/pitch", StaticFiles(directory=PITCH_DIR), name="pitch")
app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")


def main() -> None:
    ap = argparse.ArgumentParser(description="Panel de control GYMFITX")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=PUERTO_PANEL)
    args = ap.parse_args()
    print(f"\n  Panel GYMFITX  ->  http://{args.host}:{args.port}\n")
    uvicorn.run(app, host=args.host, port=args.port, log_level="warning")


if __name__ == "__main__":
    main()
