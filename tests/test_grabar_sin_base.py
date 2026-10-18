"""Verifica Pipeline.set_template(): instalar una base DESPUES de que la
camara ya esta prendida, sin reabrirla. Es lo que permite grabar la primera
toma de un ejercicio (que crea la base) y evaluar la siguiente toma en la
MISMA sesion de camara, sin apagar y volver a prender entre medio.

Mismo truco que test_pausa.py / test_swap_sink.py: mediapipe queda
sustituido por un doble minimo, no hace falta camara ni modelo real.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent


from mp_stub import instalar as _instalar_stub_mediapipe  # noqa: E402

_instalar_stub_mediapipe()

from src.captura.deteccion import tracker as tracker_mod  # noqa: E402
from src.evaluacion.plantilla import Template  # noqa: E402
from src.nucleo.ejercicio import load_exercise  # noqa: E402
from src.procesamiento.medidas.features import FeatureExtractor  # noqa: E402
from src.sesion.pipeline import Pipeline, Sink  # noqa: E402

tracker_mod.ensure_model = lambda source: Path("stub.task")

EJ = load_exercise(ROOT / "ejercicios" / "manguito_rotador.yaml")
EXTRACTOR = FeatureExtractor(EJ)


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
    assert pipe.segmenter.low == -plantilla.high   # up_down invierte el signo
    assert pipe.segmenter.high == -plantilla.low
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
    assert pipe.segmenter.low == -160.0
    assert pipe.segmenter.high == -80.0

