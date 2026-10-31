"""Quitar por completo un ejercicio archivado: sus filas en parameters/inputs.json (raw y clips), sus capas y SQL.

Archivar un ejercicio (Panel -> Rutina -> 🗑) lo deja inactivo en parameters/; esto limpia el resto para que sus
clips ya no cuenten (entrenamiento, tablas, totales). Nada se borra en el disco: las carpetas input/<capa>/<n>/ y la
plantilla pasan a sistema/archivados/<ejercicio>_<fecha>/ (recuperable). En SQL si se borra todo lo del 'type'; el numero del
type queda reservado en sql_tipos.json para no reutilizarlo. Es idempotente: si algo falla (SQL caido, un archivo
en uso) el ejercicio sigue figurando como pendiente y se reintenta."""

from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path

from src.almacenamiento import dataset_sql as SQL
from src.etiquetado import editor_puntos as EP
from src.etiquetado import exportar as EXPORTAR
from src.etiquetado.manifest import log
from src.nucleo import config as CONF
from src.nucleo import inputs as INP
from src.nucleo.config import (
    DATOS_DIR,
    EXPORT_ESTADO_PATH,
    SQL_TIPOS_PATH,
    TEMPLATES_DIR,
)

ARCHIVO_DIR = DATOS_DIR / "archivados"
PENDIENTES_PATH = DATOS_DIR / "pendientes_purga.json"     # ejercicios cuyo SQL aun no se pudo limpiar
DEPURADOS_PATH = ARCHIVO_DIR / "depurados.json"           # ya limpios: su type sigue en sql_tipos.json (reservado) pero no hay nada que quitar
SIN_EJERCICIO = "desconocido"                              # clips sin .json de origen: no se tocan
# orden por llaves foraneas: primero lo que apunta a table_file
TABLAS_DEL_TIPO = ("table_indicator", "table_frame_base", "table_frames_fix", "table_frames", "table_file",
                   "table_kpoints", "table_angles", "table_features", "table_config", "table_ejercicio")


def _leer(path, defecto):
    try:
        return json.loads(Path(path).read_text("utf-8"))
    except (OSError, ValueError):
        return defecto


def _escribir(path, datos):
    Path(path).write_text(json.dumps(datos, indent=1, ensure_ascii=False), "utf-8")


def _contar(carpeta):
    return sum(1 for _ in carpeta.rglob("*.mp4")) if carpeta.is_dir() else 0


def _capas(ej):
    """Las carpetas del ejercicio en cada capa: [(nombre de capa, ruta)]."""
    return [("raw", CONF.RECORDINGS_DIR / str(ej)), ("bronze", CONF.CLIPS_DIR / str(ej)),
            ("plate", CONF.PLATE_DIR / str(ej)), ("gold", CONF.GOLD_DIR / str(ej))]


def _pendiente(slug, si):
    p = set(_leer(PENDIENTES_PATH, []))
    (p.add if si else p.discard)(slug)
    _escribir(PENDIENTES_PATH, sorted(p))


def _depurado(slug, si):
    d = set(_leer(DEPURADOS_PATH, []))
    (d.add if si else d.discard)(slug)
    ARCHIVO_DIR.mkdir(exist_ok=True)
    _escribir(DEPURADOS_PATH, sorted(d))


def huerfanos():
    """Ejercicios que ya no estan en ejercicios/ pero aun dejan algo: clips en la tabla o en carpetas, una limpieza
    pendiente, o datos en SQL (su type en sql_tipos.json, mientras no se haya depurado)."""
    ejs = INP.ejercicios()
    nombres = ({r.get("exercise") for r in INP.filas()} | set(_leer(PENDIENTES_PATH, []))
               | (set(_leer(SQL_TIPOS_PATH, {})) - set(_leer(DEPURADOS_PATH, []))))
    for base in (CONF.CLIPS_DIR, CONF.RECORDINGS_DIR):
        if base.is_dir():
            nombres |= {ejs[int(p.name)]["slug"] for p in base.iterdir() if p.is_dir() and p.name.isdigit() and int(p.name) in ejs}
    vivos = set(EP.listar_ejercicios())
    return sorted(n for n in nombres if n and n != SIN_EJERCICIO and not n.startswith("_") and n not in vivos)


