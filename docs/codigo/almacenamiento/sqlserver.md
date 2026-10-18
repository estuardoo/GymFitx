# `src/almacenamiento/sqlserver.py`

```text
Conexion UNICA a SQL Server para todo el proyecto.

Antes habia dos modulos (src/almacenamiento/sqlserver.py con driver fijo ODBC 17 y host
PROGRAM\HYPER, y src/almacenamiento/dataset_sql.py con su propia deteccion de driver/host)
apuntando a la misma base GymFitX. Ahora todos -- src/almacenamiento/historial.py (reps,
sesiones, rutina) y src/almacenamiento/dataset_sql.py (dataset de keypoints) -- conectan por
aqui, con el host/base de src/nucleo/config.py.

Todo error de conexion sale como SQLServerNoDisponible (nunca una excepcion
cruda de pyodbc), para que quien llama pueda avisar en el panel sin tumbar
nada.
```

## Constantes

`DRIVERS_PREFERIDOS`

## class `SQLServerNoDisponible`

```text
Falta pyodbc, falta el driver ODBC, o el servidor no responde.
```

## `_requerir_pyodbc`

`def _requerir_pyodbc() -> None`

_sin docstring_

## `driver_odbc`

`def driver_odbc() -> str`

```text
El mejor driver instalado en ESTA PC. El 18 cifra por defecto -> TrustServerCertificate.
```

## `conectar`

`def conectar(database: str | None='', autocommit: bool=False, timeout: int | None=None)`

```text
Conexion nueva (con 'with ... as cx'). database="" -> la base configurada; None -> 'master'.
```

## `asegurar_base`

`def asegurar_base() -> None`

```text
Idempotente: crea la base GymFitX si no existe.
```

## `ejecutar_ddl`

`def ejecutar_ddl(ddl: str) -> None`

```text
Corre un DDL de varios statements separados por ';\n' (idempotente).
```

## `base_existe`

`def base_existe() -> bool`

_sin docstring_

## `tablas_existentes`

`def tablas_existentes() -> set[str]`

_sin docstring_

## `estado`

`def estado(tablas_esperadas: tuple[str, ...]=()) -> dict`

```text
Diagnostico para el panel: nunca revienta aunque el servidor no responda.

Primero consulta 'master': pedir DATABASE=GymFitX cuando la base aun no
existe devuelve un 'Login failed' confuso aunque el login sea correcto.
```

