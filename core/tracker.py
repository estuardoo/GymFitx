"""Capa 2: cuadro -> landmarks. Unico archivo del proyecto que importa mediapipe.

Si manana cambiamos de motor (MoveNet, YOLO-pose, lo que sea), solo se
reescribe este archivo: el resto del pipeline habla en Landmarks, no en
estructuras de MediaPipe.
"""

from __future__ import annotations

import urllib.request
from pathlib import Path

import mediapipe as mp
import numpy as np
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

from .types import Frame, Landmarks

MODELS_DIR = Path(__file__).resolve().parent.parent / "models"

MODEL_URLS = {
    "hands": (
        "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
        "hand_landmarker/float16/1/hand_landmarker.task"
    ),
    "pose": (
        "https://storage.googleapis.com/mediapipe-models/pose_landmarker/"
        "pose_landmarker_lite/float16/1/pose_landmarker_lite.task"
    ),
}


def ensure_model(source: str) -> Path:
    """Descarga el modelo la primera vez. Despues el sistema corre offline."""
    path = MODELS_DIR / f"{source}_landmarker.task"
    if path.exists() and path.stat().st_size > 0:
        return path
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Descargando modelo '{source}' a {path} ...")
    tmp = path.with_suffix(".part")
    urllib.request.urlretrieve(MODEL_URLS[source], tmp)
    tmp.replace(path)
    print("Modelo listo.")
    return path


def _to_array(points) -> np.ndarray:
    return np.array([[p.x, p.y, p.z] for p in points], dtype=np.float32)


class _BaseTracker:
    source = ""

    def detect(self, frame: Frame) -> list[Landmarks]:
        raise NotImplementedError

    def close(self) -> None:
        self._landmarker.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    @staticmethod
    def _mp_image(frame: Frame) -> "mp.Image":
        rgb = np.ascontiguousarray(frame.image[:, :, ::-1])
        return mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)


class HandTracker(_BaseTracker):
    source = "hands"

    def __init__(self, num_hands: int = 2, min_confidence: float = 0.5) -> None:
        options = vision.HandLandmarkerOptions(
            base_options=mp_python.BaseOptions(model_asset_path=str(ensure_model("hands"))),
            running_mode=vision.RunningMode.VIDEO,
            num_hands=num_hands,
            min_hand_detection_confidence=min_confidence,
            min_tracking_confidence=min_confidence,
        )
        self._landmarker = vision.HandLandmarker.create_from_options(options)

    def detect(self, frame: Frame) -> list[Landmarks]:
        r = self._landmarker.detect_for_video(self._mp_image(frame), frame.t_ms)
        salida = []
        for i, screen in enumerate(r.hand_landmarks):
            cat = r.handedness[i][0]
            salida.append(
                Landmarks(
                    source="hands",
                    world=_to_array(r.hand_world_landmarks[i]),
                    screen=_to_array(screen),
                    label=cat.category_name,
                    score=float(cat.score),
                )
            )
        return salida


class PoseTracker(_BaseTracker):
    source = "pose"

    def __init__(self, min_confidence: float = 0.5) -> None:
        options = vision.PoseLandmarkerOptions(
            base_options=mp_python.BaseOptions(model_asset_path=str(ensure_model("pose"))),
            running_mode=vision.RunningMode.VIDEO,
            num_poses=1,
            min_pose_detection_confidence=min_confidence,
            min_tracking_confidence=min_confidence,
        )
        self._landmarker = vision.PoseLandmarker.create_from_options(options)

    def detect(self, frame: Frame) -> list[Landmarks]:
        r = self._landmarker.detect_for_video(self._mp_image(frame), frame.t_ms)
        if not r.pose_landmarks:
            return []
        screen = r.pose_landmarks[0]
        world = r.pose_world_landmarks[0] if r.pose_world_landmarks else screen
        vis = float(np.mean([p.visibility for p in screen])) if screen else 0.0
        return [
            Landmarks(
                source="pose",
                world=_to_array(world),
                screen=_to_array(screen),
                label="",
                score=vis,
            )
        ]


def build_tracker(exercise) -> _BaseTracker:
    """Enruta segun lo que declare el ejercicio. El pipeline no elige, obedece."""
    if exercise.source == "hands":
        return HandTracker(num_hands=1 if exercise.hand != "any" else 2)
    if exercise.source == "pose":
        return PoseTracker()
    raise ValueError(f"Fuente no soportada: {exercise.source!r}")
