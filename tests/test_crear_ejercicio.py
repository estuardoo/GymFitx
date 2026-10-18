"""crear_ejercicio (src/etiquetado/editor_puntos.py): antes guardar_ejercicio solo podia EDITAR un
.yaml que ya existiera -- esto arma uno nuevo desde cero, sus carpetas y lo sube a SQL ya mismo."""
import json

import pytest

from src.almacenamiento import dataset_sql as SQL
from src.etiquetado import editor_puntos as EP


class SqlFalso:
    def __init__(self, monkeypatch):
        self.definiciones = {}
        m = monkeypatch
        m.setattr(SQL, "tipo_de_ejercicio", lambda e: 7)
        m.setattr(SQL, "asegurar_base_y_tablas", lambda: None)
        m.setattr(SQL, "guardar_definicion", lambda cx, t, e, d: self.definiciones.__setitem__(t, json.loads(json.dumps(d))))
        m.setattr(SQL, "guardar_catalogo", lambda *a: None)
        m.setattr(SQL, "guardar_features", lambda *a: None)

        class Cx:
            def __enter__(self): return self
            def __exit__(self, *a): return False
            def commit(self): pass
        m.setattr(SQL, "conexion", lambda: Cx())


@pytest.fixture
def entorno(tmp_path, monkeypatch):
    monkeypatch.setattr(EP, "EJERCICIOS_DIR", tmp_path / "ejercicios")
    monkeypatch.setattr(EP, "RESPALDOS_DIR", tmp_path / "ejercicios" / ".respaldos")
    monkeypatch.setattr(EP, "PENDIENTES_PATH", tmp_path / "pendientes.json")
    monkeypatch.setattr(EP, "_sql_caido_hasta", 0.0)
    clips, grabaciones = tmp_path / "clips", tmp_path / "grabaciones"
    import src.nucleo.config as CFGMOD
    monkeypatch.setattr(CFGMOD, "CLIPS_DIR", clips)
    monkeypatch.setattr(CFGMOD, "RECORDINGS_DIR", grabaciones)
    sql = SqlFalso(monkeypatch)
    return clips, grabaciones, sql


def test_crea_yaml_carpetas_y_sube_a_sql(entorno):
    clips, grabaciones, sql = entorno
    r = EP.crear_ejercicio("sentadilla_nueva")

    assert r["ok"] is True and r["sql"]["ok"] is True and r["sql"]["type"] == 7
    assert EP.leer_ejercicio("sentadilla_nueva") == {
        "name": "sentadilla_nueva", "description": "", "source": "pose",
        "features": [], "kpoints": [], "reglas": []}
    for clase in ("bien", "mal", "base"):
        assert (clips / "sentadilla_nueva" / clase).is_dir()
    assert not (clips / "sentadilla_nueva" / "descarte").exists()   # esa clase no se exporta
    assert (grabaciones / "sentadilla_nueva").is_dir()
    assert 7 in sql.definiciones


def test_nombre_invalido_no_crea_nada(entorno):
    with pytest.raises(ValueError):
        EP.crear_ejercicio("Con Espacios")
    with pytest.raises(ValueError):
        EP.crear_ejercicio("")


def test_no_pisa_un_ejercicio_que_ya_existe(entorno):
    EP.crear_ejercicio("sentadilla_nueva")
    with pytest.raises(ValueError):
        EP.crear_ejercicio("sentadilla_nueva")


def test_modificar_basicos_respalda_y_no_toca_el_slug(entorno, tmp_path):
    EP.crear_ejercicio("sentadilla_nueva")
    r = EP.modificar_ejercicio("sentadilla_nueva", {
        "name": "Sentadilla", "description": "baja y sube", "direction": "up_down",
        "min_duration_ms": "500", "max_duration_ms": 4000})
    assert r == {"ok": True, "base_invalida": False}   # sin plantilla grabada
    from src.nucleo.ejercicio import load_exercise
    ex = load_exercise(tmp_path / "ejercicios" / "sentadilla_nueva.yaml")
    assert (ex.slug, ex.name, ex.direction, ex.min_duration_ms, ex.max_duration_ms) == \
        ("sentadilla_nueva", "Sentadilla", "up_down", 500, 4000)
    assert (tmp_path / "ejercicios" / ".respaldos" / "sentadilla_nueva.yaml").exists()


def test_modificar_invalido_no_escribe(entorno, tmp_path):
    EP.crear_ejercicio("sentadilla_nueva")
    for malo in ({"direction": "lado"}, {"min_duration_ms": 5000, "max_duration_ms": 1000}, {"name": " "}):
        with pytest.raises(ValueError):
            EP.modificar_ejercicio("sentadilla_nueva", malo)
    assert EP.leer_ejercicio("sentadilla_nueva")["name"] == "sentadilla_nueva"
    with pytest.raises(ValueError):
        EP.modificar_ejercicio("no_existe", {"name": "x"})


def test_modificar_avisa_si_la_base_ya_existe(entorno, tmp_path, monkeypatch):
    import src.nucleo.config as CFGMOD
    monkeypatch.setattr(CFGMOD, "TEMPLATES_DIR", tmp_path / "plantillas")
    (tmp_path / "plantillas").mkdir()
    (tmp_path / "plantillas" / "sentadilla_nueva.npz").write_bytes(b"x")
    EP.crear_ejercicio("sentadilla_nueva")
    assert EP.modificar_ejercicio("sentadilla_nueva", {"name": "Otro"})["base_invalida"] is False
    assert EP.modificar_ejercicio("sentadilla_nueva", {"direction": "up_down"})["base_invalida"] is True


def test_figura_png_del_diagrama_de_kpoints():
    from src.interfaz.api import etiquetado
    png = etiquetado._figura_png()
    assert png[:8] == b"\x89PNG\r\n\x1a\n" and len(png) > 5000
