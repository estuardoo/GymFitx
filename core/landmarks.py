"""Nombres, indices y conexiones de los landmarks de MediaPipe.

Un solo lugar con los nombres permite que los YAML de ejercicio se escriban en
lenguaje humano ("LEFT_ELBOW") en vez de numeros magicos, y que un nombre mal
escrito falle al arrancar y no a mitad de la sesion.
"""

from __future__ import annotations

# --- Manos: 21 puntos por mano, en el orden que devuelve HandLandmarker ---
HAND_LANDMARKS = (
    "WRIST",
    "THUMB_CMC", "THUMB_MCP", "THUMB_IP", "THUMB_TIP",
    "INDEX_FINGER_MCP", "INDEX_FINGER_PIP", "INDEX_FINGER_DIP", "INDEX_FINGER_TIP",
    "MIDDLE_FINGER_MCP", "MIDDLE_FINGER_PIP", "MIDDLE_FINGER_DIP", "MIDDLE_FINGER_TIP",
    "RING_FINGER_MCP", "RING_FINGER_PIP", "RING_FINGER_DIP", "RING_FINGER_TIP",
    "PINKY_MCP", "PINKY_PIP", "PINKY_DIP", "PINKY_TIP",
)

HAND_CONNECTIONS = (
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17),
)

# --- Cuerpo: 33 puntos de PoseLandmarker ---
POSE_LANDMARKS = (
    "NOSE",
    "LEFT_EYE_INNER", "LEFT_EYE", "LEFT_EYE_OUTER",
    "RIGHT_EYE_INNER", "RIGHT_EYE", "RIGHT_EYE_OUTER",
    "LEFT_EAR", "RIGHT_EAR",
    "MOUTH_LEFT", "MOUTH_RIGHT",
    "LEFT_SHOULDER", "RIGHT_SHOULDER",
    "LEFT_ELBOW", "RIGHT_ELBOW",
    "LEFT_WRIST", "RIGHT_WRIST",
    "LEFT_PINKY", "RIGHT_PINKY",
    "LEFT_INDEX", "RIGHT_INDEX",
    "LEFT_THUMB", "RIGHT_THUMB",
    "LEFT_HIP", "RIGHT_HIP",
    "LEFT_KNEE", "RIGHT_KNEE",
    "LEFT_ANKLE", "RIGHT_ANKLE",
    "LEFT_HEEL", "RIGHT_HEEL",
    "LEFT_FOOT_INDEX", "RIGHT_FOOT_INDEX",
)

POSE_CONNECTIONS = (
    (11, 12), (11, 23), (12, 24), (23, 24),          # torso
    (11, 13), (13, 15), (12, 14), (14, 16),          # brazos
    (23, 25), (25, 27), (24, 26), (26, 28),          # piernas
    (27, 29), (29, 31), (27, 31),                    # pie izq
    (28, 30), (30, 32), (28, 32),                    # pie der
    (9, 10), (0, 11), (0, 12),                       # cabeza al tronco
)

_INDEX = {
    "hands": {n: i for i, n in enumerate(HAND_LANDMARKS)},
    "pose": {n: i for i, n in enumerate(POSE_LANDMARKS)},
}

N_POINTS = {"hands": len(HAND_LANDMARKS), "pose": len(POSE_LANDMARKS)}

# --- Regiones del cuerpo, para el selector "que partes mostrar/evaluar" del
# panel. Solo aplican a la fuente "pose" (cuerpo completo); los ejercicios
# de "hands" siempre muestran la mano entera, no tiene sentido dividirla asi.
# Los grupos se solapan a proposito en las articulaciones limite (muneca,
# hombro, cadera): asi el hueso que conecta dos regiones sigue dibujandose
# cuando ambas estan activas.
POSE_REGIONES: dict[str, tuple[str, ...]] = {
    "cabeza": ("NOSE", "LEFT_EYE_INNER", "LEFT_EYE", "LEFT_EYE_OUTER",
               "RIGHT_EYE_INNER", "RIGHT_EYE", "RIGHT_EYE_OUTER",
               "LEFT_EAR", "RIGHT_EAR", "MOUTH_LEFT", "MOUTH_RIGHT"),
    "manos": ("LEFT_WRIST", "RIGHT_WRIST", "LEFT_PINKY", "RIGHT_PINKY",
              "LEFT_INDEX", "RIGHT_INDEX", "LEFT_THUMB", "RIGHT_THUMB"),
    "brazos": ("LEFT_SHOULDER", "RIGHT_SHOULDER", "LEFT_ELBOW", "RIGHT_ELBOW",
               "LEFT_WRIST", "RIGHT_WRIST"),
    "torso": ("LEFT_SHOULDER", "RIGHT_SHOULDER", "LEFT_HIP", "RIGHT_HIP"),
    "cadera": ("LEFT_HIP", "RIGHT_HIP"),
    "piernas": ("LEFT_HIP", "RIGHT_HIP", "LEFT_KNEE", "RIGHT_KNEE",
                "LEFT_ANKLE", "RIGHT_ANKLE"),
    "pies": ("LEFT_ANKLE", "RIGHT_ANKLE", "LEFT_HEEL", "RIGHT_HEEL",
             "LEFT_FOOT_INDEX", "RIGHT_FOOT_INDEX"),
}


def regiones_de_puntos(nombres: list[str]) -> list[str]:
    """Que regiones de POSE_REGIONES tocan al menos uno de estos landmarks.

    Se usa para marcar por defecto, en el selector del panel, las zonas que
    un ejercicio realmente necesita (segun los puntos que declara su YAML) --
    el usuario despues puede ajustarlo a mano.
    """
    return sorted({clave for clave, puntos in POSE_REGIONES.items()
                   if any(n in puntos for n in nombres)})


def region_indices(nombres: list[str] | None) -> set[int] | None:
    """Traduce nombres de region a indices de POSE_LANDMARKS.

    None = sin filtro (todas las regiones, el comportamiento de siempre).
    Una lista (incluso vacia) = solo la union de esas regiones.
    """
    if nombres is None:
        return None
    tabla = _INDEX["pose"]
    return {tabla[n] for clave in nombres for n in POSE_REGIONES.get(clave, ())}


def resolve(name: str, source: str = "hands") -> int:
    """Nombre de landmark -> indice. Falla fuerte y con mensaje util."""
    try:
        tabla = _INDEX[source]
    except KeyError:
        raise ValueError(
            f"Fuente desconocida: {source!r}. Validas: hands, pose."
        ) from None
    try:
        return tabla[name]
    except KeyError:
        raise KeyError(
            f"Landmark {name!r} no existe en la fuente {source!r}. "
            f"Validos: {', '.join(tabla)}"
        ) from None


def connections(source: str) -> tuple[tuple[int, int], ...]:
    return HAND_CONNECTIONS if source == "hands" else POSE_CONNECTIONS
