"""Normalizacion de un clip de puntos y remuestreo a N cuadros. Modo "formula" (el de cada ejercicio, se define en Kpoints ->
Normalizacion): x' = (K - origen) / escala, con origen y escala como formulas entre kpoints (ver formula.py).
Modos antiguos "rectangulo" (caja 100x100) y "punto": solo para modelos ya entrenados y ejercicios sin kpoints de referencia.

La usan igual el dataset (SQL) y el clasificador en vivo."""

from __future__ import annotations

import hashlib

import numpy as np

from src.nucleo import ejercicio as EJ
from src.nucleo.config import params
from src.nucleo.landmarks import POSE_LANDMARKS
from src.procesamiento.puntos import formula as FORM

EPS_ESCALA = 1e-6


class NormalizacionInvalida(ValueError):
    """El clip no se puede normalizar con esta formula (escala 0 o sin datos, kpoint ausente): se marca y no entra."""


DEFAULT_CFG = {
    "modo": "rectangulo",       # "formula" (lo fija cada ejercicio) | "rectangulo" | "punto" (legado: lo que no dice modo)
    "origen": None, "escala": None, "puntos": None,   # modo "formula": textos + {numero: nombre del kpoint} de los que usa
    "n_frames_fijo": 30,
    "punto_centro": None, "punto_escala_a": None, "punto_escala_b": None,  # modo "punto"
    "puntos_caja": None,        # modo "rectangulo": subset de nombres para la caja (None = todos)
}


LADO_LIENZO = params("formato")["lienzo"]   # parameters/config.json: formato.lienzo


def cfg_para(point_names, cfg_guardada: dict | None = None) -> dict:
    """Config efectiva con defaults razonables para estos puntos."""
    out = {**DEFAULT_CFG, **(cfg_guardada or {})}
    nombres = list(point_names)
    if out["modo"] == "formula":
        return out
    if out["punto_centro"] not in nombres:
        out["punto_centro"] = "WRIST" if "WRIST" in nombres else nombres[0]
    if out["punto_escala_a"] not in nombres:
        out["punto_escala_a"] = out["punto_centro"]
    if out["punto_escala_b"] not in nombres:
        out["punto_escala_b"] = "MIDDLE_FINGER_MCP" if "MIDDLE_FINGER_MCP" in nombres else nombres[-1]
    validos = [n for n in (out.get("puntos_caja") or []) if n in nombres]
    out["puntos_caja"] = validos or None
    return out


def guia(cfg: dict) -> str:
    """Descriptor corto de la normalizacion (table_file.guia_fix)."""
    if cfg["modo"] == "formula":
        return f"formula:o={cfg['origen']};e={cfg['escala']}|{cfg['n_frames_fijo']}f"
    if cfg["modo"] == "rectangulo":
        caja = ",".join(cfg["puntos_caja"]) if cfg.get("puntos_caja") else "todos"
        return f"rect:{LADO_LIENZO}|{cfg['n_frames_fijo']}f|caja:{caja}"
    return f"punto:{cfg['punto_centro']}-{cfg['punto_escala_a']}-{cfg['punto_escala_b']}|{cfg['n_frames_fijo']}f"


def firma(nombres, angulos) -> str:
    """Firma corta de QUE puntos/angulos trae el clip."""
    txt = "|".join(nombres) + "#" + "|".join(angulos)
    return hashlib.sha1(txt.encode()).hexdigest()[:8]


def resamplear(fijo: np.ndarray, n_frames_fijo: int) -> np.ndarray:
    """(T,N,C) -> (n,N,C). Interpola solo sobre cuadros con dato (NaN = no detectado)."""
    t_actual = np.linspace(0, 1, len(fijo))
    t_nuevo = np.linspace(0, 1, n_frames_fijo)
    out = np.full((n_frames_fijo, fijo.shape[1], fijo.shape[2]), np.nan, dtype=np.float32)
    for n in range(fijo.shape[1]):
        for c in range(fijo.shape[2]):
            serie = fijo[:, n, c]
            ok = np.isfinite(serie)
            if ok.any():
                out[:, n, c] = np.interp(t_nuevo, t_actual[ok], serie[ok])
    return out


def resamplear_angulos(angulos: np.ndarray, n_frames_fijo: int) -> np.ndarray:
    if angulos.shape[1] == 0:
        return np.zeros((n_frames_fijo, 0), dtype=np.float32)
    return resamplear(angulos[:, :, None], n_frames_fijo)[:, :, 0]


