"""El disco manda; SQL es respaldo: interruptores (config.json), nunca romper el flujo si SQL cae."""

from src.nucleo import config as CFG


def _aislar(monkeypatch, tmp_path):
    monkeypatch.setattr(CFG, "CONFIG_PATH", tmp_path / "config.json")


def test_respaldo_por_defecto_activo_y_se_guarda(monkeypatch, tmp_path):
    _aislar(monkeypatch, tmp_path)
    assert CFG.respaldo_sql() == {"al_cortar": True, "al_entrenar": True}
    CFG.guardar_respaldo_sql(False, True)
    assert CFG.respaldo_sql() == {"al_cortar": False, "al_entrenar": True}


def test_respaldar_sql_no_lanza_si_sql_no_responde(monkeypatch):
    from src.almacenamiento import sqlserver as SQL
    from src.etiquetado import tablas as T

    def cae():
        raise SQL.SQLServerNoDisponible("sin servidor")
    monkeypatch.setattr(T.SQL, "asegurar_base_y_tablas", cae)
    assert T.respaldar_sql([{"exercise": "zancada"}]) == {"resumen": None, "error": "sin servidor"}


def test_exportar_respeta_el_interruptor_al_cortar(monkeypatch):
    from src.etiquetado import exportar as X
    vistos = []
    monkeypatch.setattr(X, "_exportar", lambda labels, todo, subir: vistos.append(subir) or {})
    for cfg, arg, esperado in [({"al_cortar": False}, None, False), ({"al_cortar": True}, None, True),
                               ({"al_cortar": False}, True, True)]:   # el boton manual fuerza la subida
        monkeypatch.setattr(X, "respaldo_sql", lambda cfg=cfg: cfg)
        X.exportar({}, subir_sql=arg)
        assert vistos[-1] is esperado
