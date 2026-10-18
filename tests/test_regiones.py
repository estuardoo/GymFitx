"""Verifica el selector de regiones del cuerpo: el mapeo nombre->indices y
que el filtro realmente reduce lo que se dibuja en el overlay.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent

from src.nucleo.landmarks import POSE_LANDMARKS, region_indices  # noqa: E402
from src.nucleo.tipos import Landmarks  # noqa: E402
from src.sesion.overlay import GROSOR_HUESO, GROSOR_PIERNA, draw_landmarks, grosor_hueso  # noqa: E402


def _pose_landmarks_falsos() -> Landmarks:
    n = len(POSE_LANDMARKS)
    # Puntos repartidos en la imagen (no todos en el mismo pixel) para que
    # contar pixeles distintos de negro sea una medida valida de "cuantos
    # puntos se dibujaron".
    screen = np.array(
        [[0.05 + 0.9 * (i / n), 0.5, 0.0] for i in range(n)], dtype=np.float32
    )
    return Landmarks(source="pose", world=screen.copy(), screen=screen, label="", score=1.0)


def test_sin_filtro_devuelve_none():
    assert region_indices(None) is None


def test_una_region_devuelve_solo_sus_indices():
    # Cadera son exactamente LEFT_HIP y RIGHT_HIP.
    idx = region_indices(["cadera"])
    nombres = {POSE_LANDMARKS[i] for i in idx}
    assert nombres == {"LEFT_HIP", "RIGHT_HIP"}


def test_lista_vacia_no_incluye_nada():
    assert region_indices([]) == set()


def test_todas_las_regiones_juntas_cubren_los_33_puntos():
    todas = ["cabeza", "manos", "brazos", "torso", "cadera", "piernas", "pies"]
    idx = region_indices(todas)
    assert idx == set(range(len(POSE_LANDMARKS)))


def test_region_desconocida_no_revienta_y_no_aporta_nada():
    assert region_indices(["region_que_no_existe"]) == set()


def test_filtrar_por_region_dibuja_menos_pixeles_que_sin_filtro():
    lms = _pose_landmarks_falsos()
    frame_completo = np.zeros((200, 400, 3), dtype=np.uint8)
    draw_landmarks(frame_completo, lms, visibles=None)

    frame_filtrado = np.zeros((200, 400, 3), dtype=np.uint8)
    draw_landmarks(frame_filtrado, lms, visibles=region_indices(["cadera"]))

    pintados_completo = int(np.count_nonzero(frame_completo.sum(axis=2)))
    pintados_filtrado = int(np.count_nonzero(frame_filtrado.sum(axis=2)))
    assert pintados_filtrado > 0, "cadera si tiene puntos, algo debe dibujarse"
    assert pintados_filtrado < pintados_completo


def test_lista_vacia_no_dibuja_nada():
    lms = _pose_landmarks_falsos()
    frame = np.zeros((200, 400, 3), dtype=np.uint8)
    draw_landmarks(frame, lms, visibles=set())
    assert int(np.count_nonzero(frame.sum(axis=2))) == 0


def test_piernas_se_dibujan_mas_gruesas_que_el_resto_en_el_video():
    cadera = POSE_LANDMARKS.index("LEFT_HIP")
    rodilla = POSE_LANDMARKS.index("LEFT_KNEE")
    hombro = POSE_LANDMARKS.index("LEFT_SHOULDER")
    codo = POSE_LANDMARKS.index("LEFT_ELBOW")
    assert grosor_hueso(cadera, rodilla, "pose") == GROSOR_PIERNA
    assert grosor_hueso(hombro, codo, "pose") == GROSOR_HUESO


def test_pipeline_set_fps_delega_en_la_fuente_si_sabe_hacerlo():
    import test_swap_sink
    test_swap_sink._instalar_stub_mediapipe()
    from test_swap_sink import EJ

    from src.sesion.pipeline import Pipeline
    from src.sesion.sumideros import Sink

    class FuenteConFps:
        def set_fps(self, fps):
            self.pedido = fps
            return True

    class FuenteSinFps:
        pass

    pipe_con = Pipeline(EJ, source=FuenteConFps(), sink=Sink(), template=None, annotate=False)
    assert pipe_con.set_fps(60) is True
    assert pipe_con.source.pedido == 60

    pipe_sin = Pipeline(EJ, source=FuenteSinFps(), sink=Sink(), template=None, annotate=False)
    assert pipe_sin.set_fps(60) is False
