"""Gesto de control (grabar/detener sin botones): muneca sostenida en la esquina superior izquierda.

- Gesto.avanzar(): logica pura (tiempo dentro de la zona, enfriamiento, re-armado).
- Gesto.evaluar() / Pipeline: integracion con detecciones de pose, sin camara.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent

from test_swap_sink import _instalar_stub_mediapipe  # noqa: E402

_instalar_stub_mediapipe()

from src.nucleo.ejercicio import load_exercise  # noqa: E402
from src.nucleo.landmarks import POSE_LANDMARKS  # noqa: E402
from src.nucleo.tipos import Frame, Landmarks  # noqa: E402
from src.sesion.gesto import (  # noqa: E402
    GESTO_ENFRIAMIENTO_MS,
    GESTO_MANTENER_MS,
    GESTO_OLVIDO_MS,
    GESTO_RECORTE,
    Gesto,
)
from src.sesion.pipeline import Pipeline  # noqa: E402
from src.sesion.sumideros import Recorder, Sink  # noqa: E402

EJ = load_exercise("manguito_rotador")


def _pipeline():
    return Pipeline(EJ, source=None, sink=Sink(), template=None, annotate=False)


def _pose(muneca_xy):
    """Pose con todos los puntos en el centro salvo la muneca derecha."""
    screen = np.full((33, 3), 0.5, dtype=np.float32)
    screen[POSE_LANDMARKS.index("RIGHT_WRIST"), :2] = muneca_xy
    return [Landmarks(source="pose", world=screen.copy(), screen=screen, label="", score=0.9)]


ADENTRO = _pose((GESTO_RECORTE / 2, GESTO_RECORTE / 2))
AFUERA = _pose((0.6, 0.6))


def test_sostener_la_muneca_dispara_una_vez():
    g = Gesto(lambda: None)
    assert g.avanzar(True, 0) is False
    assert g.avanzar(True, GESTO_MANTENER_MS - 1) is False
    assert g.avanzar(True, GESTO_MANTENER_MS) is True
    assert g.avanzar(True, GESTO_MANTENER_MS + 100) is False   # sigue adentro: no repite


def test_hay_que_salir_de_la_zona_para_volver_a_disparar():
    g = Gesto(lambda: None)
    g.avanzar(True, 0)
    assert g.avanzar(True, GESTO_MANTENER_MS) is True
    t = GESTO_MANTENER_MS + GESTO_OLVIDO_MS + 10
    g.avanzar(False, t)                                        # sale de verdad
    assert g.estado is None
    g.avanzar(True, t + 10)
    assert g.avanzar(True, t + 10 + GESTO_MANTENER_MS) is True   # ya paso el enfriamiento


def test_enfriamiento_evita_dos_disparos_seguidos():
    g = Gesto(lambda: None)
    g.avanzar(True, 0)
    assert g.avanzar(True, GESTO_MANTENER_MS) is True
    t = GESTO_MANTENER_MS + GESTO_OLVIDO_MS + 10
    g.avanzar(False, t)
    g.avanzar(True, t + 10)
    assert GESTO_MANTENER_MS < GESTO_ENFRIAMIENTO_MS           # supuesto del test
    assert g.avanzar(True, GESTO_MANTENER_MS + 500) is False   # sigue en enfriamiento


def test_perder_la_muneca_un_instante_no_reinicia_la_cuenta():
    g = Gesto(lambda: None)
    g.avanzar(True, 0)
    g.avanzar(False, GESTO_OLVIDO_MS // 2)                     # un cuadro sin ver
    assert g.estado == "dentro"
    assert g.avanzar(True, GESTO_MANTENER_MS) is True


def test_pasar_de_largo_por_la_zona_no_dispara():
    g = Gesto(lambda: None)
    g.avanzar(True, 0)
    g.avanzar(False, GESTO_OLVIDO_MS * 2)                      # salio antes de tiempo
    assert g.estado is None
    assert g.avanzar(True, GESTO_MANTENER_MS) is False         # la cuenta empezo de nuevo


def test_en_zona_lee_la_pose():
    assert Gesto.en_zona(ADENTRO) is True
    assert Gesto.en_zona(AFUERA) is False
    assert Gesto.en_zona([]) is False


def test_evaluar_llama_al_callback_al_cumplirse_el_tiempo():
    disparos = []
    g = Gesto(lambda: disparos.append(1))
    g.evaluar(ADENTRO, 0)
    g.evaluar(ADENTRO, GESTO_MANTENER_MS)
    assert disparos == [1]


def test_pipeline_procesa_cuadros_con_gesto_sin_reventar():
    p = _pipeline()
    frame = Frame(image=np.zeros((120, 160, 3), dtype=np.uint8), t_ms=0, index=0)
    p._procesar(frame)
    assert p.gesto.estado in (None, "dentro")


def test_grabando_falso_mientras_el_sink_es_el_placeholder():
    assert _pipeline().grabando is False


def test_grabando_verdadero_con_un_sink_real_de_grabacion():
    # Regresion: Recorder (como Evaluator y MultiSink) hereda de Sink, asi
    # que "isinstance(sink, Sink)" da True para CUALQUIER sumidero --
    # pipeline.grabando debe usar "type(sink) is Sink".
    p = _pipeline()
    p.swap_sink(Recorder("dummy_no_se_escribe"))
    assert p.grabando is True
    p.swap_sink(Sink())
    assert p.grabando is False


def test_anotar_pinta_la_zona_de_gesto_sin_reventar():
    p = _pipeline()
    p.gesto.estado = "dentro"
    frame = Frame(image=np.zeros((120, 160, 3), dtype=np.uint8), t_ms=0, index=0)
    p._anotar(frame, [], None)
    assert p.latest_frame is not None
