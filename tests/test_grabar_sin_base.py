"""Verifica Pipeline.set_template(): instalar una base DESPUES de que la
camara ya esta prendida, sin reabrirla. Es lo que permite grabar la primera
toma de un ejercicio (que crea la base) y evaluar la siguiente toma en la
MISMA sesion de camara, sin apagar y volver a prender entre medio.

Mismo truco que test_pausa.py / test_swap_sink.py: mediapipe queda
sustituido por un doble minimo, no hace falta camara ni modelo real.

    python tests/test_grabar_sin_base.py
"""

from __future__ import annotations

import sys
import types
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def _instalar_stub_mediapipe() -> None:
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

    class HandLandmarker:
        @classmethod
        def create_from_options(cls, options):
            return cls()

        def detect_for_video(self, image, timestamp_ms):
            return types.SimpleNamespace(hand_landmarks=[], hand_world_landmarks=[], handedness=[])

        def close(self):
            pass

    tasks_python.BaseOptions = BaseOptions
    vision.HandLandmarkerOptions = _Options
    vision.PoseLandmarkerOptions = _Options
    vision.RunningMode = RunningMode
    vision.HandLandmarker = HandLandmarker
    vision.PoseLandmarker = HandLandmarker

    tasks_python.vision = vision
    tasks.python = tasks_python
    mp.tasks = tasks

    sys.modules["mediapipe"] = mp
    sys.modules["mediapipe.tasks"] = tasks
    sys.modules["mediapipe.tasks.python"] = tasks_python
    sys.modules["mediapipe.tasks.python.vision"] = vision


_instalar_stub_mediapipe()

from core.exercise import load_exercise      # noqa: E402
from core.features import FeatureExtractor   # noqa: E402
from core.pipeline import Pipeline, Sink     # noqa: E402
from core.template import Template           # noqa: E402
import core.tracker as tracker_mod           # noqa: E402

tracker_mod.ensure_model = lambda source: Path("stub.task")

EJ = load_exercise(ROOT / "exercises" / "mano_apertura.yaml")
EXTRACTOR = FeatureExtractor(EJ)
assert EJ.direction == "down_up"  # el test asume esto para leer low/high tal cual


def _plantilla_falsa(low=70.0, high=170.0) -> Template:
    f = EXTRACTOR.size
    return Template(
        exercise=EJ.slug, names=EXTRACTOR.names, units=EXTRACTOR.units,
        data=np.zeros((10, f), dtype=np.float32),
        mu=np.zeros(f, dtype=np.float32), sigma=np.ones(f, dtype=np.float32),
        low=low, high=high, tau=10.0, n_reps=3,
    )


def test_pipeline_arranca_sin_base_no_tiene_segmentador():
    """Asi arranca 'prender camara' para un ejercicio que aun no tiene base."""
    pipe = Pipeline(EJ, source=None, sink=Sink(), template=None, annotate=False)
    assert pipe.template is None
    assert pipe.segmenter is None


def test_set_template_instala_la_base_sin_reabrir_la_camara():
    """Al terminar de grabar la primera toma (Recorder.on_stop crea la
    plantilla), instalarla con set_template() debe dejar la sesion lista
    para evaluar la siguiente toma -- mismo pipeline, mismo hilo, misma
    camara, solo cambia que ya hay umbral y segmentador."""
    pipe = Pipeline(EJ, source=None, sink=Sink(), template=None, annotate=False)
    plantilla = _plantilla_falsa()

    pipe.set_template(plantilla)

    assert pipe.template is plantilla
    assert pipe.segmenter is not None
    assert pipe.segmenter.low == plantilla.low
    assert pipe.segmenter.high == plantilla.high
    assert pipe.segmenter.reps == 0


def test_set_template_se_puede_reemplazar_en_la_misma_sesion():
    """'Usar como base' con otra grabacion, sin apagar la camara: el
    segmentador viejo se descarta del todo, no se mezcla con el nuevo."""
    pipe = Pipeline(EJ, source=None, sink=Sink(), template=None, annotate=False)
    pipe.set_template(_plantilla_falsa(low=70.0, high=170.0))
    segmentador_viejo = pipe.segmenter

    nueva = _plantilla_falsa(low=80.0, high=160.0)
    pipe.set_template(nueva)

    assert pipe.template is nueva
    assert pipe.segmenter is not segmentador_viejo
    assert pipe.segmenter.low == 80.0
    assert pipe.segmenter.high == 160.0


if __name__ == "__main__":
    fallos = 0
    for nombre, fn in sorted(globals().items()):
        if nombre.startswith("test_") and callable(fn):
            try:
                fn(); print(f"  OK    {nombre}")
            except Exception as e:
                fallos += 1; print(f"  FALLA {nombre}: {e}")
    print("\nTodo bien." if not fallos else f"\n{fallos} test(s) fallaron.")
    raise SystemExit(1 if fallos else 0)
