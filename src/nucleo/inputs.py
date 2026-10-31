"""Que video es cual: las tablas `raw` (grabaciones) y `clips` (recortes) en parameters/inputs.json, y la tabla de
ejercicios numerados en parameters/exercise.json. Todo lo demas (cortes, exportar, entrenar, panel) pregunta aqui.

    raw    {id, ej, persona, fecha, archivos, segmentos, origen_viejo}        input/raw/<ej>/<id>.mp4|npz|json
    clips  {id, ej, raw_id, seg, t_ini_ms, t_fin_ms, etiqueta 1|0|null, usar, persona, rev, copia}   input/bronze/<ej>/<id>.mp4|npz

La persona vive en el raw (un cambio llega a todos sus clips); un clip sin raw (importado suelto) trae la suya.
Los ids nunca se reutilizan (contadores). Los nombres de ejercicio solo existen en exercise.json."""

from __future__ import annotations

import copy
import json
import re
import threading
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

from src.nucleo import config as CFG

SCHEMA = 1
LOCK = threading.RLock()
CLASE_DE = {1: "bien", 0: "mal"}
ETIQUETA_DE = {"bien": 1, "mal": 0}
EXPORTABLES = tuple(ETIQUETA_DE)      # clases de un corte que se vuelven clip
SIN_ETIQUETA = "sin_etiqueta"
_COPIA = re.compile(r"_\d+$")


# ---------------------------------------------------------------- json atomico
def _leer(path, defecto):
    try:
        return json.loads(Path(path).read_text("utf-8"))
    except (OSError, ValueError):
        return defecto


def _escribir(path, obj) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n", "utf-8")
    tmp.replace(path)


# ---------------------------------------------------------------- ejercicios (id <-> slug)
def ejercicios() -> dict[int, dict]:
    return {int(k): v for k, v in (_leer(CFG.EXERCISE_PATH, {}).get("ejercicios") or {}).items()}


def id_de(slug: str) -> int | None:
    return next((i for i, e in ejercicios().items() if e.get("slug") == slug), None)


def slug_de(ej) -> str:
    e = ejercicios().get(int(ej))
    if not e:
        raise ValueError(f"no existe el ejercicio numero {ej} en exercise.json")
    return e["slug"]


def asegurar_ejercicio(slug: str, nombre: str | None = None) -> int:
    """El numero del ejercicio; si no tiene, le asigna el siguiente (los numeros no se reutilizan)."""
    with LOCK:
        doc = _leer(CFG.EXERCISE_PATH, {"schema_version": SCHEMA, "ejercicios": {}})
        ej = doc.setdefault("ejercicios", {})
        for k, v in ej.items():
            if v.get("slug") == slug:
                if not v.get("activo", True):
                    v["activo"] = True
                    _escribir(CFG.EXERCISE_PATH, doc)
                return int(k)
        n = max([int(k) for k in ej] + [doc.get("ultimo", 0)], default=0) + 1
        ej[str(n)] = {"nombre": nombre or slug, "slug": slug, "activo": True}
        doc["ultimo"] = n
        _escribir(CFG.EXERCISE_PATH, doc)
        return n


def desactivar_ejercicio(slug: str) -> None:
    """Ejercicio archivado: sigue con su numero (reservado) pero inactivo."""
    with LOCK:
        doc = _leer(CFG.EXERCISE_PATH, {})
        for v in (doc.get("ejercicios") or {}).values():
            if v.get("slug") == slug:
                v["activo"] = False
        _escribir(CFG.EXERCISE_PATH, doc)


# ---------------------------------------------------------------- tablas
def _vacia() -> dict:
    return {"schema_version": SCHEMA, "contadores": {"raw": 0, "clip": 0}, "raw": [], "clips": []}


_CACHE: dict = {}


def tabla() -> dict:
    """Copia de la tabla (se relee solo si el archivo cambio)."""
    p = Path(CFG.INPUTS_PATH)
    try:
        st = p.stat()
        llave = (str(p), st.st_mtime_ns, st.st_size)
    except OSError:
        llave = None
    if llave and _CACHE.get("llave") == llave:
        return copy.deepcopy(_CACHE["t"])
    t = _leer_tabla()
    if llave:
        _CACHE.update(llave=llave, t=copy.deepcopy(t))
    return t


