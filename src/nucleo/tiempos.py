"""Tiempos por proceso, en matriz. Complementa el log de sesion (sistema/logs/gymfitx_*.log):
   - cada proceso medido con medir("nombre") queda en una fila (n, ultima, media, p95, max, inicio, hilo)
   - la matriz se guarda en sistema/logs/tiempos_<sesion>.log y se ve en  GET /api/tiempos
   - lo que pasa de LENTO_S tambien deja una linea [tiempos] en el log de sesion
"""

from __future__ import annotations

import threading
import time
from collections import deque
from contextlib import contextmanager

from src.nucleo.config import LOG_DIR
from src.nucleo.log import SESSION_LOG_PATH, logger

LENTO_S = 1.0          # desde aqui un proceso se marca LENTO y entra al log
MUESTRAS = 200         # ultimas N duraciones por proceso (para p95)
RUTA = LOG_DIR / SESSION_LOG_PATH.name.replace("gymfitx_", "tiempos_")

log = logger("tiempos")
T0 = time.perf_counter()
_lock = threading.Lock()
_filas: dict[str, dict] = {}
_sucio = False


def registrar(nombre: str, inicio: float, dur: float) -> None:
    """inicio = perf_counter() al empezar; dur en segundos."""
    global _sucio
    with _lock:
        f = _filas.get(nombre)
        if f is None:
            f = _filas[nombre] = {"n": 0, "m": deque(maxlen=MUESTRAS), "ini": inicio - T0,
                                  "hilo": threading.current_thread().name}
        f["n"] += 1
        f["m"].append(dur)
        _sucio = True
    if dur >= LENTO_S:
        log.warning("LENTO %s: %.2f s (hilo %s)", nombre, dur, threading.current_thread().name)


@contextmanager
def medir(nombre: str):
    a = time.perf_counter()
    try:
        yield
    finally:
        registrar(nombre, a, time.perf_counter() - a)


def filas() -> list[dict]:
    """Una fila por proceso, en orden de primera aparicion en el tiempo."""
    with _lock:
        datos = [(k, f["n"], list(f["m"]), f["ini"], f["hilo"]) for k, f in _filas.items()]
    out = []
    for k, n, m, ini, hilo in sorted(datos, key=lambda x: x[3]):
        s = sorted(m)
        out.append({"proceso": k, "n": n, "ultima_ms": round(m[-1] * 1e3), "media_ms": round(sum(m) / len(m) * 1e3),
                    "p95_ms": round(s[min(len(s) - 1, int(len(s) * 0.95))] * 1e3), "max_ms": round(s[-1] * 1e3),
                    "inicio_s": round(ini, 2), "hilo": hilo})
    return out


def matriz() -> str:
    cols = ("proceso", "n", "ultima_ms", "media_ms", "p95_ms", "max_ms", "inicio_s", "hilo")
    rows = [[str(f[c]) for c in cols] for f in filas()]
    ancho = [max(len(c), *(len(r[i]) for r in rows)) if rows else len(c) for i, c in enumerate(cols)]
    fmt = lambda r: "  ".join(v.ljust(ancho[i]) if i in (0, 7) else v.rjust(ancho[i]) for i, v in enumerate(r))  # noqa: E731
    marca = "  <-- LENTO" 
    lineas = [fmt(cols), fmt(["-" * a for a in ancho])]
    for r, f in zip(rows, filas()):
        lineas.append(fmt(r) + (marca if f["max_ms"] >= LENTO_S * 1e3 else ""))
    return "\n".join(lineas)


def escribir(forzar: bool = False) -> None:
    """Reescribe la matriz de la sesion si hubo cambios (se llama al arrancar, cada 30 s y al cerrar)."""
    global _sucio
    if not (_sucio or forzar):
        return
    _sucio = False
    try:
        RUTA.write_text(f"Tiempos por proceso (ms) - sesion {SESSION_LOG_PATH.name}\n"
                        f"inicio_s = segundos desde que arranco el programa; LENTO >= {LENTO_S:g} s\n\n{matriz()}\n", "utf-8")
    except OSError:
        pass
