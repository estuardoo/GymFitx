"""Nucleo de la preparacion: lo comparten el entrenamiento y las 5 etapas ejecutables (etapas.py).

Todo sale del DISCO (input/bronze, input/raw y las tablas de parameters/inputs.json); SQL Server es solo una copia de respaldo.
Los umbrales vienen de parameters/config.json (src/nucleo/config.py: params()).
Capas: bronze (clip) -> plate (puntos y angulos sin normalizar) -> gold (vector normalizado); cada una usa el id del clip."""

from __future__ import annotations

import hashlib
import json
import threading
from pathlib import Path

import numpy as np

from src.etiquetado.manifest import _exercise_de, _leer_json, _ruta_video
from src.nucleo import config as CFG
from src.nucleo import ejercicio as EJ
from src.nucleo import inputs as INP
from src.nucleo.config import CLIPS_DIR, params
from src.procesamiento.puntos import normalizacion as NORM
from src.procesamiento.puntos import vectorizar

CLASES_CICLO = INP.EXPORTABLES   # cortes que son un ciclo completo; lo demas del video es "fuera"
_LOCK = threading.Lock()


def seleccion() -> dict:
    """{clip: false} = desmarcado a mano en el panel (no usar para entrenar)."""
    return INP.seleccion()


def grupo_de(clip: str) -> str:
    """Grabacion de la que sale un clip (o una ventana "fuera"): todos los ciclos, copias y ventanas de un mismo
    video comparten grupo, para que la validacion nunca ponga unos en entrenar y otros en probar (fuga de datos)."""
    if clip.startswith("fuera/"):   # fuera/<video>@<segundo>
        return INP.grupo_de_vid(clip[6:].rsplit("@", 1)[0])
    return INP.grupo_de_clip(clip)


# ---------------------------------------------------------------- formato y spec
def cfg_formato(ejercicio: str) -> dict:
    """Normalizacion espacial y temporal del ejercicio: la formula (origen / escala) y los cuadros que se definen en Kpoints."""
    return NORM.cfg_normalizacion(ejercicio)


def spec_de(ejercicio: str, features: str | None = None, tipo: int | None = None) -> dict:
    """La 'spec' del vector (la misma que guarda el modelo): que puntos, que medidas y como se normalizan."""
    spec = {"exercise": ejercicio, "features": features or params("formato")["componentes"], "cfg": cfg_formato(ejercicio),
            "point_names": EJ.puntos_de_ejercicio(ejercicio) or [], "kpoints": EJ.kpoints_de_ejercicio(ejercicio),
            "features_def": EJ.features_de_ejercicio(ejercicio)}
    if tipo is not None:
        spec["tipo"] = tipo
    return spec


# ---------------------------------------------------------------- clips en disco
def clips_de(ejercicio: str) -> list[dict]:
    """Clips de este ejercicio (tabla `clips` de parameters/inputs.json; sin pasar por SQL)."""
    return [r for r in INP.filas() if r["exercise"] == ejercicio]


def ruta_npz(row: dict) -> Path:
    return CLIPS_DIR / Path(row["clip"]).parent / (row.get("npz") or Path(row["clip"]).with_suffix(".npz").name)


def leer_clip(row: dict, spec: dict) -> dict:
    """{cuadros, nan_pct, prep}: tamaño del clip, % de puntos sin deteccion (solo los del ejercicio) y las medidas derivadas
    (angulos / proporciones) listas para normalizar. prep = None si el clip no trae datos."""
    z = np.load(ruta_npz(row), allow_pickle=False)
    pts = np.asarray(z["points"], dtype=np.float32)
    nombres = [str(n) for n in z["point_names"]]
    uso = [i for i, n in enumerate(nombres) if n in set(spec["point_names"])] or list(range(len(nombres)))
    nan = float(np.isnan(pts[:, uso]).any(axis=2).mean() * 100) if pts.size else 100.0
    prep = vectorizar.preparar(pts, nombres, spec["point_names"] or None, spec["kpoints"], spec["features_def"])
    return {"cuadros": len(pts), "nan_pct": round(nan, 2), "prep": prep}


def carpeta(base: Path, ejercicio: str) -> Path:
    """input/<capa>/<numero del ejercicio>/ (se crea)."""
    d = base / str(INP.asegurar_ejercicio(ejercicio))
    d.mkdir(parents=True, exist_ok=True)
    return d


def _sha(obj) -> str:
    return hashlib.sha1(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:12]


def hash_plate(spec: dict) -> str:
    return _sha([spec["point_names"], spec["kpoints"], spec["features_def"]])


