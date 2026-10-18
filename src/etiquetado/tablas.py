"""Etapa 5: llevar los clips exportados a las tablas SQL (crudo, normalizado e indicador vs base).

Aqui esta la logica; almacenamiento/dataset_sql.py solo guarda y lee."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from src.almacenamiento import dataset_sql as SQL
from src.etiquetado.manifest import OUT, _manifest, _tipo_o_primero
from src.evaluacion.similitud import DTW_VERSION, indicador
from src.nucleo.config import formato_de
from src.nucleo.ejercicio import features_de_ejercicio, kpoints_de_ejercicio, puntos_de_ejercicio
from src.procesamiento.medidas import angulos as ANG
from src.procesamiento.puntos import normalizacion as NORM
from src.procesamiento.puntos import vectorizar as VEC

RESUMEN_VACIO = {"archivos_nuevos": 0, "archivos_actualizados": 0, "archivos_sin_cambios": 0,
                 "frames": 0, "frames_fix": 0, "omitidos_sin_puntos": 0}


def cfg_de_tipo(type_, point_names):
    """Normalizacion efectiva del type: la de params.yaml (formato) + defaults (procesamiento/puntos/normalizacion.py).
    Es la MISMA con la que entrena el modelo, asi la copia en SQL no diverge del disco."""
    return NORM.cfg_para(point_names, formato_de(SQL.tipos_conocidos().get(type_)))


def poblar_desde_manifest(manifest_rows, dataset_dir, type_=1):
    """Por cada clip del manifest con .npz que ya trae 'points': registra el
    archivo, el catalogo de puntos (una vez) y sus frames crudos y normalizados.
    Si la 'guia' (parametros de normalizacion + firma de puntos) no cambio para
    un archivo que ya tiene datos, se deja tal cual. Al final recalcula
    table_indicator contra el clip 'base'."""
    resumen = dict(RESUMEN_VACIO)
    catalogo_creado = False

    with SQL.conexion() as cx:
        for row in manifest_rows:
            npz_path = Path(dataset_dir) / Path(row["clip"]).parent / (row.get("npz") or "")
            if not row.get("npz") or not npz_path.exists():
                continue
            d = np.load(npz_path, allow_pickle=True)
            if "points" not in d.files or d["points"].shape[0] == 0:
                resumen["omitidos_sin_puntos"] += 1
                continue

            # misma preparacion que el clasificador en vivo (procesamiento/puntos/vectorizar.py)
            feats = features_de_ejercicio(row.get("exercise"))
            prep = VEC.preparar(d["points"], d["point_names"], puntos_de_ejercicio(row.get("exercise")),
                                kpoints_de_ejercicio(row.get("exercise")), feats)
            if prep is None:
                resumen["omitidos_sin_puntos"] += 1
                continue
            points, nombres, angulos, nombres_ang = prep
            cfg = cfg_de_tipo(type_, nombres)
            guia = f"{NORM.guia(cfg)}|sig:{NORM.firma(nombres, nombres_ang)}|ang:v{ANG.VERSION}|met:{NORM.firma([json.dumps(f, sort_keys=True) for f in feats], [])}"

            if not catalogo_creado:
                SQL.guardar_catalogo(cx, type_, nombres, nombres_ang)
                SQL.guardar_config_activa(cx, type_, cfg, guia)
                catalogo_creado = True

            archivo, clase = row["clip"], row.get("clase")
            previo = SQL.archivo_registrado(cx, type_, archivo)
            es_nuevo = previo is None
            if es_nuevo:
                file_id = SQL.crear_archivo(cx, type_, archivo, len(points), guia, clase)
            else:
                file_id, guia_previa = previo
                # misma guia y con datos: nada que hacer (sin datos = una corrida anterior fallo a medias)
                if guia_previa == guia and SQL.frames_crudos_guardados(cx, type_, file_id) > 0:
                    resumen["archivos_sin_cambios"] += 1
                    continue
                SQL.actualizar_archivo(cx, file_id, len(points), guia, clase)

            SQL.borrar_frames(cx, type_, file_id)
            SQL.insertar_frames(cx, "table_frames", type_, file_id, points, angulos)
            resumen["frames"] += len(points)
            fijo, angulos_fijo = VEC.fijo(points, nombres, angulos, cfg, feats)
            SQL.insertar_frames(cx, "table_frames_fix", type_, file_id, fijo, angulos_fijo)
            resumen["frames_fix"] += len(fijo)
            resumen["archivos_nuevos" if es_nuevo else "archivos_actualizados"] += 1
            cx.commit()

        _actualizar_indicadores(cx, type_)

    return resumen


def respaldar_sql(rows):
    """Copia a SQL Server los clips que ya estan en disco (el disco manda; SQL es respaldo y alimenta Descomposicion /
    Ranking). -> {"resumen": contadores | None, "error": texto | None}. Nunca lanza: si SQL no responde solo lo cuenta."""
    try:
        SQL.asegurar_base_y_tablas()
        por_tipo = {}
        for row in rows:   # 'type' = ejercicio: cada uno tiene su propio catalogo de puntos
            por_tipo.setdefault(SQL.tipo_de_ejercicio(row.get("exercise", "desconocido")), []).append(row)
        resumen = dict(RESUMEN_VACIO)
        for tipo, rows_tipo in por_tipo.items():
            for k, v in poblar_desde_manifest(rows_tipo, OUT, type_=tipo).items():
                resumen[k] += v
        return {"resumen": resumen, "error": None}
    except SQL.SQLServerNoDisponible as e:
        return {"resumen": None, "error": str(e)}


def _actualizar_indicadores(cx, type_):
    """table_indicator de cada clip contra el clip 'base' de su type. La llave
    (archivo base + su guia_fix + version del DTW) evita recalcular lo que no cambio."""
    base = SQL.base_del_tipo(cx, type_)
    if not base:
        return
    base_file_id, base_archivo, base_guia_fix = base
    SQL.copiar_a_frame_base(cx, type_, base_file_id)
    guia = f"{base_archivo}|{base_guia_fix}|dtw:v{DTW_VERSION}"

    nombres = SQL.nombres_kpoints(cx, type_)
    if not nombres:
        return
    frames_base = SQL._frames_de_con(cx, type_, base_archivo, nombres)
    for file_id, archivo in SQL.otros_archivos(cx, type_, base_file_id):
        if SQL.indicadores_con_guia(cx, type_, file_id, guia) == len(nombres):
            continue
        frames_otro = SQL._frames_de_con(cx, type_, archivo, nombres)
        valores = [(i, indicador(frames_base[kp], frames_otro[kp]))
                   for i, kp in enumerate(nombres) if frames_otro.get(kp, {}).get("x")]
        SQL.reemplazar_indicadores(cx, type_, file_id, base_file_id, guia, valores)
    cx.commit()


def catalogo_puntos_disponible(manifest_rows, dataset_dir):
    """Nombres de puntos del primer clip que ya tenga 'points', filtrados por
    el .yaml de su ejercicio -- para los <select> del panel sin conectarse a SQL."""
    for row in manifest_rows:
        npz_path = Path(dataset_dir) / Path(row["clip"]).parent / (row.get("npz") or "")
        if row.get("npz") and npz_path.exists():
            d = np.load(npz_path, allow_pickle=True)
            if "point_names" in d.files:
                todos = [str(n) for n in d["point_names"]]
                deseados = puntos_de_ejercicio(row.get("exercise"))
                return [n for n in deseados if n in todos] if deseados else todos
    return []


def sql_estado(tipo=None):
    """Para Sistema → Tablas del dataset: conexion + puntos disponibles + config del ejercicio
    ('tipo') elegido en el selector (antes siempre el del primer clip)."""
    todas = _manifest()
    tipo = _tipo_o_primero(tipo, todas)
    rows = [r for r in todas if r["type"] == tipo]
    puntos = catalogo_puntos_disponible(rows, OUT)

    def _sin_puntos(r):
        p = OUT / Path(r["clip"]).parent / (r.get("npz") or "")
        return r.get("npz") and p.exists() and "points" not in np.load(p, allow_pickle=True).files

    sin_puntos = sum(1 for r in rows if _sin_puntos(r))
    return {**SQL.estado(), "tipo": tipo, "tipos": SQL.tipos_conocidos(), "puntos_disponibles": puntos,
            "config": cfg_de_tipo(tipo, puntos) if puntos else NORM.DEFAULT_CFG,
            "clips_sin_puntos_crudos": sin_puntos, "clips_totales": len(rows)}


def tipos_disponibles():
    _manifest()  # registra en sql_tipos.json cualquier ejercicio nuevo
    return SQL.tipos_conocidos()


def sql_guardar_config(body, tipo=None):
    tipo = _tipo_o_primero(tipo)
    cfg = SQL.config()
    cfg[str(tipo)] = body
    SQL.guardar_config(cfg)
    return {"ok": True, "tipo": tipo, "aviso": "Guardado, pero la normalizacion que usan las tablas y el entrenamiento sale de params.yaml (formato): cambiala ahi para que cuente."}
