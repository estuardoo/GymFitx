"""Persistencia en SQL Server (antes SQLite local, `gymfitx.db`) -- `reps`,
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
"""

from __future__ import annotations

import json
import queue
import sqlite3
import threading
import time
from datetime import date, datetime, timedelta
from pathlib import Path

from src.almacenamiento.sqlserver import SQLServerNoDisponible, _conectar, asegurar_base
from src.nucleo.config import SPOOL_PATH
from src.nucleo.tiempos import medir

DDL = """
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'reps')
CREATE TABLE reps (
    id          INT IDENTITY(1,1) PRIMARY KEY,
    ts          DATETIME2     NOT NULL,
    day         DATE          NOT NULL,
    exercise    NVARCHAR(200) NOT NULL,
    score       FLOAT         NOT NULL,
    error_z     FLOAT         NOT NULL,
    duration_ms INT           NOT NULL,
    detail      NVARCHAR(MAX) NULL,
    session_id  INT           NULL,
    modelo      NVARCHAR(100) NULL
);
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'ix_reps_day' AND object_id = OBJECT_ID('reps'))
CREATE INDEX ix_reps_day ON reps(day);
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'ix_reps_ex' AND object_id = OBJECT_ID('reps'))
CREATE INDEX ix_reps_ex ON reps(exercise, day);

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'sessions')
CREATE TABLE sessions (
    id          INT IDENTITY(1,1) PRIMARY KEY,
    started_at  DATETIME2     NOT NULL,
    ended_at    DATETIME2     NULL,
    day         DATE          NOT NULL,
    exercise    NVARCHAR(200) NOT NULL,
    modo        NVARCHAR(20)  NOT NULL,
    video       NVARCHAR(400) NULL,
    features    NVARCHAR(400) NULL,
    frames      INT           NOT NULL DEFAULT 0,
    reps        INT           NOT NULL DEFAULT 0,
    duration_ms INT           NOT NULL DEFAULT 0
);
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'ix_sessions_day' AND object_id = OBJECT_ID('sessions'))
CREATE INDEX ix_sessions_day ON sessions(day);

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'routine')
CREATE TABLE routine (
    exercise    NVARCHAR(200) PRIMARY KEY,
    target_reps INT NOT NULL DEFAULT 10,
    position    INT NOT NULL DEFAULT 0
);
"""


def asegurar_tablas() -> None:
    """Idempotente: crea la base (si falta) y las tablas reps/sessions/routine."""
    asegurar_base()
    with _conectar(autocommit=True) as cx:
        cx.execute(DDL)


def _migrar_desde_sqlite(sqlite_path: Path) -> None:
    """Una sola vez: si el 'gymfitx.db' viejo (SQLite local) todavia existe
    y 'reps' en SQL Server esta vacia, copia su historial para no perderlo.
    El .db viejo NUNCA se borra (queda de respaldo en disco). Si ya se
    migro antes (reps ya tiene filas) o el archivo no existe, no hace nada."""
    if not sqlite_path.exists():
        return
    with _conectar() as cx:
        if cx.execute("SELECT TOP (1) 1 FROM reps").fetchone():
            return  # ya hay datos -- no se re-migra

    viejo = sqlite3.connect(sqlite_path)
    viejo.row_factory = sqlite3.Row
    try:
        sesiones = [dict(r) for r in viejo.execute("SELECT * FROM sessions").fetchall()]
        repeticiones = [dict(r) for r in viejo.execute("SELECT * FROM reps").fetchall()]
        rutina = [dict(r) for r in viejo.execute("SELECT * FROM routine").fetchall()]
    except sqlite3.OperationalError:
        return  # gymfitx.db existe pero sin esas tablas (base nueva/vacia)
    finally:
        viejo.close()

    if not (sesiones or repeticiones or rutina):
        return

    with _conectar() as cx:
        mapa_sesiones = {}
        for s in sesiones:
            fila = cx.execute(
                "INSERT INTO sessions (started_at, ended_at, day, exercise, modo, video, "
                "features, frames, reps, duration_ms) OUTPUT INSERTED.id VALUES (?,?,?,?,?,?,?,?,?,?)",
                (s["started_at"], s.get("ended_at"), s["day"], s["exercise"], s["modo"],
                 s.get("video"), s.get("features"), s.get("frames", 0), s.get("reps", 0),
                 s.get("duration_ms", 0)),
            ).fetchone()
            mapa_sesiones[s["id"]] = fila[0]
        for r in repeticiones:
            cx.execute(
                "INSERT INTO reps (ts, day, exercise, score, error_z, duration_ms, detail, "
                "session_id, modelo) VALUES (?,?,?,?,?,?,?,?,?)",
                (r["ts"], r["day"], r["exercise"], r["score"], r["error_z"], r["duration_ms"],
                 r.get("detail"), mapa_sesiones.get(r.get("session_id")), r.get("modelo")),
            )
        for it in rutina:
            cx.execute(
                "INSERT INTO routine (exercise, target_reps, position) VALUES (?,?,?)",
                (it["exercise"], it["target_reps"], it["position"]),
            )
        cx.commit()


