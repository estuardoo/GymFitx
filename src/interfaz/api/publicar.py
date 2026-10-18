"""API del boton "Publicar en internet" (tunel Cloudflare, apagado por defecto). La logica vive en interfaz/tunel.py."""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from src.interfaz import tunel
from src.nucleo.config import PUERTO_PANEL
from src.nucleo.log import logger

router = APIRouter()
log = logger()


class Publicar(BaseModel):
    con_clave: bool = True


# --------------------------------------------------------------------------
# Publicar en internet (tunel Cloudflare) -- apagado por defecto
# --------------------------------------------------------------------------
@router.get("/api/publicar/estado")
async def publicar_estado() -> dict:
    return tunel.estado()


@router.post("/api/publicar/iniciar")
async def publicar_iniciar(cfg: Publicar) -> dict:
    log.info("publicar: iniciando tunel (%s)", "con clave" if cfg.con_clave else "SIN clave")
    return tunel.iniciar(PUERTO_PANEL, cfg.con_clave, log)


@router.post("/api/publicar/detener")
async def publicar_detener() -> dict:
    log.info("publicar: tunel detenido desde el panel")
    return tunel.detener()


@router.post("/api/publicar/nueva_clave")
async def publicar_nueva_clave() -> dict:
    """Genera otra clave (la anterior deja de servir) y la muestra UNA vez."""
    return tunel.nueva_clave()
