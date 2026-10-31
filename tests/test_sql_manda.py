"""Pestana Kpoints: SQL manda; sin conexion se guarda en local y se sube cuando vuelve."""

import json

import pytest

from src.almacenamiento import dataset_sql as SQL
from src.etiquetado import editor_puntos as EP
from src.nucleo import definicion as DEF

YAML = {
    "name": "brazo", "source": "pose",
    "features": [{"name": "codo", "type": "angle", "points": ["RIGHT_SHOULDER", "RIGHT_ELBOW", "RIGHT_WRIST"]}],
    "signal": {"features": ["codo"]},
    "kpoints": [{"numero": i + 1, "nombre": n, "origen": {"tipo": "landmark", "fuente": "pose", "landmark": n}}
                for i, n in enumerate(["RIGHT_SHOULDER", "RIGHT_ELBOW", "RIGHT_WRIST"])],
}


class SqlFalso:
    """Reemplaza a SQL Server: un dict por type, y un interruptor de 'sin conexion'."""

    def __init__(self, monkeypatch):
        self.definiciones, self.arriba = {}, True
        m = monkeypatch
        m.setattr(SQL, "tipo_de_ejercicio", lambda e: 1)
        m.setattr(SQL, "asegurar_base_y_tablas", self._conectado)
        m.setattr(SQL, "leer_definicion", lambda t: (self._conectado(), self.definiciones.get(t))[1])
        m.setattr(SQL, "conexion", self._conexion)
        m.setattr(SQL, "guardar_definicion", lambda cx, t, e, d: self.definiciones.__setitem__(t, json.loads(json.dumps(d))))
        m.setattr(SQL, "guardar_catalogo", lambda *a: None)
        m.setattr(SQL, "guardar_features", lambda *a: None)

    def _conectado(self):
        if not self.arriba:
            raise SQL.SQLServerNoDisponible("sin servidor")

    def _conexion(self):
        self._conectado()

        class Cx:
            def __enter__(self): return self
            def __exit__(self, *a): return False
            def commit(self): pass
        return Cx()


@pytest.fixture
def sql(tmp_path, monkeypatch):
    monkeypatch.setattr(EP, "PENDIENTES_PATH", tmp_path / "pendientes.json")
    monkeypatch.setattr(EP, "_sql_caido_hasta", 0.0)
    DEF.guardar("brazo", YAML)
    return SqlFalso(monkeypatch)


def _guardar(features):
    EP.guardar_ejercicio("brazo", {"kpoints": YAML["kpoints"], "features": features})


def test_sql_sin_el_ejercicio_recibe_la_definicion(sql):
    assert EP.sincronizar("brazo")["estado"] == "enviado"
    assert sql.definiciones[1]["features"][0]["name"] == "codo"
    assert EP.sincronizar("brazo")["estado"] == "sincronizado"


def test_sin_conexion_queda_pendiente_y_se_sube_al_volver(sql):
    EP.sincronizar("brazo")
    sql.arriba = False
    nuevas = YAML["features"] + [{"name": "otro", "type": "angle", "points": ["RIGHT_ELBOW", "RIGHT_WRIST", "RIGHT_SHOULDER"]}]
    _guardar(nuevas)
    r = EP.subir("brazo")
    assert r["ok"] is False and r["pendiente"] is True
    assert "brazo" in EP._pendientes()
    assert len(sql.definiciones[1]["features"]) == 1            # SQL no se entero

    assert EP.sincronizar("brazo")["estado"] == "sin_conexion"   # sigue caido: no toca nada
    sql.arriba = True
    EP._sql_caido_hasta = 0.0
    assert EP.sincronizar("brazo")["estado"] == "enviado"        # vuelve: lo local es lo mas nuevo y se sube
    assert len(sql.definiciones[1]["features"]) == 2
    assert EP._pendientes() == {}


def test_si_sql_tiene_otra_version_se_aplica_a_la_local(sql):
    EP.sincronizar("brazo")
    otra = json.loads(json.dumps(sql.definiciones[1]))
    otra["features"].append({"name": "de_sql", "type": "angle", "points": ["RIGHT_ELBOW", "RIGHT_WRIST", "RIGHT_SHOULDER"]})
    sql.definiciones[1] = otra                                   # alguien mas guardo esto en SQL
    assert EP.sincronizar("brazo")["estado"] == "traido"
    assert [f["name"] for f in EP.leer_ejercicio("brazo")["features"]] == ["codo", "de_sql"]
    assert EP.sincronizar("brazo")["estado"] == "sincronizado"


def test_lo_de_sql_que_dejaria_la_definicion_rota_no_se_aplica(sql):
    EP.sincronizar("brazo")
    roto = json.loads(json.dumps(sql.definiciones[1]))
    roto["source"] = "nada"                                      # un source invalido deja la definicion rota
    sql.definiciones[1] = roto
    antes = DEF.leer("brazo")
    assert EP.sincronizar("brazo")["estado"] == "conflicto"
    assert DEF.leer("brazo") == antes


def test_reintentar_sube_los_pendientes(sql):
    sql.arriba = False
    EP.subir("brazo")
    sql.arriba = True
    EP._sql_caido_hasta = 0.0
    EP.reintentar()
    assert EP._pendientes() == {} and 1 in sql.definiciones
