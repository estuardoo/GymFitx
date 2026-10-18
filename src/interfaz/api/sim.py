"""SIM: verificacion visual de deteccion + normalizacion, sin recalcular nada nuevo.

3 vistas de un clip elegido:
  1. El video original (.mp4 ya cortado).
  2. Esqueleto CRUDO superpuesto en pantalla (points_screen guardado en el .npz del clip por
     src/etiquetado/exportar.recorta_npz) + el valor de cada angulo/proporcion activa, junto a sus puntos.
  3. Esqueleto NORMALIZADO (table_frames_fix de SQL) del clip elegido, YA ALINEADO en tiempo (DTW) contra
     el clip 'base' de su ejercicio -- la MISMA alineacion que calcula table_indicator (ver
     src/evaluacion/similitud.py), asi que lo que se ve aca es exactamente lo que puntua el sistema."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.almacenamiento import dataset_sql as SQL
from src.etiquetado import editor_puntos as PUNTOS
from src.etiquetado.manifest import OUT, _manifest, _tipo_o_primero
from src.evaluacion.similitud import alinear
from src.nucleo.ejercicio import features_de_ejercicio, kpoints_de_ejercicio
from src.procesamiento.medidas import features as FEAT

router = APIRouter()


def _conexiones_por_nombre(catalogo, nombres):
    """Pares (i, j) de PUNTOS.conexiones_kpoints() pero reindexados a la POSICION de cada kpoint dentro de
    'nombres' (el orden real del arreglo que se dibuja, que puede venir en otro orden -- o ser un
    subconjunto -- del catalogo del ejercicio), en vez del orden del catalogo. conexiones_kpoints() da
    indices relativos a 'catalogo'; ac se traduce cada uno por nombre y se descarta el hueso si algun
    extremo no esta en 'nombres', en vez de tirar TODAS las conexiones por un solo kpoint que no coincida."""
    idx = {n: i for i, n in enumerate(nombres)}
    pares = []
    for a, b in PUNTOS.conexiones_kpoints(catalogo):
        na, nb = catalogo[a].get("nombre"), catalogo[b].get("nombre")
        if na in idx and nb in idx:
            pares.append([idx[na], idx[nb]])
    return pares


def _fila_de(clip):
    fila = next((r for r in _manifest() if r["clip"] == clip), None)
    if not fila:
        raise ValueError(f"'{clip}' no esta en el manifest")
    return fila


def _npz_de(clip):
    """(fila del manifest, .npz abierto) del clip, o LookupError con el motivo."""
    try:
        fila = _fila_de(clip)
    except ValueError as e:
        raise LookupError(str(e)) from None
    npz_path = OUT / Path(fila["clip"]).parent / (fila.get("npz") or "")
    if not fila.get("npz") or not npz_path.exists():
        raise LookupError(f"'{clip}' no tiene .npz")
    return fila, np.load(npz_path, allow_pickle=True)


@router.get("/api/sim/opciones")
def sim_opciones(tipo=None):
    """Ejercicio(s) y sus clips por clase (igual que Descomposicion) -- para los selectores del panel."""
    tipo = _tipo_o_primero(tipo)
    rows = [r for r in _manifest() if r["type"] == tipo]
    clips = {"base": [], "bien": [], "mal": []}
    for row in rows:
        if row["clase"] in clips:
            clips[row["clase"]].append(row["clip"])
    return {"tipo": tipo, "tipos": SQL.tipos_conocidos(), "clips": clips}


def _puntos_por_metrica(nombres, kpoints, features):
    """{nombre_metrica: [nombres de puntos involucrados]} -- para poner el numero de cada angulo/proporcion
    cerca de sus puntos (centroide)."""
    return {f["name"]: list(dict.fromkeys([*f.get("points", []), *f.get("reference", []), *f.get("cadena", [])]))
            for f in FEAT.medibles(nombres, features)}


@router.get("/api/sim/crudo")
def sim_crudo(clip: str):
    """Puntos SIN normalizar (coordenadas de pantalla 0-1, ver points_screen) + angulos/proporciones,
    cuadro a cuadro, con su tiempo relativo al INICIO DEL CLIP -- para el overlay sincronizado sobre el
    video ya cortado (vista 2)."""
    try:
        fila, d = _npz_de(clip)
    except LookupError as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    if "points_screen" not in d.files or "points_t_ms" not in d.files:
        return JSONResponse({"error": "Este clip no tiene puntos de pantalla/tiempo todavia -- vuelve a "
                                       "'Generar Cortes' en Cut/Edit para regenerarlo"}, status_code=404)

    exercise = fila.get("exercise")
    kpoints = kpoints_de_ejercicio(exercise)
    nombres = [str(n) for n in d["point_names"]]
    points = d["points"]
    features = features_de_ejercicio(exercise)
    angulos, nombres_ang, _ = FEAT.medir_clip(points, nombres, features)
    puntos_por_metrica = _puntos_por_metrica(nombres, kpoints, features)

    def lista(arr):
        a = np.round(np.asarray(arr, dtype=float), 4)
        return np.where(np.isfinite(a), a, None).tolist()

    return {
        "t_ms": d["points_t_ms"].tolist(), "nombres": nombres,
        "puntos": lista(d["points_screen"]),
        "conexiones": _conexiones_por_nombre(kpoints, nombres) if kpoints else [],
        "angulos": lista(angulos), "nombres_angulos": nombres_ang,
        "angulos_puntos": [puntos_por_metrica.get(n, []) for n in nombres_ang],
    }


@router.get("/api/sim/cuerpo3d")
def sim_cuerpo3d(clip: str):
    """Puntos 3D en metros (world, origen en la cadera) del clip, cuadro a cuadro, para el avatar 3D de SIM."""
    try:
        _, d = _npz_de(clip)
    except LookupError as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    if "points" not in d.files or not len(d["points"]):
        return JSONResponse({"error": "Este clip no tiene puntos 3D"}, status_code=404)
    t = d["points_t_ms"] if "points_t_ms" in d.files else d["t_ms"] - d["t_ms"][0]   # relativo al inicio del clip
    p = np.round(np.asarray(d["points"], dtype=float), 4)
    return {"t_ms": np.asarray(t).tolist(), "nombres": [str(n) for n in d["point_names"]],
            "puntos": np.where(np.isfinite(p), p, None).tolist()}


@router.get("/api/sim/normalizado")
def sim_normalizado(tipo: int, base: str, clip: str):
    """Puntos normalizados+remuestreados (table_frames_fix de SQL) del clip 'base' y del 'clip' elegido, con
    este ultimo YA ALINEADO en tiempo (DTW) a los frames del base -- misma funcion (alinear(), ver
    evaluacion/similitud.py) que calcula table_indicator. No renormaliza nada: es la tabla que ya arma
    tablas.py, solo que aca se ve animada en vez de reducida a un numero (vista 3)."""
    try:
        frames_base = SQL.frames_de(tipo, base)
        frames_otro = SQL.frames_de(tipo, clip) if clip != base else frames_base
    except SQL.SQLServerNoDisponible as e:
        return JSONResponse({"error": f"SQL Server no disponible: {e}"}, status_code=400)
    if not frames_base:
        return JSONResponse({"error": f"'{base}' no tiene table_frames_fix todavia -- genera/actualiza las tablas SQL"}, status_code=404)
    if not frames_otro:
        return JSONResponse({"error": f"'{clip}' no tiene table_frames_fix todavia -- genera/actualiza las tablas SQL"}, status_code=404)

    try:
        exercise = _fila_de(base).get("exercise")
    except ValueError:
        exercise = None
    catalogo = kpoints_de_ejercicio(exercise) if exercise else []

    kpoints = [kp for kp in frames_base if kp in frames_otro]
    otro_alineado, base_out, indicadores = {}, {}, {}
    for kp in kpoints:
        alineado = alinear(frames_base[kp], frames_otro[kp])
        if alineado is None:
            continue
        xb, yb = frames_base[kp]["x"], frames_base[kp]["y"]
        zb = frames_base[kp].get("z") or [0.0] * len(xb)
        base_out[kp] = [[xb[i], yb[i], zb[i]] for i in range(len(xb))]
        otro_alineado[kp] = [[x, y, zb[i]] for i, (x, y) in enumerate(alineado)]   # z: se deja la del base (alinear() solo trabaja x,y)
        mxb, myb = sum(xb) / len(xb), sum(yb) / len(yb)
        ss_tot = sum((xb[i] - mxb) ** 2 + (yb[i] - myb) ** 2 for i in range(len(xb)))
        if ss_tot >= 1e-9:
            ss_res = sum((alineado[i][0] - xb[i]) ** 2 + (alineado[i][1] - yb[i]) ** 2 for i in range(len(xb)))
            indicadores[kp] = round(max(0.0, 1 - ss_res / ss_tot) * 100, 2)

    nombres = [kp for kp in kpoints if kp in base_out]
    conexiones = _conexiones_por_nombre(catalogo, nombres) if catalogo else []
    return {
        "nombres": nombres, "conexiones": conexiones,
        "base": [base_out[kp] for kp in nombres],
        "otro": [otro_alineado[kp] for kp in nombres],
        "indicadores": [indicadores.get(kp) for kp in nombres],
    }
