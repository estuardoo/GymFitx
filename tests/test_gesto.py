"""Verifica el gesto de mano (control de grabar/detener sin botones):

- _clasificar_gesto_mano(): la logica pura de abierta/cerrada + zona muerta,
  sin tracker ni camara.
- _revisar_gesto_mano(): la integracion completa (recorte + tracker de
  gesto + bus), con mediapipe sustituido por el mismo doble minimo que usan
  los demas tests -- solo confirma que corre sin reventar, no un curl
  puntual (el doble siempre devuelve los mismos puntos fijos).

    python tests/test_gesto.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

from test_swap_sink import _instalar_stub_mediapipe  # noqa: E402

_instalar_stub_mediapipe()

from core.exercise import load_exercise                                    # noqa: E402
from core.pipeline import (GESTO_UMBRAL_ABIERTA, GESTO_UMBRAL_CERRADA,      # noqa: E402
                            Pipeline)
from core.sinks import Recorder, Sink                                       # noqa: E402
from core.types import Frame                                                # noqa: E402

EJ = load_exercise(ROOT / "exercises" / "manguito_rotador.yaml")
ABIERTA = GESTO_UMBRAL_ABIERTA + 10
CERRADA = GESTO_UMBRAL_CERRADA - 10
ZONA_MUERTA = (GESTO_UMBRAL_ABIERTA + GESTO_UMBRAL_CERRADA) / 2


def _pipeline():
    return Pipeline(EJ, source=None, sink=Sink(), template=None, annotate=False)


def test_de_abierta_a_cerrada_dispara():
    p = _pipeline()
    assert p._clasificar_gesto_mano(ABIERTA) is False
    assert p._clasificar_gesto_mano(CERRADA) is True


def test_mantenerse_cerrada_no_vuelve_a_disparar():
    p = _pipeline()
    p._clasificar_gesto_mano(ABIERTA)
    assert p._clasificar_gesto_mano(CERRADA) is True
    assert p._clasificar_gesto_mano(CERRADA) is False
    assert p._clasificar_gesto_mano(CERRADA) is False


def test_repetir_el_gesto_dispara_de_nuevo():
    p = _pipeline()
    p._clasificar_gesto_mano(ABIERTA)
    assert p._clasificar_gesto_mano(CERRADA) is True
    p._clasificar_gesto_mano(ABIERTA)
    assert p._clasificar_gesto_mano(CERRADA) is True


def test_cerrar_sin_haber_estado_abierta_tambien_dispara():
    # A pedido: con una sola vez que se cierre el puno alcanza, no hace
    # falta ver la mano abierta primero (p.ej. entra a la zona ya cerrada).
    p = _pipeline()   # estado inicial: None (no "abierta")
    assert p._clasificar_gesto_mano(CERRADA) is True


def test_zona_muerta_mantiene_el_estado_anterior():
    p = _pipeline()
    p._clasificar_gesto_mano(ABIERTA)
    p._clasificar_gesto_mano(ZONA_MUERTA)   # ambiguo: no cambia de estado
    assert p._clasificar_gesto_mano(CERRADA) is True   # sigue viniendo de "abierta"


def test_revisar_gesto_mano_corre_sin_reventar_con_el_tracker_de_prueba():
    p = _pipeline()
    frame = Frame(image=np.zeros((120, 160, 3), dtype=np.uint8), t_ms=0, index=0)
    p._revisar_gesto_mano(frame)   # no debe lanzar excepcion
    assert p._gesto_mano_estado in (None, "abierta", "cerrada")


def test_manos_detalle_apagado_por_defecto_y_no_arma_tracker():
    p = _pipeline()
    assert p._manos_detalle_activo is False
    assert p._tracker_manos_detalle is None   # no se paga el costo si nadie lo prendio


def test_activar_manos_detalle_arma_el_tracker_una_sola_vez():
    p = _pipeline()
    p.set_manos_detalle(True)
    assert p._manos_detalle_activo is True
    tracker = p._tracker_manos_detalle
    assert tracker is not None
    p.set_manos_detalle(False)
    assert p._manos_detalle_activo is False
    assert p._tracker_manos_detalle is tracker   # apagar no lo destruye, solo dispensa de usarlo
    p.set_manos_detalle(True)
    assert p._tracker_manos_detalle is tracker   # prender de nuevo no reconstruye


def test_grabando_falso_mientras_el_sink_es_el_placeholder():
    p = _pipeline()
    assert p.grabando is False


def test_grabando_verdadero_con_un_sink_real_de_grabacion():
    # Regresion: Recorder (como Evaluator y MultiSink) hereda de Sink, asi
    # que "isinstance(sink, Sink)" da True para CUALQUIER sumidero y nunca
    # distingue grabando de no grabando -- pipeline.grabando debe usar
    # "type(sink) is Sink" para que esto funcione de verdad.
    p = _pipeline()
    p.swap_sink(Recorder("dummy_no_se_escribe"))
    assert p.grabando is True
    p.swap_sink(Sink())
    assert p.grabando is False


def test_anotar_pinta_la_zona_de_gesto_cuando_hay_mano_sin_reventar():
    p = _pipeline()
    p._gesto_mano_estado = "abierta"   # simula mano detectada en la esquina
    frame = Frame(image=np.zeros((120, 160, 3), dtype=np.uint8), t_ms=0, index=0)
    p._anotar(frame, [], None)   # no debe lanzar excepcion
    assert p.latest_frame is not None


def test_anotar_con_dedos_detallados_corre_sin_reventar():
    # detecciones=[] a proposito: lo que se prueba es que _anotar() ademas
    # corre el tracker de dedos detallados (HandTracker de prueba) y lo
    # dibuja encima sin reventar -- la deteccion pose en si ya tiene su
    # propio test (test_swap_sink, test_pausa, etc).
    p = _pipeline()
    p.set_manos_detalle(True)
    frame = Frame(image=np.zeros((120, 160, 3), dtype=np.uint8), t_ms=0, index=0)
    p._anotar(frame, [], None)   # no debe lanzar excepcion
    assert p.latest_frame is not None


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
