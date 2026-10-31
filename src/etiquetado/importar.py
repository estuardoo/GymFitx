"""Subir clips ya cortados (bien / mal) a un ejercicio, sin pasar por grabacion + etiquetado.

Cada clip queda como si lo hubiera exportado el panel: una fila en la tabla `clips` (parameters/inputs.json, etiqueta 1/0 y
persona si se sabe) y sus archivos input/bronze/<n del ejercicio>/<id>.mp4 + .npz con los puntos del catalogo. Si el SQL
Server responde, registro en SQL (poblar_desde_manifest); si no, el clip queda local y "Sistema -> Generar tablas" lo sube
despues. Un clip sin video fuente (raw_id vacio) lleva su propia persona."""

from __future__ import annotations

import csv
import io
import json
import re
import subprocess
import tempfile
import threading
from pathlib import Path

import numpy as np

from src.almacenamiento import dataset_sql as SQL
from src.etiquetado import editor_puntos as EP
from src.etiquetado import exportar as EXPORTAR
from src.etiquetado.manifest import OUT, log
from src.etiquetado.previews import ffmpeg_exe
from src.etiquetado.tablas import poblar_desde_manifest
from src.nucleo import inputs as INP
from src.procesamiento import offline as deteccion

CLASES = INP.EXPORTABLES   # ('bien', 'mal'): la clase base ya no existe
_VIDEO = re.compile(r"\.(mp4|mov|avi|mkv|webm|m4v)$", re.I)


def _nombre(original: str) -> str:
    stem = re.sub(r"[^a-z0-9_-]+", "_", Path(original).stem.lower()).strip("_") or "clip"
    return stem[:60]


def _duracion(mp4: Path) -> float:
    import cv2
    cap = cv2.VideoCapture(str(mp4))
    try:
        fps = cap.get(cv2.CAP_PROP_FPS) or 0
        return round(cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps, 3) if fps else 0.0
    finally:
        cap.release()


def _quitar_clip(row):
    for ext in ("mp4", "npz"):
        (OUT / row["clip"]).with_suffix("." + ext).unlink(missing_ok=True)
    with INP.editar() as t:
        t["clips"] = [c for c in t["clips"] if INP.clave(c) != row["clip"]]


def _fila(cid):
    return next(r for r in INP.filas() if r["id"] == cid)


def _una(slug, clase, nombre_original, src: Path, extras=None):
    """Un archivo: transcodifica, detecta puntos, registra el clip y devuelve su fila (o lanza)."""
    extras = extras or {}
    with INP.editar() as t:
        c = INP.registrar_clip(t, slug, etiqueta=INP.ETIQUETA_DE[clase], t_ini_ms=0, t_fin_ms=0, seg=1,
                               persona=extras.get("persona") or None,
                               origen_viejo=f"importados/{slug}/{_nombre(nombre_original)}.mp4")
        c["nombre"] = _nombre(nombre_original)
        c.update({k: extras[k] for k in ("vista", "fecha", "video_origen") if extras.get(k)})
        cid, ej = c["id"], c["ej"]
    mp4, npz = INP.ruta_clip(ej, cid, "mp4"), INP.ruta_clip(ej, cid, "npz")
    try:
        r = subprocess.run([ffmpeg_exe(), "-y", "-hide_banner", "-loglevel", "error", "-i", str(src),
                            "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-an", str(mp4)],
                           capture_output=True, text=True)
        if r.returncode:
            raise ValueError(f"ffmpeg no pudo leer el video: {(r.stderr or '')[:160]}")
        # npz minimo con los campos que espera recorta_npz; los puntos los agrega la deteccion
        np.savez_compressed(npz, values=np.zeros((0, 0), np.float32), t_ms=np.zeros(0, np.int64),
                            names=np.array([], dtype=str), units=np.array([], dtype=str))
        deteccion.detectar_puntos_si_faltan(mp4, slug)   # DeteccionNoDisponible sube tal cual
        if "points" not in np.load(npz, allow_pickle=False).files:
            raise ValueError("no se detecto ninguna persona en el video")
        dur = _duracion(mp4)
    except Exception:
        mp4.unlink(missing_ok=True)
        npz.unlink(missing_ok=True)
        with INP.editar() as t:
            t["clips"] = [c for c in t["clips"] if c["id"] != cid]
        raise
    with INP.editar() as t:
        for c in t["clips"]:
            if c["id"] == cid:
                c["t_fin_ms"] = round(dur * 1000)
    return _fila(cid)


