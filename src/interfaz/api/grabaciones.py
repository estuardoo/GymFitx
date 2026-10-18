"""API de grabaciones: listar, descargar features en CSV y usar una toma como nueva base."""

from __future__ import annotations

import numpy as np
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

from src.evaluacion.plantilla import build_template, template_path
from src.interfaz.control import sesion
from src.nucleo.config import EXERCISES_DIR, RECORDINGS_DIR, TEMPLATES_DIR
from src.nucleo.ejercicio import load_all
from src.nucleo.tipos import FeatureVec
from src.procesamiento.medidas.features import FeatureExtractor
from src.sesion.grabacion import features_a_csv, listar_grabaciones, resolver_json, uso_en_disco

router = APIRouter()


class UsarComoBase(BaseModel):
    ruta_relativa: str


@router.get("/api/recordings")
def recordings(limit: int = 40, exercise: str | None = None) -> dict:
    return {"grabaciones": listar_grabaciones(RECORDINGS_DIR, limit, exercise),
            "disco": uso_en_disco(RECORDINGS_DIR)}


@router.get("/api/recordings/csv")
def recording_csv(ruta_relativa: str) -> Response:
    """Descarga en CSV las features (movimientos) ya guardadas en el .npz de
    una grabación -- los ángulos y proporciones del ejercicio, que ya se
    archivan automáticamente al terminar cada sesión.
    """
    try:
        json_path = resolver_json(RECORDINGS_DIR, ruta_relativa)
    except ValueError as e:
        raise HTTPException(400, str(e)) from None
    npz_path = json_path.with_suffix(".npz")
    if not npz_path.exists():
        raise HTTPException(404, "No se encontraron las features de esa grabación.")

    return Response(
        content=features_a_csv(npz_path),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{npz_path.stem}.csv"'},
    )


@router.post("/api/recordings/use_as_base")
def use_as_base(cfg: UsarComoBase) -> dict:
    """Recalibra la plantilla de un ejercicio a partir de una grabacion archivada.

    No hace falta redecodificar el video: las features de cada cuadro ya
    quedaron guardadas en el .npz cuando se archivo la sesion, asi que esto
    corre en milisegundos, sea cual sea el largo del video.
    """
    if sesion.activa:
        raise HTTPException(409, "Detén la sesión en curso antes de recalibrar una base.")

    try:
        json_path = resolver_json(RECORDINGS_DIR, cfg.ruta_relativa)
    except ValueError as e:
        raise HTTPException(400, str(e)) from None
    npz_path = json_path.with_suffix(".npz")
    if not json_path.exists() or not npz_path.exists():
        raise HTTPException(404, "No se encontraron los metadatos o las features de esa grabación.")

    import json
    meta = json.loads(json_path.read_text(encoding="utf-8"))
    slug = meta["exercise"]
    ejercicios = load_all(EXERCISES_DIR)
    if slug not in ejercicios:
        raise HTTPException(404, f"El ejercicio '{slug}' de esa grabación ya no existe.")
    ex = ejercicios[slug]
    extractor = FeatureExtractor(ex)

    z = np.load(npz_path, allow_pickle=False)
    valores, tiempos = z["values"], z["t_ms"]
    if list(z["names"]) != extractor.names:
        raise HTTPException(
            400, "El YAML de este ejercicio cambió desde que se grabó esta sesión "
                 "(las features no coinciden); no se puede recalibrar desde ella.")

    frames = [
        FeatureVec(values=valores[i], valid=~np.isnan(valores[i]), t_ms=int(tiempos[i]))
        for i in range(len(tiempos))
    ]
    try:
        plantilla = build_template(frames, ex, extractor)
    except ValueError as e:
        raise HTTPException(400, str(e)) from None

    plantilla.save(template_path(TEMPLATES_DIR, slug))
    resultado = plantilla.to_dict()
    sesion.bus.emit({"type": "template_saved", "exercise": slug, "template": resultado,
                     "origen": "grabacion"})
    return resultado