def codigos_de(kpoints) -> dict[int, str]:
    """{codigo C: nombre del kpoint} de los puntos del cuerpo marcados en el ejercicio. C = landmark de MediaPipe + 1: fijo en todos los
    ejercicios (C24 = cadera izquierda siempre). Los derivados no tienen codigo C: se arman en la formula con medio()."""
    out = {}
    for k in kpoints or []:
        o = k.get("origen") or {}
        if o.get("tipo") == "landmark" and o.get("fuente") == "pose" and o.get("landmark") in POSE_LANDMARKS:
            out[POSE_LANDMARKS.index(o["landmark"]) + 1] = k["nombre"]
    return out


def formulas_defecto(kpoints) -> tuple[str, str] | None:
    """(origen, escala) por defecto si el ejercicio trae hombros y caderas: origen = medio de caderas,
    escala = largo del tronco (medio de hombros -> medio de caderas). None si faltan."""
    c = codigos_de(kpoints)
    if not {12, 13, 24, 25} <= set(c):
        return None
    return "medio(C24,C25)", "dist(medio(C12,C13), medio(C24,C25))"


def k_a_c(texto, kpoints) -> str:
    """Formulas guardadas con K<n> (posicion en la lista, formato viejo) -> C<nn> fijo, segun el catalogo actual del ejercicio."""
    import re
    num = {k.get("numero"): k for k in kpoints or []}

    def cambia(m):
        o = (num.get(int(m.group(1))) or {}).get("origen") or {}
        i = POSE_LANDMARKS.index(o["landmark"]) + 1 if o.get("tipo") == "landmark" and o.get("landmark") in POSE_LANDMARKS else None
        return f"C{i:02d}" if i else m.group(0)
    return re.sub(r"\b[Kk](\d{1,3})\b", cambia, texto or "")


def escala_del_clip(valores) -> float:
    """Mediana de la escala sobre los cuadros validos (finitos y > 0): una escala por clip, estable ante un cuadro malo."""
    v = np.asarray(valores, dtype=np.float64)
    v = v[np.isfinite(v) & (v > EPS_ESCALA)]
    if not len(v):
        raise NormalizacionInvalida("la escala es 0 o no hay datos en ningun cuadro")
    return float(np.median(v))


def valores_formula(points, point_names, cfg) -> tuple[np.ndarray, np.ndarray]:
    """(origen (T,2) por cuadro, escala (T,) por cuadro) de la formula de cfg sobre los puntos del clip."""
    nombres = list(point_names)
    K = {}
    for n in set(FORM.usados(cfg["origen"])) | set(FORM.usados(cfg["escala"])):
        nom = (cfg.get("puntos") or {}).get(str(n))
        if nom not in nombres:
            raise NormalizacionInvalida(f"C{n:02d}: el punto {nom or '?'} no viene en este clip")
        K[n] = np.asarray(points[:, nombres.index(nom), :2], dtype=np.float64)
    try:
        return FORM.evaluar(cfg["origen"], K, "p"), FORM.evaluar(cfg["escala"], K, "n")
    except ValueError as e:
        raise NormalizacionInvalida(str(e)) from None


def _normalizar_formula(points, point_names, cfg):
    """(K - origen) / escala en x e y; z solo se divide por la escala (el origen es 2D). origen por cuadro, escala una por clip."""
    origen, esc = valores_formula(points, point_names, cfg)
    escala = escala_del_clip(esc)
    out = np.array(points, dtype=np.float32)
    out[..., :2] = (points[..., :2] - origen[:, None, :]) / escala
    out[..., 2:] = points[..., 2:] / escala
    return out


def _normalizar_punto(points, point_names, cfg):
    nombres = list(point_names)
    ic = nombres.index(cfg["punto_centro"])
    ia = nombres.index(cfg["punto_escala_a"])
    ib = nombres.index(cfg["punto_escala_b"])
    centrado = points - points[:, ic:ic + 1, :]
    escala = np.linalg.norm(points[:, ia, :] - points[:, ib, :], axis=-1)
    escala = np.where(escala > 1e-6, escala, 1.0).reshape(-1, 1, 1)
    return centrado / escala


