"""API de entrenamiento: clips a usar, entrenar, corridas, modelos y descomposicion.

Rutas sync ("def", no "async def"): FastAPI las corre en su threadpool, asi
que cortar/entrenar (CPU) no bloquea el websocket ni el video de la camara."""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.entrenamiento import datos as DATOS
from src.entrenamiento import descomposicion as DESCOMP
from src.entrenamiento import modelos as MODELOS
from src.entrenamiento import reportes as REPORTES
from src.entrenamiento.entrenar import entrenar
from src.etiquetado.manifest import log
from src.nucleo.config import guardar_matriz_modelos, matriz_modelos

router = APIRouter()


@router.get("/api/entrenar/clips")
def dataset_entrenar_clips(tipo: str | None = None):
    return DATOS.clips_entrenamiento(int(tipo) if tipo else None)


@router.get("/api/entrenamientos")
def dataset_entrenamientos():
    return REPORTES.entrenamientos()


@router.get("/api/modelos")
def dataset_modelos():
    return MODELOS.modelos_disponibles()


@router.get("/api/modelos/matriz")
def modelos_matriz():
    """epocas / max_iter / parar de cada modelo que itera (la matriz de src/nucleo/config.py + lo guardado)."""
    return matriz_modelos()


@router.post("/api/modelos/matriz")
def modelos_matriz_guardar(body: dict):
    try:
        return guardar_matriz_modelos(body.get("cambios") or {})
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@router.post("/api/entrenar")
def dataset_entrenar(body: dict):
    try:
        return entrenar(body.get("test_pct", 20), body.get("modelos"), body.get("tipo"),
                              body.get("features") or "ambos", body.get("fuera", True))
    except ValueError as e:
        log.info(f"entrenar rechazado: {e}")  # queda en gymfitx.log, no solo en el navegador
        return JSONResponse({"error": str(e)}, status_code=400)


@router.post("/api/entrenar/seleccion")
def dataset_entrenar_seleccion(body: dict):
    return DATOS.guardar_seleccion(body.get("cambios") or {}, body.get("tipo"))


@router.post("/api/descomp/opciones")
def dataset_descomp_opciones(body: dict):
    return DESCOMP.descomp_opciones(body.get("tipo"))


@router.post("/api/descomp/analizar")
def dataset_descomp_analizar(body: dict):
    try:
        return DESCOMP.descomp_analizar(body.get("tipo"), body.get("base"), body.get("bien"),
                                      body.get("mal"), body.get("activos"))
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@router.post("/api/descomp/ranking")
def dataset_descomp_ranking(body: dict):
    try:
        return DESCOMP.descomp_ranking(body.get("tipo"))
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)
