"""API de la pestana Sistema: log, librerias, version de Python, apagar/reiniciar y laminas del pitch."""

from __future__ import annotations

import asyncio
import importlib.metadata as metadata
import os
import re
import shutil
import subprocess
import sys
import threading

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.almacenamiento import sqlserver
from src.etiquetado import manifest, tablas
from src.interfaz import control, tunel
from src.nucleo import config as CFG
from src.nucleo.config import PITCH_DIR, ROOT, params
from src.nucleo.log import SESSION_LOG_PATH, logger
from src.preparacion import etapas

router = APIRouter()


log = logger()


def _cerrar_todo() -> None:
    """Antes de salir: guarda la toma en curso, vacia la cola de SQL y baja el tunel."""
    if control.sesion.activa:
        control.sesion.stop()
    control.store.flush(timeout=5)
    tunel.detener()


class ServidorSql(BaseModel):
    host: str
    base: str = "GymFitX"


@router.get("/api/system/sql")
async def sql_servidor() -> dict:
    """Servidor y base en uso (de datos/config.json si existe) + estado de la conexion."""
    estado = await asyncio.to_thread(sqlserver.estado)
    return {**estado, "archivo": str(CFG.CONFIG_PATH), "guardado": CFG.CONFIG_PATH.exists()}


@router.post("/api/system/sql")
async def sql_servidor_guardar(cfg: ServidorSql) -> dict:
    """Guarda servidor/base en datos/config.json, lo aplica sin reiniciar y reconecta."""
    try:
        CFG.guardar_servidor_sql(cfg.host, cfg.base)
    except ValueError as e:
        raise HTTPException(400, str(e)) from None
    log.info("servidor SQL cambiado desde Sistema: %s / %s", cfg.host, cfg.base)
    await asyncio.to_thread(control.store.reconectar)
    return await sql_servidor()


class RespaldoSql(BaseModel):
    al_cortar: bool
    al_entrenar: bool


@router.get("/api/system/respaldo-sql")
def respaldo_sql_estado() -> dict:
    """El disco es la fuente de los datos; SQL Server es una copia. Cuando se actualiza la copia: al cortar y/o al entrenar."""
    return {**CFG.respaldo_sql(), "archivo": str(CFG.CONFIG_PATH)}


@router.post("/api/system/respaldo-sql")
def respaldo_sql_guardar(cfg: RespaldoSql) -> dict:
    return {**CFG.guardar_respaldo_sql(cfg.al_cortar, cfg.al_entrenar), "archivo": str(CFG.CONFIG_PATH)}


@router.post("/api/system/respaldo-sql/ahora")
def respaldo_sql_ahora() -> dict:
    """Copia a SQL todos los clips del disco ya mismo (ignora las dos opciones de arriba)."""
    return tablas.respaldar_sql(manifest._manifest())


class ListaDroidcam(BaseModel):
    lista: list[str]


@router.get("/api/system/droidcam")
def droidcam_lista() -> dict:
    return {"lista": CFG.droidcams(), "archivo": str(CFG.CONFIG_PATH)}


@router.post("/api/system/droidcam")
def droidcam_guardar(cfg: ListaDroidcam) -> dict:
    """Guarda la lista de DroidCam (IP:puerto) en datos/config.json; aparecen en amarillo en el selector de camaras."""
    try:
        lista = CFG.guardar_droidcams(cfg.lista)
    except ValueError as e:
        raise HTTPException(400, str(e)) from None
    return {"lista": lista, "archivo": str(CFG.CONFIG_PATH)}


class CambiarVersionPython(BaseModel):
    version: str


class ActualizarLibreria(BaseModel):
    nombre: str | None = None   # None = actualizar todo requirements.txt


@router.get("/api/log")
async def log_tail(lines: int = 200) -> dict:
    if not SESSION_LOG_PATH.exists():
        return {"lineas": []}
    texto = SESSION_LOG_PATH.read_text(encoding="utf-8", errors="replace").splitlines()
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


