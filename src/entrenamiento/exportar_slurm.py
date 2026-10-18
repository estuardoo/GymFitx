"""Exporta, para UN ejercicio, los datos crudos por video y por cuadro (puntos x,y,z de cada kpoint y las
metricas -- angulos y proporciones activados -- ya normalizadas 0..1) a un .npz AUTOCONTENIDO: para leerlo
despues no hace falta SQL Server ni el resto de GYMFITX, solo numpy.

Pensado para copiarlo a un cluster/supercomputador y correr ahi scripts/busqueda_features_slurm.py (ver ese
archivo para el flujo completo). Se corre en la PC que SI tiene acceso a SQL Server:

    python scripts/exportar_dataset_slurm.py --ejercicio manguito_rotador

Repetible para cualquier ejercicio: solo cambia --ejercicio."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import numpy as np

from src.almacenamiento import dataset_sql as SQL
from src.entrenamiento.datos import CLASES_NO_ENTRENABLES, seleccion
from src.etiquetado.editor_puntos import codigo_kpoint, leer_ejercicio
from src.etiquetado.manifest import _manifest
from src.nucleo import ejercicio as EJ
from src.procesamiento.medidas import features as FEAT


def exportar(ejercicio: str, out) -> dict:
    """Arma y guarda el .npz de 'ejercicio' en 'out'. -> resumen para mostrar en consola."""
    tipo = SQL.tipo_de_ejercicio(ejercicio)
    point_names = EJ.puntos_de_ejercicio(ejercicio) or []
    if not point_names:
        raise ValueError(f"'{ejercicio}' no tiene catalogo de kpoints (arma uno en la pestaña Kpoints primero)")
    kpoints = (leer_ejercicio(ejercicio) or {}).get("kpoints") or []
    # codigo universal (C../M../D..) de cada point_names[i], mismo orden -- para no confundir el K0N de
    # busqueda_features_slurm.py (posicion en ESTE ejercicio) con el landmark real (ver config.json del AHPC)
    point_codes = [codigo_kpoint(kp, kpoints) for kp in kpoints] if kpoints else [""] * len(point_names)
    feats = FEAT.medibles(point_names, EJ.features_de_ejercicio(ejercicio))
    metric_names = [f["name"] for f in feats]
    metric_types = [f["type"] for f in feats]

    crudos = SQL.frames_fix_por_archivo(tipo)
    sel = seleccion()
    puntos, metricas, clips, y = [], [], [], []
    for row in _manifest():
        if row["type"] != tipo or row["clase"] in CLASES_NO_ENTRENABLES or sel.get(row["clip"]) is False:
            continue
        d = crudos.get(row["clip"])
        if d is None:   # clip sin table_frames_fix todavia (genera cortes + tablas SQL antes de exportar)
            continue
        puntos.append(d[0])
        metricas.append(d[1])
        clips.append(row["clip"])
        y.append(row["clase"])

    if not puntos:
        raise ValueError(f"Sin clips de '{ejercicio}' en table_frames_fix -- genera cortes y tablas SQL primero")

    largos = Counter(p.shape[0] for p in puntos)
    comun = largos.most_common(1)[0][0]
    if len(largos) > 1:   # clips con otra normalizacion/catalogo mezclados (otro n_frames_fijo): se descartan
        ok = [i for i, p in enumerate(puntos) if p.shape[0] == comun]
        puntos, metricas, clips, y = ([x[i] for i in ok] for x in (puntos, metricas, clips, y))

    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        out,
        points=np.stack(puntos).astype(np.float32), point_names=np.array(point_names),
        point_codes=np.array(point_codes),
        metrics=np.stack(metricas).astype(np.float32), metric_names=np.array(metric_names),
        metric_types=np.array(metric_types), clips=np.array(clips), y=np.array(y),
        ejercicio=ejercicio, tipo=tipo,
    )
    return {"archivo": str(out), "clips": len(clips), "frames_por_clip": comun, "kpoints": len(point_names),
            "metricas": len(metric_names), "clases": dict(Counter(y)), "point_codes": point_codes}
