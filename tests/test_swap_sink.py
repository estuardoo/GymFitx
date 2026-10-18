"""Verifica que swap_sink() decople 'prender la camara' de 'grabar', sin
perder cuadros ni cruzar resultados entre el sumidero de antes y el de
despues. Mismo truco que test_pausa.py: mediapipe queda sustituido por un
doble minimo, no hace falta camara ni modelo real.
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

# El stub no necesita un archivo de modelo real.
tracker_mod.ensure_model = lambda source: Path("stub.task")

EJ = load_exercise(ROOT / "ejercicios" / "manguito_rotador.yaml")


class _EspiaSink(Sink):
    """Registra que cuadros le llegaron y si lo cerraron, sin tocar disco."""

    def __init__(self):
        self.iniciado = False
        self.cerrado = False
        self.vistos: list[int] = []

    def on_start(self, pipe):
        self.iniciado = True

    def on_frame(self, pipe, frame, fv):
        self.vistos.append(frame.t_ms)

    def on_stop(self, pipe):
        self.cerrado = True


class _SinkQueRevienta(Sink):
    """Simula un sumidero que falla al cerrar (disco lleno, ffmpeg, etc)."""

    def on_stop(self, pipe):
        raise RuntimeError("disco lleno")


def _frame(t_ms: int) -> Frame:
    img = np.zeros((60, 80, 3), dtype=np.uint8)
    return Frame(image=img, t_ms=t_ms, index=0)


def test_los_cuadros_van_al_sumidero_activo_en_cada_momento():
    """El corazon de la funcionalidad: 'prender camara' (preview) y 'grabar'
    corren el MISMO pipeline; solo cambia adonde van los cuadros."""
    preview = _EspiaSink()
    pipe = Pipeline(EJ, source=None, sink=preview, template=None, annotate=False)

    pipe._procesar(_frame(0))
    pipe._procesar(_frame(33))
    assert preview.vistos == [0, 33]

    grabacion = _EspiaSink()
    anterior = pipe.swap_sink(grabacion)
    assert anterior is preview
    assert preview.cerrado, "el sumidero de preview debe cerrarse al reemplazarlo"
    assert grabacion.iniciado, "el sumidero nuevo debe arrancar al instalarse"

    pipe._procesar(_frame(66))
    pipe._procesar(_frame(99))

    # La preview no debe recibir nada mas; la grabacion solo lo de despues del swap.
    assert preview.vistos == [0, 33]
    assert grabacion.vistos == [66, 99]


def test_detener_grabacion_vuelve_a_un_sumidero_neutro_sin_perder_cuadros():
    """'Detener' (sin apagar la camara) vuelve a un Sink() nulo y sigue
    procesando cuadros sin errores ni fugas hacia el sumidero ya cerrado."""
    pipe = Pipeline(EJ, source=None, sink=Sink(), template=None, annotate=False)
    grabacion = _EspiaSink()
    pipe.swap_sink(grabacion)
    pipe._procesar(_frame(0))

    anterior = pipe.swap_sink(Sink())
    assert anterior is grabacion
    assert grabacion.cerrado

    pipe._procesar(_frame(33))  # no debe fallar, y no debe llegar a 'grabacion'
    assert grabacion.vistos == [0]


def test_swap_sink_no_se_traba_si_el_sumidero_anterior_revienta_al_cerrar():
    """Si el sumidero viejo revienta en on_stop (disco lleno, ffmpeg, lo que
    sea), el swap al sumidero nuevo tiene que pasar igual -- si no, "detener
    grabacion" queda trabado sin avisar nada: el gesto/boton dispara el swap
    desde el bus, que traga cualquier excepcion de quien escucha, asi que sin
    esta proteccion el fallo desaparece en silencio y el video sigue grabando.
    """
    eventos = []
    pipe = Pipeline(EJ, source=None, sink=_SinkQueRevienta(), template=None, annotate=False)
    pipe.bus.subscribe(eventos.append)

    nuevo = _EspiaSink()
    anterior = pipe.swap_sink(nuevo)

    assert anterior.__class__ is _SinkQueRevienta
    assert pipe.sink is nuevo, "el swap debe completarse aunque el sumidero anterior falle al cerrar"
    assert nuevo.iniciado
    assert any(e.get("type") == "error" for e in eventos), "el fallo debe avisarse, no perderse"

