"""Subir clips ya cortados (bien / mal / base) a un ejercicio, sin pasar por grabacion + etiquetado.

Cada clip queda como si lo hubiera exportado el panel: datos/clips/<ejercicio>/<clase>/<nombre>.mp4
+ .npz con los puntos del catalogo, fila en manifest.json y, si el SQL Server responde, registro en
SQL (poblar_desde_manifest). Si SQL no responde el clip queda local y "Sistema -> Generar tablas"
lo sube despues (estas filas tienen 'origen' fuera de labels, exportar() las conserva)."""

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
from src.etiquetado.manifest import DATA, LABELS, MANIFEST, OUT, log
from src.etiquetado.previews import ffmpeg_exe
from src.etiquetado.tablas import poblar_desde_manifest
from src.procesamiento import offline as deteccion

CLASES = ("bien", "mal", "base")
_VIDEO = re.compile(r"\.(mp4|mov|avi|mkv|webm|m4v)$", re.I)


def _nombre(original: str) -> str:
    stem = re.sub(r"[^a-z0-9_-]+", "_", Path(original).stem.lower()).strip("_") or "clip"
    return stem[:60]


def _unico(carpeta: Path, stem: str) -> str:
    n, cand = 1, stem
    while (carpeta / f"{cand}.mp4").exists():
        n += 1
        cand = f"{stem}_{n}"
    return cand


def _duracion(mp4: Path) -> float:
    import cv2
    cap = cv2.VideoCapture(str(mp4))
    try:
        fps = cap.get(cv2.CAP_PROP_FPS) or 0
        return round(cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps, 3) if fps else 0.0
    finally:
        cap.release()


def _quitar_clip(row):
    for p in (OUT / row["clip"], (OUT / row["clip"]).with_suffix(".npz")):
        p.unlink(missing_ok=True)


def _borrar_en_sql(type_, archivo):
    """Quita un clip de SQL (indicadores, frames, fila); los indicadores se recalculan al registrar el nuevo."""
    with SQL.conexion() as cx:
        r = SQL.archivo_registrado(cx, type_, archivo)
        if r:
            fid = r[0]
            cx.execute("DELETE FROM table_indicator WHERE file_id=? OR base_file_id=?", (fid, fid))
            for t in ("table_frame_base", "table_frames_fix", "table_frames"):
                cx.execute(f"DELETE FROM {t} WHERE file_id=?", (fid,))
            cx.execute("DELETE FROM table_file WHERE id=?", (fid,))
            cx.commit()


def _una(slug, clase, nombre_original, src: Path):
    """Un archivo: transcodifica, detecta puntos, devuelve la fila de manifest (o lanza)."""
    d = OUT / slug / clase
    d.mkdir(parents=True, exist_ok=True)
    name = _unico(d, _nombre(nombre_original))
    mp4, npz = d / f"{name}.mp4", d / f"{name}.npz"
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
        if "points" not in np.load(npz, allow_pickle=True).files:
            raise ValueError("no se detecto ninguna persona en el video")
        dur = _duracion(mp4)
    except Exception:
        mp4.unlink(missing_ok=True)
        npz.unlink(missing_ok=True)
        raise
    return {"clip": f"{slug}/{clase}/{name}.mp4", "npz": f"{name}.npz",
            "origen": f"importados/{slug}/{name}.mp4", "seg": 1, "clase": clase, "reps": 0,
            "ini": 0.0, "fin": dur, "dur": dur, "exercise": slug}


