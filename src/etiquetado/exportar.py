"""Etapa 4: exportar cada segmento etiquetado como clip (.mp4 + .npz con sus kpoints) al disco y, si Sistema lo pide
(respaldo_sql.al_cortar), copiarlo a SQL.

Salta los videos cuyos cortes no cambiaron (hash por video en export_estado.json)."""

from __future__ import annotations

import json
import subprocess
import threading

from src.almacenamiento import dataset_sql as SQL
from src.etiquetado.cortes import CFG
from src.etiquetado.manifest import DATA, LABELS, MANIFEST, OUT, _exercise_de, _manifest, _ruta_video, _slug, log
from src.etiquetado.previews import ffmpeg_exe
from src.etiquetado.tablas import RESUMEN_VACIO, respaldar_sql
from src.nucleo.config import EXPORT_ESTADO_PATH, respaldo_sql
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
    d = np.load(npz, allow_pickle=True)
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


def limpiar_previos(labels):
    """Borra los clips ya exportados de estos videos antes de recortar de nuevo (evita huerfanos si cambiaste la cantidad o clase de los cortes)."""
    for vid in labels:
        slug = _slug(vid)
        for f in OUT.glob(f"*/*/{slug}_s*"):   # OUT/<ejercicio>/<clase>/<archivo>
            f.unlink()


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
        d = np.load(npz, allow_pickle=True)
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
        return any(s.get("clase") and s["clase"] not in CFG["no_exportar"] for s in info.get("segmentos", []))
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


def _exportar(labels, todo, subir_sql):
    estado = json.loads(ESTADO.read_text("utf-8")) if ESTADO.exists() else {}
    prev_rows = {}
    for row in _manifest():
        row.pop("type", None)   # derivado, no se guarda en manifest.json
        prev_rows.setdefault(row["origen"], []).append(row)

    rows, errs, saltados = [], [], 0
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
        # el hash sin cambios solo confirma que los CORTES no cambiaron -- si
        # alguien borro los .mp4/.npz ya exportados por fuera de esta app (o
        # quedaron huerfanos de una corrida anterior), hay que re-exportar de
        # todas formas en vez de arrastrar filas de manifest.json que apuntan
        # a archivos que ya no existen (eso es lo que se ve como "cortes que
        # no cargan").
        if not todo and estado.get(vid) == h and all((OUT / r["clip"]).exists() for r in prev):
            rows.extend(prev)
            saltados += 1
            _avanzar(vid)
            continue
        limpiar_previos({vid: info})
        for i, seg in enumerate(segs, 1):
            cl = seg.get("clase")
            if not cl or cl in CFG["no_exportar"]:
                continue
            d = OUT / exercise / cl
            d.mkdir(parents=True, exist_ok=True)
            name = f"{_slug(vid)}_s{i:02d}_{cl}_r{seg.get('reps', 0)}"
            cmd = [ffmpeg_exe(), "-y", "-hide_banner", "-loglevel", "error", "-i", str(src),
                   "-ss", f"{seg['ini']:.3f}", "-to", f"{seg['fin']:.3f}",
                   "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-an",
                   str(d / (name + ".mp4"))]
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode:
                errs.append(f"{name}: {(r.stderr or '')[:180]}")
                continue
            rows.append({"clip": f"{exercise}/{cl}/{name}.mp4", "npz": recorta_npz(src, seg["ini"], seg["fin"], d / (name + ".npz")),
                         "origen": vid, "seg": i, "clase": cl, "reps": seg.get("reps", 0),
                         "ini": round(seg["ini"], 3),
                         "fin": round(seg["fin"], 3), "dur": round(seg["fin"] - seg["ini"], 3),
                         "exercise": exercise})
        estado[vid] = h
        _avanzar(vid)
    # clips de un 'origen' que no esta en labels (importados aparte, sin video fuente que cortar aqui):
    # se conservan tal cual -- si no, este write_text los borraba del manifest en el proximo "Generar".
    rows.extend(r for origen, prev in prev_rows.items() if origen not in labels for r in prev)
    MANIFEST.write_text(json.dumps(rows, indent=2, ensure_ascii=False), "utf-8")
    ESTADO.write_text(json.dumps(estado, indent=1), "utf-8")

    sql_resumen, sql_error = None, None
    if subir_sql:   # el corte ya quedo en disco; si el SQL Server no responde, solo se avisa
        copia = respaldar_sql(rows)
        sql_resumen, sql_error = copia["resumen"], copia["error"]

    log.info(f"exportar: {len(rows)} clips, {saltados} saltados, {len(errs)} errores"
             f"{f', sql_error={sql_error}' if sql_error else f', sql={sql_resumen}'}"
             f"{f', deteccion_errores={deteccion_errores}' if deteccion_errores else ''}")
    return {"clips": len(rows), "errores": errs, "manifest": MANIFEST.name, "saltados": saltados,
            "sql": sql_resumen, "sql_error": sql_error, "deteccion_errores": deteccion_errores}


def estado_export():
    labels = json.loads(LABELS.read_text("utf-8")) if LABELS.exists() else {}
    estado = json.loads(ESTADO.read_text("utf-8")) if ESTADO.exists() else {}
    total = pend = 0
    for vid, info in labels.items():
        segs = info.get("segmentos", [])
        if not any(s.get("clase") for s in segs):
            continue
        total += 1
        if estado.get(vid) != _hash(segs, _npz_tiene_puntos(DATA / vid)):
            pend += 1
    return {"pendientes": pend, "total": total}


def sql_generar():
    """Boton manual de Sistema → Tablas del dataset. No lee manifest.json y ya -- eso solo
    veria los clips como quedaron la ULTIMA vez que se corto, y un clip
    cortado antes de tener deteccion de puntos se quedaria "omitido_sin_puntos"
    para siempre por mas veces que le des click. Por eso reusa exportar():
    si a un video le faltan puntos los detecta y re-recorta antes de subir a
    SQL (exportar ya se salta los que no cambiaron, via el hash)."""
    labels = json.loads(LABELS.read_text("utf-8")) if LABELS.exists() else {}
    r = exportar(labels, subir_sql=True)   # boton manual: sube aunque el respaldo automatico este apagado
    if r["sql_error"]:
        raise SQL.SQLServerNoDisponible(r["sql_error"])
    resumen = r["sql"] or dict(RESUMEN_VACIO)
    log.info(f"sql_generar: {resumen}")
    return {**resumen, "deteccion_errores": r["deteccion_errores"]}
