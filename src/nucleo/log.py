"""Log del proyecto: un archivo por sesion en datos/logs/ (antes habia uno solo,
gymfitx.log, que rotaba y se perdia el rastro de en que arranque paso cada error).

    from gymfitx.log import logger
    log = logger("dataset")        # -> lineas "2026-09-23 10:00:00  [dataset] mensaje"

SESSION_LOG_PATH es el archivo de ESTA sesion (panel de Sistema lo muestra).
Solo se guardan las ultimas MAX_SESIONES para no llenar el disco.
"""

from __future__ import annotations

import logging
from datetime import datetime

from src.nucleo.config import LOG_DIR

_RAIZ = "gymfitx"
MAX_SESIONES = 30

LOG_DIR.mkdir(parents=True, exist_ok=True)
SESSION_LOG_PATH = LOG_DIR / f"gymfitx_{datetime.now():%Y%m%d_%H%M%S}.log"


def _podar_sesiones_viejas() -> None:
    archivos = sorted(LOG_DIR.glob("gymfitx_*.log"), key=lambda p: p.name)
    for viejo in archivos[:-MAX_SESIONES]:
        try:
            viejo.unlink(missing_ok=True)
        except OSError:   # abierto por otro proceso (Windows) o carpeta de solo lectura: no debe impedir arrancar
            pass


class _Prefijo(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        sub = record.name[len(_RAIZ) + 1:] if record.name.startswith(_RAIZ + ".") else ""
        record.prefijo = f"[{sub}] " if sub else ""
        return super().format(record)


def _configurar() -> logging.Logger:
    raiz = logging.getLogger(_RAIZ)
    if not raiz.handlers:
        raiz.setLevel(logging.INFO)
        raiz.propagate = False
        _podar_sesiones_viejas()
        manejador = logging.FileHandler(SESSION_LOG_PATH, encoding="utf-8")
        manejador.setFormatter(_Prefijo("%(asctime)s  %(prefijo)s%(message)s", "%Y-%m-%d %H:%M:%S"))
        raiz.addHandler(manejador)
        consola = logging.StreamHandler()
        consola.setLevel(logging.WARNING)       # la ventana del .bat solo muestra problemas
        consola.setFormatter(_Prefijo("%(prefijo)s%(message)s"))
        raiz.addHandler(consola)
    return raiz


def logger(nombre: str | None = None) -> logging.Logger:
    raiz = _configurar()
    return raiz if not nombre else raiz.getChild(nombre)
