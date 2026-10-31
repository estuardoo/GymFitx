"""Etapa 4: exportar cada segmento etiquetado como clip (.mp4 + .npz con sus kpoints) al disco y, si Sistema lo pide
(respaldo_sql.al_cortar), copiarlo a SQL.

Cada clip es una fila de la tabla `clips` (parameters/inputs.json) y vive en input/bronze/<ej>/<id>.{mp4,npz}. Un corte que ya
tenia clip (mismo video y numero de corte) conserva su id al volver a exportar. Salta los videos cuyos cortes no cambiaron
(hash por video en sistema/export_estado.json)."""

from __future__ import annotations

import json
import subprocess
import threading

from src.almacenamiento import dataset_sql as SQL
from src.etiquetado.manifest import DATA, _exercise_de, _ruta_video, log
from src.etiquetado.previews import ffmpeg_exe
from src.etiquetado.tablas import RESUMEN_VACIO, respaldar_sql
from src.nucleo import config as CONF
from src.nucleo import inputs as INP
from src.nucleo.config import EXPORT_ESTADO_PATH, INPUTS_PATH, respaldo_sql
from src.procesamiento import offline as deteccion


def recorta_npz(src, ini, fin, dst):
    """Recorta values/t_ms del npz hermano al rango [ini,fin] en segundos.
    Si el npz del video fuente ya trae keypoints crudos (points/point_names/
    -- grabaciones nuevas de GYMFITX), los recorta igual y los copia al
    clip: sin esto, table_frames/table_frames_fix en SQL quedaban siempre
    vacias aunque el video fuente si tuviera los puntos."""
    try:
        import numpy as np
    except ImportError:
        return None
    npz = src.with_suffix(".npz")
    if not npz.exists():
        return None
    d = np.load(npz, allow_pickle=False)
    t = d["t_ms"] - d["t_ms"][0]
    m = (t >= ini * 1000) & (t <= fin * 1000)
    extra = {}
    if "points" in d.files:
        if "points_t_ms" in d.files:
            # src/procesamiento/offline.py: eje de tiempo propio (re-decodifico el video, no
            # coincide frame a frame con el t_ms de las features en vivo).
            # Corregido: ese eje YA empieza en el cuadro 0 del video (i*1000/fps),
            # asi que no se le resta su primer valor -- antes, si la mano no
            # aparecia en el primer cuadro, todo el recorte quedaba corrido.
            tp = d["points_t_ms"]
            mp_ = (tp >= ini * 1000) & (tp <= fin * 1000)
            # relativo al INICIO DEL CLIP (no del video fuente): lo que necesita SIM (pestana SIM) para
            # sincronizar el overlay de puntos con la reproduccion del .mp4 YA CORTADO.
            extra["points_t_ms"] = tp[mp_] - ini * 1000
        else:
            mp_ = m  # puntos grabados en vivo por GYMFITX: mismo eje que values/t_ms
        extra["points"] = d["points"][mp_]
        extra["point_names"] = d["point_names"]
        if "points_screen" in d.files:   # coordenadas 0-1 para dibujar overlay sobre el video (ver SIM)
            extra["points_screen"] = d["points_screen"][mp_]
    # Mejora: antes, si no caia ninguna feature en vivo (~7 fps) dentro del
    # segmento, el clip quedaba SIN .npz aunque si tuviera puntos detectados
    # (y SQL lo omitia). Ahora solo se descarta si no hay ni una cosa ni la otra.
    if not m.any() and not len(extra.get("points", ())):
        return None
    np.savez(dst, values=d["values"][m], t_ms=d["t_ms"][m], names=d["names"], units=d["units"], **extra)
    return dst.name


def _quitar_archivos(ej, cid):
    for ext in ("mp4", "npz"):
        INP.ruta_clip(ej, cid, ext).unlink(missing_ok=True)


ESTADO = EXPORT_ESTADO_PATH  # hash de segmentos por video en el ultimo export, para saltar los que no cambiaron


def _hash(segmentos, tiene_puntos=False):
    import hashlib
    payload = json.dumps({"segmentos": segmentos, "tiene_puntos": tiene_puntos}, sort_keys=True)
    return hashlib.sha1(payload.encode()).hexdigest()


