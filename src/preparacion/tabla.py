"""Nucleo de la preparacion: lo comparten el entrenamiento y las 5 etapas ejecutables (etapas.py).

Todo sale del DISCO (datos/clips, manifest.json, etiquetas.json, grabaciones); SQL Server es solo una copia de respaldo.
Los umbrales vienen de params.yaml (src/nucleo/config.py: params())."""

from __future__ import annotations

import json
import re
from pathlib import Path, PurePosixPath

import numpy as np

from src.etiquetado.manifest import LABELS, _exercise_de, _leer_json, _ruta_video
from src.nucleo import ejercicio as EJ
from src.nucleo.config import CLIPS_DIR, MANIFEST_PATH, SELECCION_PATH, formato_de, params
from src.procesamiento.puntos import normalizacion as NORM
from src.procesamiento.puntos import vectorizar

CLASES_CICLO = ("bien", "mal", "base")   # cortes que son un ciclo completo; lo demas del video es "fuera"
COPIA = re.compile(r"_\d+$")             # ..._bien_2.mp4: copia del mismo ciclo (riesgo de fuga entre train y test)


def seleccion() -> dict:
    """{clip: false} = desmarcado a mano en el panel (no usar para entrenar)."""
    try:
        return json.loads(SELECCION_PATH.read_text("utf-8")) if SELECCION_PATH.exists() else {}
    except (OSError, ValueError):
        return {}


def grupo_de(clip: str) -> str:
    """Grabacion de la que sale un clip (o una ventana "fuera"): todos los ciclos, copias (_2, _3) y ventanas de un mismo
    video comparten grupo, para que la validacion nunca ponga unos en entrenar y otros en probar (fuga de datos)."""
    if clip.startswith("fuera/"):   # fuera/<ruta del video>@<segundo>
        return re.sub(r"_s\d+.*$", "", PurePosixPath(clip[6:].rsplit("@", 1)[0]).with_suffix("").as_posix().replace("/", "__"))
    return re.sub(r"_s\d+.*$", "", PurePosixPath(clip).stem)


# ---------------------------------------------------------------- formato y spec
def cfg_formato(ejercicio: str) -> dict:
    """Normalizacion espacial y temporal: defaults de normalizacion.py + params.yaml (formato, y formato.por_ejercicio)."""
    return {**NORM.DEFAULT_CFG, **formato_de(ejercicio)}


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
    """Filas del manifest.json de este ejercicio (sin pasar por SQL)."""
    return [r for r in _leer_json(MANIFEST_PATH, []) if r.get("clip", "").split("/")[0] == ejercicio]


def ruta_npz(row: dict) -> Path:
    return CLIPS_DIR / Path(row["clip"]).parent / (row.get("npz") or Path(row["clip"]).with_suffix(".npz").name)


def leer_clip(row: dict, spec: dict) -> dict:
    """{cuadros, nan_pct, prep}: tamaño del clip, % de puntos sin deteccion (solo los del ejercicio) y las medidas derivadas
    (angulos / proporciones) listas para normalizar. prep = None si el clip no trae datos."""
    z = np.load(ruta_npz(row), allow_pickle=True)
    pts = np.asarray(z["points"], dtype=np.float32)
    nombres = [str(n) for n in z["point_names"]]
    uso = [i for i, n in enumerate(nombres) if n in set(spec["point_names"])] or list(range(len(nombres)))
    nan = float(np.isnan(pts[:, uso]).any(axis=2).mean() * 100) if pts.size else 100.0
    prep = vectorizar.preparar(pts, nombres, spec["point_names"] or None, spec["kpoints"], spec["features_def"])
    return {"cuadros": len(pts), "nan_pct": round(nan, 2), "prep": prep}


def motivos_limpieza(cuadros: int, nan_pct: float) -> list[str]:
    p = params("limpieza")
    return ([f"muy corto (<{p['min_frames']} cuadros)"] if cuadros < p["min_frames"] else []) + \
           ([f"muchos puntos sin detectar (>{p['max_nan_pct']} %)"] if nan_pct > p["max_nan_pct"] else [])


def vectores(ejercicio: str, spec: dict) -> dict[str, np.ndarray]:
    """{clip: vector final} de los clips del disco que pasan la limpieza -- lo que lee el entrenamiento (en vez de SQL)."""
    fuera = set(params("seleccion")["excluir_clases"])
    aplicar = params("limpieza")["aplicar"]
    salida = {}
    for r in clips_de(ejercicio):
        if r["clase"] in fuera or not ruta_npz(r).exists():
            continue
        try:
            c = leer_clip(r, spec)
        except Exception:   # noqa: BLE001 - un .npz ilegible deja el clip sin vector; el mensaje de armar() lo cuenta
            continue
        if c["prep"] is None or (aplicar and motivos_limpieza(c["cuadros"], c["nan_pct"])):
            continue
        v = vectorizar.vector_de_prep(c["prep"], spec)
        if v.size:
            salida[r["clip"]] = v
    return salida


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
    for vid, info in _leer_json(LABELS, {}).items():
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
        d = np.load(src.with_suffix(".npz"), allow_pickle=True)
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