def _normalizar_rectangulo(points, indices_caja=None):
    """Caja envolvente del clip completo -> lienzo fijo de 100x100 con un solo
    factor de escala (no deforma). Si se dan indices_caja, la caja sale solo
    de esos puntos pero la transformacion se aplica a todos."""
    ref = points[:, indices_caja, :] if indices_caja else points
    minimo = np.nanmin(ref, axis=(0, 1))
    ancho = max(np.nanmax(ref[..., 0]) - minimo[0], 1e-6)
    alto = max(np.nanmax(ref[..., 1]) - minimo[1], 1e-6)
    factor = min((LADO_LIENZO - 1) / ancho, (LADO_LIENZO - 1) / alto)
    return (points - minimo) * factor


def normalizar(points, point_names, cfg: dict) -> np.ndarray:
    """(T,N,3) crudo -> (n_frames_fijo,N,3) segun cfg (ya resuelta con cfg_para)."""
    if cfg["modo"] == "formula":
        fijo = _normalizar_formula(points, point_names, cfg)
    elif cfg["modo"] == "rectangulo":
        indices_caja = None
        if cfg.get("puntos_caja"):
            nombres = list(point_names)
            indices_caja = [nombres.index(n) for n in cfg["puntos_caja"] if n in nombres] or None
        fijo = _normalizar_rectangulo(points, indices_caja)
    else:
        fijo = _normalizar_punto(points, point_names, cfg)
    return resamplear(fijo, cfg["n_frames_fijo"])


# ---------------------------------------------------------------- la normalizacion de cada ejercicio (guide.json -> normalizacion)
def normalizacion_de(exercise):
    """Normalizacion del ejercicio (guide.json -> normalizacion): {origen, escala, n_frames, propia}. Lo que falte sale del
    defecto (hombros/caderas del catalogo; n_frames de config.json formato.n_frames_defecto). propia=False: la formula es la propuesta, nunca se guardo."""
    d = EJ.leer_def(exercise) or {}
    n = d.get("normalizacion") or {}
    por_defecto = formulas_defecto(d.get("kpoints")) or (None, None)
    origen, escala = (k_a_c(n.get(c), d.get("kpoints")) or None for c in ("origen", "escala"))
    return {"origen": origen or por_defecto[0], "escala": escala or por_defecto[1],
            "n_frames": int(n.get("n_frames") or params("formato")["n_frames_defecto"]), "propia": bool(n.get("origen") and n.get("escala"))}


def validar_normalizacion(norm, kpoints):
    """Valida {origen, escala, n_frames} contra el catalogo; ValueError con mensaje para el panel. -> dict limpio."""
    numeros = list(codigos_de(kpoints))
    n_frames = int(norm.get("n_frames") or 0)
    if not 2 <= n_frames <= 300:
        raise ValueError("n_frames debe estar entre 2 y 300")
    o, e = str(norm.get("origen") or "").strip(), str(norm.get("escala") or "").strip()
    FORM.validar(o, "p", numeros)
    FORM.validar(e, "n", numeros)
    return {"origen": o, "escala": e, "n_frames": n_frames}


def cfg_de_normalizacion(origen, escala, n_frames, kpoints):
    """cfg de modo 'formula' para estas formulas; ValueError si nombran un punto que el ejercicio no tiene marcado."""
    nombres = codigos_de(kpoints)
    usados = sorted(set(FORM.usados(origen) + FORM.usados(escala)))
    faltan = [f"C{u:02d}" + (f" ({POSE_LANDMARKS[u - 1]})" if 1 <= u <= len(POSE_LANDMARKS) else "") for u in usados if u not in nombres]
    if faltan:
        raise ValueError(f"la normalizacion usa {', '.join(faltan)}, que no esta marcado en los kpoints del ejercicio")
    return {**DEFAULT_CFG, "modo": "formula", "origen": origen, "escala": escala,
            "n_frames_fijo": int(n_frames), "puntos": {str(u): nombres[u] for u in usados}}


def cfg_normalizacion(exercise):
    """La cfg de normalizacion lista para procesamiento/puntos (la misma para gold, SQL, entrenamiento y modelo en vivo).
    Sin formula posible (ejercicio sin hombros/caderas y sin configurar) cae al modo antiguo 'rectangulo'."""
    n = normalizacion_de(exercise)
    if not (n["origen"] and n["escala"]):
        return {**DEFAULT_CFG, "modo": "rectangulo", "n_frames_fijo": n["n_frames"]}
    try:
        return cfg_de_normalizacion(n["origen"], n["escala"], n["n_frames"], EJ.kpoints_de_ejercicio(exercise))
    except ValueError as e:
        raise ValueError(f"'{exercise}': {e}. Corrigela en Kpoints -> Normalizacion") from None