def _npz_tiene_puntos(mp4_path):
    """Sin correr deteccion: firma de los puntos crudos que YA trae el .npz
    hermano ('' si no tiene). Si cambia el catalogo de puntos cambia la firma
    y los clips se vuelven a recortar con los puntos nuevos."""
    npz = mp4_path.with_suffix(".npz")
    if not npz.exists():
        return ""
    import numpy as np
    try:
        d = np.load(npz, allow_pickle=False)
        if "points" not in d.files:
            return ""
        v = int(d["deteccion_version"]) if "deteccion_version" in d.files else 1
        return f"v{v}:" + "|".join(str(n) for n in d["point_names"])
    except Exception:
        return ""


_EXPORT_LOCK = threading.Lock()
PROGRESO = {"activo": False, "hecho": 0, "total": 0, "video": ""}   # lo lee GET /api/export_progreso (videos, no cortes)


_CONTAR = set()


def _avanzar(vid):
    if vid in _CONTAR:
        PROGRESO["hecho"] += 1


def _videos_a_cortar(labels):
    def con_clase(info):
        return any(s.get("clase") in INP.EXPORTABLES for s in info.get("segmentos", []))
    out = []
    for vid, info in labels.items():
        try:
            if con_clase(info) and _ruta_video(vid).exists():
                out.append(vid)
        except ValueError:
            continue
    return out


def exportar(labels, todo=False, subir_sql=None):
    """Un solo export a la vez: dos clics seguidos (o 'Generar cortes' + 'Generar
    tablas') corrian en paralelo e insertaban el mismo clip dos veces en SQL
    (UNIQUE KEY UQ_table_file_type_archivo, visto en cortador.log)."""
    with _EXPORT_LOCK:
        _CONTAR.clear()
        _CONTAR.update(_videos_a_cortar(labels))
        PROGRESO.update(activo=True, hecho=0, total=len(_CONTAR), video="")
        try:
            return _exportar(labels, todo, respaldo_sql()["al_cortar"] if subir_sql is None else subir_sql)
        finally:
            PROGRESO["activo"] = False


def _planear(vid, segs, exercise):
    """Dentro de la tabla: un clip por corte bien/mal (reusa el id del corte que ya tenia) y fuera los que sobran.
    -> (ej, [(seg, clip_row)], ids_sobrantes) o None si el video no esta en la tabla `raw`."""
    with INP.editar() as t:
        raw = INP.raw_de_vid(vid, t)
        if raw is None:
            return None
        previos = {c.get("seg"): c for c in t["clips"] if c.get("raw_id") == raw["id"]}
        plan = []
        for i, seg in enumerate(segs, 1):
            if seg.get("clase") not in INP.EXPORTABLES:
                continue
            campos = {"etiqueta": INP.ETIQUETA_DE[seg["clase"]], "t_ini_ms": round(seg["ini"] * 1000),
                      "t_fin_ms": round(seg["fin"] * 1000), "reps": seg.get("reps", 0)}
            c = previos.pop(i, None)
            if c is None:
                c = INP.registrar_clip(t, exercise, raw_id=raw["id"], seg=i, **campos)
            else:
                c.update(campos, rev=c.get("rev", 1) + 1)
            plan.append((i, seg, c))
        sobran = list(previos.values())
        t["clips"] = [c for c in t["clips"] if c not in sobran]
        return raw["ej"], plan, [c["id"] for c in sobran]


