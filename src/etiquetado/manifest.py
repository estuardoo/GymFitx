"""Rutas e indice del dataset: que video es cual, que clips se exportaron (manifest.json) y de que ejercicio.

Lo comparten cortes, exportar, tablas y entrenamiento."""

from __future__ import annotations

import json
from pathlib import Path

from src.almacenamiento import dataset_sql as SQL
from src.nucleo.config import CLIPS_DIR, ETIQUETAS_PATH, MANIFEST_PATH, RECORDINGS_DIR
from src.nucleo.log import logger

DATA, OUT = RECORDINGS_DIR, CLIPS_DIR          # grabaciones de entrada, clips de salida


LABELS, MANIFEST = ETIQUETAS_PATH, MANIFEST_PATH


def _slug(vid: str) -> str:
    """Identificador plano y unico para nombrar clips/preview de un video, a
    partir de su ruta relativa a DATA (ej. 'sentadilla/2026-08-25/073012_serie.mp4'
    -> 'sentadilla__2026-08-25__073012_serie'). Hace falta desde que DATA paso
    a ser datos/grabaciones/ (anidada por ejercicio/fecha): el nombre pelado del
    archivo ya no identifica un video sin ambiguedad -- dos grabaciones de
    dias distintos pueden compartir el mismo HHMMSS_modo.mp4."""
    return Path(vid).with_suffix("").as_posix().replace("/", "__")


def _ruta_video(vid: str) -> Path:
    """Del identificador que maneja el panel (ruta relativa a DATA, ej.
    'sentadilla/2026-08-25/073012_serie.mp4') al archivo real, validando que
    no se escape de datos/grabaciones/ -- mismo criterio que src.sesion.grabacion.resolver_json."""
    base = DATA.resolve()
    candidato = (base / vid).resolve()
    if base not in candidato.parents and candidato != base:
        raise ValueError(f"ruta fuera de datos/grabaciones/: {vid}")
    return candidato


# mismo log que el panel (datos/gymfitx.log), con prefijo "dataset"
log = logger("dataset")


def _leer_json(path, defecto):
    try:
        return json.loads(path.read_text("utf-8")) if path.exists() else defecto
    except Exception:
        return defecto


def _manifest() -> list[dict]:
    """manifest.json con 'exercise' y 'type' ya resueltos en cada fila (antes
    se releia y completaba igual en 7 funciones distintas)."""
    rows = _leer_json(MANIFEST, [])
    for row in rows:
        if not row.get("exercise"):
            row["exercise"] = _exercise_de(DATA / row["origen"])
        row["type"] = SQL.tipo_de_ejercicio(row["exercise"])
    return rows


def _tipo_o_primero(tipo, rows=None):
    """El type pedido por el panel, o el del primer clip si no se paso."""
    if tipo not in (None, ""):
        return int(tipo)
    rows = _manifest() if rows is None else rows
    return rows[0]["type"] if rows else 1


def _exercise_de(mp4_path):
    """El ejercicio del video (mismo nombre que su ejercicios/*.yaml),
    leido del .json que graba GYMFITX -- de eso depende el 'type' en SQL y
    que puntos le importan a table_kpoints (ver nucleo/ejercicio.puntos_de_ejercicio)."""
    json_path = mp4_path.with_suffix(".json")
    if json_path.exists():
        try:
            return json.loads(json_path.read_text("utf-8")).get("exercise", "desconocido")
        except Exception:
            pass
    return "desconocido"
