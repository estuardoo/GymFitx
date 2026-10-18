"""Verifica src/evaluacion/esquemas.py: agrupar esquemas y armar la tabla comparativa.
No toca video ni camara -- son funciones puras sobre listas de puntajes.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

from src.evaluacion.esquemas import esquemas_de, grupo_de, tabla_comparacion  # noqa: E402


def test_grupo_de_separa_por_doble_guion_bajo():
    assert grupo_de("manguito_rotador") == "manguito_rotador"
    assert grupo_de("manguito_rotador__hombro") == "manguito_rotador"
    assert grupo_de("manguito_rotador__solo_codo") == "manguito_rotador"


def test_esquemas_de_filtra_y_ordena_por_slug():
    ejercicios = {
        "manguito_rotador__b": "B", "manguito_rotador": "A",
        "mano_apertura": "otro", "manguito_rotador__c": "C",
    }
    out = esquemas_de("manguito_rotador", ejercicios)
    assert list(out) == ["manguito_rotador", "manguito_rotador__b", "manguito_rotador__c"]
    assert "mano_apertura" not in out


def test_esquemas_de_sin_coincidencias_da_vacio():
    assert esquemas_de("no_existe", {"algo": "x"}) == {}


def test_tabla_comparacion_promedia_y_correlaciona():
    resultados = {
        ("esq_a", "dtw_biomec"): [90.0, 80.0, 70.0],
        ("esq_a", "angulos_directo"): [88.0, 79.0, 69.0],   # casi identico -> correlacion alta
        ("esq_b", "dtw_biomec"): [95.0, 60.0, 85.0],         # sin relacion -> correlacion baja
    }
    t = tabla_comparacion(resultados)
    assert t["filas"][("esq_a", "dtw_biomec")]["promedio"] == 80.0
    assert t["filas"][("esq_a", "dtw_biomec")]["n"] == 3
    r_alta = t["correlacion"]["('esq_a', 'dtw_biomec') ~ ('esq_a', 'angulos_directo')"]
    assert r_alta > 0.99


def test_tabla_comparacion_con_una_sola_columna_no_correlaciona():
    t = tabla_comparacion({("solo", "dtw_biomec"): [50.0, 60.0]})
    assert t["correlacion"] == {}


def test_tabla_comparacion_con_lista_vacia_no_revienta():
    t = tabla_comparacion({("x", "dtw_biomec"): []})
    assert t["filas"][("x", "dtw_biomec")]["promedio"] is None

