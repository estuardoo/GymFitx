"""mediapipe falso para los tests: PoseLandmarker devuelve siempre la misma pose de 33 puntos (sin camara ni modelo)."""

from __future__ import annotations

import sys
import types

# 33 puntos fijos, distintos entre si (para que los angulos no salgan degenerados)
_PUNTOS = [(0.3 + 0.01 * i, 0.1 + 0.02 * i, 0.01 * (i % 3)) for i in range(33)]


def instalar() -> None:
    if "mediapipe" in sys.modules and getattr(sys.modules["mediapipe"], "_ES_STUB", False):
        return

    mp = types.ModuleType("mediapipe")
    mp._ES_STUB = True
    mp.ImageFormat = types.SimpleNamespace(SRGB=1)
    mp.Image = lambda image_format=None, data=None: types.SimpleNamespace(data=data)

    tasks = types.ModuleType("mediapipe.tasks")
    tasks_python = types.ModuleType("mediapipe.tasks.python")
    vision = types.ModuleType("mediapipe.tasks.python.vision")

    class BaseOptions:
        def __init__(self, model_asset_path=None):
            self.model_asset_path = model_asset_path

    class _Options:
        def __init__(self, **kw):
            self.__dict__.update(kw)

    class RunningMode:
        VIDEO = "video"

    class _Landmark:
        def __init__(self, x, y, z):
            self.x, self.y, self.z, self.visibility = x, y, z, 0.95

    class _Resultado:
        pose_landmarks = [[_Landmark(*p) for p in _PUNTOS]]
        pose_world_landmarks = [[_Landmark(*p) for p in _PUNTOS]]

    class PoseLandmarker:
        @classmethod
        def create_from_options(cls, options):
            return cls()

        def detect_for_video(self, image, timestamp_ms):
            return _Resultado()

        def close(self):
            pass

    tasks_python.BaseOptions = BaseOptions
    vision.PoseLandmarkerOptions = _Options
    vision.RunningMode = RunningMode
    vision.PoseLandmarker = PoseLandmarker

    tasks_python.vision = vision
    tasks.python = tasks_python
    mp.tasks = tasks

    sys.modules["mediapipe"] = mp
    sys.modules["mediapipe.tasks"] = tasks
    sys.modules["mediapipe.tasks.python"] = tasks_python
    sys.modules["mediapipe.tasks.python.vision"] = vision
