"""Documentos que genera el pipeline (nunca a mano, para que no se desincronicen):
  - diccionario de datos: una fila por columna de la tabla final -> docs/diccionario/<ej>.csv y .md
  - informe de limpieza en Markdown -> reportes/<n>/limpieza.md (el .json lo escribe la etapa limpiar)
Sin marcas de tiempo ni nada que cambie de una corrida a otra: mismas entradas, mismos bytes."""

from __future__ import annotations

import csv

from src.etiquetado.editor_puntos import codigo_kpoint
from src.nucleo import inputs as INP
from src.nucleo.componentes import componentes, mascara_metricas
from src.nucleo.config import DICCIONARIO_DIR, REPORTES_DIR
from src.procesamiento.medidas.features import ESCALA_TIPO, medibles
from src.procesamiento.puntos.normalizacion import LADO_LIENZO

UNIDAD = {"angle": "grados", "proporcion": "%", "distance_ratio": "razon"}


def _escribir(ruta, texto: str) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="\n") as fh:   # \n siempre: el mismo archivo en Windows y en Linux
        fh.write(texto)


def columnas(spec: dict, nombres: list[str]) -> list[dict]:
    """Las columnas del vector, en el MISMO orden que `vectorizar.aplanar`: por cuadro, primero x/y/z de cada kpoint y
    luego las metricas activas (angulos / proporciones). `nombres` = kpoints que traen los clips (el orden del vector)."""
    cfg, n = spec["cfg"], int(spec["cfg"]["n_frames_fijo"])
    ejes = [("x", "y", "z")[i] for i in componentes(spec["features"])[0]]
    mets = medibles(nombres, spec["features_def"])
    cod = {k["nombre"]: codigo_kpoint(k, spec["kpoints"]) for k in spec["kpoints"]}
    activas = mascara_metricas([m["type"] for m in mets], spec["features"], len(mets))
    mets = [m for m, ok in zip(mets, activas) if ok]
    rect, form = cfg.get("modo") == "rectangulo", cfg.get("modo") == "formula"
    if form:   # K<N> = kpoint numero N del ejercicio; x,y: (K - origen) / escala, 4 decimales
        norm = f"(K - {cfg['origen']}) / ({cfg['escala']}) en x,y (z solo / escala); escala = mediana por clip; 4 decimales"
    else:
        norm = (f"caja {LADO_LIENZO}x{LADO_LIENZO} (rectangulo), 2 decimales" if rect
                else f"centrado en {cfg.get('punto_centro')} / distancia {cfg.get('punto_escala_a')}-{cfg.get('punto_escala_b')}")
    filas = []
    for f in range(1, n + 1):
        for p in nombres:
            for e in ejes:
                filas.append({"columna": f"f{f:02d}_{p}_{e}", "cuadro": f, "tipo": "kpoint", "unidad": "coordenada",
                              "rango": f"0..{LADO_LIENZO}" if rect else "libre (largos de escala)" if form else "libre", "origen": f"MediaPipe Pose {p}, eje {e}",
                              "transformacion": f"{norm}; remuestreado a {n} cuadros",
                              "descripcion": f"Posicion {e} de {p} en el cuadro {f} de {n} del ciclo"})
        for m in mets:
            expr = ">".join(cod.get(q, q) for q in (m.get("cadena") or [*m["points"], *m.get("reference", [])]))
            filas.append({"columna": f"f{f:02d}_{m['name']}", "cuadro": f, "tipo": m["type"], "unidad": UNIDAD.get(m["type"], m["type"]),
                          "rango": "0..1", "origen": expr,
                          "transformacion": f"valor / {ESCALA_TIPO.get(m['type'], 180.0):g}, recortado a 0..1; remuestreado a {n} cuadros",
                          "descripcion": f"{m['name']} ({UNIDAD.get(m['type'], m['type'])}) en el cuadro {f} de {n}"})
    return filas


def escribir_diccionario(ejercicio: str, spec: dict, filas: list[dict], n_features: int) -> None:
    """CSV + Markdown. Falla si las columnas descritas no son exactamente las de la tabla final (criterio: 100 %)."""
    if len(filas) != n_features:
        raise ValueError(f"el diccionario de '{ejercicio}' describe {len(filas)} columnas y la tabla final tiene {n_features}")
    cab = ["columna", "cuadro", "tipo", "unidad", "rango", "origen", "transformacion", "descripcion"]
    DICCIONARIO_DIR.mkdir(parents=True, exist_ok=True)
    with open(DICCIONARIO_DIR / f"{ejercicio}.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cab, lineterminator="\n")
        w.writeheader()
        w.writerows(filas)
    md = [f"# Diccionario de datos: {ejercicio}", "",
          f"{len(filas)} columnas = las de `input/gold/{ejercicio}/X.npy` (contrastado al generarlo) · componentes `{spec['features']}` · "
          f"{spec['cfg']['n_frames_fijo']} cuadros por ciclo.", "",
          "Lo genera `python -m src.preparacion.etapas formatear " + ejercicio + "` (etapa 3.5). El CSV trae ademas `cuadro` y `descripcion`.", "",
          "| columna | tipo | unidad | rango | origen | transformacion |", "|---|---|---|---|---|---|"]
    md += [f"| {f['columna']} | {f['tipo']} | {f['unidad']} | {f['rango']} | {f['origen']} | {f['transformacion']} |" for f in filas]
    _escribir(DICCIONARIO_DIR / f"{ejercicio}.md", "\n".join(md) + "\n")


def ruta_reporte(ejercicio: str, nombre: str):
    """output/reportes/<n>/<nombre>: los informes de un ejercicio, en su carpeta numerada."""
    return REPORTES_DIR / str(INP.id_de(ejercicio)) / nombre


def escribir_limpieza_md(inf: dict) -> None:
    p = inf["parametros"]
    md = [f"# Informe de limpieza: {inf['ejercicio']}", "",
          f"Umbrales de `parameters/config.json` (limpieza): min_frames={p['min_frames']}, max_nan_pct={p['max_nan_pct']}, aplicar={p['aplicar']}.", "",
          f"- Clips seleccionados para limpiar: **{inf['entran']}** de {inf['clips_total']} en el manifest",
          f"- Salen por la limpieza: **{inf['salen']}**" + (" (marcados, no se sacan: `aplicar: false`)" if not p["aplicar"] else ""),
          f"- Quedan para construir: **{inf['quedan']}** ({', '.join(f'{c}: {n}' for c, n in sorted(inf['por_clase_quedan'].items())) or 'ninguno'})",
          f"- Copias `_N` entre los que quedan (riesgo de fuga si se partiera por clip; se agrupan por grabacion): **{inf['copias']}**", "",
          "## Motivos", ""]
    md += [f"- {k}: {n}" for k, n in sorted(inf["motivos"].items())] or ["- (ninguno)"]
    md += ["", "## Clips marcados", "", "| clip | clase | cuadros | % NaN | motivos |", "|---|---|---|---|---|"]
    md += [f"| {c['clip']} | {c['clase']} | {c['cuadros']} | {c['nan_pct']} | {'; '.join(c['motivos'])} |" for c in inf["clips"] if c["motivos"]]
    _escribir(ruta_reporte(inf["ejercicio"], "limpieza.md"), "\n".join(md) + "\n")
