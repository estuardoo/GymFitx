"""Kpoints de pose: resolucion, derivados y guardado del editor."""

import numpy as np
import pytest
import yaml

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
def ext(tmp_path):
    p = tmp_path / "pose.yaml"
    p.write_text(yaml.safe_dump(YAML), "utf-8")
    return FeatureExtractor(load_exercise(p))


def test_extractor_mide_el_angulo_con_nombres_de_kpoints(ext):
    fv = ext.extract([_pose()], 0)
    assert fv.values[0] == pytest.approx(90.0, abs=0.5)


def test_resolver_kpoints_y_derivado():
    valores, _ = KP.resolver(YAML["kpoints"], [_pose()])
    assert np.allclose(valores[2], (0.3, 0, 0))
    assert np.allclose(valores[3], (0.15, 0, 0))              # punto medio codo-muneca


def test_feature_con_kpoint_inexistente_no_carga(tmp_path):
    malo = {**YAML, "features": [{"name": "x", "type": "angle", "points": ["RIGHT_ELBOW", "nada", "RIGHT_WRIST"]}],
            "signal": {"features": ["x"]}}
    p = tmp_path / "malo.yaml"
    p.write_text(yaml.safe_dump(malo), "utf-8")
    with pytest.raises((ValueError, KeyError)):
        load_exercise(p)


def test_el_editor_no_guarda_un_ejercicio_que_no_carga(tmp_path, monkeypatch):
    from src.etiquetado import editor_puntos as EP
    monkeypatch.setattr(EP, "EJERCICIOS_DIR", tmp_path)
    monkeypatch.setattr(EP, "RESPALDOS_DIR", tmp_path / ".respaldos")
    p = tmp_path / "pose.yaml"
    p.write_text(yaml.safe_dump(YAML), "utf-8")
    antes = p.read_text("utf-8")
    # un source invalido rompe el yaml: no se guarda nada
    with pytest.raises(ValueError, match="no se guardo nada"):
        EP.guardar_ejercicio("pose", {"source": "nada", "kpoints": YAML["kpoints"], "features": YAML["features"]})
    assert p.read_text("utf-8") == antes
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


def test_guardar_descarta_signal_features_viejas(tmp_path, monkeypatch):
    import shutil

    from src.etiquetado import editor_puntos as ep
    ej = tmp_path / "ejercicios"
    ej.mkdir()
    shutil.copy(ep.EJERCICIOS_DIR / "cuerpo_completo.yaml", ej / "x.yaml")
    monkeypatch.setattr(ep, "EJERCICIOS_DIR", ej)
    monkeypatch.setattr(ep, "RESPALDOS_DIR", ej / ".r")
    kps = [{"numero": i, "nombre": n, "origen": {"tipo": "landmark", "fuente": "pose", "landmark": n}}
           for i, n in enumerate(["RIGHT_SHOULDER", "RIGHT_ELBOW", "RIGHT_WRIST"], 1)]
    a, b, c = (k["nombre"] for k in kps)
    ep.guardar_ejercicio("x", {"source": "pose", "kpoints": kps,
                              "features": [{"name": "a1", "type": "angle", "points": [a, b, c]}]})
    assert "features" not in (yaml.safe_load((ej / "x.yaml").read_text("utf-8")).get("signal") or {})


def test_exportar_acepta_todo():
    import inspect

    from src.etiquetado import exportar as X
    assert "todo" in inspect.signature(X.exportar).parameters


def test_eliminar_ejercicio_lo_archiva_y_ya_no_se_lista(tmp_path, monkeypatch):
    from src.etiquetado import editor_puntos as ep
    monkeypatch.setattr(ep, "EJERCICIOS_DIR", tmp_path)
    monkeypatch.setattr(ep, "RESPALDOS_DIR", tmp_path / ".respaldos")
    (tmp_path / "x.yaml").write_text(yaml.safe_dump(YAML), "utf-8")
    assert ep.listar_ejercicios() == ["x"]
    r = ep.eliminar_ejercicio("x")
    assert ep.listar_ejercicios() == []
    assert (tmp_path / ".respaldos" / r["respaldo"]).exists()
    with pytest.raises(ValueError):
        ep.eliminar_ejercicio("x")
