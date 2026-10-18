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
    clips, graba, plant = tmp_path / "clips", tmp_path / "grabaciones", tmp_path / "plantillas"
    for slug in ("viejo", "vivo"):
        (clips / slug / "bien").mkdir(parents=True)
        (clips / slug / "bien" / "a.mp4").write_bytes(b"x")
    (graba / "viejo" / "2026-01-01").mkdir(parents=True)
    (graba / "viejo" / "2026-01-01" / "v.mp4").write_bytes(b"x")
    plant.mkdir()
    (plant / "viejo.npz").write_bytes(b"x")
    m = {"manifest": tmp_path / "manifest.json", "etiq": tmp_path / "etiquetas.json", "estado": tmp_path / "estado.json",
         "sel": tmp_path / "sel.json", "tipos": tmp_path / "tipos.json", "pend": tmp_path / "pend.json"}
    m["manifest"].write_text(json.dumps([{"clip": "viejo/bien/a.mp4", "exercise": "viejo"}, {"clip": "vivo/bien/a.mp4", "exercise": "vivo"}]))
    m["etiq"].write_text(json.dumps({"viejo/2026-01-01/v.mp4": {}, "vivo/2026-01-01/w.mp4": {}}))
    m["estado"].write_text(json.dumps({"viejo/2026-01-01/v.mp4": "h"}))
    m["sel"].write_text(json.dumps({"bien/a.mp4": False}))
    m["tipos"].write_text(json.dumps({"viejo": 5, "vivo": 6, "desconocido": 9}))
    for nombre, valor in (("CLIPS_DIR", clips), ("RECORDINGS_DIR", graba), ("TEMPLATES_DIR", plant), ("ARCHIVO_DIR", tmp_path / "archivados"),
                          ("MANIFEST_PATH", m["manifest"]), ("ETIQUETAS_PATH", m["etiq"]), ("EXPORT_ESTADO_PATH", m["estado"]),
                          ("SELECCION_PATH", m["sel"]), ("SQL_TIPOS_PATH", m["tipos"]), ("PENDIENTES_PATH", m["pend"]), ("DEPURADOS_PATH", tmp_path / "archivados" / "depurados.json")):
        monkeypatch.setattr(D, nombre, valor)
    monkeypatch.setattr(D.EP, "listar_ejercicios", lambda: ["vivo"])
    monkeypatch.setattr(D.EP, "leer_ejercicio", lambda s: {} if s == "vivo" else None)
    return tmp_path, m, SqlFalso(monkeypatch)


def test_huerfanos_y_plan(datos):
    assert D.huerfanos() == ["viejo"]      # no 'vivo', ni 'desconocido'
    p = D.plan()
    assert p == [{"slug": "viejo", "type": 5, "clips_manifest": 1, "clips_disco": 1, "grabaciones": 1, "sql_archivos": 7}]


def test_depurar_quita_manifest_cortes_seleccion_y_sql(datos):
    tmp, m, sql = datos
    r = D.depurar("viejo")
    assert r["clips"] == 1 and r["errores"] == [] and r["sql_error"] is None and r["sql"]["archivos"] == 3
    assert [x["exercise"] for x in json.loads(m["manifest"].read_text())] == ["vivo"]
    assert list(json.loads(m["etiq"].read_text())) == ["vivo/2026-01-01/w.mp4"] and json.loads(m["estado"].read_text()) == {}
    assert json.loads(m["sel"].read_text()) == {}
    # archivos conservados en datos/archivados/<slug>_<fecha>/
    dest = next(p for p in (tmp / "archivados").iterdir() if p.is_dir())
    assert (dest / "clips" / "viejo" / "bien" / "a.mp4").exists() and (dest / "grabaciones" / "viejo").is_dir() and (dest / "plantillas" / "viejo.npz").exists()
    assert not (tmp / "clips" / "viejo").exists() and (tmp / "clips" / "vivo" / "bien" / "a.mp4").exists()
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
    assert [x["exercise"] for x in json.loads(m["manifest"].read_text())] == ["vivo"]   # lo local ya quedo limpio
    assert D.huerfanos() == ["viejo"]      # sigue figurando por el pendiente
    sql.caido = False
    assert D.depurar_todos()[0]["sql"]["archivos"] == 3 and json.loads(m["pend"].read_text()) == []


def test_no_depura_un_ejercicio_vivo(datos):
    with pytest.raises(ValueError):
        D.depurar("vivo")
    assert D.depurar_todos(["vivo"]) == []
