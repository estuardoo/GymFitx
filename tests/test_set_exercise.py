"""Verifica Pipeline.set_exercise(): cambiar de ejercicio con la camara ya
prendida, sin reabrirla. Mismo truco que test_swap_sink.py: mediapipe queda
sustituido por un doble minimo.

    python tests/test_set_exercise.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

from test_swap_sink import _instalar_stub_mediapipe  # noqa: E402

_instalar_stub_mediapipe()

from core.exercise import load_exercise  # noqa: E402
from core.landmarks import regiones_de_puntos  # noqa: E402
from core.pipeline import Pipeline  # noqa: E402
from core.sinks import Sink  # noqa: E402

EX_MANOS = load_exercise(ROOT / "exercises" / "mano_apertura.yaml")
EX_POSE = load_exercise(ROOT / "exercises" / "manguito_rotador.yaml")


def test_set_exercise_cambia_extractor_y_tracker():
    pipe = Pipeline(EX_MANOS, source=None, sink=Sink(), template=None, annotate=False)
    tracker_viejo = pipe.tracker
    assert pipe.exercise is EX_MANOS

    pipe.set_exercise(EX_POSE)

    assert pipe.exercise is EX_POSE
    assert pipe.extractor.source == "pose"
    assert pipe.tracker is not tracker_viejo
    # El extractor nuevo tiene el tamano de features del ejercicio nuevo.
    assert pipe.extractor.size == len(EX_POSE.features)


def test_set_exercise_sin_plantilla_deja_en_modo_previsualizacion():
    pipe = Pipeline(EX_MANOS, source=None, sink=Sink(), template=None, annotate=False)
    pipe.set_exercise(EX_POSE)
    assert pipe.template is None
    assert pipe.segmenter is None


def test_regiones_de_puntos_del_ejercicio_pose_no_esta_vacio():
    puntos = [p for f in EX_POSE.features for p in (list(f["points"]) + list(f.get("reference", [])))]
    regiones = regiones_de_puntos(puntos)
    assert regiones, "el ejercicio de hombro deberia tocar al menos una region"
    assert set(regiones) <= {"cabeza", "manos", "brazos", "torso", "cadera", "piernas", "pies"}


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
