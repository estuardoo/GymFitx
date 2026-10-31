"""Comparar 'esquemas' (que features/regiones del cuerpo se miden) y modelos
(como se compara) entre si, sobre las MISMAS grabaciones.

Un esquema es, en este proyecto, simplemente OTRA definicion de ejercicio
que describe el mismo movimiento real con otro conjunto de features/regiones
-- ver parameters/<n>/ y src/nucleo/ejercicio.py. No hace falta un concepto nuevo:
dos definiciones que empiezan igual ya son dos variantes del mismo movimiento.

Convencion de nombres: 'manguito_rotador' y 'manguito_rotador__hombro'
pertenecen los dos al grupo 'manguito_rotador' (todo antes de '__'). Una definicion
sin '__' es su propio grupo de un solo esquema.

Por que se pueden compartir los MISMOS videos entre esquemas sin volver a
grabar: cada sesion ya archiva el video crudo, sin anotar (ver
src/sesion/grabacion.py). scripts/reprocesar.py ya sabe reprocesar ese video con OTRO
ejercicio adjunto -- el pipeline no distingue camara de video. Este
modulo solo automatiza ese reproceso para muchos esquemas x muchos modelos
a la vez y arma la tabla comparativa.

Lo que este modulo NO hace todavia (ver matriz de pendientes): matriz de
confusion y MAE contra una etiqueta humana -- hace falta la herramienta de
etiquetado, que todavia no existe.
"""

from __future__ import annotations

import numpy as np


def grupo_de(slug: str) -> str:
    """'manguito_rotador__hombro' -> 'manguito_rotador'. Sin '__', el slug
    entero es su propio grupo (un solo esquema)."""
    return slug.split("__", 1)[0]


def esquemas_de(movimiento: str, ejercicios: dict) -> dict:
    """Todos los ejercicios (slug -> Exercise) que son esquemas del mismo
    movimiento, ordenados por slug para que la salida sea reproducible."""
    return {
        slug: ex for slug, ex in sorted(ejercicios.items())
        if grupo_de(slug) == movimiento
    }


def tabla_comparacion(resultados: dict[tuple[str, str], list[float]]) -> dict:
    """resultados: {(esquema, modelo): [score_rep1, score_rep2, ...]}, todas
    sobre el MISMO video y en el mismo orden de repeticion.

    Devuelve promedio/desvio por celda (esquema, modelo) y una matriz de
    correlacion entre todas las celdas -- que tan de acuerdo estan entre si
    modelos y esquemas sobre las mismas repeticiones. No necesita ninguna
    etiqueta humana: es acuerdo entre modelos, no acierto contra la verdad.
    """
    filas = {}
    for clave, scores in resultados.items():
        arr = np.asarray(scores, dtype=float)
        filas[clave] = {
            "promedio": round(float(np.mean(arr)), 1) if arr.size else None,
            "desvio": round(float(np.std(arr)), 1) if arr.size else None,
            "n": len(scores),
        }

    claves = list(resultados)
    n_min = min((len(v) for v in resultados.values()), default=0)
    correlacion = {}
    if n_min >= 2 and len(claves) >= 2:
        M = np.array([resultados[k][:n_min] for k in claves], dtype=float)
        with np.errstate(invalid="ignore"):
            C = np.corrcoef(M)
        for i in range(len(claves)):
            for j in range(i + 1, len(claves)):
                r = C[i, j]
                correlacion[f"{claves[i]} ~ {claves[j]}"] = (
                    round(float(r), 3) if np.isfinite(r) else None
                )

    return {"filas": filas, "correlacion": correlacion}
