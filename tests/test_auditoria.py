"""Cambios de la auditoria (H1 lote SQL, H2 cuerpos tipados, H4 avisos, H8 servidores): cada uno con su prueba."""

import logging

import numpy as np
from fastapi.testclient import TestClient

from src.almacenamiento import dataset_sql as SQL
from src.etiquetado import cortes as CORTES
from src.interfaz.app import app

client = TestClient(app)


class _Cursor:
    def __init__(self):
        self.llamadas, self.fast_executemany = [], False

    def executemany(self, sql, filas):
        self.llamadas.append((sql, list(filas)))

    def close(self):
        pass


class _Conexion:
    def __init__(self):
        self.cur, self.execute_llamadas = _Cursor(), 0

    def cursor(self):
        return self.cur

    def execute(self, *_):
        self.execute_llamadas += 1


def test_insertar_frames_un_lote_no_un_insert_por_cuadro():
    cx = _Conexion()
    pts = [np.arange(99, dtype=float).reshape(33, 3) + i for i in range(5)]
    ang = [np.array([1.0, 2.0]) for _ in range(5)]
    SQL.insertar_frames(cx, "table_frames", "zancada", 7, pts, ang)
    assert cx.execute_llamadas == 0 and len(cx.cur.llamadas) == 1
    sql, filas = cx.cur.llamadas[0]
    assert "INSERT INTO table_frames " in sql and len(filas) == 5 and cx.cur.fast_executemany
    assert filas[0][:3] == ("zancada", 7, 1) and len(filas[0]) == 7
    assert filas[0][3:6] == SQL._ejes_str(pts[0])
    assert filas[0][6] == SQL._angulos_str(ang[0])


def test_insertar_frames_sin_cuadros_no_toca_sql():
    cx = _Conexion()
    SQL.insertar_frames(cx, "table_frames_fix", "zancada", 1, [], [])
    assert cx.cur.llamadas == [] and cx.execute_llamadas == 0


def test_json_corrupto_no_tumba_el_listado_y_avisa(caplog):
    from src.nucleo import inputs as INP
    with INP.editar() as t:
        raw = INP.registrar_raw(t, "zancada")
    INP.ruta_raw(raw["ej"], raw["id"], "mp4").write_bytes(b"x")
    INP.ruta_raw(raw["ej"], raw["id"], "json").write_text("{no es json", encoding="utf-8")
    with caplog.at_level(logging.WARNING):
        out = CORTES.videos()
    assert len(out) == 1 and out[0]["id"] == raw["id"]
    assert f"{raw['id']:06d}.json" in caplog.text


def test_entrenar_tipo_malo_da_422_no_500():
    assert client.post("/api/entrenar", json={"test_pct": "no-es-numero"}).status_code == 422


def test_puntos_crear_nombre_no_texto_da_422():
    assert client.post("/api/puntos/crear", json={"nombre": ["x"]}).status_code == 422


def test_archivados_depurar_slugs_no_lista_da_422():
    assert client.post("/api/archivados/depurar", json={"slugs": "uno"}).status_code == 422


def test_ahpc_exportar_ejercicios_no_lista_da_422():
    assert client.post("/api/ahpc/exportar", json={"ejercicios": "zancada"}).status_code == 422


def test_servidor_de_fabrica_sigue_y_config_puede_ampliarlo(monkeypatch):
    from src.nucleo import config as C
    assert C.SERVIDORES_POR_PC["HYPERCUBE"] == r"HYPERCUBE\SERVER"
    monkeypatch.setitem(C._AJUSTES, "servidores_por_pc", {"NUEVA": r"NUEVA\INST"})
    assert {**C.SERVIDORES_POR_PC, **C._AJUSTES["servidores_por_pc"]}["NUEVA"] == r"NUEVA\INST"
