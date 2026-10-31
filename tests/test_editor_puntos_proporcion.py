"""guardar_ejercicio/leer_ejercicio con el nuevo tipo 'proporcion' y el flag
'activo': round-trip completo del editor de Puntos, sin tocar parameters/ real (los tests usan una carpeta temporal)."""

import pytest

import src.etiquetado.editor_puntos as EP
from src.nucleo import definicion as DEF
from src.nucleo.ejercicio import load_exercise

CADENA = ["LEFT_HIP", "LEFT_KNEE", "LEFT_ANKLE"]


@pytest.fixture(autouse=True)
def _ejercicio():
    DEF.guardar("cadera", {"name": "cadera", "source": "pose", "features": []})


def test_guarda_angulo_y_proporcion_de_una_misma_cadena_y_los_relee():
    EP.guardar_ejercicio("cadera", {
        "features": [
            {"name": "rodilla", "type": "angle", "points": CADENA},
            {"name": "rodilla_p1", "type": "proporcion", "points": CADENA[:2], "cadena": CADENA},
            {"name": "rodilla_p2", "type": "proporcion", "points": CADENA[1:], "cadena": CADENA,
             "activo": False},
        ],
    })
    datos = EP.leer_ejercicio("cadera")
    nombres = {f["name"]: f for f in datos["features"]}
    assert set(nombres) == {"rodilla", "rodilla_p1", "rodilla_p2"}
    assert nombres["rodilla_p2"]["activo"] is False
    assert "activo" not in nombres["rodilla_p1"]   # activo:true no se escribe, es el default


def test_activo_false_sobrevive_pero_no_entra_al_ejercicio_en_vivo():
    EP.guardar_ejercicio("cadera", {
        "features": [
            {"name": "rodilla_p1", "type": "proporcion", "points": CADENA[:2], "cadena": CADENA,
             "activo": False},
            {"name": "rodilla_p2", "type": "proporcion", "points": CADENA[1:], "cadena": CADENA},
        ],
    })
    ex = load_exercise("cadera")
    assert ex.feature_names == ["rodilla_p2"]


def test_proporcion_sin_cadena_valida_revienta():
    with pytest.raises(ValueError, match="cadena"):
        EP.guardar_ejercicio("cadera", {
            "features": [{"name": "x", "type": "proporcion", "points": ["LEFT_HIP", "LEFT_KNEE"]}],
        })


def test_points_no_consecutivo_en_la_cadena_revienta():
    with pytest.raises(ValueError, match="consecutivo"):
        EP.guardar_ejercicio("cadera", {
            "features": [{"name": "x", "type": "proporcion",
                          "points": ["LEFT_HIP", "LEFT_ANKLE"], "cadena": CADENA}],
        })