def importar_clips(slug, clase, archivos, reemplazar=False, avance=None):
    """archivos: [(nombre_original, ruta_temporal[, extras])]; extras (persona, vista, fecha...) van a la fila del manifest. Devuelve {"ok": [clips], "errores": [str],
    "sql": resumen|None, "sql_error": str|None, "base_reemplazada": bool}."""
    if clase not in CLASES:
        raise ValueError(f"clase invalida: {clase}")
    if EP.leer_ejercicio(slug) is None:
        raise ValueError(f"no existe el ejercicio '{slug}'")
    if clase == "base" and len(archivos) > 1:
        raise ValueError("solo puede haber un clip base por ejercicio: sube uno")
    out = {"ok": [], "errores": [], "sql": None, "sql_error": None, "base_reemplazada": False}

    nuevas = []
    for nombre, ruta, *extra in archivos:
        if avance:
            avance(nombre)
        if not _VIDEO.search(nombre or ""):
            out["errores"].append(f"{nombre}: no es un video")
            continue
        try:
            nuevas.append({**_una(slug, clase, nombre, Path(ruta)), **(extra[0] if extra else {})})
        except (ValueError, deteccion.DeteccionNoDisponible) as e:
            out["errores"].append(f"{nombre}: {e}")
    if not nuevas:
        return out

    viejas = []
    with EXPORTAR._EXPORT_LOCK:   # mismo candado que exportar(): manifest.json se reescribe entero
        rows = json.loads(MANIFEST.read_text("utf-8")) if MANIFEST.exists() else []
        if clase == "base":
            viejas = [r for r in rows if r.get("exercise") == slug and r.get("clase") == "base"]
            if viejas and not reemplazar:
                for r in nuevas:
                    _quitar_clip(r)
                out["errores"].append("ya hay un clip base para este ejercicio")
                out["base_existente"] = True
                return out
            rows = [r for r in rows if r not in viejas]
            out["base_reemplazada"] = bool(viejas)
        rows.extend(nuevas)
        MANIFEST.write_text(json.dumps(rows, indent=2, ensure_ascii=False), "utf-8")
    out["ok"] = [r["clip"] for r in nuevas]

    try:   # SQL caido: el clip ya quedo local, "Generar tablas" lo sube luego
        SQL.asegurar_base_y_tablas()
        tipo = SQL.tipo_de_ejercicio(slug)
        for r in viejas:
            _borrar_en_sql(tipo, r["clip"])
        out["sql"] = poblar_desde_manifest(nuevas, OUT, type_=tipo)
    except SQL.SQLServerNoDisponible as e:
        out["sql_error"] = str(e)
    for r in viejas:
        _quitar_clip(r)
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
# Carpeta completa: <carpeta>/{Base,Bien,Mal}/P1..Pn/*.mp4 (+ indice.csv opcional con persona/vista/fecha)
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
        d = np.load(clip.with_suffix(".npz"), allow_pickle=True)
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


