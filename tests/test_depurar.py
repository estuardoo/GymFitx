"""depurar (src/etiquetado/depurar.py): un ejercicio archivado sale del manifest, los cortes y SQL; los archivos se conservan."""
import json

import pytest

from src.etiquetado import depurar as D


class Cursor:
    def __init__(self, n): self.rowcount = n
    def fetchone(self): return (7,)


class SqlFalso:
    def __init__(self, monkeypatch):
        self.sentencias, self.caido = [], False
        sql = self

        class Cx:
            def __enter__(self): return self
            def __exit__(self, *a): return False
            def execute(self, q, params=()):
                sql.sentencias.append((q, params))
                return Cursor(3)
            def commit(self): pass

        def asegurar():
            if sql.caido:
                raise D.SQL.SQLServerNoDisponible("sin conexion")
        monkeypatch.setattr(D.SQL, "asegurar_base_y_tablas", asegurar)
        monkeypatch.setattr(D.SQL, "conexion", lambda: Cx())


@pytest.fixture
def datos(tmp_path, monkeypatch):
    from src.nucleo import inputs as INP
    plant = tmp_path / "plantillas"
    plant.mkdir()
    (plant / "viejo.npz").write_bytes(b"x")
    with INP.editar() as t:
        for slug in ("viejo", "vivo"):
            raw = INP.registrar_raw(t, slug)
            INP.ruta_raw(raw["ej"], raw["id"]).write_bytes(b"x")
            c = INP.registrar_clip(t, slug, etiqueta=1, t_ini_ms=0, t_fin_ms=1000, raw_id=raw["id"], seg=0)
            INP.ruta_clip(c["ej"], c["id"]).write_bytes(b"x")
    m = {"estado": tmp_path / "estado.json", "tipos": tmp_path / "tipos.json", "pend": tmp_path / "pend.json"}
    viejo_vid = INP.vid_de(INP.tabla()["raw"][0])
    m["estado"].write_text(json.dumps({viejo_vid: "h", "otro/x.mp4": "h"}))
    m["tipos"].write_text(json.dumps({"viejo": 5, "vivo": 6, "desconocido": 9}))
    for nombre, valor in (("TEMPLATES_DIR", plant), ("ARCHIVO_DIR", tmp_path / "archivados"), ("EXPORT_ESTADO_PATH", m["estado"]),
                          ("SQL_TIPOS_PATH", m["tipos"]), ("PENDIENTES_PATH", m["pend"]),
                          ("DEPURADOS_PATH", tmp_path / "archivados" / "depurados.json")):
        monkeypatch.setattr(D, nombre, valor)
    monkeypatch.setattr(D.EP, "listar_ejercicios", lambda: ["vivo"])
    monkeypatch.setattr(D.EP, "leer_ejercicio", lambda s: {} if s == "vivo" else None)
    return tmp_path, m, SqlFalso(monkeypatch)


def test_huerfanos_y_plan(datos):
    assert D.huerfanos() == ["viejo"]      # no 'vivo', ni 'desconocido'
    p = D.plan()
    assert p == [{"slug": "viejo", "type": 5, "clips_manifest": 1, "clips_disco": 1, "grabaciones": 1, "sql_archivos": 7}]


def test_depurar_quita_tablas_estado_y_mueve_capas(datos):
    from src.nucleo import config as C
    from src.nucleo import inputs as INP
    tmp, m, sql = datos
    r = D.depurar("viejo")
    assert r["clips"] == 1 and r["errores"] == [] and r["sql_error"] is None and r["sql"]["archivos"] == 3
    assert [x["exercise"] for x in INP.filas()] == ["vivo"] and [x["ej"] for x in INP.tabla()["raw"]] == [INP.id_de("vivo")]
    assert json.loads(m["estado"].read_text()) == {"otro/x.mp4": "h"}
    # archivos conservados en sistema/archivados/<slug>_<fecha>/<capa>/<n>; el vivo no se toca
    dest = next(p for p in (tmp / "archivados").iterdir() if p.is_dir())
    nv, nvivo = INP.id_de("viejo"), INP.id_de("vivo")
    assert (dest / "bronze" / str(nv) / "000001.mp4").exists() and (dest / "raw" / str(nv)).is_dir() and (dest / "plantillas" / "viejo.npz").exists()
    assert not (C.CLIPS_DIR / str(nv)).exists() and (C.CLIPS_DIR / str(nvivo) / "000002.mp4").exists()
    # SQL: todas las tablas del type 5, primero las que apuntan a table_file
    tablas = [q.split("FROM ")[1].split(" ")[0] for q, p in sql.sentencias if q.startswith("DELETE")]
    assert tablas == list(D.TABLAS_DEL_TIPO) and all(p == (5,) for _, p in sql.sentencias)
    assert D.huerfanos() == []             # nada mas que depurar; el type queda reservado
    assert json.loads(m["tipos"].read_text())["viejo"] == 5


def test_sql_caido_queda_pendiente_y_se_reintenta(datos):
    tmp, m, sql = datos
    sql.caido = True
    r = D.depurar("viejo")
    assert r["sql_error"] == "sin conexion" and json.loads(m["pend"].read_text()) == ["viejo"]
    from src.nucleo import inputs as INP
    assert [x["exercise"] for x in INP.filas()] == ["vivo"]   # lo local ya quedo limpio
    assert D.huerfanos() == ["viejo"]      # sigue figurando por el pendiente
    sql.caido = False
    assert D.depurar_todos()[0]["sql"]["archivos"] == 3 and json.loads(m["pend"].read_text()) == []


def test_no_depura_un_ejercicio_vivo(datos):
    with pytest.raises(ValueError):
        D.depurar("vivo")
    assert D.depurar_todos(["vivo"]) == []