def importar_clips(slug, clase, archivos, reemplazar=False, avance=None):
    """archivos: [(nombre_original, ruta_temporal[, extras])]; extras (persona, vista, fecha...) van a la fila del clip.
    `reemplazar` ya no hace nada (no hay clip base que reemplazar). Devuelve {"ok": [clips], "errores": [str],
    "sql": resumen|None, "sql_error": str|None}."""
    if clase not in CLASES:
        raise ValueError(f"clase invalida: {clase} (solo {', '.join(CLASES)})")
    if EP.leer_ejercicio(slug) is None:
        raise ValueError(f"no existe el ejercicio '{slug}'")
    out = {"ok": [], "errores": [], "sql": None, "sql_error": None}

    nuevas = []
    for nombre, ruta, *extra in archivos:
        if avance:
            avance(nombre)
        if not _VIDEO.search(nombre or ""):
            out["errores"].append(f"{nombre}: no es un video")
            continue
        try:
            nuevas.append(_una(slug, clase, nombre, Path(ruta), extra[0] if extra else None))
        except (ValueError, deteccion.DeteccionNoDisponible) as e:
            out["errores"].append(f"{nombre}: {e}")
    if not nuevas:
        return out
    out["ok"] = [r["clip"] for r in nuevas]

    try:   # SQL caido: el clip ya quedo local, "Generar tablas" lo sube luego
        SQL.asegurar_base_y_tablas()
        tipo = SQL.tipo_de_ejercicio(slug)
        out["sql"] = poblar_desde_manifest(nuevas, OUT, type_=tipo)
    except SQL.SQLServerNoDisponible as e:
        out["sql_error"] = str(e)
    log.info(f"importar {slug}/{clase}: {len(nuevas)} clips, {len(out['errores'])} errores, "
             f"sql_error={out['sql_error']}")
    return out


def guardar_subidas(subidas):
    """[(nombre, file-like)] -> (carpeta temporal a cerrar, [(nombre, ruta)])."""
    tmp = tempfile.TemporaryDirectory(prefix="gymfitx_up_")
    out = []
    for i, (nombre, f) in enumerate(subidas):
        p = Path(tmp.name) / f"{i}{Path(nombre or '').suffix}"
        with open(p, "wb") as dst:
            while chunk := f.read(1 << 20):
                dst.write(chunk)
        out.append((nombre, p))
    return tmp, out


# ---------------------------------------------------------------------------
# Carpeta completa: <carpeta>/{Bien,Mal}/P1..Pn/*.mp4 (+ indice.csv opcional con persona/vista/fecha). Una carpeta Base se ignora.
# ---------------------------------------------------------------------------
PROGRESO = {"activo": False, "hecho": 0, "total": 0, "archivo": "", "resultado": None}


def _natural(txt):
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", txt.lower())]


def listar_carpeta(carpeta):
    """[(clase, nombre, ruta, extras)] ordenado por clase, persona (P1, P2, ... P10) y nombre."""
    base = Path(carpeta)
    if not base.is_dir():
        raise ValueError(f"no existe la carpeta: {carpeta}")
    indice = {}
    if (base / "indice.csv").exists():
        with open(base / "indice.csv", encoding="utf-8-sig", newline="") as f:
            indice = {r["archivo"].replace("\\", "/"): r for r in csv.DictReader(f)}
    out = []
    for clase in CLASES:
        d = next((p for p in base.iterdir() if p.is_dir() and p.name.lower() == clase), None)
        if d is None:
            continue
        for f in sorted((p for p in d.rglob("*") if p.is_file() and _VIDEO.search(p.name)),
                        key=lambda p: (_natural(p.parent.name), p.name)):
            r = indice.get(f.relative_to(base).as_posix(), {})
            persona = f.parent.name if f.parent != d else r.get("persona", "")
            extras = {k: v for k, v in {"persona": persona, "vista": r.get("vista"), "fecha": r.get("fecha"),
                                         "video_origen": r.get("video_origen")}.items() if v}
            out.append((clase, f.name, f, extras))
    return out


