"""Rutas e indice del dataset: que video es cual, que clips se exportaron (tabla `clips` de parameters/inputs.json) y de que
ejercicio. Lo comparten cortes, exportar, tablas y entrenamiento."""

from __future__ import annotations

import json
from pathlib import Path

from src.almacenamiento import dataset_sql as SQL
from src.nucleo import inputs as INP
from src.nucleo.config import CLIPS_DIR, RECORDINGS_DIR
from src.nucleo.log import logger

DATA, OUT = RECORDINGS_DIR, CLIPS_DIR          # input/raw (grabaciones), input/bronze (clips)


def _slug(vid: str) -> str:
    """Identificador plano y unico de un video, a partir de su ruta relativa a DATA
    (ej. '1/000007.mp4' -> '1__000007'): sirve de nombre para sus previews."""
    return Path(vid).with_suffix("").as_posix().replace("/", "__")


def _ruta_video(vid: str) -> Path:
    """Del identificador que maneja el panel (ruta relativa a DATA, ej.
    '1/000007.mp4') al archivo real, validando que
    no se escape de input/raw/ -- mismo criterio que src.sesion.grabacion.resolver_json."""
    base = DATA.resolve()
    candidato = (base / vid).resolve()
    if base not in candidato.parents and candidato != base:
        raise ValueError(f"ruta fuera de input/raw/: {vid}")
    return candidato


# mismo log que el panel (sistema/logs), con prefijo "dataset"
log = logger("dataset")


def _leer_json(path, defecto):
    try:
        return json.loads(path.read_text("utf-8")) if path.exists() else defecto
    except Exception:
        return defecto


def _manifest() -> list[dict]:
    """Los clips (tabla `clips`) con 'exercise' y 'type' ya resueltos en cada fila."""
    rows = INP.filas()
    for row in rows:
        row["type"] = SQL.tipo_de_ejercicio(row["exercise"])
    return rows


def _tipo_o_primero(tipo, rows=None):
    """El type pedido por el panel, o el del primer clip si no se paso."""
    if tipo not in (None, ""):
        return int(tipo)
    rows = _manifest() if rows is None else rows
    return rows[0]["type"] if rows else 1


def _exercise_de(mp4_path):
    """El ejercicio del video: su carpeta es el numero (input/raw/<n>/), que exercise.json traduce a nombre. Si el video
    esta fuera de esa estructura se lee del .json que graba GYMFITX."""
    p = Path(mp4_path)
    try:
        return INP.slug_de(int(p.parent.name))
    except ValueError:
        pass
    json_path = p.with_suffix(".json")
    if json_path.exists():
        try:
            return json.loads(json_path.read_text("utf-8")).get("exercise", "desconocido")
        except (OSError, ValueError) as e:
            log.warning("ejercicio no legible en %s: %s", json_path.name, e)
    return "desconocido"
