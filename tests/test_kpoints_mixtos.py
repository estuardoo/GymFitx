"""Kpoints de pose: resolucion, derivados y guardado del editor."""

import numpy as np
import pytest

from src.nucleo import definicion as DEF
from src.nucleo.ejercicio import load_exercise
from src.nucleo.landmarks import POSE_LANDMARKS
from src.nucleo.tipos import Landmarks
from src.procesamiento.medidas.features import FeatureExtractor
from src.procesamiento.puntos import kpoints as KP

YAML = {
    "name": "pose", "source": "pose",
    "features": [
        {"name": "codo", "type": "angle", "points": ["RIGHT_SHOULDER", "RIGHT_ELBOW", "RIGHT_WRIST"]},
    ],
    "signal": {"features": ["codo"]},
    "kpoints": [
        {"numero": 1, "nombre": "RIGHT_SHOULDER", "origen": {"tipo": "landmark", "fuente": "pose", "landmark": "RIGHT_SHOULDER"}},
        {"numero": 2, "nombre": "RIGHT_ELBOW", "origen": {"tipo": "landmark", "fuente": "pose", "landmark": "RIGHT_ELBOW"}},
        {"numero": 3, "nombre": "RIGHT_WRIST", "origen": {"tipo": "landmark", "fuente": "pose", "landmark": "RIGHT_WRIST"}},
        {"numero": 4, "nombre": "medio", "origen": {"tipo": "derivado", "de": [2, 3]}},
    ],
}


def _pose():
    w = np.zeros((33, 3), dtype=np.float32)
    w[POSE_LANDMARKS.index("RIGHT_SHOULDER")] = (0, -0.3, 0)
    w[POSE_LANDMARKS.index("RIGHT_ELBOW")] = (0, 0, 0)
    w[POSE_LANDMARKS.index("RIGHT_WRIST")] = (0.3, 0, 0)
    return Landmarks(source="pose", world=w, screen=w.copy())


@pytest.fixture
def ext():
    DEF.guardar("pose", YAML)
    return FeatureExtractor(load_exercise("pose"))


def test_extractor_mide_el_angulo_con_nombres_de_kpoints(ext):
    fv = ext.extract([_pose()], 0)
    assert fv.values[0] == pytest.approx(90.0, abs=0.5)


def test_resolver_kpoints_y_derivado():
    valores, _ = KP.resolver(YAML["kpoints"], [_pose()])
    assert np.allclose(valores[2], (0.3, 0, 0))
    assert np.allclose(valores[3], (0.15, 0, 0))              # punto medio codo-muneca


def test_feature_con_kpoint_inexistente_no_carga():
    malo = {**YAML, "features": [{"name": "x", "type": "angle", "points": ["RIGHT_ELBOW", "nada", "RIGHT_WRIST"]}],
            "signal": {"features": ["x"]}}
    DEF.guardar("malo", malo)
    with pytest.raises((ValueError, KeyError)):
        load_exercise("malo")


def test_el_editor_no_guarda_un_ejercicio_que_no_carga():
    from src.etiquetado import editor_puntos as EP
    DEF.guardar("pose", YAML)
    antes = DEF.leer("pose")
    # un source invalido rompe la definicion: no se guarda nada
    with pytest.raises(ValueError, match="no se guardo nada"):
        EP.guardar_ejercicio("pose", {"source": "nada", "kpoints": YAML["kpoints"], "features": YAML["features"]})
    assert DEF.leer("pose") == antes
    EP.guardar_ejercicio("pose", {"kpoints": YAML["kpoints"], "features": YAML["features"]})   # y uno valido si


def test_cabeza_grande_brazos_a_20_grados_y_pies_hacia_afuera():
    import math

    from src.etiquetado.editor_puntos import POSE_PUNTOS as P
    assert P["LEFT_EAR"][0] > 0.6 and P["NOSE"][1] > 1.0                          # cabeza mas ancha y separada del torso
    hombro, codo, muneca = P["LEFT_SHOULDER"], P["LEFT_ELBOW"], P["LEFT_WRIST"]
    apertura = math.degrees(math.atan2(codo[0] - hombro[0], hombro[1] - codo[1]))   # la figura mira al usuario: LEFT_ a la derecha   # respecto a la vertical del cuerpo
    assert abs(apertura) == pytest.approx(20, abs=1.5)
    assert muneca[1] > codo[1]                                                     # antebrazo hacia arriba (saludando)
    assert P["LEFT_FOOT_INDEX"][0] > P["LEFT_HEEL"][0] and P["RIGHT_FOOT_INDEX"][0] < P["RIGHT_HEEL"][0]   # puntas hacia afuera


def test_codigos_cuerpo_y_derivados():
    from src.etiquetado.editor_puntos import codigo_kpoint
    kps = [{"numero": 1, "nombre": "NOSE", "origen": {"tipo": "landmark", "fuente": "pose", "landmark": "NOSE"}},
           {"numero": 2, "nombre": "d", "origen": {"tipo": "derivado", "de": [1, 1]}}]
    assert [codigo_kpoint(k, kps) for k in kps] == ["C01", "D01"]


def test_vista_espejo_su_derecha_queda_a_la_izquierda():
    from src.etiquetado.editor_puntos import POSE_PUNTOS as P
    assert P["LEFT_SHOULDER"][0] > 0.5 > P["RIGHT_SHOULDER"][0]
    assert P["LEFT_WRIST"][0] > 0.5 > P["RIGHT_WRIST"][0]


def test_guardar_descarta_signal_features_viejas():
    from src.etiquetado import editor_puntos as ep
    DEF.guardar("x", DEF.leer("cuerpo_completo"))
    kps = [{"numero": i, "nombre": n, "origen": {"tipo": "landmark", "fuente": "pose", "landmark": n}}
           for i, n in enumerate(["RIGHT_SHOULDER", "RIGHT_ELBOW", "RIGHT_WRIST"], 1)]
    a, b, c = (k["nombre"] for k in kps)
    ep.guardar_ejercicio("x", {"source": "pose", "kpoints": kps,
                              "features": [{"name": "a1", "type": "angle", "points": [a, b, c]}]})
    assert "features" not in (DEF.leer("x").get("signal") or {})


def test_exportar_acepta_todo():
    import inspect

    from src.etiquetado import exportar as X
    assert "todo" in inspect.signature(X.exportar).parameters


def test_eliminar_ejercicio_lo_archiva_y_ya_no_se_lista():
    from src.etiquetado import editor_puntos as ep
    DEF.guardar("x", YAML)
    assert "x" in ep.listar_ejercicios()
    ep.eliminar_ejercicio("x")
    assert "x" not in ep.listar_ejercicios()
    DEF.guardar("x", YAML)                     # crearlo de nuevo lo reactiva con el mismo numero
    assert "x" in ep.listar_ejercicios()
    ep.eliminar_ejercicio("x")
    with pytest.raises(ValueError):
        ep.eliminar_ejercicio("x")