REINTENTO_S = 30.0


def _serializable(v):
    return v.isoformat() if isinstance(v, (datetime, date)) else v


class Storage:
    """Misma API de siempre (open_session, close_session, log_rep,
    set_routine, routine, today, daily, by_exercise, recent, sessions,
    streak, close) contra SQL Server, pero sin tumbar el panel si el
    servidor no responde (ver docstring del modulo). 'path' es la ruta del
    viejo gymfitx.db, solo para migrar su historial la primera vez."""

    def __init__(self, path: str | Path, spool: str | Path = SPOOL_PATH,
                 hilo_escritor: bool = True) -> None:
        self._sqlite_viejo = Path(path)
        self._spool = Path(spool)
        self._listo = False
        self._ultimo_intento = -1e9
        self.error: str | None = None
        self._lock = threading.Lock()
        self._cola: queue.Queue = queue.Queue()
        self._hilo = None
        if hilo_escritor:
            self._hilo = threading.Thread(target=self._escritor, daemon=True, name="storage-sql")
            self._hilo.start()
        if hilo_escritor:   # el servidor abre sin esperar a SQL; las lecturas esperan el candado, max. SQLSERVER_TIMEOUT_S
            threading.Thread(target=self._asegurar, daemon=True, name="sql-inicial").start()
        else:
            self._asegurar()

    # -- conexion perezosa --
    def _asegurar(self) -> bool:
        """Crea tablas / migra la primera vez que SQL Server responde."""
        if self._listo:
            return True
        with self._lock:
            if self._listo:
                return True
            # sin conexion: no reintentar en cada lectura (cada intento cuesta
            # hasta 5 s de timeout y /api/state hace varias lecturas seguidas)
            if self.error and time.monotonic() - self._ultimo_intento < REINTENTO_S:
                return False
            self._ultimo_intento = time.monotonic()
            try:
                with medir("sql:conectar+tablas"):
                    asegurar_tablas()
                try:
                    _migrar_desde_sqlite(self._sqlite_viejo)
                except SQLServerNoDisponible:
                    raise
                except Exception:
                    pass  # una migracion con problemas no debe impedir arrancar la app
                self._listo, self.error = True, None
            except SQLServerNoDisponible as e:
                self.error = str(e)
        return self._listo

    def reconectar(self) -> bool:
        """Tras cambiar el servidor en Sistema: olvida el error y prueba ya."""
        with self._lock:
            self._listo, self.error, self._ultimo_intento = False, None, -1e9
        return self._asegurar()

    def estado(self) -> dict:
        return {"motor": "sqlserver", "conectado": self._listo and self.error is None,
                "error": self.error, "pendientes": self.pendientes()}

    def pendientes(self) -> int:
        n = self._cola.qsize()
        if self._spool.exists():
            n += sum(1 for linea in self._spool.read_text("utf-8").splitlines() if linea.strip())
        return n

    def close(self) -> None:
        self.flush()

    # -- cola de escritura (hilo propio) --
    def _encolar(self, sql: str, args: tuple) -> None:
        op = {"sql": sql, "args": [_serializable(a) for a in args]}
        if self._hilo is None:          # modo sincrono (tests / scripts)
            self._ejecutar_o_guardar(op)
        else:
            self._cola.put(op)

    def _ejecutar(self, ops: list[dict]) -> None:
        if not self._asegurar():
            raise SQLServerNoDisponible(self.error or "SQL Server no disponible")
        with _conectar() as cx:
            for op in ops:
                cx.execute(op["sql"], tuple(op["args"]))
            cx.commit()

    def _ejecutar_o_guardar(self, op: dict) -> None:
        try:
            self._ejecutar([op])
        except SQLServerNoDisponible as e:
            self.error, self._listo, self._ultimo_intento = str(e), False, time.monotonic()
            with self._spool.open("a", encoding="utf-8") as f:
                f.write(json.dumps(op, ensure_ascii=False) + "\n")

    def reintentar_pendientes(self) -> int:
        """Vuelca pendientes_sql.jsonl a SQL Server. Devuelve cuantas escribio."""
        if not self._spool.exists():
            return 0
        lineas = [l for l in self._spool.read_text("utf-8").splitlines() if l.strip()]
        if not lineas:
            self._spool.unlink(missing_ok=True)
            return 0
        try:
            self._ejecutar([json.loads(l) for l in lineas])
        except SQLServerNoDisponible as e:
            self.error = str(e)
            return 0
        self._spool.unlink(missing_ok=True)
        return len(lineas)

    def _escritor(self) -> None:
        while True:
            try:
                op = self._cola.get(timeout=REINTENTO_S)
            except queue.Empty:
                self.reintentar_pendientes()
                continue
            if op is None:              # marca de flush
                self._cola.task_done()
                continue
            self._ejecutar_o_guardar(op)
            self._cola.task_done()

    def flush(self, timeout: float = 10.0) -> None:
        """Espera a que la cola se vacie (apagado del panel, tests)."""
        if self._hilo is None:
            return
        fin = threading.Event()
        def _esperar():
            self._cola.join()
            fin.set()
        threading.Thread(target=_esperar, daemon=True).start()
        fin.wait(timeout)

    # -- escritura --
    def open_session(self, exercise: str, modo: str) -> int | None:
        """Sincrono (hace falta el id). None si SQL Server no responde: la
        sesion sigue, sus repeticiones se guardan sin session_id."""
        if not self._asegurar():
            return None
        ahora = datetime.now()
        try:
            with _conectar() as cx:
                fila = cx.execute(
                    "INSERT INTO sessions (started_at, day, exercise, modo) "
                    "OUTPUT INSERTED.id VALUES (?,?,?,?)",
                    (ahora, ahora.date(), exercise, modo),
                ).fetchone()
                cx.commit()
                return int(fila[0])
        except SQLServerNoDisponible as e:
            self.error, self._listo, self._ultimo_intento = str(e), False, time.monotonic()
            return None

    def close_session(self, session_id: int | None, meta: dict, rutas: dict) -> None:
        if session_id is None:
            return
        self._encolar(
            "UPDATE sessions SET ended_at=?, video=?, features=?, frames=?, reps=?, "
            "duration_ms=? WHERE id=?",
            (meta.get("ended_at"), rutas.get("video"), rutas.get("features"),
             int(meta.get("frames", 0)), int(meta.get("reps", 0)),
             int(meta.get("duration_ms", 0)), session_id),
        )

    def log_rep(self, exercise: str, score, session_id: int | None = None,
                modelo: str | None = None) -> None:
        """No bloquea: va a la cola del hilo escritor (antes esperaba a SQL
        Server dentro del hilo de la camara, en cada repeticion)."""
        ahora = datetime.now()
        self._encolar(
            "INSERT INTO reps (ts, day, exercise, score, error_z, duration_ms, detail, "
            "session_id, modelo) VALUES (?,?,?,?,?,?,?,?,?)",
            (ahora, ahora.date(), exercise, float(score.total), float(score.error_z),
             int(score.duration_ms), json.dumps(score.to_dict()["per_feature"]),
             session_id, modelo),
        )

    def set_routine(self, items: list[dict]) -> None:
        """Sincrono: el panel necesita saber si se guardo. Lanza SQLServerNoDisponible."""
        if not self._asegurar():
            raise SQLServerNoDisponible(self.error or "SQL Server no disponible")
        with _conectar() as cx:
            cx.execute("DELETE FROM routine")
            if items:
                # executemany no existe en pyodbc.Connection (solo en Cursor); cx.execute()
                # es solo un atajo de 1 sentencia -- de ahi salia el AttributeError.
                cx.cursor().executemany(
                    "INSERT INTO routine (exercise, target_reps, position) VALUES (?,?,?)",
                    [(it["exercise"], int(it.get("target_reps", 10)), i) for i, it in enumerate(items)],
                )
            cx.commit()

    # -- lectura --
    def _rows(self, sql: str, args: tuple = ()) -> list[dict]:
        """Sin conexion devuelve [] (y deja el motivo en self.error)."""
        if not self._asegurar():
            return []
        try:
            with medir("sql:consulta"), _conectar() as cx:
                cur = cx.execute(sql, args)
                columnas = [c[0] for c in cur.description]
                return [dict(zip(columnas, fila)) for fila in cur.fetchall()]
        except SQLServerNoDisponible as e:
            self.error, self._listo, self._ultimo_intento = str(e), False, time.monotonic()
            return []

    def routine(self) -> list[dict]:
        return self._rows("SELECT exercise, target_reps FROM routine ORDER BY position")

    def today(self) -> list[dict]:
        return self._rows(
            "SELECT exercise, COUNT(*) AS reps, ROUND(AVG(score),1) AS avg_score, "
            "ROUND(MAX(score),1) AS best FROM reps WHERE day = ? GROUP BY exercise",
            (date.today(),),
        )

    def daily(self, days: int = 14) -> list[dict]:
        desde = date.today() - timedelta(days=days - 1)
        return self._rows(
            "SELECT day, COUNT(*) AS reps, ROUND(AVG(score),1) AS avg_score "
            "FROM reps WHERE day >= ? GROUP BY day ORDER BY day",
            (desde,),
        )

    def by_exercise(self, days: int = 30) -> list[dict]:
        desde = date.today() - timedelta(days=days - 1)
        return self._rows(
            "SELECT exercise, day, ROUND(AVG(score),1) AS avg_score, COUNT(*) AS reps "
            "FROM reps WHERE day >= ? GROUP BY exercise, day ORDER BY day",
            (desde,),
        )

    def recent(self, limit: int = 20) -> list[dict]:
        return self._rows(
            "SELECT TOP (?) ts, exercise, ROUND(score,1) AS score, duration_ms "
            "FROM reps ORDER BY id DESC",
            (limit,),
        )

    def sessions(self, limit: int = 30) -> list[dict]:
        return self._rows(
            "SELECT TOP (?) id, started_at, exercise, modo, video, frames, reps, duration_ms "
            "FROM sessions ORDER BY id DESC",
            (limit,),
        )

    def streak(self) -> int:
        """Dias consecutivos con al menos una repeticion, contando hacia atras."""
        dias = {r["day"] for r in self._rows("SELECT DISTINCT day FROM reps")}
        n, d = 0, date.today()
        while d in dias:
            n += 1
            d -= timedelta(days=1)
        return n
