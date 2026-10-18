"""Verifica la aritmetica de pausa del Pipeline, sin camara ni MediaPipe real.

Esta es la unica prueba del proyecto que importa src.sesion.pipeline (las demas
evitan a proposito el modulo que carga mediapipe). Para poder correr sin la
libreria instalada -y sin descargar el modelo- se sustituye 'mediapipe' en
sys.modules por un doble minimo antes de importar: el HandLandmarker del
doble ignora el modelo y siempre devuelve una mano con landmarks fijos, que
es todo lo que este test necesita para verificar que los TIEMPOS se ajustan
bien alrededor de una pausa.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent


from mp_stub import instalar as _instalar_stub_mediapipe  # noqa: E402

_instalar_stub_mediapipe()

from src.captura.deteccion import tracker as tracker_mod  # noqa: E402
from src.nucleo.ejercicio import load_exercise  # noqa: E402
from src.nucleo.tipos import Frame  # noqa: E402
from src.sesion.pipeline import Pipeline, Sink  # noqa: E402

# El stub no necesita un archivo de modelo real; evita que ensure_model()
# intente descargarlo o toque la carpeta models/ real del proyecto.
tracker_mod.ensure_model = lambda source: Path("stub.task")

EJ = load_exercise(ROOT / "ejercicios" / "manguito_rotador.yaml")


class _EspiaSink(Sink):
    """Registra el t_ms con el que llega cada cuadro que SI se procesa."""

    def __init__(self):
        self.vistos: list[int] = []

    def on_start(self, pipe):
        pass

    def on_frame(self, pipe, frame, fv):
        self.vistos.append(frame.t_ms)

    def on_rep(self, pipe, seg):
        pass

    def on_stop(self, pipe):
        pass


def _frame(t_ms: int) -> Frame:
    img = np.zeros((60, 80, 3), dtype=np.uint8)
    return Frame(image=img, t_ms=t_ms, index=0)


def _construir_pipeline() -> tuple[Pipeline, _EspiaSink]:
    espia = _EspiaSink()
    # source=None: este test llama _procesar() directamente, nunca pipe.run().
    pipe = Pipeline(EJ, source=None, sink=espia, template=None, annotate=False)
    return pipe, espia


def test_procesa_normalmente_sin_pausa():
    pipe, espia = _construir_pipeline()
    for t in (0, 33, 66, 99):
        pipe._procesar(_frame(t))
    assert espia.vistos == [0, 33, 66, 99]
    assert pipe.frames_vistos == 4


def test_los_cuadros_en_pausa_no_llegan_al_sumidero():
    pipe, espia = _construir_pipeline()
    pipe._procesar(_frame(0))
    pipe._procesar(_frame(33))
    pipe.pause()
    assert pipe.is_paused
    for t in (66, 99, 132, 165, 198):
        pipe._procesar(_frame(t))       # deben ser ignorados, ninguno debe llegar
    assert espia.vistos == [0, 33]      # solo los dos de antes de pausar
    assert pipe.frames_vistos == 2      # el contador tampoco avanza en pausa


def test_al_reanudar_la_pausa_se_descuenta_del_tiempo():
    """El punto central: reanudar debe continuar la cadencia previa, sin salto."""
    pipe, espia = _construir_pipeline()
    pipe._procesar(_frame(0))
    pipe._procesar(_frame(33))

    pipe.pause()
    for t in (66, 99, 132, 165, 198):    # ~165 ms de pausa real, todos descartados
        pipe._procesar(_frame(t))
    pipe.resume()
    assert not pipe.is_paused

    pipe._procesar(_frame(231))          # primer cuadro real tras reanudar

    # Sin el descuento de pausa, este cuadro llegaria marcado t=231 (un salto
    # de 198ms respecto al anterior) y tanto el filtro como el segmentador lo
    # verian como un movimiento brusco que nunca ocurrio.
    assert espia.vistos == [0, 33, 66], espia.vistos
    pasos = [b - a for a, b in zip(espia.vistos, espia.vistos[1:])]
    assert pasos == [33, 33], f"la cadencia deberia seguir en 33ms, no {pasos}"


def test_dos_pausas_seguidas_acumulan_el_descuento():
    """Pausar dos veces en la misma sesion debe sumar ambos descuentos."""
    pipe, espia = _construir_pipeline()
    for t in (0, 33):
        pipe._procesar(_frame(t))

    pipe.pause()
    for t in (66, 99, 132):              # ~99ms de pausa real, descartados
        pipe._procesar(_frame(t))
    pipe.resume()
    for t in (165, 198):
        pipe._procesar(_frame(t))        # deberian continuar la cadencia de 33ms

    pipe.pause()
    for t in (231, 264):                 # ~66ms de segunda pausa, descartados
        pipe._procesar(_frame(t))
    pipe.resume()
    for t in (297, 330):
        pipe._procesar(_frame(t))        # deberian seguir exactamente donde iban

    # Con las dos pausas descontadas, la cadencia de 33ms nunca se interrumpe:
    # da igual cuanto haya durado cada pausa en tiempo real.
    assert espia.vistos == [0, 33, 66, 99, 132, 165], espia.vistos


def test_pausar_sin_sesion_activa_no_revienta():
    pipe, espia = _construir_pipeline()
    pipe.pause()   # nunca se proceso ningun cuadro: no debe fallar
    assert pipe.is_paused
    pipe.resume()
    assert not pipe.is_paused