def _leer_tabla() -> dict:
    t = _leer(CFG.INPUTS_PATH, None) or _vacia()
    c = t.setdefault("contadores", {})
    c["raw"] = max(c.get("raw", 0), max((r["id"] for r in t.get("raw", [])), default=0))
    c["clip"] = max(c.get("clip", 0), max((r["id"] for r in t.get("clips", [])), default=0))
    t.setdefault("raw", [])
    t.setdefault("clips", [])
    return t


@contextmanager
def editar():
    """with editar() as t: ...  -> lee, deja modificar y guarda al salir (si no hubo error). Un solo escritor a la vez."""
    with LOCK:
        t = tabla()
        yield t
        _escribir(CFG.INPUTS_PATH, t)


def _nuevo_id(t: dict, cual: str) -> int:
    t["contadores"][cual] += 1
    return t["contadores"][cual]


# ---------------------------------------------------------------- rutas
def ruta_raw(ej, rid, ext="mp4") -> Path:
    return CFG.RECORDINGS_DIR / str(int(ej)) / f"{int(rid):06d}.{ext}"


def ruta_clip(ej, cid, ext="mp4") -> Path:
    return CFG.CLIPS_DIR / str(int(ej)) / f"{int(cid):06d}.{ext}"


def vid_de(raw: dict) -> str:
    """El identificador de un video para el panel: ruta relativa a input/raw ('1/000007.mp4')."""
    return f"{raw['ej']}/{raw['id']:06d}.mp4"


def clave(clip: dict) -> str:
    """El identificador de un clip: ruta relativa a input/bronze ('1/000123.mp4')."""
    return f"{clip['ej']}/{clip['id']:06d}.mp4"


def _partes(ruta: str):
    p = Path(ruta)
    try:
        return int(p.parent.name), int(p.stem)
    except ValueError:
        return None


def raw_de_vid(vid: str, t: dict | None = None) -> dict | None:
    k = _partes(vid)
    if k is None:
        return None
    return next((r for r in (t or tabla())["raw"] if (r["ej"], r["id"]) == k), None)


def clip_de_clave(cl: str, t: dict | None = None) -> dict | None:
    k = _partes(cl)
    if k is None:
        return None
    return next((c for c in (t or tabla())["clips"] if (c["ej"], c["id"]) == k), None)


# ---------------------------------------------------------------- altas
def registrar_raw(t: dict, slug: str, *, fecha: str | None = None, persona: str | None = None, archivos=("mp4", "npz", "json"),
                  origen_viejo: str | None = None, segmentos: list | None = None) -> dict:
    """Fila nueva en `raw` (no crea archivos: los escribe quien graba). Dentro de `with editar() as t`."""
    row = {"id": _nuevo_id(t, "raw"), "ej": asegurar_ejercicio(slug), "persona": persona,
           "fecha": fecha or datetime.now().isoformat(timespec="seconds"), "archivos": list(archivos),
           "origen_viejo": origen_viejo, "segmentos": segmentos or []}
    t["raw"].append(row)
    ruta_raw(row["ej"], row["id"]).parent.mkdir(parents=True, exist_ok=True)
    return row


def registrar_clip(t: dict, slug: str, *, etiqueta, t_ini_ms: int, t_fin_ms: int, raw_id: int | None = None, seg: int | None = None,
                   reps: int = 0, persona: str | None = None, origen_viejo: str | None = None, copia: bool = False) -> dict:
    row = {"id": _nuevo_id(t, "clip"), "ej": asegurar_ejercicio(slug), "raw_id": raw_id, "seg": seg,
           "t_ini_ms": int(t_ini_ms), "t_fin_ms": int(t_fin_ms), "etiqueta": etiqueta, "reps": reps, "usar": True,
           "persona": persona, "rev": 1, "copia": copia, "origen_viejo": origen_viejo}
    t["clips"].append(row)
    ruta_clip(row["ej"], row["id"]).parent.mkdir(parents=True, exist_ok=True)
    return row


def es_copia(nombre: str) -> bool:
    """'..._bien_2' = copia del mismo ciclo (riesgo de fuga entre entrenar y probar)."""
    return bool(_COPIA.search(Path(nombre).stem))


