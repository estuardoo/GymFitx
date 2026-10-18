"""Mide donde se va el tiempo al arrancar.   python scripts/perfil_arranque.py
1) imports pesados  2) SQL (tablas / conexion)  3) /api/state por partes  4) perfil de funciones."""
import cProfile
import io
import os
import pstats
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def t(nombre, fn):
    a = time.perf_counter()
    try:
        r = fn()
    except Exception as e:
        r = f"ERROR {type(e).__name__}: {e}"
    print(f"{time.perf_counter() - a:7.2f} s  {nombre}")
    return r


print("== 1. imports ==")
for m in ("numpy", "cv2", "mediapipe", "pyodbc", "fastapi"):
    t(f"import {m}", lambda m=m: __import__(m))
t("import src.interfaz.control  (crea Storage -> toca SQL)", lambda: __import__("src.interfaz.control"))
t("import src.interfaz.app", lambda: __import__("src.interfaz.app"))

print("\n== 2. SQL ==")
from src.almacenamiento import historial as H  # noqa: E402
from src.interfaz import control as C  # noqa: E402

print("  estado:", C.store.estado())
t("asegurar_tablas()", H.asegurar_tablas)
t("store.routine()", C.store.routine)
t("store.today()", C.store.today)
t("store.streak()", C.store.streak)

print("\n== 3. /api/state ==")
from fastapi.testclient import TestClient  # noqa: E402

from src.interfaz.app import app  # noqa: E402

cli = TestClient(app)
for i in (1, 2):
    t(f"GET /api/state (vez {i})", lambda: cli.get("/api/state"))
t("GET /", lambda: cli.get("/"))

print("\n== 4. donde se gasta (top 15, /api/state) ==")
pr = cProfile.Profile()
from src.interfaz.api.sesion import state  # noqa: E402

pr.enable()
state()   # directo: el TestClient corre en otro hilo y cProfile no lo ve
pr.disable()
s = io.StringIO()
pstats.Stats(pr, stream=s).sort_stats("cumulative").print_stats(15)
print(s.getvalue())

print("== 5. matriz de tiempos de esta corrida (en el panel real: /api/tiempos y datos/logs/tiempos_*.log) ==")
from src.nucleo import tiempos  # noqa: E402

print(tiempos.matriz())
