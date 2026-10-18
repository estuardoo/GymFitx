"""Feature 'proporcion': tramo de una cadena de kpoints / suma de tramos, x100.
Cubre las 3 reglas pedidas: la cadena necesita 3+ puntos, los tramos de una
misma cadena siempre suman 100, y 'activo: false' saca la feature del ejercicio
cargado (pipeline en vivo / entrenamiento) sin borrarla del .yaml.
"""

from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parent.parent

from src.nucleo.ejercicio import Exercise, load_exercise  # noqa: E402
from src.procesamiento.medidas.features import FeatureExtractor, compute_features  # noqa: E402

CADENA = ["LEFT_HIP", "LEFT_KNEE", "LEFT_ANKLE", "LEFT_FOOT_INDEX"]
FEATURES_PROPORCION = [
    {"name": "p1", "type": "proporcion", "points": ["LEFT_HIP", "LEFT_KNEE"], "cadena": CADENA},
    {"name": "p2", "type": "proporcion", "points": ["LEFT_KNEE", "LEFT_ANKLE"], "cadena": CADENA},
    {"name": "p3", "type": "proporcion", "points": ["LEFT_ANKLE", "LEFT_FOOT_INDEX"], "cadena": CADENA},
]


def _ejercicio(features):
    return Exercise(slug="t", name="t", source="pose", features=features, signal_features=[])


def test_los_tramos_de_una_cadena_suman_100():
    rng = np.random.default_rng(1)
    P = rng.normal(size=(33, 3)).astype(np.float32)
    ext = FeatureExtractor(_ejercicio(FEATURES_PROPORCION))
    vals = ext.from_points(P)
    assert abs(vals.sum() - 100.0) < 1e-3


def test_extractor_compilado_igual_al_escalar():
    rng = np.random.default_rng(2)
    P = rng.normal(size=(33, 3)).astype(np.float32)
    ex = _ejercicio(FEATURES_PROPORCION)
    ext = FeatureExtractor(ex)
    rapido = ext.from_points(P)
    lento = compute_features(P, ex.features, ex.source)
    for i, nombre in enumerate(ext.names):
        assert abs(rapido[i] - lento[nombre]) < 1e-3


def test_cadena_corta_revienta_al_cargar(tmp_path):
    yml = tmp_path / "x.yaml"
    yml.write_text(
        "name: x\nsource: pose\nfeatures:\n"
        "  - name: p1\n    type: proporcion\n    points: [LEFT_HIP, LEFT_KNEE]\n"
        "    cadena: [LEFT_HIP, LEFT_KNEE]\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="cadena"):
        load_exercise(yml)


def test_activo_false_no_entra_al_ejercicio_cargado(tmp_path):
    yml = tmp_path / "x.yaml"
    yml.write_text(
        "name: x\nsource: pose\nfeatures:\n"
        "  - name: p1\n    type: proporcion\n    points: [LEFT_HIP, LEFT_KNEE]\n"
        "    cadena: [LEFT_HIP, LEFT_KNEE, LEFT_ANKLE]\n    activo: false\n"
        "  - name: p2\n    type: proporcion\n    points: [LEFT_KNEE, LEFT_ANKLE]\n"
        "    cadena: [LEFT_HIP, LEFT_KNEE, LEFT_ANKLE]\n",
        encoding="utf-8",
    )
    ex = load_exercise(yml)
    assert ex.feature_names == ["p2"]   # p1 (activo:false) queda fuera