def _unir(clips, destino):
    """Concatena mp4 (mismo origen, mismos parametros) en uno solo: copia directa; si no cuadra, re-codifica."""
    with tempfile.TemporaryDirectory(prefix="gymfitx_cat_") as tmp:
        lista = Path(tmp) / "lista.txt"
        lista.write_text("".join("file '" + p.resolve().as_posix().replace("'", "'\\''") + "'\n" for p in clips), "utf-8")
        for codec in (["-c", "copy"], ["-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-an"]):
            r = subprocess.run([ffmpeg_exe(), "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0",
                                "-i", str(lista), *codec, str(destino)], capture_output=True, text=True)
            if not r.returncode:
                return
        raise ValueError(f"ffmpeg no pudo unir los clips: {(r.stderr or '')[:160]}")


def _npz_unido(clips, durs, destino):
    """npz del video reconstruido = los puntos de cada clip, uno detras de otro con su tiempo desplazado (no se
    vuelve a detectar). Sin 'points' en algun clip no hay npz (el panel lo detecta al exportar)."""
    import numpy as np

    from src.procesamiento.puntos.kpoints import VERSION_DETECCION
    pts, tms, scr, off, nombres, version = [], [], [], 0.0, None, VERSION_DETECCION
    for clip, dur in zip(clips, durs, strict=True):
        d = np.load(clip.with_suffix(".npz"), allow_pickle=False)
        if "points" not in d.files:
            return False
        n = len(d["points"])
        t = d["points_t_ms"] if "points_t_ms" in d.files else np.arange(n) * (dur * 1000.0 / max(n, 1))
        pts.append(d["points"])
        tms.append(np.asarray(t, dtype=np.float64) + off * 1000.0)
        if "points_screen" in d.files:
            scr.append(d["points_screen"])
        nombres = d["point_names"] if nombres is None else nombres
        version = int(d["deteccion_version"]) if "deteccion_version" in d.files else version
        off += dur
    t = np.concatenate(tms)
    extra = {"points_screen": np.concatenate(scr)} if len(scr) == len(pts) else {}
    np.savez_compressed(destino, values=np.zeros((len(t), 1), np.float32), t_ms=t.astype(np.int64),
                        names=np.array(["_"]), units=np.array([""]), points=np.concatenate(pts),
                        points_t_ms=t, point_names=nombres, deteccion_version=np.array(version), **extra)
    return True


def _clip_de(t, clase, nombre, persona):
    """Fila de `clips` importada con ese nombre y clase (la de esa persona, o la que aun no tiene persona)."""
    et = INP.ETIQUETA_DE[clase]
    cand = [c for c in t["clips"] if c.get("nombre") == nombre and c.get("etiqueta") == et]
    return next((c for c in cand if (c.get("persona") or "") == (persona or "")), None) or \
        next((c for c in cand if not c.get("persona") and c.get("raw_id") is None), None)


