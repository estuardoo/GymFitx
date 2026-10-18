"""Etapa 6: orquesta un entrenamiento: datos -> modelos + validacion -> reportes -> modelo.joblib con su spec."""

from __future__ import annotations

from src.almacenamiento import dataset_sql as SQL
from src.entrenamiento import datos as DATOS
from src.entrenamiento import modelos as MODELOS
from src.entrenamiento import reportes as REPORTES
from src.entrenamiento import validacion as VALID
from src.etiquetado import editor_puntos as PUNTOS
from src.etiquetado import tablas as TABLAS
from src.etiquetado.manifest import log
from src.nucleo import ejercicio as EJ
from src.nucleo.componentes import componentes, mascara_metricas
from src.nucleo.config import leer_ajustes, matriz_modelos, params, respaldo_sql
from src.preparacion import tabla as TABLA
from src.procesamiento.medidas import features as FEAT


def entrenar(test_pct=None, modelos=None, tipo=None, features="ambos", fuera=True):
    """Entrena y compara clasificadores sobre table_frames_fix de los clips del
    manifest, con el mismo k-fold para todos.

    - Criterio: F1 macro (no accuracy): con clases desbalanceadas un modelo que
      dice siempre la clase mayoritaria ya saca buen accuracy.
    - 'linea_base' (DummyClassifier, clase mas frecuente) se reporta para
      comparar; nunca puede ganar.
    - 'anidado' = estimacion sin sesgo del procedimiento de seleccion.
    - El modelo guardado lleva su 'spec' (puntos, normalizacion, features)
      para que el panel en vivo arme exactamente el mismo vector."""
    try:
        import joblib
        import matplotlib  # noqa: F401 -- lo usan las graficas (reportes.py)
        import numpy as np
        from sklearn.dummy import DummyClassifier
        from sklearn.metrics import classification_report, f1_score
        from sklearn.preprocessing import LabelEncoder
    except ImportError as e:
        raise ValueError(f"Falta instalar una libreria para entrenar: {e}. Corre: pip install scikit-learn matplotlib joblib") from None
    from collections import Counter
    from datetime import datetime

    # 1. datos: salen del DISCO (src/preparacion); SQL es solo una copia de respaldo
    test_pct = test_pct or params("entrenamiento")["test_pct"]
    rows = DATOS._manifest()
    if not rows:
        raise ValueError("No hay clips en el manifest: primero genera los cortes")
    if tipo in (None, ""):  # sin eleccion explicita: el ejercicio mas frecuente en el manifest
        tipo = Counter(r["type"] for r in rows).most_common(1)[0][0]
    tipo = int(tipo)
    ejes, con_ang, con_pro = componentes(features)
    if not ejes and not con_ang and not con_pro:
        raise ValueError("Elige al menos una cosa para el modelo: ejes (X, Y, Z), angulos o proporciones")
    exercise = SQL.tipos_conocidos().get(tipo, "?")
    feats0 = FEAT.medibles(EJ.puntos_de_ejercicio(exercise) or [], EJ.features_de_ejercicio(exercise))
    tipos = [f["type"] for f in feats0] or None
    spec = TABLA.spec_de(exercise, features, tipo)   # puntos, normalizacion (params.yaml) y angulos ACTIVADOS en Kpoints
    desde_sql = leer_ajustes().get("fuente_entrenamiento") == "sql"   # datos/config.json; por defecto el disco
    ds = DATOS.armar(rows, tipo, features, tipos, None if desde_sql else TABLA.vectores(exercise, spec))
    spec["n_features"] = len(ds["X"][0])
    kpoints, cfg_usada, feats = spec["kpoints"], spec["cfg"], spec["features_def"]
    nombres_pts = spec["point_names"]
    fuera_info = None
    if fuera:   # clase "fuera" (ventanas sin ciclo) para que el modelo cuente solo en vivo; sin grabaciones con cortes no pasa nada
        vecs, nombres_f, ventana_ms = DATOS.ventanas_fuera(exercise, spec, tope=len(ds["X"]))
        if len(vecs) >= 4:
            ds["X"] += vecs
            ds["y"] += ["fuera"] * len(vecs)
            ds["clips"] += nombres_f
            ds["conteo"]["fuera"] = len(vecs)
            spec["ventana_ms"] = ventana_ms
            fuera_info = {"n": len(vecs), "ventana_ms": ventana_ms}
    clips = ds["clips"]
    if tipos and (con_ang or con_pro) and ejes:   # pediste metricas pero las tablas SQL solo traen puntos: no entrenar en silencio
        solo_puntos = cfg_usada["n_frames_fijo"] * len(ejes) * len(EJ.puntos_de_ejercicio(exercise) or [])
        if len(ds["X"]) and len(ds["X"][0]) == solo_puntos:
            raise ValueError("Marcaste angulos/proporciones pero las tablas SQL de este ejercicio no los traen (solo puntos). "
                             "Dale a 'Regenerar todos los cortes' y luego a 'Generar / actualizar tablas'.")
    le = LabelEncoder()
    le.fit(sorted(set(ds["y"])))
    clases = list(le.classes_)
    X = np.array(ds["X"])
    y = le.transform(ds["y"])

    # 2. modelos y validacion
    grupos = [DATOS.grupo_de(c) for c in clips]   # una grabacion nunca queda a la vez en entrenar y en probar
    k = VALID.elegir_k(test_pct, ds["conteo"], clases, len(X), VALID.grupos_por_clase(ds["y"], grupos))
    skf = VALID.PorGrabacion(k, grupos, params("entrenamiento")["semilla"])
    catalogo = MODELOS.catalogo()
    if modelos:
        catalogo = [(n, e) for n, e in catalogo if n in modelos]
        if not catalogo:
            raise ValueError("Ningun modelo valido seleccionado")
    resultados = [VALID.evaluar(n, e, X, y, skf) for n, e in catalogo]
    linea_base = VALID.sin_privados(VALID.evaluar("linea_base", DummyClassifier(strategy="most_frequent"), X, y, skf))
    validos = [r for r in resultados if "accuracy" in r]
    if not validos:
        raise ValueError("Ningun modelo pudo entrenarse: " +
                         "; ".join(f"{r['nombre']}: {r.get('error', '?')}" for r in resultados))
    validos.sort(key=lambda r: (r["f1_macro"], r["accuracy"]), reverse=True)
    mejor = validos[0]
    anidado = VALID.cv_anidada(catalogo, X, y, skf)

    # 3. reportes
    numero, out = REPORTES.nueva_corrida()
    y_pred, y_proba = mejor["_y_pred"], mejor["_y_proba"]
    REPORTES.grafico_comparacion(out, numero, resultados, linea_base, mejor)
    REPORTES.grafico_confusion(out, numero, y, y_pred, clases, mejor["nombre"])
    REPORTES.grafico_roc(out, numero, y, y_proba, clases, mejor["nombre"])

    # 4. modelo + spec: la 'llave' para comparar corridas y para que el vivo arme el MISMO vector
    angulos = []
    if con_ang or con_pro:
        medidos = FEAT.medibles(nombres_pts, feats)
        medidos = [f for f, ok in zip(medidos, mascara_metricas([f["type"] for f in medidos], features, len(medidos))) if ok]
        if medidos:   # [nombre, recorrido con codigos (C05>C06>C07), tipo]
            cod = {k["nombre"]: PUNTOS.codigo_kpoint(k, kpoints) for k in kpoints}
            angulos = [[f["name"], ">".join(cod.get(p, p) for p in (f.get("cadena") or [*f["points"], *f.get("reference", [])])), f["type"]]
                       for f in medidos]
    mejor["_est"].fit(X, y)  # el mejor modelo, reentrenado con todos los datos disponibles
    it_final = MODELOS.iteraciones_usadas(mejor["_est"]) if MODELOS.tope(mejor["nombre"]) else None
    joblib.dump({"modelo": mejor["_est"], "clases": clases, "nombre": mejor["nombre"], "spec": spec},
                out / "modelo.joblib")

    respaldo = TABLAS.respaldar_sql([r for r in rows if r["type"] == tipo]) if respaldo_sql()["al_entrenar"] else None   # copia en SQL Server; si no responde, solo se anota

    # F1 del ganador en cada fold (mismos folds que la CV): su desviacion dice cuanto es ruido
    f1_folds = [round(float(f1_score(y[te], y_pred[te], average="macro", zero_division=0)), 4) for _, te in skf.split(X, y)]
    reporte = classification_report(y, y_pred, labels=range(len(clases)), target_names=clases, output_dict=True, zero_division=0)
    predicciones = [{"clip": clips[i], "real": clases[y[i]], "prediccion": clases[y_pred[i]], "ok": bool(y[i] == y_pred[i])} for i in range(len(clips))]
    meta = {"numero": numero, "fecha": datetime.now().isoformat(timespec="seconds"),
            "test_pct": test_pct, "k": k, "n_muestras": len(X), "clases": clases,
            "excluidas": ds["excluidas"], "no_entrenables": len(ds["no_entrenables"]), "criterio": "f1_macro",
            "mejor_modelo": mejor["nombre"], "accuracy": mejor["accuracy"], "f1_macro": mejor["f1_macro"],
            "linea_base": linea_base, "anidado": anidado, "reporte": reporte,
            "errores": sum(1 for pr in predicciones if not pr["ok"]), "predicciones": predicciones,
            "modelos": [VALID.sin_privados(r) for r in resultados],
            "tipo": tipo, "exercise": exercise, "config": cfg_usada,
            "features": features, "excluidos_manual": ds["excluidos_manual"],
            "desincronizados": ds["desincronizados"],
            # lo que define la corrida (para compararla con la anterior): kpoints numerados 1..N por su
            # posicion, angulos como [nombre, 'a-b-c'] y cuantos clips de cada clase entraron
            "kpoints_usados": nombres_pts if ejes else [], "ejes": "".join("xyz"[i] for i in ejes),
            "angulos": [list(a) for a in angulos],
            # epocas/max_iter/parar con los que se entreno (matriz de config) y cuantas iteraciones uso el ganador
            # al reentrenar con todo ('iteraciones' de cada modelo, por fold, va dentro de 'modelos')
            "matriz_modelos": {n: f for n, f in matriz_modelos().items() if n in {r["nombre"] for r in resultados}},
            "iteraciones_mejor": {"tope": MODELOS.tope(mejor["nombre"]), "usadas": it_final} if it_final is not None else None,
            "f1_folds": f1_folds, "f1_std": round(float(np.std(f1_folds)), 4), "n_features": int(X.shape[1]),
            "conteo_clases": {c: int(n) for c, n in Counter(ds["y"]).items()}, "fuera": fuera_info,
            "validacion": "StratifiedGroupKFold por grabacion", "grabaciones": len(set(grupos)),
            "fuente": "sql" if desde_sql else "disco", "respaldo_sql": respaldo}
    REPORTES.guardar_meta(out, meta)
    log.info(REPORTES.matriz_iteraciones(numero, meta["modelos"]))
    log.info(f"entrenar run_{numero}: tipo={exercise} (type {tipo}), mejor={mejor['nombre']} "
             f"f1={mejor['f1_macro']} acc={mejor['accuracy']} (linea base f1={linea_base.get('f1_macro')}), "
             f"anidado={anidado}, n_muestras={len(X)}, features={features}")
    meta = REPORTES.entrenamientos()[-1]  # la misma corrida, ya con 'vs_anterior'
    if meta["vs_anterior"]:
        v = meta["vs_anterior"]
        log.info(f"entrenar run_{numero} vs run_{v['contra']}: {v['veredicto']} (dF1={v['delta_f1']:+.3f}, "
                 f"dAcc={v['delta_accuracy']:+.3f}); cambios: {', '.join(v['cambios']) or 'ninguno'}")
    return meta