def hash_gold(spec: dict) -> str:
    """Todo lo que cambia el vector final: si cambia (normalizacion, componentes, limpieza...) el gold se rehace."""
    return _sha([spec["features"], spec["cfg"], spec["point_names"], spec["kpoints"], spec["features_def"], params("limpieza")])


def _guardar_json(ruta: Path, obj) -> None:
    tmp = ruta.with_suffix(".tmp")
    tmp.write_text(json.dumps(obj, indent=1, ensure_ascii=False, sort_keys=True) + "\n", "utf-8")
    tmp.replace(ruta)


def llave(row: dict) -> str:
    return Path(row["clip"]).stem          # '000123'


def plates(filas: list[dict], spec: dict) -> dict[str, dict]:
    """{clip: {cuadros, nan_pct, prep}} desde input/plate (se regenera lo que cambio: el clip o el catalogo de puntos).
    prep = (puntos, nombres, angulos, nombres_ang) o None si el clip no trae datos."""
    out, h = {}, hash_plate(spec)
    with _LOCK:
        for ej in {r["exercise"] for r in filas}:
            d = carpeta(CFG.PLATE_DIR, ej)
            meta = _leer_json(d / "meta.json", {})
            sucio = False
            for r in (r for r in filas if r["exercise"] == ej):
                k, npz = llave(r), ruta_npz(r)
                p, a, m = d / f"{k}.p.npy", d / f"{k}.a.npy", meta.get(k)
                if (m and m.get("h") == h and p.exists() and a.exists()
                        and min(p.stat().st_mtime, a.stat().st_mtime) >= npz.stat().st_mtime):
                    out[r["clip"]] = {"cuadros": m["cuadros"], "nan_pct": m["nan_pct"],
                                      "prep": (np.load(p), m["nombres"], np.load(a), m["nombres_ang"])}
                    continue
                c = leer_clip(r, spec)
                out[r["clip"]] = c
                if c["prep"] is not None:
                    puntos, nombres, angulos, nombres_ang = c["prep"]
                    np.save(p, np.asarray(puntos, dtype=np.float32))
                    np.save(a, np.asarray(angulos, dtype=np.float32))
                    meta[k] = {"h": h, "nombres": list(nombres), "nombres_ang": list(nombres_ang),
                               "cuadros": c["cuadros"], "nan_pct": c["nan_pct"]}
                    sucio = True
            if sucio:
                _guardar_json(d / "meta.json", meta)
    return out


def motivos_limpieza(cuadros: int, nan_pct: float) -> list[str]:
    p = params("limpieza")
    return ([f"muy corto (<{p['min_frames']} cuadros)"] if cuadros < p["min_frames"] else []) + \
           ([f"muchos puntos sin detectar (>{p['max_nan_pct']} %)"] if nan_pct > p["max_nan_pct"] else [])


def vectores(ejercicio: str, spec: dict) -> dict[str, np.ndarray]:
    """{clip: vector final} de los clips del disco que pasan la limpieza -- lo que lee el entrenamiento (en vez de SQL).
    Pasa por plate y gold: lo que ya esta calculado y al dia se lee tal cual."""
    fuera = set(params("seleccion")["excluir_clases"])
    aplicar = params("limpieza")["aplicar"]
    filas = [r for r in clips_de(ejercicio) if r["clase"] not in fuera and ruta_npz(r).exists()]
    pl = plates(filas, spec)
    d, h = carpeta(CFG.GOLD_DIR, ejercicio), hash_gold(spec)
    meta = _leer_json(d / "meta.json", {})
    vigente = meta.get("hash") == h
    salida = {}
    for r in filas:
        c = pl.get(r["clip"])
        if c is None or c["prep"] is None or (aplicar and motivos_limpieza(c["cuadros"], c["nan_pct"])):
            continue
        f, p = d / f"{llave(r)}.npy", carpeta(CFG.PLATE_DIR, ejercicio) / f"{llave(r)}.a.npy"
        if vigente and f.exists() and (not p.exists() or f.stat().st_mtime >= p.stat().st_mtime):
            salida[r["clip"]] = np.load(f)
            continue
        v = vectorizar.vector_de_prep(c["prep"], spec)
        if v.size:
            np.save(f, np.asarray(v, dtype=np.float32))
            salida[r["clip"]] = v
    if not vigente:
        _guardar_json(d / "meta.json", {**meta, "hash": h})
    return salida


