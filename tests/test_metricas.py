"""Metricas del ejercicio: angulos y proporciones activados, crudas y normalizadas; progreso del corte."""
import numpy as np
import pytest

from src.procesamiento.medidas import features as F
from src.procesamiento.puntos import vectorizar as V

NOMBRES = ["a", "b", "c"]
FEATS = [
    {"name": "ang", "type": "angle", "points": ["a", "b", "c"]},
    {"name": "pro", "type": "proporcion", "points": ["a", "b"], "cadena": ["a", "b", "c"]},
    {"name": "apagada", "type": "angle", "points": ["a", "b", "c"], "activo": False},
    {"name": "sin_punto", "type": "angle", "points": ["a", "b", "z"]},
]


def _pts(T=6):
    p = np.zeros((T, 3, 3), dtype=np.float32)
    p[:, 0] = (0, 1, 0)     # a
    p[:, 1] = (0, 0, 0)     # b (vertice)
    p[:, 2] = (3, 0, 0)     # c  -> angulo 90, tramo a-b = 1 de 4 = 25 %
    return p


def test_solo_mide_los_activos_y_medibles():
    v, nombres, tipos = F.medir_clip(_pts(), NOMBRES, FEATS)
    assert nombres == ["ang", "pro"] and tipos == ["angle", "proporcion"]
    assert v[0] == pytest.approx([90.0, 25.0])


def test_normalizada_0_a_1_por_tipo():
    n = F.normalizar_metricas(np.array([[90.0, 25.0, 8.0]]), ["angle", "proporcion", "distance_ratio"])
    assert n[0] == pytest.approx([0.5, 0.25, 1.0])      # razon recortada a 4 -> 1


def test_vector_usa_la_misma_definicion_que_el_entrenamiento():
    cfg = {"n_frames_fijo": 4}
    spec = {"point_names": NOMBRES, "kpoints": [], "cfg": cfg, "features": "angulos", "features_def": FEATS}
    vec = V.vector_de_clip(_pts(), NOMBRES, spec)
    assert vec.shape == (4 * 2,) and vec[:2] == pytest.approx([0.5, 0.25])
    sin = V.vector_de_clip(_pts(), NOMBRES, {**spec, "features_def": [FEATS[0]]})
    assert sin.shape == (4,)                              # cambia el conjunto de filas activas, cambia el vector


def test_progreso_cuenta_videos_no_cortes(monkeypatch):
    from src.etiquetado import exportar as X
    monkeypatch.setattr(X, "_ruta_video", lambda v: type("R", (), {"exists": lambda s: True})())
    labels = {"v1": {"segmentos": [{"clase": "bien"}, {"clase": "mal"}]}, "v2": {"segmentos": [{"clase": "bien"}]},
              "v3": {"segmentos": [{}]}}
    assert X._videos_a_cortar(labels) == ["v1", "v2"]     # 3 cortes pero 2 videos


@pytest.mark.parametrize("usar,largo", [("xyzap", 4 * (9 + 2)), ("xyz", 4 * 9), ("x", 4 * 3), ("xz", 4 * 6),
                                        ("a", 4), ("p", 4), ("ap", 8), ("ambos", 4 * 11), ("puntos", 4 * 9), ("angulos", 8)])
def test_el_vector_solo_lleva_lo_activado(usar, largo):
    spec = {"point_names": NOMBRES, "kpoints": [], "cfg": {"n_frames_fijo": 4}, "features": usar, "features_def": FEAT_OK}
    assert V.vector_de_clip(_pts(), NOMBRES, spec).shape == (largo,)


FEAT_OK = FEATS[:2]


def test_metricas_por_tipo():
    spec = {"point_names": NOMBRES, "kpoints": [], "cfg": {"n_frames_fijo": 4}, "features_def": FEAT_OK}
    assert V.vector_de_clip(_pts(), NOMBRES, {**spec, "features": "a"})[0] == pytest.approx(0.5)     # el angulo
    assert V.vector_de_clip(_pts(), NOMBRES, {**spec, "features": "p"})[0] == pytest.approx(0.25)    # la proporcion


def test_features_con_nombres_crudos_se_traducen_a_kpoints():
    from src.nucleo.ejercicio import resolver_features
    kps = [{"numero": i, "nombre": f"{lm.lower()}_{i}", "origen": {"tipo": "landmark", "fuente": "pose", "landmark": lm}}
           for i, lm in enumerate(["RIGHT_SHOULDER", "RIGHT_ELBOW", "RIGHT_WRIST"], 1)]
    f = [{"name": "a", "type": "angle", "points": ["RIGHT_SHOULDER", "RIGHT_ELBOW", "RIGHT_WRIST"]}]
    assert resolver_features(f, kps)[0]["points"] == ["right_shoulder_1", "right_elbow_2", "right_wrist_3"]
    assert resolver_features(f, []) == f                                                 # sin catalogo, tal cual
