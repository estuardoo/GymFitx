"""Definicion de cada ejercicio: UNA sola fuente, parameters/ (antes ejercicios/<slug>.yaml + un espejo numerado).

    parameters/exercise.json       numero -> nombre, slug, fuente (source), sql_tipo, activo
    parameters/<n>/kpoints.json    los puntos del ejercicio
    parameters/<n>/angles.json     angulos / proporciones (features, con 'activo')
    parameters/<n>/guide.json      el resto: description, segmentation, signal, reglas, base_clip, clasificador...

leer() junta todo en el dict de siempre ({name, description, source, features, kpoints, ...}); guardar() lo reparte.
Un ejercicio archivado queda con su numero (reservado) pero inactivo: ya no aparece en slugs()."""

from __future__ import annotations

import json
from pathlib import Path

from src.nucleo import config as CFG
from src.nucleo import inputs as INP

SCHEMA = 1
_APARTE = ("name", "source", "kpoints", "features")      # name/source viven en exercise.json; el resto en su archivo


def _dir(ej: int) -> Path:
    return Path(CFG.PARAMETROS_DIR) / str(ej)


def _json(p: Path, defecto=None):
    try:
        return json.loads(p.read_text("utf-8"))
    except (OSError, ValueError):
        return defecto


def _fila(slug: str) -> tuple[int, dict] | None:
    for n, e in INP.ejercicios().items():
        if e.get("slug") == slug and e.get("activo", True):
            return n, e
    return None


def slugs() -> list[str]:
    """Ejercicios activos que tienen definicion."""
    return sorted(e["slug"] for n, e in INP.ejercicios().items()
                  if e.get("activo", True) and (_dir(n) / "guide.json").exists())


def existe(slug: str) -> bool:
    f = _fila(slug)
    return bool(f and (_dir(f[0]) / "guide.json").exists())


def leer(slug: str) -> dict | None:
    """La definicion completa del ejercicio (None si no existe)."""
    f = _fila(slug) if slug else None
    if not f:
        return None
    n, e = f
    guia = _json(_dir(n) / "guide.json")
    if guia is None:
        return None
    return {"name": e.get("nombre") or slug, "source": e.get("fuente", "pose"),
            "features": _json(_dir(n) / "angles.json", {}).get("angulos") or [],
            "kpoints": _json(_dir(n) / "kpoints.json", {}).get("kpoints") or [],
            **{k: v for k, v in guia.items() if k not in ("schema_version", "ejercicio")}}


def _escribir(ruta: Path, obj) -> None:
    INP._escribir(ruta, obj)


def guardar(slug: str, data: dict) -> int:
    """Escribe la definicion completa; guarda antes una copia de la anterior en sistema/respaldos/. -> numero del ejercicio."""
    anterior = leer(slug)
    if anterior is not None:
        r = Path(CFG.DATOS_DIR) / "respaldos" / f"{slug}.json"
        _escribir(r, anterior)
    n = INP.asegurar_ejercicio(slug, data.get("name"))
    with INP.LOCK:
        doc = INP._leer(CFG.EXERCISE_PATH, {"schema_version": SCHEMA, "ejercicios": {}})
        doc["ejercicios"][str(n)].update(nombre=data.get("name") or slug, fuente=data.get("source", "pose"))
        _escribir(CFG.EXERCISE_PATH, doc)
        d = _dir(n)
        _escribir(d / "kpoints.json", {"schema_version": SCHEMA, "ejercicio": n, "kpoints": data.get("kpoints") or []})
        _escribir(d / "angles.json", {"schema_version": SCHEMA, "ejercicio": n, "angulos": data.get("features") or []})
        _escribir(d / "guide.json", {"schema_version": SCHEMA, "ejercicio": n,
                                     **{k: v for k, v in data.items() if k not in _APARTE}})
    return n


def archivar(slug: str) -> None:
    """Lo saca de la lista (sigue con su numero y sus archivos; crear otro con el mismo nombre lo reactiva)."""
    INP.desactivar_ejercicio(slug)
