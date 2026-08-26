"""Persistencia. SQLite y nada mas: sin ORM, sin migraciones, sin ceremonia.

Dos tablas. 'reps' es el hecho atomico del sistema (una repeticion puntuada);
todo el panel diario se deriva de ella con agregaciones. 'routine' guarda que
piensa hacer hoy y cuantas veces.
"""

from __future__ import annotations

import json
import sqlite3
import threading
from datetime import date, datetime, timedelta
from pathlib import Path

ESQUEMA = """
CREATE TABLE IF NOT EXISTS reps (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    ts          TEXT    NOT NULL,
    day         TEXT    NOT NULL,
    exercise    TEXT    NOT NULL,
    score       REAL    NOT NULL,
    error_z     REAL    NOT NULL,
    duration_ms INTEGER NOT NULL,
    detail      TEXT
);
CREATE INDEX IF NOT EXISTS ix_reps_day ON reps(day);
CREATE INDEX IF NOT EXISTS ix_reps_ex  ON reps(exercise, day);

CREATE TABLE IF NOT EXISTS sessions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at  TEXT    NOT NULL,
    ended_at    TEXT,
    day         TEXT    NOT NULL,
    exercise    TEXT    NOT NULL,
    modo        TEXT    NOT NULL,
    video       TEXT,
    features    TEXT,
    frames      INTEGER DEFAULT 0,
    reps        INTEGER DEFAULT 0,
    duration_ms INTEGER DEFAULT 0
);
CREATE INDEX IF NOT EXISTS ix_ses_day ON sessions(day);

CREATE TABLE IF NOT EXISTS routine (
    exercise    TEXT    PRIMARY KEY,
    target_reps INTEGER NOT NULL DEFAULT 10,
    position    INTEGER NOT NULL DEFAULT 0
);
"""


class Storage:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # El pipeline corre en un hilo y el servidor en otro: una conexion, un lock.
        self._cx = sqlite3.connect(self.path, check_same_thread=False)
        self._cx.row_factory = sqlite3.Row
        self._lock = threading.Lock()
        with self._lock:
            self._cx.executescript(ESQUEMA)
            # Migracion aditiva: una base creada antes de las sesiones no tiene
            # esta columna. Agregarla es seguro y no pierde datos.
            try:
                self._cx.execute("ALTER TABLE reps ADD COLUMN session_id INTEGER")
            except sqlite3.OperationalError:
                pass
            self._cx.commit()

    def close(self) -> None:
        with self._lock:
            self._cx.close()

    # -- escritura --
    def open_session(self, exercise: str, modo: str) -> int:
        ahora = datetime.now()
        with self._lock:
            cur = self._cx.execute(
                "INSERT INTO sessions (started_at, day, exercise, modo) VALUES (?,?,?,?)",
                (ahora.isoformat(timespec="seconds"), ahora.date().isoformat(), exercise, modo),
            )
            self._cx.commit()
            return int(cur.lastrowid)

    def close_session(self, session_id: int, meta: dict, rutas: dict) -> None:
        with self._lock:
            self._cx.execute(
                "UPDATE sessions SET ended_at=?, video=?, features=?, frames=?, reps=?, "
                "duration_ms=? WHERE id=?",
                (meta.get("ended_at"), rutas.get("video"), rutas.get("features"),
                 int(meta.get("frames", 0)), int(meta.get("reps", 0)),
                 int(meta.get("duration_ms", 0)), session_id),
            )
            self._cx.commit()

    def log_rep(self, exercise: str, score, session_id: int | None = None) -> int:
        ahora = datetime.now()
        with self._lock:
            cur = self._cx.execute(
                "INSERT INTO reps (ts, day, exercise, score, error_z, duration_ms, detail, "
                "session_id) VALUES (?,?,?,?,?,?,?,?)",
                (
                    ahora.isoformat(timespec="seconds"),
                    ahora.date().isoformat(),
                    exercise,
                    float(score.total),
                    float(score.error_z),
                    int(score.duration_ms),
                    json.dumps(score.to_dict()["per_feature"]),
                    session_id,
                ),
            )
            self._cx.commit()
            return int(cur.lastrowid)

    def set_routine(self, items: list[dict]) -> None:
        with self._lock:
            self._cx.execute("DELETE FROM routine")
            self._cx.executemany(
                "INSERT INTO routine (exercise, target_reps, position) VALUES (?,?,?)",
                [(it["exercise"], int(it.get("target_reps", 10)), i) for i, it in enumerate(items)],
            )
            self._cx.commit()

    # -- lectura --
    def _rows(self, sql: str, args: tuple = ()) -> list[dict]:
        with self._lock:
            return [dict(r) for r in self._cx.execute(sql, args).fetchall()]

    def routine(self) -> list[dict]:
        return self._rows("SELECT exercise, target_reps FROM routine ORDER BY position")

    def today(self) -> list[dict]:
        return self._rows(
            "SELECT exercise, COUNT(*) AS reps, ROUND(AVG(score),1) AS avg_score, "
            "ROUND(MAX(score),1) AS best FROM reps WHERE day = ? GROUP BY exercise",
            (date.today().isoformat(),),
        )

    def daily(self, days: int = 14) -> list[dict]:
        desde = (date.today() - timedelta(days=days - 1)).isoformat()
        return self._rows(
            "SELECT day, COUNT(*) AS reps, ROUND(AVG(score),1) AS avg_score "
            "FROM reps WHERE day >= ? GROUP BY day ORDER BY day",
            (desde,),
        )

    def by_exercise(self, days: int = 30) -> list[dict]:
        desde = (date.today() - timedelta(days=days - 1)).isoformat()
        return self._rows(
            "SELECT exercise, day, ROUND(AVG(score),1) AS avg_score, COUNT(*) AS reps "
            "FROM reps WHERE day >= ? GROUP BY exercise, day ORDER BY day",
            (desde,),
        )

    def recent(self, limit: int = 20) -> list[dict]:
        return self._rows(
            "SELECT ts, exercise, ROUND(score,1) AS score, duration_ms "
            "FROM reps ORDER BY id DESC LIMIT ?",
            (limit,),
        )

    def sessions(self, limit: int = 30) -> list[dict]:
        return self._rows(
            "SELECT id, started_at, exercise, modo, video, frames, reps, duration_ms "
            "FROM sessions ORDER BY id DESC LIMIT ?",
            (limit,),
        )

    def streak(self) -> int:
        """Dias consecutivos con al menos una repeticion, contando hacia atras."""
        dias = {r["day"] for r in self._rows("SELECT DISTINCT day FROM reps")}
        n, d = 0, date.today()
        while d.isoformat() in dias:
            n += 1
            d -= timedelta(days=1)
        return n
