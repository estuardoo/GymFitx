"""Catalogo de 'kpoints' de un ejercicio -> puntos por cuadro.

UNA sola implementacion para los dos caminos:
  - offline: src/procesamiento/offline.py re-decodifica el video grabado (30 fps reales)
    y arma el dataset de entrenamiento.
  - en vivo: src/sesion/pipeline.py arma los mismos puntos por cuadro para que el
    clasificador entrenado (src/evaluacion/comparadores/) puntue cada repeticion.

Cada kpoint de la definicion: {"numero", "nombre", "origen"} con
  origen = {"tipo": "landmark", "fuente": "pose", "landmark": NOMBRE}
         o {"tipo": "derivado", "de": [numero_a, numero_b]}  (punto medio de dos kpoints previos)
"""

from __future__ import annotations

import numpy as np

from src.nucleo.landmarks import POSE_LANDMARKS

FUENTES_KPOINT = ("pose",)

# Sube cuando cambia QUE se guarda en el .npz. Un .npz con version menor se re-detecta solo.
VERSION_DETECCION = 2

_NAN3 = np.full(3, np.nan, dtype=np.float32)


def nombres(kpoints) -> list[str]:
    return [kp["nombre"] for kp in kpoints or []]


def resolver(kpoints, detecciones):
    """Detecciones (Landmarks de pose) de UN cuadro -> (world (K,3), screen (K,2)) en el orden del
    catalogo; NaN donde el punto no se vio. None si no se vio ningun punto del catalogo (cuadro sin dato)."""
    valores: dict = {}   # (fuente, landmark) -> (3,) world, para MEDIR
    en_pant: dict = {}   # (fuente, landmark) -> (2,) screen 0-1, para DIBUJAR
    for d in detecciones:
        if d.source == "pose":
            valores.update({("pose", nm): xyz for nm, xyz in zip(POSE_LANDMARKS, d.world)})
            en_pant.update({("pose", nm): xy[:2] for nm, xy in zip(POSE_LANDMARKS, d.screen)})
    if not valores:
        return None

    res, res_pant = {}, {}
    for kp in kpoints:
        origen = kp["origen"]
        if origen["tipo"] == "landmark":
            clave = (origen["fuente"], origen["landmark"])
            res[kp["numero"]] = np.asarray(valores.get(clave, _NAN3), dtype=np.float32)
            res_pant[kp["numero"]] = np.asarray(en_pant.get(clave, _NAN3[:2]), dtype=np.float32)
        else:  # derivado: punto medio de otros dos kpoints ya resueltos
            a, b = origen["de"]
            res[kp["numero"]] = (res[a] + res[b]) / 2
            res_pant[kp["numero"]] = (res_pant[a] + res_pant[b]) / 2
    fila = np.stack([res[kp["numero"]] for kp in kpoints])
    if np.isnan(fila).all():
        return None
    return fila, np.stack([res_pant[kp["numero"]] for kp in kpoints])