# ---------------------------------------------------------------- lectura "como siempre" (filas del antiguo manifest)
def persona_de(clip: dict, raws: dict) -> str | None:
    raw = raws.get(clip.get("raw_id"))
    return raw.get("persona") if raw else clip.get("persona")


def filas(t: dict | None = None) -> list[dict]:
    """Los clips con la forma que el resto del codigo siempre uso (clip, npz, origen, clase, ini, fin, exercise, persona...)."""
    t = t or tabla()
    raws = {r["id"]: r for r in t["raw"]}
    ejs = ejercicios()
    out = []
    for c in t["clips"]:
        e = ejs.get(c["ej"])
        if not e:
            continue
        raw = raws.get(c.get("raw_id"))
        ini, fin = c["t_ini_ms"] / 1000, c["t_fin_ms"] / 1000
        out.append({"clip": clave(c), "npz": f"{c['id']:06d}.npz", "id": c["id"], "raw_id": c.get("raw_id"),
                    "origen": vid_de(raw) if raw else (c.get("origen_viejo") or f"importados/{e['slug']}/{c['id']:06d}.mp4"),
                    "seg": c.get("seg"), "clase": CLASE_DE.get(c.get("etiqueta"), SIN_ETIQUETA), "reps": c.get("reps", 0),
                    "ini": round(ini, 3), "fin": round(fin, 3), "dur": round(fin - ini, 3), "exercise": e["slug"],
                    "persona": persona_de(c, raws), "usar": c.get("usar", True), "copia": bool(c.get("copia"))})
    return out


def grupo_de_vid(vid: str, t: dict | None = None) -> str:
    """Grupo de validacion de un video: todos sus ciclos y ventanas comparten grupo (sin fuga entre entrenar y probar)."""
    raw = raw_de_vid(vid, t)
    return f"r{raw['id']}" if raw else Path(vid).with_suffix("").as_posix().replace("/", "__")


def grupo_de_clip(cl: str, t: dict | None = None) -> str:
    t = t or tabla()
    c = clip_de_clave(cl, t)
    if c is None:
        return Path(cl).stem
    if c.get("raw_id") is not None:
        return f"r{c['raw_id']}"
    return re.sub(r"_s\d+.*$", "", Path(c.get("origen_viejo") or cl).stem)   # clip suelto: su video de origen


# ---------------------------------------------------------------- cortes de cada raw (antes etiquetas.json)
def leer_labels() -> dict:
    """{vid: {"segmentos": [...], ...}} de los raw que tienen cortes."""
    out = {}
    for r in tabla()["raw"]:
        if r.get("segmentos") or r.get("reconstruido"):
            info = {"segmentos": r.get("segmentos", [])}
            if r.get("reconstruido"):
                info.update(reconstruido=True, persona=r.get("persona"))
            out[vid_de(r)] = info
    return out


def guardar_labels(body: dict) -> None:
    """Mezcla (no reemplaza): un video no mencionado conserva sus cortes."""
    with editar() as t:
        for vid, info in body.items():
            raw = raw_de_vid(vid, t)
            if raw is None:
                continue
            raw["segmentos"] = info.get("segmentos", [])
            if info.get("reconstruido"):
                raw["reconstruido"] = True
                if info.get("persona"):
                    raw["persona"] = info["persona"]


# ---------------------------------------------------------------- persona y seleccion manual
def asignar_persona(raw_id: int, persona: str | None) -> dict:
    with editar() as t:
        raw = next((r for r in t["raw"] if r["id"] == int(raw_id)), None)
        if raw is None:
            raise ValueError(f"no existe el video {raw_id}")
        raw["persona"] = persona or None
        return {"id": raw["id"], "persona": raw["persona"],
                "clips": sum(1 for c in t["clips"] if c.get("raw_id") == raw["id"])}


def seleccion() -> dict:
    """{clip: False} = desmarcado a mano en el panel (no usar para entrenar)."""
    return {clave(c): False for c in tabla()["clips"] if c.get("usar") is False}


def guardar_seleccion(cambios: dict) -> int:
    with editar() as t:
        for cl, usar in cambios.items():
            c = clip_de_clave(cl, t)
            if c is not None:
                c["usar"] = bool(usar)
        return sum(1 for c in t["clips"] if c.get("usar") is False)
