"""Verifica la aritmetica de pausa del Pipeline, sin camara ni MediaPipe real.

Esta es la unica prueba del proyecto que importa core.pipeline (las demas
evitan a proposito el modulo que carga mediapipe). Para poder correr sin la
libreria instalada -y sin descargar el modelo- se sustituye 'mediapipe' en
sys.modules por un doble minimo antes de importar: el HandLandmarker del
doble ignora el modelo y siempre devuelve una mano con landmarks fijos, que
es todo lo que este test necesita para verificar que los TIEMPOS se ajustan
bien alrededor de una pausa.

    python tests/test_pausa.py
"""

from __future__ import annotations

import sys
import types
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def _instalar_stub_mediapipe() -> None:
    """Un mediapipe falso: basta para que core.tracker importe y funcione."""
    if "mediapipe" in sys.modules and getattr(sys.modules["mediapipe"], "_ES_STUB", False):
        return  # ya instalado por una corrida anterior en el mismo proceso

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

    # 21 puntos fijos con forma de mano semiabierta, en el orden de HAND_LANDMARKS.
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
    vision.PoseLandmarker = HandLandmarker  # no se usa en este test, basta con que exista

    tasks_python.vision = vision
    tasks.python = tasks_python
    mp.tasks = tasks

    sys.modules["mediapipe"] = mp
    sys.modules["mediapipe.tasks"] = tasks
    sys.modules["mediapipe.tasks.python"] = tasks_python
    sys.modules["mediapipe.tasks.python.vision"] = vision


_instalar_stub_mediapipe()

from core.exercise import load_exercise      # noqa: E402
from core.pipeline import Pipeline, Sink      # noqa: E402
from core.tracker import ensure_model         # noqa: E402
from core.types import Frame                  # noqa: E402
import core.tracker as tracker_mod            # noqa: E402

# El stub no necesita un archivo de modelo real; evita que ensure_model()
# intente descargarlo o toque la carpeta models/ real del proyecto.
tracker_mod.ensure_model = lambda source: Path("stub.task")

EJ = load_exercise(ROOT / "exercises" / "mano_apertura.yaml")


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
