"""Etapa 3: cortar y etiquetar grabaciones (bien / mal / base / descarte por segmento).

datos/etiquetas.json es la UNICA fuente del etiquetado y se guarda por mezcla."""

from __future__ import annotations

import json
import threading

from src.etiquetado import editor_puntos as PUNTOS
from src.etiquetado.manifest import DATA, LABELS, _exercise_de, _ruta_video
from src.nucleo.config import AJUSTES_PATH
from src.procesamiento import offline as deteccion

CFG ={"clases": ["bien", "mal", "base", "descarte"], "no_exportar": ["descarte"]}


try:  # ponytail: yaml opcional; sin PyYAML se usan los defaults de arriba
    import yaml
    CFG.update((yaml.safe_load(AJUSTES_PATH.read_text("utf-8")) or {}).get("cortes") or {})
except Exception:
    pass


def videos():
    out = []
    for mp4 in sorted(DATA.rglob("*.mp4")):  # datos/grabaciones/<ejercicio>/<fecha>/*.mp4 -- recursivo
        meta = {}
        js = mp4.with_suffix(".json")
        if js.exists():
            try:
                meta = json.loads(js.read_text("utf-8"))
            except Exception:
                pass
        out.append({"file": mp4.relative_to(DATA).as_posix(), "ejercicio": meta.get("exercise_name", ""),
                    "dur_ms": meta.get("duration_ms", 0), "frames": meta.get("frames", 0),
                    "npz": meta.get("features", ""), "fps": meta.get("fps_medio", 0)})
    return out


def estado_config():
    return {"clases": CFG["clases"], "no_exportar": CFG["no_exportar"], "videos": videos()}


def leer_labels():
    return json.loads(LABELS.read_text("utf-8")) if LABELS.exists() else {}


def guardar_labels(body):
    # merge, no reemplazo: una pestana vieja que nunca cargo TODOS los
    # videos (dejada abierta de una sesion anterior) solo debe poder
    # tocar los videos que ella conoce -- sobrescribir el archivo
    # entero con su copia incompleta borraba el trabajo de otros
    # videos etiquetados despues, en otra pestana/sesion.
    actual = json.loads(LABELS.read_text("utf-8")) if LABELS.exists() else {}
    actual.update(body)
    LABELS.write_text(json.dumps(actual, indent=1, ensure_ascii=False), "utf-8")
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
    d = np.load(npz, allow_pickle=True) if npz.exists() else None
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
