"""Clip de puntos -> vector de largo fijo para el clasificador.

Es la MISMA transformacion para entrenar y para puntuar en vivo:
  - src/almacenamiento/dataset_sql.py la usa para llenar table_frames / table_frames_fix
    (lo que lee entrenar()).
  - src/evaluacion/comparadores/ la usa para convertir una repeticion en vivo en el
    mismo vector que vio el modelo al entrenar.
Si cambia algo aqui, cambia en los dos lados a la vez: no pueden divergir.

Pasos:
  1. filtrar los puntos al catalogo del ejercicio y descartar cuadros sin dato
  2. angulos de la mano (src/procesamiento/medidas/angulos.py, convencion flexion)
  3. normalizar el espacio (formula entre kpoints del ejercicio; antes "rectangulo"/"punto") y remuestrear a
     n_frames_fijo cuadros (interpolacion lineal)
  4. por cuadro: [x1,y1,z1, x2,y2,z2, ..., angulos...], concatenado; NaN -> 0"""

from __future__ import annotations

import numpy as np

from src.nucleo.componentes import componentes, mascara_metricas
from src.procesamiento.medidas import features as FEAT
from src.procesamiento.puntos.normalizacion import NormalizacionInvalida, cfg_para, normalizar, resamplear_angulos


def preparar(points, point_names, deseados=None, kpoints=None, features=None):
    """Paso 1+2: filtra al catalogo, quita cuadros sin dato y calcula angulos.
    Devuelve (points (T,N,3), nombres, angulos (T,A), nombres_angulos) o None
    si no queda ningun cuadro con dato."""
    points = np.asarray(points, dtype=np.float32)
    nombres = [str(n) for n in point_names]
    if len(points) == 0:
        return None
    con_dato = ~np.isnan(points).all(axis=(1, 2))
    points = points[con_dato]
    if points.shape[0] == 0:
        return None
    if deseados:
        indices = [nombres.index(n) for n in deseados if n in nombres]
        if indices:
            points, nombres = points[:, indices, :], [nombres[i] for i in indices]
    if FEAT.medibles(nombres, features):   # los angulos y proporciones activados en Kpoints (crudos, como salen)
        angulos, nombres_ang, _ = FEAT.medir_clip(points, nombres, features)
    else:          # sin angulos ni proporciones activados: solo puntos
        angulos, nombres_ang = np.zeros((len(points), 0), dtype=np.float32), []
    return points, nombres, angulos, nombres_ang


def fijo(points, nombres, angulos, cfg, features=None):
    """Paso 3: (puntos normalizados (n,N,3), angulos (n,A)), redondeados igual
    que se guardan en SQL (2 y 4 decimales) para que vivo == entrenamiento. Las metricas (angulos,
    proporciones) se llevan a 0..1 por tipo: es la tabla normalizada; la cruda va en table_frames."""
    pts = np.round(normalizar(points, nombres, cfg), 4 if cfg["modo"] == "formula" else 2)   # formula: ~-3..3 (largos de tronco), pide mas decimales
    medidos = FEAT.medibles(nombres, features)
    tipos = [f["type"] for f in medidos] if medidos else None
    ang = np.round(FEAT.normalizar_metricas(resamplear_angulos(angulos, cfg["n_frames_fijo"]), tipos), 4)
    return pts, ang


def aplanar(pts_fix: np.ndarray, ang_fix: np.ndarray, usar: str = "ambos", tipos=None) -> np.ndarray:
    """Paso 4: el vector final. usar: ver componentes(); tipos = tipo de cada columna de ang_fix (None = angulos)."""
    ejes, _, _ = componentes(usar)
    mask = np.array(mascara_metricas(tipos, usar, ang_fix.shape[1]), dtype=bool)
    partes = []
    for i in range(len(pts_fix)):
        if ejes:
            partes.append(pts_fix[i][:, ejes].reshape(-1))
        if ang_fix.shape[1]:
            partes.append(ang_fix[i][mask])
    vec = np.concatenate(partes) if partes else np.zeros(0, dtype=np.float32)
    return np.nan_to_num(vec.astype(np.float32), nan=0.0)


def vector_de_prep(prep, spec: dict) -> np.ndarray:
    """Pasos 3+4 sobre lo que devolvio preparar(): normaliza, remuestrea y aplana con la 'spec' del modelo."""
    pts, nombres, ang, _ = prep
    cfg = cfg_para(nombres, spec.get("cfg"))
    try:
        pts_fix, ang_fix = fijo(pts, nombres, ang, cfg, spec.get("features_def"))
    except NormalizacionInvalida:   # escala 0 / kpoint ausente: el clip no entra (vector vacio, como un clip sin datos)
        return np.zeros(0, dtype=np.float32)
    medidos = FEAT.medibles(nombres, spec.get("features_def"))
    return aplanar(pts_fix, ang_fix, spec.get("features", "ambos"), [f["type"] for f in medidos] if medidos else None)


def vector_de_clip(points, point_names, spec: dict) -> np.ndarray | None:
    """Todo junto, con la 'spec' que guarda entrenar() en el modelo:
    {"point_names": [...], "kpoints": [...], "cfg": {...}, "features": "ambos"}."""
    prep = preparar(points, point_names, spec.get("point_names"), spec.get("kpoints"), spec.get("features_def"))
    return None if prep is None else vector_de_prep(prep, spec)
