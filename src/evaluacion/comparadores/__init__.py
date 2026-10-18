"""Comparadores intercambiables: cada uno puntua una repeticion contra la
plantilla con una estrategia distinta, para poder elegir y comparar.

Todos parten de las MISMAS features (angulos + razones de distancia, ya
invariantes a camara -- ver src/procesamiento/medidas/features.py) y de la MISMA plantilla
calibrada (src/evaluacion/plantilla.py). Lo unico que cambia es como se comparan en
el tiempo:

- dtw_biomec (default, el original del proyecto): alinea con DTW, tolera
  ritmos distintos entre la base y la repeticion.
- angulos_directo: remuestrea la repeticion a la duracion de la plantilla y
  compara cuadro a cuadro, sin alinear -- mas simple y mas rapido, pero
  castiga diferencias de ritmo. Sirve de control para medir cuanto aporta
  el DTW.

- clasificador: el modelo entrenado en la pestana Entrenamiento
  (datos/entrenamientos/run_N/modelo.joblib). Convierte los kpoints de la
  repeticion en el MISMO vector que vio al entrenar (src/procesamiento/puntos/vectorizar.py) y
  el puntaje es la probabilidad de "bien" (0-100). Es lo que cierra el
  ciclo captura -> etiqueta -> entrena -> puntua en vivo. Solo aparece si
  hay un modelo entrenado para el ejercicio (ver buscar_clasificador).

Registro: cada comparador vive en su propio modulo (dtw, angulos_directo, clasificador)."""

from __future__ import annotations

import time

from src.evaluacion.comparadores.angulos_directo import _angulos_directo
from src.evaluacion.comparadores.clasificador import (  # noqa: F401
    Clasificador,
    DetectorCiclos,
    buscar_clasificador,
    cargar_clasificador,
)
from src.evaluacion.comparadores.dtw import compare as _dtw_biomec
from src.nucleo.tipos import Segment

# clave -> {nombre para mostrar, funcion compare(seg, template) -> Score}
MODELOS: dict[str, dict] = {
    "dtw_biomec": {"nombre": "DTW + biomecanica", "fn": _dtw_biomec},
    "angulos_directo": {"nombre": "Angulos (sin DTW)", "fn": _angulos_directo},
}

DEFAULT_MODEL = "dtw_biomec"

CLAVE_CLASIFICADOR = "clasificador"

def comparar_todos(segment: Segment, template, clasificador: Clasificador | None = None) -> dict[str, dict]:
    """Corre TODOS los modelos registrados (y el clasificador dataset, si hay)
    sobre la MISMA repeticion y mide cuanto tarda cada uno."""
    out: dict[str, dict] = {}
    for clave, m in MODELOS.items():
        t0 = time.perf_counter()
        score = m["fn"](segment, template)
        latencia_ms = (time.perf_counter() - t0) * 1000.0
        out[clave] = {"nombre": m["nombre"], "score": score, "latencia_ms": round(latencia_ms, 3)}
    if clasificador is not None:
        t0 = time.perf_counter()
        score = clasificador.puntuar(segment, template)
        out[CLAVE_CLASIFICADOR] = {"nombre": f"Clasificador entrenado ({clasificador.nombre}, {clasificador.run})",
                                   "score": score,
                                   "latencia_ms": round((time.perf_counter() - t0) * 1000.0, 3)}
    return out
