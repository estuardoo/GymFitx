"""Verifica la conexion unica src/almacenamiento/sqlserver.py SIN un SQL Server real: que la
ausencia del driver o del servidor se reporte con claridad (SQLServerNoDisponible
o estado() con conectado=False) en vez de reventar.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

from src.almacenamiento import sqlserver  # noqa: E402
from src.nucleo import config


def test_host_por_pc_y_variable_de_entorno():
    assert config.SERVIDORES_POR_PC["HYPERCUBE"] == r"HYPERCUBE\SERVER"
    assert config.SQLSERVER_DB


def test_estado_sin_driver_no_revienta():
    if sqlserver.pyodbc is not None:
        return  # con driver instalado (otra maquina) este test no aplica
    r = sqlserver.estado(("reps", "table_file"))
    assert r["conectado"] is False
    assert r["tablas_faltantes"] == ["reps", "table_file"]
    assert "pyodbc" in r["error"]


def test_operaciones_sin_driver_dan_sqlservernodisponible():
    if sqlserver.pyodbc is not None:
        return
    for fn in (sqlserver.asegurar_base, sqlserver.tablas_existentes, lambda: sqlserver.conectar()):
        try:
            fn()
            raise AssertionError("deberia haber lanzado SQLServerNoDisponible")
        except sqlserver.SQLServerNoDisponible:
            pass


def test_dataset_y_storage_usan_la_misma_conexion():
    from src.almacenamiento import dataset_sql as dataset_sql
    from src.almacenamiento import historial as storage
    assert storage.SQLServerNoDisponible is sqlserver.SQLServerNoDisponible
    assert dataset_sql.SQLServerNoDisponible is sqlserver.SQLServerNoDisponible
    assert dataset_sql.SQLSERVER_HOST == config.SQLSERVER_HOST



def test_servidor_elegido_en_sistema_se_guarda_en_config_json_y_se_lee_al_arrancar(tmp_path, monkeypatch):
    import importlib
    import json
    monkeypatch.setattr(config, "CONFIG_PATH", tmp_path / "config.json")
    host0, base0 = config.SQLSERVER_HOST, config.SQLSERVER_DB
    try:
        config.guardar_servidor_sql(" OTRAPC\\SQL ", "Pruebas")
        assert json.loads((tmp_path / "config.json").read_text("utf-8")) == {"sqlserver_host": "OTRAPC\\SQL",
                                                                            "sqlserver_db": "Pruebas"}
        assert sqlserver.estado()["host"] == "OTRAPC\\SQL"           # se aplica sin reiniciar
        monkeypatch.setenv("GYMFITX_DATOS", str(tmp_path))            # al arrancar, config.json manda
        assert importlib.reload(config).SQLSERVER_HOST == "OTRAPC\\SQL"
    finally:
        monkeypatch.delenv("GYMFITX_DATOS")
        importlib.reload(config)
        config.SQLSERVER_HOST, config.SQLSERVER_DB = host0, base0
