"""Matriz de modelos (epocas / max_iter / parar) y las iteraciones usadas que se reportan al entrenar."""
import json

import numpy as np
import pytest
from sklearn.model_selection import StratifiedKFold

import src.nucleo.config as C
from src.entrenamiento import modelos as M
from src.entrenamiento import reportes as R
from src.entrenamiento import validacion as V


@pytest.fixture
def ajustes(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "CONFIG_PATH", tmp_path / "config.json")
    return tmp_path / "config.json"


def _datos():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(90, 6))
    return X, (X[:, 0] + rng.normal(scale=.5, size=90) > 0).astype(int)


def test_matriz_por_defecto_y_override(ajustes):
    assert C.matriz_modelos()["mlp"] == {"epocas": None, "max_iter": 2000, "parar": False, "paciencia": 10, "tol": 1e-4}
    assert len(C.matriz_modelos()) == 17 and set(C.matriz_modelos()["knn"].values()) == {None}   # todos los modelos, aunque no iteren
    C.guardar_matriz_modelos({"mlp": {"max_iter": 50}, "random_forest": {"epocas": 10}})
    assert json.loads(ajustes.read_text())["modelos"] == {"mlp": {"max_iter": 50}, "random_forest": {"epocas": 10}}
    nombres = dict(M.catalogo())
    assert nombres["random_forest"].n_estimators == 10 and nombres["mlp"][-1].max_iter == 50
    C.guardar_matriz_modelos({"mlp": {"max_iter": 2000}})   # volver al default borra la fila guardada
    assert "mlp" not in json.loads(ajustes.read_text())["modelos"]


@pytest.mark.parametrize("cambios", [{"mlp": {"epocas": 5}}, {"knn": {"max_iter": 5}}, {"mlp": {"max_iter": 0}},
                                     {"mlp": {"parar": 1}}, {"mlp": {"max_iter": True}}, {"mlp": {"tol": 0}},
                                     {"mlp": {"paciencia": 2.5}}, {"nuevo": {"max_iter": 3}}])
def test_matriz_rechaza_celdas_invalidas(ajustes, cambios):
    with pytest.raises(ValueError):
        C.guardar_matriz_modelos(cambios)
    assert not ajustes.exists()


def test_parar_aplica_early_stopping(ajustes):
    C.guardar_matriz_modelos({"mlp": {"parar": True, "paciencia": 4, "tol": 0.01}, "gradient_boosting": {"parar": True, "paciencia": 6},
                              "sgd_logistico": {"paciencia": 9}, "logistic": {"tol": 0.5}})
    c = dict(M.catalogo())
    mlp = c["mlp"][-1]
    assert mlp.early_stopping is True and mlp.n_iter_no_change == 4 and mlp.tol == 0.01
    assert c["gradient_boosting"].n_iter_no_change == 6
    assert c["sgd_logistico"][-1].n_iter_no_change == 9 and c["logistic"][-1].tol == 0.5
    assert dict(M.catalogo())["hist_gradient_boosting"].n_iter_no_change == 10   # defaults de sklearn intactos


def test_evaluar_reporta_iteraciones_usadas(ajustes):
    X, y = _datos()
    C.guardar_matriz_modelos({"mlp": {"max_iter": 2000, "parar": True}, "random_forest": {"epocas": 7}})
    skf = StratifiedKFold(3, shuffle=True, random_state=1)
    c = dict(M.catalogo())
    rf = V.evaluar("random_forest", c["random_forest"], X, y, skf)
    assert rf["iteraciones"] == {"tope": 7, "min": 7, "media": 7.0, "max": 7, "freno": False}
    mlp = V.evaluar("mlp", c["mlp"], X, y, skf)
    it = mlp["iteraciones"]
    assert it["tope"] == 2000 and it["freno"] and 1 <= it["min"] <= it["max"] < 2000
    assert "iteraciones" not in V.evaluar("knn", c["knn"], X, y, skf)        # no itera
    assert "iteraciones" not in V.evaluar("svm", c["svm"], X, y, skf)        # itera por dentro pero sin tope configurado
    assert V.evaluar("ridge", c["ridge"], X, y, skf)["_y_proba"] is None     # sin predict_proba


def test_matriz_log_y_cambios_entre_corridas():
    ms = [{"nombre": "mlp", "f1_macro": .9, "iteraciones": {"tope": 2000, "min": 80, "media": 90.0, "max": 100, "freno": True}},
          {"nombre": "knn", "f1_macro": .8}]
    txt = R.matriz_iteraciones(3, ms)
    assert "run_3" in txt and "mlp" in txt and "2000" in txt and "no itera" in txt
    a = {"matriz": {"mlp": {"epocas": None, "max_iter": 2000, "parar": False}}}
    b = {"matriz": {"mlp": {"epocas": None, "max_iter": 500, "parar": False}}}
    base = dict(frames=None, features=None, kpoints=None, angulos=None, modo=None, test_pct=None, clips=None)
    assert R._cambios({**base, **a}, {**base, **b}) == ["mlp.max_iter 2000→500"]


def test_endpoints_matriz(ajustes):
    from fastapi.testclient import TestClient

    from src.interfaz.app import app
    c = TestClient(app)
    assert c.get("/api/modelos/matriz").json()["mlp"]["max_iter"] == 2000
    assert c.post("/api/modelos/matriz", json={"cambios": {"mlp": {"max_iter": 300}}}).json()["mlp"]["max_iter"] == 300
    assert c.post("/api/modelos/matriz", json={"cambios": {"knn": {"max_iter": 3}}}).status_code == 400
    assert c.post("/api/modelos/matriz", json={"cambios": {"mlp": {"tol": "x"}}}).status_code == 400