def _exportar(labels, todo, subir_sql):
    estado = json.loads(ESTADO.read_text("utf-8")) if ESTADO.exists() else {}
    prev_rows = {}
    for row in INP.filas():
        prev_rows.setdefault(row["origen"], []).append(row)

    errs, saltados = [], 0
    deteccion_errores = {}
    for vid, info in labels.items():
        try:
            src = _ruta_video(vid)
        except ValueError:
            continue
        if not src.exists():
            continue
        segs = info.get("segmentos", [])
        exercise = _exercise_de(src)  # se resuelve antes: src/procesamiento/offline.py lo necesita para saber que catalogo de kpoints usar
        try:  # ponytail: si no hay mediapipe a mano, se sigue sin puntos crudos...
            deteccion.detectar_puntos_si_faltan(src, exercise)
        except deteccion.DeteccionNoDisponible as e:
            # ...pero hay que decir por que, o el panel se ve "vacio" sin explicacion
            deteccion_errores[vid] = str(e)
        PROGRESO["video"] = vid
        h = _hash(segs, _npz_tiene_puntos(src))
        prev = prev_rows.get(vid, [])
        # el hash sin cambios solo confirma que los CORTES no cambiaron -- si alguien borro los .mp4/.npz ya exportados por
        # fuera de esta app, hay que re-exportar de todas formas en vez de arrastrar filas que apuntan a archivos que no existen.
        if not todo and estado.get(vid) == h and all((CONF.CLIPS_DIR / r["clip"]).exists() for r in prev):
            saltados += 1
            _avanzar(vid)
            continue
        plan = _planear(vid, segs, exercise)
        if plan is None:
            continue
        ej, cortes, sobran = plan
        for cid in sobran:
            _quitar_archivos(ej, cid)
        malos = []
        for i, seg, c in cortes:
            mp4, npz = INP.ruta_clip(ej, c["id"], "mp4"), INP.ruta_clip(ej, c["id"], "npz")
            mp4.unlink(missing_ok=True)   # los migrados son enlaces duros a datos/: se escribe un archivo nuevo, no el original
            npz.unlink(missing_ok=True)
            cmd = [ffmpeg_exe(), "-y", "-hide_banner", "-loglevel", "error", "-i", str(src),
                   "-ss", f"{seg['ini']:.3f}", "-to", f"{seg['fin']:.3f}",
                   "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-an", str(mp4)]
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode:
                errs.append(f"{vid} corte {i}: {(r.stderr or '')[:180]}")
                malos.append(c["id"])
                continue
            if recorta_npz(src, seg["ini"], seg["fin"], npz) is None:
                npz.unlink(missing_ok=True)
        if malos:   # sin video no hay clip: fuera de la tabla
            with INP.editar() as t:
                t["clips"] = [c for c in t["clips"] if c["id"] not in malos]
            for cid in malos:
                _quitar_archivos(ej, cid)
        estado[vid] = h
        _avanzar(vid)
    rows = INP.filas()
    ESTADO.write_text(json.dumps(estado, indent=1), "utf-8")

    sql_resumen, sql_error = None, None
    if subir_sql:   # el corte ya quedo en disco; si el SQL Server no responde, solo se avisa
        copia = respaldar_sql(rows)
        sql_resumen, sql_error = copia["resumen"], copia["error"]

    log.info(f"exportar: {len(rows)} clips, {saltados} saltados, {len(errs)} errores"
             f"{f', sql_error={sql_error}' if sql_error else f', sql={sql_resumen}'}"
             f"{f', deteccion_errores={deteccion_errores}' if deteccion_errores else ''}")
    return {"clips": len(rows), "errores": errs, "manifest": INPUTS_PATH.name, "saltados": saltados,
            "sql": sql_resumen, "sql_error": sql_error, "deteccion_errores": deteccion_errores}


def estado_export():
    labels = INP.leer_labels()
    estado = json.loads(ESTADO.read_text("utf-8")) if ESTADO.exists() else {}
    total = pend = 0
    for vid, info in labels.items():
        segs = info.get("segmentos", [])
        if not any(s.get("clase") in INP.EXPORTABLES for s in segs):
            continue
        total += 1
        if estado.get(vid) != _hash(segs, _npz_tiene_puntos(DATA / vid)):
            pend += 1
    return {"pendientes": pend, "total": total}


def sql_generar():
    """Boton manual de Sistema → Tablas del dataset. No lee la tabla de clips y ya -- eso solo
    veria los clips como quedaron la ULTIMA vez que se corto, y un clip
    cortado antes de tener deteccion de puntos se quedaria "omitido_sin_puntos"
    para siempre por mas veces que le des click. Por eso reusa exportar():
    si a un video le faltan puntos los detecta y re-recorta antes de subir a
    SQL (exportar ya se salta los que no cambiaron, via el hash)."""
    r = exportar(INP.leer_labels(), subir_sql=True)   # boton manual: sube aunque el respaldo automatico este apagado
    if r["sql_error"]:
        raise SQL.SQLServerNoDisponible(r["sql_error"])
    resumen = r["sql"] or dict(RESUMEN_VACIO)
    log.info(f"sql_generar: {resumen}")
    return {**resumen, "deteccion_errores": r["deteccion_errores"]}
