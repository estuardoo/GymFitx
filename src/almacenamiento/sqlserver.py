"""Conexion UNICA a SQL Server para todo el proyecto.

Antes habia dos modulos (src/almacenamiento/sqlserver.py con driver fijo ODBC 17 y host
PROGRAM\\HYPER, y src/almacenamiento/dataset_sql.py con su propia deteccion de driver/host)
apuntando a la misma base GymFitX. Ahora todos -- src/almacenamiento/historial.py (reps,
sesiones, rutina) y src/almacenamiento/dataset_sql.py (dataset de keypoints) -- conectan por
aqui, con el host/base de src/nucleo/config.py.

Todo error de conexion sale como SQLServerNoDisponible (nunca una excepcion
cruda de pyodbc), para que quien llama pueda avisar en el panel sin tumbar
nada.
"""

from __future__ import annotations

from src.nucleo import config as CFG
from src.nucleo.config import SQLSERVER_DB, SQLSERVER_HOST  # noqa: F401 -- nombres historicos

try:
    import pyodbc
except ImportError:  # el driver es cosa de la maquina que corre el panel de verdad
    pyodbc = None

DRIVERS_PREFERIDOS = ("ODBC Driver 18 for SQL Server", "ODBC Driver 17 for SQL Server",
                      "SQL Server Native Client 11.0", "SQL Server")


class SQLServerNoDisponible(RuntimeError):
    """Falta pyodbc, falta el driver ODBC, o el servidor no responde."""


def _requerir_pyodbc() -> None:
    if pyodbc is None:
        raise SQLServerNoDisponible(
            "Falta el paquete 'pyodbc' (pip install pyodbc) y el driver ODBC "
            "de SQL Server en esta maquina."
        )


def driver_odbc() -> str:
    """El mejor driver instalado en ESTA PC. El 18 cifra por defecto -> TrustServerCertificate."""
    _requerir_pyodbc()
    instalados = set(pyodbc.drivers())
    for d in DRIVERS_PREFERIDOS:
        if d in instalados:
            return d
    raise SQLServerNoDisponible(
        "No hay driver ODBC de SQL Server en esta PC. Instala 'ODBC Driver 18 for SQL Server' "
        "(https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)")


def conectar(database: str | None = "", autocommit: bool = False, timeout: int | None = None):
    """Conexion nueva (con 'with ... as cx'). database="" -> la base configurada; None -> 'master'."""
    if database == "":
        database = CFG.SQLSERVER_DB
    _requerir_pyodbc()
    driver = driver_odbc()
    cadena = (
        f"DRIVER={{{driver}}};"
        f"SERVER={CFG.SQLSERVER_HOST};"
        f"DATABASE={database or 'master'};"
        "Trusted_Connection=yes;"
        + ("TrustServerCertificate=yes;" if "18" in driver else "")
    )
    try:
        return pyodbc.connect(cadena, autocommit=autocommit, timeout=timeout or CFG.SQLSERVER_TIMEOUT_S)
    except Exception as e:
        raise SQLServerNoDisponible(
            f"No se pudo conectar a '{CFG.SQLSERVER_HOST}' (base '{database or 'master'}'): {e}"
        ) from None


# alias con el nombre historico (lo usaban storage.py y los tests)
_conectar = conectar


def asegurar_base() -> None:
    """Idempotente: crea la base GymFitX si no existe."""
    with conectar(database=None, autocommit=True) as cx:
        cx.execute(
            f"IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = '{CFG.SQLSERVER_DB}') "
            f"CREATE DATABASE [{CFG.SQLSERVER_DB}]"
        )


def ejecutar_ddl(ddl: str) -> None:
    """Corre un DDL de varios statements separados por ';\\n' (idempotente)."""
    asegurar_base()
    with conectar(autocommit=True) as cx:
        for stmt in ddl.strip().split(";\n"):
            if stmt.strip():
                cx.execute(stmt)


def base_existe() -> bool:
    with conectar(database=None) as cx:
        return cx.execute("SELECT 1 FROM sys.databases WHERE name = ?",
                          (CFG.SQLSERVER_DB,)).fetchone() is not None


def tablas_existentes() -> set[str]:
    with conectar() as cx:
        return {r[0] for r in cx.execute("SELECT name FROM sys.tables").fetchall()}


def estado(tablas_esperadas: tuple[str, ...] = ()) -> dict:
    """Diagnostico para el panel: nunca revienta aunque el servidor no responda.

    Primero consulta 'master': pedir DATABASE=GymFitX cuando la base aun no
    existe devuelve un 'Login failed' confuso aunque el login sea correcto."""
    base = {"host": CFG.SQLSERVER_HOST, "base": CFG.SQLSERVER_DB}
    try:
        if not base_existe():
            return {**base, "conectado": False, "tablas_faltantes": list(tablas_esperadas),
                    "error": f"La base '{CFG.SQLSERVER_DB}' aun no existe en {CFG.SQLSERVER_HOST}. "
                             "Se crea sola con 'Generar / actualizar tablas'."}
        existentes = tablas_existentes()
    except SQLServerNoDisponible as e:
        return {**base, "conectado": False, "tablas_faltantes": list(tablas_esperadas), "error": str(e)}
    return {**base, "conectado": True, "error": None,
            "tablas_faltantes": [t for t in tablas_esperadas if t not in existentes]}