def previa_normalizacion(nombre, norm, clip=None):
    """Prueba la formula en un clip (por numero; sin numero, el del medio) SIN guardar: valores de origen y escala y
    donde quedan los kpoints que usa. ValueError con mensaje para el panel si la formula o el clip no sirven."""
    kps = EJ.kpoints_de_ejercicio(nombre)
    limpio = NORM.validar_normalizacion(norm, kps)
    cfg = NORM.cfg_de_normalizacion(limpio["origen"], limpio["escala"], limpio["n_frames"], kps)
    filas = [r for r in clips_de(nombre) if ruta_npz(r).exists()]
    if not filas:
        raise ValueError("este ejercicio aun no tiene clips para probar la formula")
    ids = [int(llave(r)) for r in filas if llave(r).isdigit()]
    fila = next((r for r in filas if clip and llave(r).isdigit() and int(llave(r)) == int(clip)), filas[len(filas) // 2])
    prep = leer_clip(fila, spec_de(nombre))["prep"]
    if prep is None:
        raise ValueError(f"el clip {int(llave(fila))} no trae puntos")
    pts, nombres, _, _ = prep
    origen, esc = NORM.valores_formula(pts, nombres, cfg)
    escala = NORM.escala_del_clip(esc)
    fijo = NORM._normalizar_formula(pts, nombres, cfg)
    mid = len(fijo) // 2
    ejemplo = {nm: [round(float(v), 3) for v in fijo[mid, nombres.index(nm), :2]] for nm in cfg["puntos"].values() if nm in nombres}
    validos = esc[np.isfinite(esc) & (esc > NORM.EPS_ESCALA)]
    return {"clip": int(llave(fila)), "clips": ids[:80], "cuadros": len(pts), "validos": int(len(validos)),
            "origen": [round(float(np.nanmedian(origen[:, i])), 4) for i in (0, 1)], "escala": round(escala, 4),
            "escala_min": round(float(validos.min()), 4), "escala_max": round(float(validos.max()), 4), "ejemplo": ejemplo}


# ---------------------------------------------------------------- clase "fuera" (registros generados)
def _iou(a0, a1, b0, b1):
    inter = max(0.0, min(a1, b1) - max(a0, b0))
    return inter / ((a1 - a0) + (b1 - b0) - inter) if inter else 0.0


def ventanas_crudas(exercise, tope, paso=None, iou_max=None):
    """Ventanas del largo de un ciclo tomadas de los tramos de las grabaciones fuente que no estan cortados como
    bien/mal/base: (lista de (puntos, nombres, 'fuera/<video>@<seg>'), ventana_ms). ([], None) si no hay."""
    p = params("construccion")["fuera"]
    paso, iou_max = paso or p["paso"], iou_max or p["iou_max"]
    videos, durs = [], []
    for vid, info in INP.leer_labels().items():
        try:
            src = _ruta_video(vid)
            if _exercise_de(src) != exercise or not src.with_suffix(".npz").exists():
                continue
        except ValueError:
            continue
        if info.get("reconstruido"):   # clips unidos: no hay tramos "fuera" reales (los cortes se ven como saltos)
            continue
        cortes = [(c["ini"], c["fin"]) for c in info.get("segmentos", []) if c.get("clase") in CLASES_CICLO]
        if cortes:
            videos.append((vid, src, cortes))
            durs += [f - i for i, f in cortes]
    if not durs:
        return [], None
    W = float(np.median(durs))
    cand = []
    for vid, src, cortes in videos:
        d = np.load(src.with_suffix(".npz"), allow_pickle=False)
        if "points" not in d.files:
            continue
        tp = (d["points_t_ms"] if "points_t_ms" in d.files else d["t_ms"] - d["t_ms"][0]) / 1000.0
        for ini in np.arange(0.0, float(tp[-1]) - W, W * paso):
            if max(_iou(ini, ini + W, i, f) for i, f in cortes) >= iou_max:
                continue
            m = (tp >= ini) & (tp <= ini + W)
            if m.sum() >= p["min_cuadros"]:
                cand.append((d["points"][m], d["point_names"], f"fuera/{vid}@{ini:.1f}"))
    if len(cand) > tope:   # no mas "fuera" que ciclos: con ventanas solapadas sobraria y desbalancearia
        cand = [cand[i] for i in np.linspace(0, len(cand) - 1, tope).astype(int)]
    return cand, int(round(W * 1000))


def ventanas_fuera(exercise, spec, tope, paso=None, iou_max=None):
    """Ejemplos de la clase "fuera" ya vectorizados, para que el modelo aprenda a decir "aqui no hay ciclo" (lo que permite
    contar en vivo con ventana deslizante). -> (vectores, nombres, ventana_ms); ([], [], None) si no hay grabaciones."""
    cand, ventana = ventanas_crudas(exercise, tope, paso, iou_max)
    vecs, nombres = [], []
    for pts, pn, nombre in cand:
        v = vectorizar.vector_de_clip(pts, pn, spec)
        if v is not None and v.size == spec["n_features"]:
            vecs.append(v)
            nombres.append(nombre)
    return vecs, nombres, ventana