def reconstruir_originales(slug, carpeta):
    """Con el indice.csv de la carpeta (video_origen, inicio_s...) arma, por cada video original, UN video con sus
    clips unidos en orden (los tramos entre cortes no existen: el original no se tiene), lo deja en
    input/raw/<n>/<id>.mp4 con su .npz/.json, registra sus cortes en la tabla `raw` (pestana Cut/Edit) y apunta los
    clips a el. Agrega al indice.csv video_reconstruido / ini_rec_s / fin_rec_s. Repetible: lo ya reconstruido se salta."""
    idx = Path(carpeta) / "indice.csv"
    if not idx.exists():
        return {"videos": 0, "motivo": "no hay indice.csv"}
    raw = idx.read_bytes()
    filas = list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"), newline="")))
    hechos, pos, grupos = 0, {}, {}   # pos: archivo del indice -> (video reconstruido, ini, fin)
    with EXPORTAR._EXPORT_LOCK:   # tabla de clips, cortes y export_estado se reescriben enteros
        estado = json.loads(EXPORTAR.ESTADO.read_text("utf-8")) if EXPORTAR.ESTADO.exists() else {}
        with INP.editar() as t:
            for f in filas:
                clase = f["clase"].lower()
                c = _clip_de(t, clase, _nombre(Path(f["archivo"]).name), f.get("persona", "")) if clase in CLASES else None
                if c is not None and f.get("video_origen"):
                    grupos.setdefault((f.get("persona", ""), f.get("fecha") or "sin_fecha", f["video_origen"]), []).append(
                        (float(f.get("inicio_s") or 0), f, c))
            for (persona, fecha, origen), items in sorted(grupos.items(), key=lambda kv: (_natural(kv[0][0]), kv[0][1:])):
                items.sort(key=lambda it: it[0])
                marca = f"{persona}|{fecha}|{origen}"
                rv = next((r for r in t["raw"] if r.get("reconstruido_de") == marca), None)
                if rv is not None and len(rv.get("segmentos") or []) == len(items) and INP.ruta_raw(rv["ej"], rv["id"]).exists():
                    pass   # ya reconstruido con estos mismos clips
                else:
                    if rv is None:
                        rv = INP.registrar_raw(t, slug, fecha=None if fecha == "sin_fecha" else fecha, persona=persona or None,
                                               origen_viejo=f"importados/{persona}_{Path(origen).stem}")
                        rv["reconstruido_de"] = marca
                    dst = INP.ruta_raw(rv["ej"], rv["id"])
                    rutas = [INP.ruta_clip(c["ej"], c["id"]) for _, _, c in items]
                    durs = [_duracion(p) for p in rutas]
                    _unir(rutas, dst)
                    segs, tt = [], 0.0
                    for (_, f, _c), dur in zip(items, durs, strict=True):
                        segs.append({"ini": round(tt, 3), "fin": round(tt + dur, 3), "clase": f["clase"].lower(), "reps": 1,
                                     "persona": persona, "ini_orig": float(f.get("inicio_s") or 0),
                                     "fin_orig": float(f.get("fin_s") or 0)})
                        tt += dur
                    tiene_npz = _npz_unido(rutas, durs, dst.with_suffix(".npz"))
                    dst.with_suffix(".json").write_text(json.dumps({
                        "exercise": slug, "modo": "reconstruido", "reconstruido": True, "persona": persona, "fecha": fecha,
                        "video": dst.name, "features": dst.with_suffix(".npz").name if tiene_npz else None,
                        "fuente": f"indice.csv ({origen})", "duration_ms": int(tt * 1000), "reps": len(items)},
                        ensure_ascii=False, indent=2), "utf-8")
                    rv.update(segmentos=segs, reconstruido=True, persona=persona or rv.get("persona"))
                    estado[INP.vid_de(rv)] = EXPORTAR._hash(segs, EXPORTAR._npz_tiene_puntos(dst))   # "Generar cortes" no los vuelve a cortar
                    hechos += 1
                vid = INP.vid_de(rv)
                for n, ((_, f, c), sg) in enumerate(zip(items, rv["segmentos"], strict=True), 1):
                    c.update(raw_id=rv["id"], seg=n, t_ini_ms=round(sg["ini"] * 1000), t_fin_ms=round(sg["fin"] * 1000))
                    pos[f["archivo"]] = (vid, sg["ini"], sg["fin"])
        if hechos or pos:
            EXPORTAR.ESTADO.write_text(json.dumps(estado, indent=1), "utf-8")
    nuevos = ["video_reconstruido", "ini_rec_s", "fin_rec_s"]
    campos = list(filas[0].keys()) + [c for c in nuevos if c not in filas[0]] if filas else []
    for f in filas:
        v, i, e = pos.get(f["archivo"], ("", "", ""))
        f.update(video_reconstruido=v, ini_rec_s=i, fin_rec_s=e)
    buf = io.StringIO(newline="")
    w = csv.DictWriter(buf, fieldnames=campos, lineterminator="\r\n")
    w.writeheader()
    w.writerows(filas)
    idx.write_bytes((b"\xef\xbb\xbf" if raw.startswith(b"\xef\xbb\xbf") else b"") + buf.getvalue().encode("utf-8"))
    return {"videos": len(grupos), "nuevos": hechos}


