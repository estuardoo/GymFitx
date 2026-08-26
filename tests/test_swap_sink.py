"""Verifica que swap_sink() decople 'prender la camara' de 'grabar', sin
perder cuadros ni cruzar resultados entre el sumidero de antes y el de
despues. Mismo truco que test_pausa.py: mediapipe queda sustituido por un
doble minimo, no hace falta camara ni modelo real.

    python tests/test_swap_sink.py
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

    _PUNTOS = [(0.0, 0.0, 0.0)] + [(0.02 * i, 0.05 + 0.01 * (i % 5), 0.0) for i in range(20)]

    class _Landmark:
        def __init__(self, x, y, z):
            self.x, self.y, self.z = x, y, z

    class _Categoria:
        category_name = "Right"
        score = 0.95

    class _Resultado:
        hand_landmarks = [[_Landmark(*p) for p in _PUNTOS]]
        hand_world_landmarks = [[_Landmark(*p) for p in _PUNTOS]]
        handedness = [[_Categoria()]]

    class HandLandmarker:
        @classmethod
        def create_from_options(cls, options):
            return cls()

        def detect_for_video(self, image, timestamp_ms):
            return _Resultado()

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
from core.pipeline import Pipeline, Sink     # noqa: E402
from core.types import Frame                 # noqa: E402
import core.tracker as tracker_mod           # noqa: E402

# El stub no necesita un archivo de modelo real.
tracker_mod.ensure_model = lambda source: Path("stub.task")

EJ = load_exercise(ROOT / "exercises" / "mano_apertura.yaml")


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
