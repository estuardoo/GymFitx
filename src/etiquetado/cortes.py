"""Etapa 3: cortar y etiquetar grabaciones (bien / mal / base / descarte por segmento).

Los cortes de cada video viven en la tabla `raw` de parameters/inputs.json (campo `segmentos`) y se guardan por mezcla."""

from __future__ import annotations

import json
import threading

from src.etiquetado import editor_puntos as PUNTOS
from src.etiquetado.manifest import _exercise_de, _ruta_video
from src.nucleo import inputs as INP
from src.nucleo.config import params
from src.nucleo.log import logger
from src.procesamiento import offline as deteccion

log = logger("dataset")

CFG = {"clases": ["bien", "mal", "descarte"], "no_exportar": ["descarte"]}


try:  # parameters/config.json -> "cortes"; sin esa seccion se usan los defaults de arriba
    CFG.update(params("cortes"))
except ValueError:
    pass


def videos():
    """Los videos de `raw` con su metadata (persona, fecha) y la del .json que graba GYMFITX."""
    tab = INP.tabla()
    out = []
    for r in tab["raw"]:
        mp4 = INP.ruta_raw(r["ej"], r["id"], "mp4")
        if not mp4.exists():
            continue
        meta = {}
        js = mp4.with_suffix(".json")
        if js.exists():
            try:
                meta = json.loads(js.read_text("utf-8"))
            except (OSError, ValueError) as e:   # JSON corrupto: el video sigue listado, sin metadatos
                log.warning("sin metadatos legibles en %s: %s", js.name, e)
        out.append({"file": INP.vid_de(r), "id": r["id"], "ej": r["ej"],
                    "ejercicio": meta.get("exercise_name") or INP.ejercicios().get(r["ej"], {}).get("nombre", ""),
                    "persona": r.get("persona"), "fecha": r.get("fecha"),
                    "dur_ms": meta.get("duration_ms", 0), "frames": meta.get("frames", 0),
                    "npz": meta.get("features", ""), "fps": meta.get("fps_medio", 0)})
    return out


def estado_config():
    return {"clases": CFG["clases"], "no_exportar": CFG["no_exportar"], "videos": videos()}


def leer_labels():
    return INP.leer_labels()


def guardar_labels(body):
    # merge, no reemplazo: una pestana vieja que nunca cargo TODOS los videos solo debe poder tocar los que ella conoce --
    # sobrescribir todo con su copia incompleta borraba el trabajo de otros videos etiquetados despues.
    INP.guardar_labels(body)
    return {"ok": True}


_OVERLAY_LOCK = threading.Lock()


def overlay_de(file):
    """Puntos en coordenadas de pantalla (0-1) por cuadro, para dibujar el esqueleto
    sobre el video mientras se reproduce. Si el video aun no tiene la
    deteccion con el catalogo actual, se corre aqui (la primera vez tarda)."""
    import numpy as np
    src = _ruta_video(file)
    if not src.exists():
        raise ValueError(f"No existe {file}")
    exercise = _exercise_de(src)
    kpoints = (PUNTOS.leer_ejercicio(exercise) or {}).get("kpoints") or []
    error = None
    with _OVERLAY_LOCK:  # una deteccion a la vez (mediapipe no es barato)
        try:
            deteccion.detectar_puntos_si_faltan(src, exercise)
        except deteccion.DeteccionNoDisponible as e:
            error = str(e)
    npz = src.with_suffix(".npz")
    d = np.load(npz, allow_pickle=False) if npz.exists() else None
    if d is None or "points_screen" not in d.files:
        return {"t_ms": [], "exercise": exercise,
                "error": error or "Este video todavia no tiene puntos de pantalla detectados"}

    def lista(arr):
        a = np.round(arr.astype(float), 4)
        return np.where(np.isfinite(a), a, None).tolist()

    out = {"t_ms": d["points_t_ms"].tolist(), "nombres": [str(n) for n in d["point_names"]],
           "puntos": lista(d["points_screen"]),
           "conexiones": PUNTOS.conexiones_kpoints(kpoints) if kpoints else [],
           "exercise": exercise, "error": error}
    return out