def _ya_importados(slug):
    """Claves (clase, nombre, persona) de los clips ya importados de este ejercicio."""
    t = INP.tabla()
    raws = {r["id"]: r for r in t["raw"]}
    ej = INP.id_de(slug)
    return {(INP.CLASE_DE.get(c["etiqueta"]), c.get("nombre"), INP.persona_de(c, raws) or "")
            for c in t["clips"] if c["ej"] == ej and c.get("nombre")}


def _asignar_personas(slug, todos):
    """Un clip importado antes SIN persona que ahora aparece en la carpeta con persona la recibe (en vez de duplicarse)."""
    ej, n = INP.id_de(slug), 0
    with INP.editar() as t:
        for clase, nombre, _ruta, extras in todos:
            p = extras.get("persona")
            if not p:
                continue
            for c in t["clips"]:
                if (c["ej"] == ej and c.get("nombre") == _nombre(nombre) and c.get("etiqueta") == INP.ETIQUETA_DE[clase]
                        and not c.get("persona") and c.get("raw_id") is None):
                    c["persona"] = p
                    n += 1
                    break
    return n


def importar_carpeta(slug, carpeta, reemplazar_base=True):
    """Importa una carpeta entera, incremental: lo que ya esta importado (misma clase, nombre y persona) se salta, asi que
    repetirlo solo suma lo nuevo; los ya importados sin persona reciben la de la carpeta. Devuelve
    {"ok", "saltados", "errores", "sql_error", "por_clase", "personas_asignadas"}."""
    if EP.leer_ejercicio(slug) is None:
        raise ValueError(f"no existe el ejercicio '{slug}'")
    todos = listar_carpeta(carpeta)
    if not todos:
        raise ValueError("no hay videos en Bien/Mal dentro de esa carpeta")
    asignadas = _asignar_personas(slug, todos)
    hechos = _ya_importados(slug)
    nuevos = [t for t in todos if (t[0], _nombre(t[1]), t[3].get("persona") or "") not in hechos]
    PROGRESO.update(total=len(nuevos), hecho=0, archivo="")
    res = {"ok": 0, "saltados": len(todos) - len(nuevos), "errores": [], "sql_error": None, "por_clase": {},
           "personas_asignadas": asignadas}

    def avance(nombre):
        PROGRESO.update(hecho=PROGRESO["hecho"] + 1, archivo=nombre)

    for clase in CLASES:
        lote = [(n, r, e) for c, n, r, e in nuevos if c == clase]
        if not lote:
            continue
        r = importar_clips(slug, clase, lote, avance=avance)
        res["ok"] += len(r["ok"])
        res["por_clase"][clase] = len(r["ok"])
        res["errores"] += r["errores"]
        res["sql_error"] = res["sql_error"] or r["sql_error"]
    PROGRESO["archivo"] = "reconstruyendo los videos originales…"
    try:
        res["originales"] = reconstruir_originales(slug, carpeta)
    except Exception as e:   # los clips ya quedaron importados; esto se puede repetir
        res["errores"].append(f"originales: {e}")
        log.exception("reconstruir originales")
    return res


def iniciar_carpeta(slug, carpeta):
    """Lanza importar_carpeta en un hilo (son minutos: re-codifica y detecta puntos clip por clip).
    El avance se lee de PROGRESO; al terminar queda el resultado ahi."""
    if PROGRESO["activo"]:
        raise ValueError("ya hay una importacion en curso")
    listar_carpeta(carpeta)   # falla ya (no existe / vacia) en vez de dentro del hilo
    PROGRESO.update(activo=True, hecho=0, total=0, archivo="", resultado=None)

    def correr():
        try:
            PROGRESO["resultado"] = importar_carpeta(slug, carpeta)
        except Exception as e:   # el panel lo muestra; no debe morir en silencio dentro del hilo
            PROGRESO["resultado"] = {"error": str(e)}
            log.exception("importar carpeta")
        finally:
            PROGRESO["activo"] = False

    threading.Thread(target=correr, daemon=True).start()
