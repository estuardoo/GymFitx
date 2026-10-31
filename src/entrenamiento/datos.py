"""Etapa 6a: que clips entran al entrenamiento (seleccion manual) y armar X / y desde SQL."""

from __future__ import annotations

from src.almacenamiento import dataset_sql as SQL
from src.etiquetado.manifest import _manifest
from src.nucleo import inputs as INP
from src.nucleo.config import params
from src.preparacion.tabla import (  # noqa: F401 -- se re-exportan para quien ya los importaba de aqui
    CLASES_CICLO,
    grupo_de,
    seleccion,
    ventanas_fuera,
)


def guardar_seleccion(cambios, tipo=None):
    """cambios: {clip: bool}. Se guarda en la tabla `clips` (campo `usar`); por defecto todo clip nuevo SI se usa.
    Espejo en SQL (table_file.usar) si responde."""
    excluidos = INP.guardar_seleccion(cambios)
    if tipo is not None:
        try:
            SQL.marcar_uso(int(tipo), {c: bool(u) for c, u in cambios.items()})
        except SQL.SQLServerNoDisponible:
            pass
    return {"excluidos": excluidos}


def clips_entrenamiento(tipo=None):
    """Para la tabla 'Clips para entrenar': todos los clips del manifest de
    este type con su clase y si estan marcados para usarse."""
    sel = seleccion()
    return [{"clip": r["clip"], "clase": r["clase"], "origen": r["origen"], "seg": r.get("seg"),
             "ini": r.get("ini"), "fin": r.get("fin"), "dur": r.get("dur"), "type": r["type"],
             "usar": sel.get(r["clip"], True), "persona": r.get("persona") or "sin_persona"}
            for r in _manifest() if tipo is None or r["type"] == int(tipo)]


CLASES_NO_ENTRENABLES = tuple(params("seleccion")["excluir_clases"])   # parameters/config.json: 'base' es la referencia, no una clase a predecir


def armar(rows, tipo, features, tipos=None, vectores=None, personas=None):
    """X, y (clase) y clips de este type, mas lo que se dejo afuera y por que. `vectores` = {clip: vector} armado desde
    el disco (src/preparacion/etapas.py, lo normal); sin el se leen de table_frames_fix en SQL. `personas` = lista de
    personas (P1, P2...) que entran; None = todas. ValueError con un mensaje para el panel si no alcanza para entrenar."""
    from collections import Counter
    if vectores is not None:
        features_sql = vectores
    else:
        try:
            features_sql = SQL.features_por_archivo(tipo, features, tipos)
        except SQL.SQLServerNoDisponible as e:
            raise ValueError(f"No se pudo leer table_frames_fix: {e}") from None

    sel = seleccion()
    excluidos_manual, excluidos_persona, del_tipo, sin_sql, no_entrenables = [], [], [], [], []
    X, y, clips = [], [], []
    for r in rows:
        if r["type"] != tipo:
            continue
        if r["clase"] in CLASES_NO_ENTRENABLES:
            no_entrenables.append(r["clip"])
            continue
        if personas is not None and (r.get("persona") or "sin_persona") not in personas:  # casilla de persona en el panel
            excluidos_persona.append(r["clip"])
            continue
        if sel.get(r["clip"]) is False:  # desmarcado con clic en el panel (p.ej. mal etiquetado)
            excluidos_manual.append(r["clip"])
            continue
        del_tipo.append(r["clip"])
        vec = features_sql.get(r["clip"])
        if vec is None:
            sin_sql.append(r["clip"])
            continue
        X.append(vec)
        y.append(r["clase"])
        clips.append(r["clip"])
    # Vectores de largo distinto = quedaron en SQL con OTRO catalogo (otra mano,
    # otros puntos o angulos): se entrena con los al dia y se avisa.
    desincronizados = []
    if X and len({len(x) for x in X}) > 1:
        largo = Counter(len(x) for x in X).most_common(1)[0][0]
        desincronizados = [c for c, x in zip(clips, X) if len(x) != largo]
        clips = [c for c, x in zip(clips, X) if len(x) == largo]
        y = [cl for cl, x in zip(y, X) if len(x) == largo]
        X = [x for x in X if len(x) == largo]
    if len(X) < params("entrenamiento")["min_muestras"]:
        raise ValueError(
            f"Muy pocos clips para entrenar: {len(X)} utilizables de {len(del_tipo)} de este ejercicio en el manifest. "
            f"{len(sin_sql)} sin datos (tabla del disco o table_frames_fix){' (p.ej. ' + sin_sql[0] + ')' if sin_sql else ''}, "
            f"{len(excluidos_manual)} desmarcados a mano, {len(excluidos_persona)} de personas no marcadas, "
            f"{len(desincronizados)} con otro catalogo de puntos. "
            "Dale a 'Generar cortes' y luego a 'Generar / actualizar tablas'.")

    cont = Counter(y)
    excluidas = [c for c, n in cont.items() if n < 2]
    if excluidas:
        clips = [cl for cl, c in zip(clips, y) if c not in excluidas]
        X = [x for x, c in zip(X, y) if c not in excluidas]
        y = [c for c in y if c not in excluidas]
    if len(set(y)) < 2:
        raise ValueError(f"Se necesita al menos 2 clases con 2+ clips cada una para entrenar (excluidas por muy pocos clips: {excluidas or 'ninguna'})")
    return {"X": X, "y": y, "clips": clips, "conteo": cont, "excluidas": excluidas,
            "excluidos_manual": excluidos_manual, "excluidos_persona": excluidos_persona, "no_entrenables": no_entrenables,
            "desincronizados": desincronizados}
