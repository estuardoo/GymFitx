"""Quitar por completo un ejercicio archivado: manifest, cortes, seleccion de entrenamiento y SQL.

Archivar un ejercicio (Panel -> Rutina -> 🗑) saca su .yaml de ejercicios/; esto limpia el resto para que sus
clips ya no cuenten (entrenamiento, tablas, totales). Nada se borra en el disco: clips, grabaciones y plantilla
pasan a datos/archivados/<ejercicio>_<fecha>/ (recuperable). En SQL si se borra todo lo del 'type'; el numero del
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
from src.nucleo.config import (
    CLIPS_DIR,
    DATOS_DIR,
    ETIQUETAS_PATH,
    EXPORT_ESTADO_PATH,
    MANIFEST_PATH,
    RECORDINGS_DIR,
    SELECCION_PATH,
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
    """Ejercicios que ya no estan en ejercicios/ pero aun dejan algo: clips en el manifest o en carpetas, una limpieza
    pendiente, o datos en SQL (su type en sql_tipos.json, mientras no se haya depurado)."""
    nombres = ({r.get("exercise") for r in _leer(MANIFEST_PATH, [])} | set(_leer(PENDIENTES_PATH, []))
               | (set(_leer(SQL_TIPOS_PATH, {})) - set(_leer(DEPURADOS_PATH, []))))
    for base in (CLIPS_DIR, RECORDINGS_DIR):
        if base.is_dir():
            nombres |= {p.name for p in base.iterdir() if p.is_dir()}
    vivos = set(EP.listar_ejercicios())
    return sorted(n for n in nombres if n and n != SIN_EJERCICIO and not n.startswith("_") and n not in vivos)


def plan():
    """Que se quitaria de cada ejercicio archivado (para confirmar antes). sql_archivos=None si SQL no responde."""
    tipos, manifest = _leer(SQL_TIPOS_PATH, {}), _leer(MANIFEST_PATH, [])
    out = [{"slug": s, "type": tipos.get(s), "clips_manifest": sum(1 for r in manifest if r.get("exercise") == s),
            "clips_disco": _contar(CLIPS_DIR / s), "grabaciones": _contar(RECORDINGS_DIR / s), "sql_archivos": None}
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
    """Deja el ejercicio 'slug' (ya archivado) fuera del manifest, los cortes, la seleccion y SQL."""
    if EP.leer_ejercicio(slug) is not None:
        raise ValueError(f"'{slug}' sigue en ejercicios/: archivalo primero")
    r = {"slug": slug, "clips": 0, "movido_a": None, "errores": [], "sql": None, "sql_error": None}
    destino = ARCHIVO_DIR / f"{slug}_{datetime.now():%Y%m%d_%H%M%S}"
    with EXPORTAR._EXPORT_LOCK:   # mismo candado que exportar(): manifest.json se reescribe entero
        manifest = _leer(MANIFEST_PATH, [])
        quitar = [x for x in manifest if x.get("exercise") == slug]
        if quitar:
            _escribir(MANIFEST_PATH, [x for x in manifest if x.get("exercise") != slug])
            sel = _leer(SELECCION_PATH, {})
            claves = {"/".join(Path(x["clip"]).parts[1:]) for x in quitar}   # "clase/nombre.mp4"
            if any(k in sel for k in claves):
                _escribir(SELECCION_PATH, {k: v for k, v in sel.items() if k not in claves})
        for path in (ETIQUETAS_PATH, EXPORT_ESTADO_PATH):   # cortes de sus videos: si no, el proximo export los recrearia
            datos = _leer(path, {})
            resto = {k: v for k, v in datos.items() if not k.startswith(slug + "/")}
            if len(resto) != len(datos):
                _escribir(path, resto)
        r["clips"] = len(quitar)
        for origen, sub in ((CLIPS_DIR / slug, "clips"), (RECORDINGS_DIR / slug, "grabaciones"),
                            (TEMPLATES_DIR / f"{slug}.npz", "plantillas")):
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
