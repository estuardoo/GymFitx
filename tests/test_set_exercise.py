"""Verifica Pipeline.set_exercise(): cambiar de ejercicio con la camara ya
prendida, sin reabrirla. Mismo truco que test_swap_sink.py: mediapipe queda
sustituido por un doble minimo.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

from test_swap_sink import _instalar_stub_mediapipe  # noqa: E402

_instalar_stub_mediapipe()

from src.nucleo.ejercicio import load_exercise  # noqa: E402
from src.nucleo.landmarks import regiones_de_puntos  # noqa: E402
from src.sesion.pipeline import Pipeline  # noqa: E402
from src.sesion.sumideros import Sink  # noqa: E402

EX_OTRO = load_exercise("cuerpo_completo")
EX_POSE = load_exercise("manguito_rotador")


def test_set_exercise_cambia_extractor_y_tracker():
    pipe = Pipeline(EX_OTRO, source=None, sink=Sink(), template=None, annotate=False)
    tracker_viejo = pipe.tracker
    assert pipe.exercise is EX_OTRO

    pipe.set_exercise(EX_POSE)

    assert pipe.exercise is EX_POSE
    assert pipe.extractor.source == "pose"
    assert pipe.tracker is not tracker_viejo
    # El extractor nuevo tiene el tamano de features del ejercicio nuevo.
    assert pipe.extractor.size == len(EX_POSE.features)


def test_set_exercise_sin_plantilla_deja_en_modo_previsualizacion():
    pipe = Pipeline(EX_OTRO, source=None, sink=Sink(), template=None, annotate=False)
    pipe.set_exercise(EX_POSE)
    assert pipe.template is None
    assert pipe.segmenter is None


def test_regiones_de_puntos_del_ejercicio_pose_no_esta_vacio():
    puntos = [p for f in EX_POSE.features for p in (list(f["points"]) + list(f.get("reference", [])))]
    regiones = regiones_de_puntos(puntos)
    assert regiones, "el ejercicio de hombro deberia tocar al menos una region"
    assert set(regiones) <= {"cabeza", "manos", "brazos", "torso", "cadera", "piernas", "pies"}