def plan():
    """Que se quitaria de cada ejercicio archivado (para confirmar antes). sql_archivos=None si SQL no responde."""
    tipos, filas = _leer(SQL_TIPOS_PATH, {}), INP.filas()
    out = [{"slug": s, "type": tipos.get(s), "clips_manifest": sum(1 for r in filas if r.get("exercise") == s),
            "clips_disco": _contar(CONF.CLIPS_DIR / str(INP.id_de(s))), "grabaciones": _contar(CONF.RECORDINGS_DIR / str(INP.id_de(s))),
            "sql_archivos": None}
           for s in huerfanos()]
    try:
        with SQL.conexion() as cx:
            for d in out:
                if d["type"] is not None:
                    d["sql_archivos"] = cx.execute("SELECT COUNT(*) FROM table_file WHERE type=?", (d["type"],)).fetchone()[0]
    except SQL.SQLServerNoDisponible:
        pass
    return out


def _purgar_sql(tipo):
    borradas = {}
    with SQL.conexion() as cx:
        for t in TABLAS_DEL_TIPO:
            borradas[t] = cx.execute(f"DELETE FROM {t} WHERE type=?", (tipo,)).rowcount
        cx.commit()
    return {"archivos": borradas["table_file"], "frames": borradas["table_frames"] + borradas["table_frames_fix"]}


def depurar(slug):
    """Deja el ejercicio 'slug' (ya archivado) fuera de las tablas, los cortes y SQL."""
    if EP.leer_ejercicio(slug) is not None:
        raise ValueError(f"'{slug}' sigue en ejercicios/: archivalo primero")
    r = {"slug": slug, "clips": 0, "movido_a": None, "errores": [], "sql": None, "sql_error": None}
    destino = ARCHIVO_DIR / f"{slug}_{datetime.now():%Y%m%d_%H%M%S}"
    ej = INP.id_de(slug)
    with EXPORTAR._EXPORT_LOCK:   # mismo candado que exportar(): la tabla se reescribe entera
        if ej is not None:
            with INP.editar() as t:
                r["clips"] = sum(1 for c in t["clips"] if c["ej"] == ej)
                vids = {INP.vid_de(x) for x in t["raw"] if x["ej"] == ej}
                t["clips"] = [c for c in t["clips"] if c["ej"] != ej]
                t["raw"] = [x for x in t["raw"] if x["ej"] != ej]
            datos = _leer(EXPORT_ESTADO_PATH, {})   # el hash de sus videos: si no, el proximo export los daria por hechos
            resto = {k: v for k, v in datos.items() if k not in vids}
            if len(resto) != len(datos):
                _escribir(EXPORT_ESTADO_PATH, resto)
            INP.desactivar_ejercicio(slug)
        origenes = [(p, capa) for capa, p in _capas(ej)] if ej is not None else []
        origenes.append((TEMPLATES_DIR / f"{slug}.npz", "plantillas"))
        for origen, sub in origenes:
            if origen.exists():
                try:
                    (destino / sub).mkdir(parents=True, exist_ok=True)
                    shutil.move(str(origen), str(destino / sub / origen.name))
                    r["movido_a"] = destino.name
                except OSError as e:   # archivo en uso: queda donde estaba y se reintenta en la proxima
                    r["errores"].append(f"{sub}: {e}")
    tipo = _leer(SQL_TIPOS_PATH, {}).get(slug)
    if tipo is not None:
        try:   # SQL caido: se anota y se reintenta (el boton de Sistema lo vuelve a intentar)
            SQL.asegurar_base_y_tablas()
            r["sql"] = _purgar_sql(tipo)
            _pendiente(slug, False)
        except SQL.SQLServerNoDisponible as e:
            r["sql_error"] = str(e)
            _pendiente(slug, True)
    if r["errores"]:
        _pendiente(slug, True)
    _depurado(slug, tipo is None or (r["sql"] is not None and not r["errores"]))
    log.info(f"depurar {slug}: {r['clips']} clips del manifest, sql={r['sql']}, sql_error={r['sql_error']}, errores={r['errores']}")
    return r


def depurar_todos(slugs=None):
    """Los ejercicios archivados que aun dejan datos (o solo los de 'slugs')."""
    pendientes = huerfanos()
    return [depurar(s) for s in pendientes if slugs is None or s in slugs]
