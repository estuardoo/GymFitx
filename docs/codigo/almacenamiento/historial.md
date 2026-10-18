# `src/almacenamiento/historial.py`

```text
Persistencia en SQL Server (antes SQLite local, `gymfitx.db`) -- `reps`,
`sessions` y `routine` viven en la MISMA base `GymFitX` que ya usan
`src/almacenamiento/dataset_sql.py` (dataset de keypoints), por la conexion unica de
`src/almacenamiento/sqlserver.py`: un solo motor para todo. Los videos/recordings siguen en
disco como siempre -- esto solo mueve las TABLAS, nunca los archivos.

Cada metodo abre y cierra su propia conexion corta
(igual que sqlserver.py) -- no hay conexion ni lock compartidos como antes
con sqlite3 (ahi hacia falta porque una sola conexion sqlite3 se compartia
entre el hilo del pipeline y el del servidor).

Resiliencia (antes el panel NO arrancaba si SQL Server no respondia, porque
Storage() se construye al importar src/interfaz/app.py):
  - El panel arranca igual; las tablas se crean en el primer uso exitoso.
  - Lecturas sin conexion devuelven [] y dejan el motivo en `self.error`
    (el panel lo muestra en /api/state -> "almacen").
  - Escrituras de repeticiones y cierre de sesion van a una cola con un hilo
    propio: el hilo de la camara nunca espera un timeout de SQL Server. Si
    el servidor no responde, la escritura se guarda en `pendientes_sql.jsonl`
    y se reintenta sola cada 30 s -- no se pierde ninguna repeticion.

Dos tablas antes, dos ahora (mas 'routine'), sin ORM, sin ceremonia: la
misma filosofia del archivo original, solo cambia el motor debajo.
```

## Constantes

`DDL`, `REINTENTO_S`

## `asegurar_tablas`

`def asegurar_tablas() -> None`

```text
Idempotente: crea la base (si falta) y las tablas reps/sessions/routine.
```

## `_migrar_desde_sqlite`

`def _migrar_desde_sqlite(sqlite_path: Path) -> None`

```text
Una sola vez: si el 'gymfitx.db' viejo (SQLite local) todavia existe
y 'reps' en SQL Server esta vacia, copia su historial para no perderlo.
El .db viejo NUNCA se borra (queda de respaldo en disco). Si ya se
migro antes (reps ya tiene filas) o el archivo no existe, no hace nada.
```

## `_serializable`

`def _serializable(v)`

_sin docstring_

## class `Storage`

```text
Misma API de siempre (open_session, close_session, log_rep,
set_routine, routine, today, daily, by_exercise, recent, sessions,
streak, close) contra SQL Server, pero sin tumbar el panel si el
servidor no responde (ver docstring del modulo). 'path' es la ruta del
viejo gymfitx.db, solo para migrar su historial la primera vez.
```

### `Storage.__init__`

`def __init__(self, path: str | Path, spool: str | Path=SPOOL_PATH, hilo_escritor: bool=True) -> None`

_sin docstring_

### `Storage._asegurar`

`def _asegurar(self) -> bool`

```text
Crea tablas / migra la primera vez que SQL Server responde.
```

### `Storage.reconectar`

`def reconectar(self) -> bool`

```text
Tras cambiar el servidor en Sistema: olvida el error y prueba ya.
```

### `Storage.estado`

`def estado(self) -> dict`

_sin docstring_

### `Storage.pendientes`

`def pendientes(self) -> int`

_sin docstring_

### `Storage.close`

`def close(self) -> None`

_sin docstring_

### `Storage._encolar`

`def _encolar(self, sql: str, args: tuple) -> None`

_sin docstring_

### `Storage._ejecutar`

`def _ejecutar(self, ops: list[dict]) -> None`

_sin docstring_

### `Storage._ejecutar_o_guardar`

`def _ejecutar_o_guardar(self, op: dict) -> None`

_sin docstring_

### `Storage.reintentar_pendientes`

`def reintentar_pendientes(self) -> int`

```text
Vuelca pendientes_sql.jsonl a SQL Server. Devuelve cuantas escribio.
```

### `Storage._escritor`

`def _escritor(self) -> None`

_sin docstring_

### `Storage.flush`

`def flush(self, timeout: float=10.0) -> None`

```text
Espera a que la cola se vacie (apagado del panel, tests).
```

### `Storage.open_session`

`def open_session(self, exercise: str, modo: str) -> int | None`

```text
Sincrono (hace falta el id). None si SQL Server no responde: la
sesion sigue, sus repeticiones se guardan sin session_id.
```

### `Storage.close_session`

`def close_session(self, session_id: int | None, meta: dict, rutas: dict) -> None`

_sin docstring_

### `Storage.log_rep`

`def log_rep(self, exercise: str, score, session_id: int | None=None, modelo: str | None=None) -> None`

```text
No bloquea: va a la cola del hilo escritor (antes esperaba a SQL
Server dentro del hilo de la camara, en cada repeticion).
```

### `Storage.set_routine`

`def set_routine(self, items: list[dict]) -> None`

```text
Sincrono: el panel necesita saber si se guardo. Lanza SQLServerNoDisponible.
```

### `Storage._rows`

`def _rows(self, sql: str, args: tuple=()) -> list[dict]`

```text
Sin conexion devuelve [] (y deja el motivo en self.error).
```

### `Storage.routine`

`def routine(self) -> list[dict]`

_sin docstring_

### `Storage.today`

`def today(self) -> list[dict]`

_sin docstring_

### `Storage.daily`

`def daily(self, days: int=14) -> list[dict]`

_sin docstring_

### `Storage.by_exercise`

`def by_exercise(self, days: int=30) -> list[dict]`

_sin docstring_

### `Storage.recent`

`def recent(self, limit: int=20) -> list[dict]`

_sin docstring_

### `Storage.sessions`

`def sessions(self, limit: int=30) -> list[dict]`

_sin docstring_

### `Storage.streak`

`def streak(self) -> int`

```text
Dias consecutivos con al menos una repeticion, contando hacia atras.
```

