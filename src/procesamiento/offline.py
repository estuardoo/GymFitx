"""Detecta los kpoints del ejercicio sobre un video YA GRABADO: es la fuente
del dataset de entrenamiento.

Por que offline y no solo en vivo: desde que la grabacion guarda TODOS los
cuadros de la camara (captura desacoplada, ver src/sesion/pipeline.py), el video
tiene ~30 fps reales, mientras que la deteccion en vivo corre a lo que de la
CPU. Re-detectar sobre el video da puntos en cada cuadro. La resolucion
kpoint-por-cuadro es la misma funcion que el vivo (src.procesamiento.puntos.kpoints.resolver) y
los trackers son los de src/captura/deteccion/tracker.py: no hay logica duplicada.

Se llama desde exportar() en src/etiquetado/cortes.py, una vez por video (si el .npz
hermano ya tiene los puntos que le hacen falta a este ejercicio no hace nada
-- por eso es seguro llamarlo en cada corte). Aislado a proposito: si falta
GYMFITX, mediapipe u opencv-python, se lanza DeteccionNoDisponible y quien
llama decide seguir sin puntos para ese video en vez de tumbar el corte
entero.

Los puntos quedan con su PROPIO eje de tiempo (points_t_ms), independiente
del t_ms de las features ya guardadas: salen de re-decodificar el .mp4 ahora,
no de la sesion de captura original, asi que no coincide frame a frame con
el t_ms de 'values'. recorta_npz() en src/etiquetado/cortes.py los recorta cada uno con
su propia mascara de tiempo.

Dos modos, segun si el ejercicio ya tiene un catalogo de 'kpoints' (ver
src/etiquetado/editor_puntos.py) en su definicion:

- CON catalogo: se guardan los kpoints del ejercicio en UN array de puntos nombrados como el
  usuario los llamo, calculando tambien los derivados (punto medio de otros dos). Si el catalogo
  cambia (se agrega un kpoint nuevo) el set de nombres guardado ya no coincide con el pedido
  y se vuelve a detectar solo, en el siguiente export -- automatico.
- SIN catalogo todavia: se guardan los 33 landmarks crudos con sus nombres de MediaPipe.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from src.nucleo.log import logger
from src.procesamiento.puntos import kpoints as KP
from src.procesamiento.puntos.kpoints import VERSION_DETECCION

log = logger("procesamiento")


class DeteccionNoDisponible(RuntimeError):
    """Falta GYMFITX, mediapipe/opencv-python, o el modelo -- nunca tumba el corte de videos."""


def _cargar_motor():
    try:
        from src.captura.deteccion.tracker import PoseTracker
        from src.nucleo.landmarks import POSE_LANDMARKS
        from src.nucleo.tipos import Frame
    except ImportError as e:
        raise DeteccionNoDisponible(
            f"Falta mediapipe/opencv-python, o el motor de deteccion de GYMFITX no cargo: {e}") from None
    return PoseTracker, Frame, POSE_LANDMARKS


def _kpoints_de(exercise):
    """(kpoints, source) de la definicion de ese ejercicio. kpoints es [] si el
    ejercicio no existe, no tiene definicion, o no tiene catalogo definido todavia
    -- en cualquiera de esos casos quien llama cae al modo viejo."""
    from src.nucleo.ejercicio import leer_def
    datos = leer_def(exercise) if exercise else None
    if datos is None:
        return [], "pose"
    return datos.get("kpoints") or [], datos.get("source", "pose")


def _abrir_video(mp4_path):
    import cv2
    cap = cv2.VideoCapture(str(mp4_path))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    return cap, fps


def _detectar_legacy(mp4_path, source):
    """Guarda los 33 landmarks crudos con sus nombres de MediaPipe -- para ejercicios sin catalogo de kpoints."""
    PoseTracker, Frame, POSE_LANDMARKS = _cargar_motor()
    if source != "pose":
        raise DeteccionNoDisponible(f"Fuente de deteccion no soportada: {source!r}")
    tracker = PoseTracker()

    cap, fps = _abrir_video(mp4_path)
    puntos, pantalla, t_ms_lista = [], [], []
    try:
        i = 0
        while True:
            ok, img = cap.read()
            if not ok:
                break
            t_ms = int(round(i * 1000 / fps))
            detecciones = tracker.detect(Frame(image=img, t_ms=t_ms, index=i))
            if detecciones:
                elegido = max(detecciones, key=lambda d: d.score)
                puntos.append(elegido.world)
                pantalla.append(elegido.screen[:, :2])
                t_ms_lista.append(t_ms)
            i += 1
    finally:
        cap.release()
        tracker.close()

    if not puntos:
        return None
    return {
        "points": np.stack(puntos).astype(np.float32),
        "points_t_ms": np.array(t_ms_lista, dtype=np.int64),
        "point_names": np.array(POSE_LANDMARKS),
        "points_screen": np.stack(pantalla).astype(np.float32),
        "deteccion_version": np.array(VERSION_DETECCION),
    }


def _detectar_combinado(mp4_path, kpoints):
    """Resuelve cada kpoint por cuadro con src.procesamiento.puntos.kpoints.resolver -- la MISMA funcion que
    usa el pipeline en vivo, asi offline y vivo producen exactamente los mismos puntos."""
    PoseTracker, Frame, _ = _cargar_motor()
    tracker = PoseTracker()

    cap, fps = _abrir_video(mp4_path)
    puntos, pantalla, t_ms_lista = [], [], []
    try:
        i = 0
        while True:
            ok, img = cap.read()
            if not ok:
                break
            t_ms = int(round(i * 1000 / fps))
            r = KP.resolver(kpoints, tracker.detect(Frame(image=img, t_ms=t_ms, index=i)))
            if r is not None:
                puntos.append(r[0])
                pantalla.append(r[1])
                t_ms_lista.append(t_ms)
            i += 1
    finally:
        cap.release()
        tracker.close()

    if not puntos:
        return None
    return {
        "points": np.stack(puntos).astype(np.float32),
        "points_t_ms": np.array(t_ms_lista, dtype=np.int64),
        "point_names": np.array(KP.nombres(kpoints)),
        "points_screen": np.stack(pantalla).astype(np.float32),
        "deteccion_version": np.array(VERSION_DETECCION),
    }


def _version(npz_dict):
    v = npz_dict.get("deteccion_version")
    return int(v) if v is not None else 1


def detectar_puntos_si_faltan(mp4_path: Path, exercise: str | None = None) -> bool:
    """True si acabo de detectar y guardar puntos nuevos en el .npz hermano;
    False si ya tenia los que le hacen falta a este ejercicio, o si no hay
    .npz que actualizar. 'exercise' se lee del .json hermano si no se pasa."""
    npz_path = mp4_path.with_suffix(".npz")
    json_path = mp4_path.with_suffix(".json")
    if not npz_path.exists():
        return False
    existente = dict(np.load(npz_path, allow_pickle=False))

    if exercise is None and json_path.exists():
        try:
            exercise = json.loads(json_path.read_text("utf-8")).get("exercise")
        except (OSError, ValueError) as e:
            log.warning("ejercicio no legible en %s: %s", json_path.name, e)

    kpoints, legacy_source = _kpoints_de(exercise)

    if kpoints:
        # con catalogo: se re-detecta si el set de nombres guardado no es
        # EXACTAMENTE el que el catalogo pide ahora mismo (kpoint agregado o
        # quitado desde el ultimo export) -- el "automatico al exportar" pedido.
        necesarios = {kp["nombre"] for kp in kpoints}
        tiene = set(str(n) for n in existente["point_names"]) if "point_names" in existente else set()
        if "points" in existente and tiene == necesarios and _version(existente) >= VERSION_DETECCION:
            return False
        try:
            import cv2  # noqa: F401
        except ImportError:
            raise DeteccionNoDisponible("Falta opencv-python (pip install opencv-python)") from None
        resultado = _detectar_combinado(mp4_path, kpoints)
    else:
        if "points" in existente and ("points_t_ms" not in existente or _version(existente) >= VERSION_DETECCION):
            return False  # puntos grabados en vivo por GYMFITX (sin points_t_ms): no se tocan
        try:
            import cv2  # noqa: F401
        except ImportError:
            raise DeteccionNoDisponible("Falta opencv-python (pip install opencv-python)") from None
        resultado = _detectar_legacy(mp4_path, legacy_source or "pose")

    if resultado is None:
        return False
    for k in ("points", "points_t_ms", "point_names", "manos", "points_screen", "manos_screen",
              "deteccion_version", "invertir_manos"):  # manos*/invertir: restos de npz viejos
        existente.pop(k, None)
    existente.update(resultado)
    np.savez_compressed(npz_path, **existente)
    return True