@router.get("/api/libraries")
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


@router.post("/api/system/libraries/update")
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


@router.get("/api/system/python")
async def python_entorno() -> dict:
    actual = f"{sys.version_info.major}.{sys.version_info.minor}"
    detectadas = _detectar_versiones_python()
    return {"actual": actual, "actual_completa": sys.version.split()[0],
            "detectadas": detectadas}


@router.post("/api/system/python_version")
async def cambiar_version_python(cfg: CambiarVersionPython) -> dict:
    """Recrea el entorno virtual con otra version de Python y reinicia.

    No cambia el interprete de este proceso en caliente (no se puede); en
    su lugar deja la version pedida en un archivo que UPDATE.bat lee al
    crear el .venv, borra el .venv actual para forzar que se rearme, y
    corre UPDATE.bat (rehace el entorno y, al terminar, abre la app). Tarda mas:
    reinstala todo.
    """
    disponibles = _detectar_versiones_python()
    if disponibles and cfg.version not in disponibles:
        raise HTTPException(400, f"Version '{cfg.version}' no detectada en este equipo.")

    (ROOT / "python_version.txt").write_text(cfg.version.strip(), encoding="utf-8")
    shutil.rmtree(ROOT / ".venv", ignore_errors=True)

    _cerrar_todo()
    log.info("cambio de version de Python solicitado desde el panel: %s", cfg.version)
    bat = ROOT / "UPDATE.bat"
    subprocess.Popen(
        ["cmd", "/c", "start", "", str(bat)],
        cwd=str(ROOT), creationflags=getattr(subprocess, "DETACHED_PROCESS", 0), close_fds=True,
    )
    threading.Timer(0.5, lambda: os._exit(0)).start()
    return {"ok": True}


@router.post("/api/system/shutdown")
async def system_shutdown() -> dict:
    """Guarda lo que haya en curso y cierra el proceso del servidor. El
    .bat, al ver que python termino, cierra la ventana de cmd sola.
    """
    _cerrar_todo()
    log.info("apagado solicitado desde el panel")
    threading.Timer(0.5, lambda: os._exit(0)).start()
    return {"ok": True}


@router.post("/api/system/restart")
async def system_restart() -> dict:
    """Como apagar, pero antes relanza GYMFITX.bat en una ventana nueva."""
    _cerrar_todo()
    log.info("reinicio solicitado desde el panel")
    bat = ROOT / "GYMFITX.bat"
    subprocess.Popen(
        ["cmd", "/c", "start", "", str(bat)],
        cwd=str(ROOT), creationflags=getattr(subprocess, "DETACHED_PROCESS", 0), close_fds=True,
    )
    threading.Timer(0.5, lambda: os._exit(0)).start()
    return {"ok": True}


def _pitch():
    """Laminas del pitch (docs/pitch/*.png, en orden) + el .pptx original."""
    if not PITCH_DIR.exists():
        return {"laminas": [], "pptx": None}
    laminas = sorted((f.name for f in PITCH_DIR.glob("*.png")),
                     key=lambda n: int("".join(c for c in n if c.isdigit()) or 0))
    return {"laminas": laminas, "pptx": next((f.name for f in PITCH_DIR.glob("*.pptx")), None)}


@router.get("/api/pitch")
def dataset_pitch():
    return _pitch()


class Generar(BaseModel):
    ejercicio: str | None = None   # None = todos


@router.post("/api/docs/generar")
def docs_generar(g: Generar) -> dict:
    """Corre las 5 etapas (seleccionar → formatear): deja los reportes en reportes/, el diccionario en docs/diccionario/ y
    la tabla final en datos/final/. Sin ejercicio, los de params.yaml (ejercicios)."""
    resultado = {}
    for ej in [g.ejercicio] if g.ejercicio else params("ejercicios"):
        try:
            resultado[ej] = etapas.todo(ej)
        except (ValueError, OSError) as e:
            resultado[ej] = {"error": str(e)}
    return resultado
