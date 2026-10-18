"""Tests de la capa de persistencia (src/almacenamiento/historial.py), ahora sobre SQL Server.

Igual que tests/test_sqlserver.py: sin un SQL Server real ni pyodbc
instalado en esta maquina no se puede abrir una conexion de verdad, asi que
esto prueba (a) la logica pura que no toca la base (DDL, _migrar_desde_sqlite
con archivo inexistente) y (b) que la ausencia del driver se reporte como
SQLServerNoDisponible, nunca como un traceback crudo de pyodbc -- lo mismo
que ya se exige del resto de la capa SQL Server. Contra un servidor real se
prueba desde la maquina que lo tiene (Windows), no desde aca.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

from src.almacenamiento import historial as storage  # noqa: E402
from src.almacenamiento import sqlserver  # noqa: E402


def test_ddl_declara_las_tres_tablas_con_guarda_idempotente():
    # Pura: nunca toca la base, solo el texto del DDL.
    for tabla in ("reps", "sessions", "routine"):
        assert f"sys.tables WHERE name = '{tabla}'" in storage.DDL
        assert f"CREATE TABLE {tabla}" in storage.DDL


def test_migrar_desde_sqlite_sin_archivo_no_hace_nada():
    # Pura: el archivo no existe, retorna antes de tocar SQL Server -- no
    # deberia reventar ni con pyodbc ausente.
    storage._migrar_desde_sqlite(Path("/no/existe/gymfitx.db"))


def test_sin_pyodbc_asegurar_tablas_da_sqlservernodisponible():
    if sqlserver.pyodbc is not None:
        return  # si esta instalado (otra maquina), este test no aplica
    try:
        storage.asegurar_tablas()
        raise AssertionError("deberia haber lanzado SQLServerNoDisponible")
    except storage.SQLServerNoDisponible:
        pass


def test_sin_sql_server_el_panel_arranca_igual():
    """Antes Storage() lanzaba al importar src/interfaz/app.py: el panel no abria."""
    if sqlserver.pyodbc is not None:
        return
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        st = storage.Storage("/no/existe/gymfitx.db", spool=Path(d) / "p.jsonl", hilo_escritor=False)
        assert st.error and "pyodbc" in st.error
        assert st.estado()["conectado"] is False
        # lecturas: listas vacias, no excepciones
        for fn in (st.routine, st.today, st.daily, st.by_exercise, st.recent, st.sessions):
            assert fn() == []
        assert st.streak() == 0
        assert st.open_session("x", "serie") is None


def test_sin_sql_server_las_repeticiones_no_se_pierden():
    """log_rep va a pendientes_sql.jsonl y se vuelca cuando vuelve el servidor."""
    if sqlserver.pyodbc is not None:
        return
    import json
    import tempfile
    score = type("S", (), {"total": 88.0, "error_z": 0.3, "duration_ms": 900,
                           "to_dict": lambda self: {"per_feature": {"a": 1.0}}})()
    with tempfile.TemporaryDirectory() as d:
        spool = Path(d) / "p.jsonl"
        st = storage.Storage("/no/existe/gymfitx.db", spool=spool, hilo_escritor=False)
        st.log_rep("mano", score, None, "dtw_biomec")
        st.log_rep("mano", score, None, "dtw_biomec")
        lineas = spool.read_text("utf-8").splitlines()
        assert len(lineas) == 2 and st.pendientes() == 2
        op = json.loads(lineas[0])
        assert op["sql"].startswith("INSERT INTO reps") and op["args"][2] == "mano"
        # sin servidor, reintentar no borra nada
        assert st.reintentar_pendientes() == 0 and spool.exists()


def test_set_routine_sin_servidor_avisa():
    if sqlserver.pyodbc is not None:
        return
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        st = storage.Storage("/x.db", spool=Path(d) / "p.jsonl", hilo_escritor=False)
        try:
            st.set_routine([{"exercise": "x"}])
            raise AssertionError("deberia haber lanzado SQLServerNoDisponible")
        except storage.SQLServerNoDisponible:
            pass