def reconstruir_originales(slug, carpeta):
    """Con el indice.csv de la carpeta (video_origen, inicio_s...) arma, por cada video original, UN video con sus
    clips unidos en orden (los tramos entre cortes no existen: el original no se tiene), lo deja en
    datos/grabaciones/<slug>/<fecha>/<persona>_<origen>.mp4 con su .npz/.json, registra sus cortes en
    etiquetas.json (pestana Cut/Edit) y apunta los clips del manifest a el. Agrega al indice.csv
    video_reconstruido / ini_rec_s / fin_rec_s. Repetible: lo ya reconstruido se salta."""
    from src.etiquetado import exportar as EXPORTAR
    idx = Path(carpeta) / "indice.csv"
    if not idx.exists():
        return {"videos": 0, "motivo": "no hay indice.csv"}
    raw = idx.read_bytes()
    filas = list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"), newline="")))
    grupos = {}
    for f in filas:
        clip = f"{slug}/{f['clase'].lower()}/{_nombre(Path(f['archivo']).name)}.mp4"
        if f.get("video_origen") and (OUT / clip).exists():
            grupos.setdefault((f.get("persona", ""), f.get("fecha") or "sin_fecha", f["video_origen"]), []).append(
                (float(f.get("inicio_s") or 0), f, clip))
    hechos = 0
    with EXPORTAR._EXPORT_LOCK:   # manifest, etiquetas y export_estado se reescriben enteros
        rows = json.loads(MANIFEST.read_text("utf-8")) if MANIFEST.exists() else []
        por_clip = {r["clip"]: r for r in rows}
        labels = json.loads(LABELS.read_text("utf-8")) if LABELS.exists() else {}
        estado = json.loads(EXPORTAR.ESTADO.read_text("utf-8")) if EXPORTAR.ESTADO.exists() else {}
        pos = {}   # archivo del indice -> (video reconstruido, ini, fin)
        for (persona, fecha, origen), items in sorted(grupos.items(), key=lambda kv: (_natural(kv[0][0]), kv[0][1:])):
            items.sort(key=lambda t: t[0])
            vid = f"{slug}/{fecha}/{persona}_{Path(origen).stem}.mp4".replace("//", "/")
            dst = DATA / vid
            segs = (labels.get(vid) or {}).get("segmentos") or []
            if dst.exists() and len(segs) == len(items):
                pass   # ya reconstruido con estos mismos clips
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                rutas = [OUT / c for _, _, c in items]
                durs = [_duracion(p) for p in rutas]
                _unir(rutas, dst)
                segs, t = [], 0.0
                for (_, f, _clip), dur in zip(items, durs, strict=True):
                    segs.append({"ini": round(t, 3), "fin": round(t + dur, 3), "clase": f["clase"].lower(), "reps": 1,
                                 "persona": persona, "ini_orig": float(f.get("inicio_s") or 0),
                                 "fin_orig": float(f.get("fin_s") or 0)})
                    t += dur
                tiene_npz = _npz_unido(rutas, durs, dst.with_suffix(".npz"))
                dst.with_suffix(".json").write_text(json.dumps({
                    "exercise": slug, "modo": "reconstruido", "reconstruido": True, "persona": persona, "fecha": fecha,
                    "video": dst.name, "features": dst.with_suffix(".npz").name if tiene_npz else None,
                    "fuente": f"indice.csv ({origen})", "duration_ms": int(t * 1000), "reps": len(items)},
                    ensure_ascii=False, indent=2), "utf-8")
                labels[vid] = {"segmentos": segs, "reconstruido": True, "persona": persona}
                estado[vid] = EXPORTAR._hash(segs, EXPORTAR._npz_tiene_puntos(dst))   # "Generar cortes" no los vuelve a cortar
                hechos += 1
            for n, ((_, f, clip), sg) in enumerate(zip(items, segs, strict=True), 1):
                if clip in por_clip:
                    por_clip[clip].update(origen=vid, seg=n, ini=sg["ini"], fin=sg["fin"],
                                          dur=round(sg["fin"] - sg["ini"], 3), persona=persona)
                pos[f["archivo"]] = (vid, sg["ini"], sg["fin"])
        if hechos or pos:
            MANIFEST.write_text(json.dumps(rows, indent=2, ensure_ascii=False), "utf-8")
            LABELS.write_text(json.dumps(labels, indent=1, ensure_ascii=False), "utf-8")
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


def importar_carpeta(slug, carpeta, reemplazar_base=True):
    """Importa una carpeta entera, incremental: lo que ya esta en datos/clips/<slug>/<clase>/ se salta, asi que
    repetirlo solo suma lo nuevo. Devuelve {"ok", "saltados", "errores", "sql_error", "por_clase"}."""
    if EP.leer_ejercicio(slug) is None:
        raise ValueError(f"no existe el ejercicio '{slug}'")
    todos = listar_carpeta(carpeta)
    if not todos:
        raise ValueError("no hay videos en Base/Bien/Mal dentro de esa carpeta")
    nuevos = [t for t in todos if not (OUT / slug / t[0] / f"{_nombre(t[1])}.mp4").exists()]
    PROGRESO.update(total=len(nuevos), hecho=0, archivo="")
    res = {"ok": 0, "saltados": len(todos) - len(nuevos), "errores": [], "sql_error": None, "por_clase": {}}

    def avance(nombre):
        PROGRESO.update(hecho=PROGRESO["hecho"] + 1, archivo=nombre)

    for clase in ("base", "bien", "mal"):
        lote = [(n, r, e) for c, n, r, e in nuevos if c == clase]
        if not lote:
            continue
        r = importar_clips(slug, clase, lote, reemplazar=reemplazar_base, avance=avance)
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
