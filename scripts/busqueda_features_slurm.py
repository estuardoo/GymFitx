#!/usr/bin/env python3
"""Busqueda aleatoria de que kpoints/angulos/proporciones mueven el accuracy y el F1 de un ejercicio.

Standalone a proposito -- solo necesita numpy + scikit-learn, nada de GYMFITX -- para poder correrlo en un
cluster/supercomputador copiando UNICAMENTE este archivo y el .npz de scripts/exportar_dataset_slurm.py
(el modulo AHPC del panel arma ambos en un .zip listo para subir).

Flujo completo (repetible para cualquier ejercicio: solo cambia --ejercicio / --dataset):
  1. En la PC con SQL Server (o desde la pestana AHPC del panel):
       python scripts/exportar_dataset_slurm.py --ejercicio <nombre>
     -> datos/slurm/<nombre>.npz
  2. Copia ese .npz (y este script) al cluster.
  3. Ahi:
       python busqueda_features_slurm.py --dataset <nombre>.npz --z 300 --salida resultados.csv
     Para repartir las Z pruebas en un SLURM array (mas rapido, mismas combinaciones divididas entre
     tareas): --tarea-id/--n-tareas -- ver slurm_busqueda_features.sbatch, un ejemplo de sbatch listo.
  4. Mientras corre (o cuando termine): cada tarea deja un <salida>.estado.json (cuantas combinaciones ya
     hizo, cuantas le tocan, % y si termino) -- scripts/estado_busqueda_slurm.py junta los de todas las
     tareas del array en una tabla (no necesita numpy/sklearn, se puede correr en el cluster aunque el
     modulo de python este roto). ponytail: si una tarea revienta a mitad de una combinacion, su
     estado.json se queda pegado en el ultimo % con terminado=false para siempre -- cruzalo con sacct
     (ver LEEME.txt) para distinguir "sigue corriendo" de "fallo".
  5. Para ver la matriz resumen, la tabla de detalle y la grafica de progreso a partir del/los .csv que
     salieron: scripts/resumen_busqueda_slurm.py (se corre en tu PC, no hace falta el cluster para eso).

Que hace: cada 'prueba' es UNA combinacion al azar -- un subconjunto de tamano al azar (1..m) de los m
kpoints del ejercicio (con sus 3 ejes x,y,z), un subconjunto (1..p) de sus p angulos y un subconjunto (1..q)
de sus q proporciones -- y la entrena/mide, con el catalogo COMPLETO de modelos (los mismos ~14 del panel
Entrenamiento), con el mismo k-fold para todos.

El .csv de salida trae una fila por (escenario, modelo), TODO codificado -- nada de nombres/texto (esos ya
estan en tu tabla SQL): llave (= escenario*100 + codigo del modelo, ver MODELOS_CODIGO), type, modelo
(codigo), escenario, K01..KN/A01..AN/P01..PN (1 si ese kpoint/angulo/proporcion se uso en esta fila, 0 si
no -- mismo orden que point_names/metric_types de ese ejercicio en el .npz), accuracy, f1_macro, error.

Combinaciones que NO se repiten entre corridas, y 'escenario' es GLOBAL y persistente: cada combinacion
probada queda anotada en un '<dataset>.historial.json' junto al .npz (o el que le pases con --historial),
con el numero de escenario que le toco -- ese numero es suyo para siempre, nunca se reasigna ni se repite,
asi hayas corrido el script muchas veces. Si vuelves a correr el script sobre el mismo dataset (mismo o
distinto --semilla/--z), las Z combinaciones nuevas EXCLUYEN las que ya estan en ese historial y siguen la
numeracion de escenario donde se quedo -- asi cada corrida agrega escenarios nuevos, nunca repite ni
renumera los de antes. Borra ese .json si alguna vez quieres empezar de cero.

--heuristico: por default el sorteo es puro azar (cada kpoint/angulo/proporcion tiene la misma chance de
entrar). Con --heuristico, antes de sortear se entrena UNA vez un RandomForest de referencia con TODO
activado, se mide que tan importante fue cada kpoint/angulo/proporcion (feature_importances_), y el sorteo
de las Z combinaciones queda sesgado hacia lo que mas importa -- sigue habiendo exploracion (nada llega a
probabilidad 0), pero deja de tratar todo por igual. Con el mismo Z, suele encontrar mejores combinaciones
mas rapido que el azar puro; el costo es una corrida de referencia extra al principio (no cuenta contra Z).

--escalada: ACTIVADO POR DEFECTO (ver PARAMETROS POR DEFECTO mas abajo) -- CADA TAREA hace su propio
hill-climbing local en vez de sortear combinaciones sueltas: prueba un lote inicial al azar de --lote
combinaciones (tambien sesgado por --heuristico si esta activo; por default LOTE_PCT_POR_DEFECTO de --z), se
queda con las --arranques mejores (por default ARRANQUES_PCT_POR_DEFECTO de ese lote) y desde cada una prueba
vecinos -- un solo kpoint/angulo/proporcion agregado o quitado a la vez -- moviendose hacia el vecino apenas
uno mejora el accuracy y descartandolo si no, hasta --intentos-sin-mejora vecinos seguidos sin mejorar o
hasta agotar el presupuesto de esa cadena. Usa --no-escalada para el azar puro de siempre (cada combinacion
un sorteo independiente, --z es el total de la corrida repartido entre tareas en vez del presupuesto POR
TAREA). Cada tarea explora sola, sin coordinarse con las demas (cada una tiene su propio bloque de
escenario_id y su propio '<dataset>.historial.tN.json'), asi que sigue corriendo en paralelo igual de bien
que el modo sin escalada -- lo que cambia es que cada tarea, en vez de recibir una lista pareja de
combinaciones al azar, persigue su propio mejor resultado local. Todo se sigue comparando contra la
linea_base (escenario=-1) de siempre.

--arranques (multi-arranque, solo tiene efecto con --escalada, que es el default): en vez de escalar desde
LA mejor combinacion del lote inicial nomas, cada tarea se queda con las --arranques mejores de ese lote y
escala una cadena de vecinos INDEPENDIENTE desde cada una, repartiendo lo que queda del presupuesto (--z
menos el lote) entre todas a partes iguales -- distinto punto de partida puede llegar a un optimo local
distinto, asi que el mejor de todas las cadenas suele ser mas robusto que una sola escalada que se puede
quedar pegada en el primer optimo que encuentra. Las cadenas comparten el historial de la tarea (ninguna
re-explora lo que otra ya probo). Por default se calcula solo (ver PARAMETROS POR DEFECTO), no hace falta
pasarlo a mano."""

from __future__ import annotations

import argparse
import csv
import json
import random
import time
import warnings
from pathlib import Path

import numpy as np

# sklearn avisa (FutureWarning) de cosas que van a cambiar en versiones futuras (ej: SVC(probability=True))
# -- no afecta el resultado de esta corrida, solo ensucia el log de miles de combinaciones. Se silencia aca
# nomas (no cambia el comportamiento de nada, solo lo que se imprime).
warnings.filterwarnings("ignore", category=FutureWarning)

# Codigo numerico fijo de cada modelo -- fijo a mano (no "el orden en que modelos() los devuelve") porque
# lightgbm/catboost/xgboost solo aparecen si estan instalados: si dependiera del orden de modelos(), el mismo
# numero significaria un modelo distinto segun que maquina lo corrio. 0 = fila de referencia (linea_base).
MODELOS_CODIGO = {
    "linea_base": 0, "random_forest": 1, "extra_trees": 2, "gradient_boosting": 3,
    "hist_gradient_boosting": 4, "adaboost": 5, "logistic": 6, "sgd_logistico": 7, "ridge": 8, "lda": 9,
    "svm": 10, "knn": 11, "decision_tree": 12, "mlp": 13, "naive_bayes": 14,
    "lightgbm": 15, "catboost": 16, "xgboost": 17,
}

# --escalada: cada tarea reserva su propio bloque de escenario_id (tarea_id * esto) para no chocar con las
# demas SIN coordinarse -- de sobra para cualquier corrida real (una tarea explorando mas de 100k
# combinaciones nuevas en una sola corrida no es realista).
RESERVA_ESCENARIOS_POR_TAREA = 100_000

# ============================================================================
# PARAMETROS POR DEFECTO DE LA BUSQUEDA -- todos juntos aca arriba para poder ajustarlos a mano sin tener
# que ir a buscarlos en el resto del archivo. Cualquiera se puede pisar por linea de comandos (--escalada/
# --no-escalada, --lote, --arranques, --intentos-sin-mejora) sin tocar este archivo.
#
# Por que hill-climbing (multi-arranque) y no azar puro por default: con un lote inicial del
# LOTE_PCT_POR_DEFECTO de --z, te quedas con el ARRANQUES_PCT_POR_DEFECTO de ese lote como semillas, y
# escalas el 1-LOTE_PCT_POR_DEFECTO restante del presupuesto desde esas semillas (ver escalada() mas abajo)
# -- con los valores de aca abajo: 20% del presupuesto para explorar al azar, te quedas con el 10% mejor de
# ESE 20%, y usas el 80% restante del presupuesto escalando (probando vecinos) desde esas semillas.
# ============================================================================
ESCALADA_POR_DEFECTO = True          # False (o --no-escalada) = azar puro, un sorteo independiente por combinacion
LOTE_PCT_POR_DEFECTO = 0.20          # % de --z para el lote inicial al azar, antes de escalar
ARRANQUES_PCT_POR_DEFECTO = 0.10     # % del lote inicial que se usa como semillas para escalar (top-N)
INTENTOS_SIN_MEJORA_POR_DEFECTO = 10  # vecinos seguidos sin mejorar antes de que una cadena se detenga
# ============================================================================


def _lote_y_arranques(z: int, lote: int | None, arranques: int | None) -> tuple[int, int]:
    """Resuelve --lote/--arranques cuando no se pasaron por linea de comandos (quedan en None): el
    LOTE_PCT_POR_DEFECTO de --z para el lote inicial, y el ARRANQUES_PCT_POR_DEFECTO de ESE lote como
    semillas para escalar (ver PARAMETROS POR DEFECTO arriba) -- minimo 1 en ambos casos. Un --lote/
    --arranques explicito por linea de comandos siempre gana, se usa tal cual."""
    if lote is None:
        lote = max(1, round(z * LOTE_PCT_POR_DEFECTO))
    if arranques is None:
        arranques = max(1, round(lote * ARRANQUES_PCT_POR_DEFECTO))
    return lote, arranques


def cargar(ruta):
    d = np.load(ruta, allow_pickle=True)
    return {"points": d["points"], "point_names": [str(n) for n in d["point_names"]],
            "metrics": d["metrics"], "metric_names": [str(n) for n in d["metric_names"]],
            "metric_types": [str(t) for t in d["metric_types"]],
            "y": np.array([str(v) for v in d["y"]]), "clips": [str(c) for c in d["clips"]],
            "ejercicio": str(d["ejercicio"]), "tipo": int(d["tipo"]) if "tipo" in d.files else 0}


def grupo_de(clip):
    """Grabacion de origen del clip (igual que src/entrenamiento/datos.py): sus ciclos y copias _2/_3 no se separan entre entrenar y probar."""
    import re
    return re.sub(r"_s\d+.*$", "", Path(clip).stem)


GRUPOS = None   # ponytail: global para no cambiar la firma de evaluar(); lo fija main() con la grabacion de cada clip


def elegir_k(y, test_pct, grupos=None):
    conteo = {c: int((y == c).sum()) for c in set(y)}
    tope = min(conteo.values())
    if grupos is not None:   # cada fold necesita al menos una grabacion de cada clase
        tope = min(tope, min(len({g for g, v in zip(grupos, y) if v == c}) for c in conteo))
    return max(2, min(round(100 / test_pct), tope, len(y) // 2))


def _elige_subconjunto(rng, n, pesos):
    """Subconjunto de tamano al azar (1..n). Sin pesos: azar uniforme. Con pesos: sesgado hacia los indices
    de mayor peso via muestreo ponderado sin reemplazo (Efraimidis-Spirakis: clave = u**(1/peso), top-k)."""
    if not n:
        return []
    k = rng.randint(1, n)
    if pesos is None:
        return sorted(rng.sample(range(n), k))
    claves = sorted(((rng.random() ** (1 / pesos[i]), i) for i in range(n)), reverse=True)
    return sorted(i for _, i in claves[:k])


def combinacion_azar(rng, m, p, q, pesos_m=None, pesos_p=None, pesos_q=None):
    """Un subconjunto de tamano al azar (1..n) por categoria -- [] si esa categoria no tiene nada que elegir.
    Sin pesos_*: azar uniforme (default). Con pesos_*: sesgado hacia los indices de mayor peso -- ver
    importancias() / --heuristico."""
    return (_elige_subconjunto(rng, m, pesos_m), _elige_subconjunto(rng, p, pesos_p), _elige_subconjunto(rng, q, pesos_q))


def _normalizar_con_piso(valores, piso):
    """Normaliza a pesos > 0 con un 'piso' -- ningun indice llega a probabilidad ~0 (se conserva exploracion)."""
    n = len(valores)
    if not n:
        return []
    tot = sum(valores)
    if tot <= 0:
        return [1.0] * n
    return [piso / n + (1 - piso) * (v / tot) for v in valores]


def importancias(ds, idx_metric_ang, idx_metric_pro, piso=0.1):
    """Para --heuristico: entrena UNA vez un RandomForest de referencia con TODO activado (no cuenta contra
    --z) y devuelve (pesos_m, pesos_p, pesos_q) -- que tan importante fue cada kpoint/angulo/proporcion
    (feature_importances_, sumada sobre frames y ejes x,y,z), listos para combinacion_azar."""
    from sklearn.ensemble import RandomForestClassifier
    m = len(ds["point_names"])
    idx_metric = idx_metric_ang + idx_metric_pro
    X = vector(ds, list(range(m)), idx_metric)
    est = RandomForestClassifier(n_estimators=150, random_state=42)
    est.fit(X, ds["y"])
    imp = est.feature_importances_

    n_frames = ds["points"].shape[1]
    ancho_puntos = n_frames * m * 3
    imp_pts = imp[:ancho_puntos].reshape(n_frames, m, 3).sum(axis=(0, 2))
    imp_met = imp[ancho_puntos:].reshape(n_frames, len(idx_metric)).sum(axis=0)
    p = len(idx_metric_ang)

    return (_normalizar_con_piso(list(imp_pts), piso),
            _normalizar_con_piso(list(imp_met[:p]), piso),
            _normalizar_con_piso(list(imp_met[p:]), piso))


def _firma(combo):
    pts, ang, pro = combo
    return f"{pts}|{ang}|{pro}"


def historial_de(args) -> Path:
    return Path(args.historial) if args.historial else Path(args.dataset).with_name(Path(args.dataset).stem + ".historial.json")


def cargar_historial(ruta: Path) -> dict:
    """{firma: escenario_id}. escenario_id es GLOBAL y nunca se reasigna -- una vez que una combinacion entra
    aca, ese numero es suyo para siempre (para esta exercise/--historial), aunque corras el script mil veces."""
    return json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else {}


def guardar_historial(ruta: Path, vistas: dict) -> None:
    ruta.write_text(json.dumps(dict(sorted(vistas.items(), key=lambda kv: kv[1])), ensure_ascii=False), encoding="utf-8")


def guardar_estado(ruta: Path, **campos) -> None:
    """Archivo chico (<salida>.estado.json) que esta tarea se va sobreescribiendo sola cada vez que termina
    una combinacion -- para saber cuanto avanzo, si termino o si sigue corriendo SIN depender de sacct/squeue
    ni de contar filas del .csv. Lo lee scripts/estado_busqueda_slurm.py (arma una tabla con todas las tareas
    del array); no necesita numpy/sklearn, se puede mirar aunque el job siga corriendo."""
    campos["actualizado"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    ruta.write_text(json.dumps(campos, ensure_ascii=False), encoding="utf-8")


def guardar_avance_txt(ruta: Path, **campos) -> None:
    """<salida>.avance.txt -- lo mismo que guardar_estado() pero en texto plano (un 'cat' en el cluster
    alcanza, sin json.loads) y actualizado cada 5 min nomas (no en cada combinacion): pensado para un
    vistazo rapido de 'n/total' por tarea sin generar IO de mas en corridas con combinaciones muy rapidas.
    Al terminar la tarea se le agrega 'fin' y 'duracion_seg' (ver main)."""
    ruta.write_text("\n".join(f"{k}: {v}" for k, v in campos.items()) + "\n", encoding="utf-8")


def vecino(rng, combo, m, p, q):
    """Un vecino de 'combo' para hill-climbing (--escalada): voltea (agrega o quita) UN solo elemento al
    azar en K, A o P -- el cambio minimo posible, para explorar alrededor del mejor punto encontrado hasta
    ahora en vez de saltar a un punto completamente distinto. Nunca deja una categoria en 0 si ya tenia 1
    (evita el vecino vacio)."""
    pts, ang, pro = [list(x) for x in combo]
    categorias = [(pts, m), (ang, p), (pro, q)]
    j = rng.choice([j for j, (_, n) in enumerate(categorias) if n])
    g, n = categorias[j]
    i = rng.randrange(n)
    if i in g:
        if len(g) > 1:
            g.remove(i)
    else:
        g.append(i)
    return tuple(sorted(grupo) for grupo, _ in categorias)


def combinaciones_nuevas(rng, m, p, q, z, vistas: dict, intentos_por_combo=200,
                          pesos_m=None, pesos_p=None, pesos_q=None, base_id=None):
    """Hasta 'z' combinaciones que NO esten en 'vistas' (mismo objeto -- se va llenando, y a cada nueva le
    asigna el siguiente escenario_id GLOBAL, nunca antes usado en este historial). Si el espacio de
    combinaciones ya se agoto (todas probadas en corridas anteriores), devuelve las que alcanzo a encontrar.
    pesos_*: ver combinacion_azar / --heuristico. base_id: si se pasa, arranca la numeracion ahi en vez de
    max(vistas)+1 -- lo usa --escalada para reservar un bloque de ids propio por tarea. Devuelve
    [(escenario_id, combo), ...]."""
    siguiente = base_id if base_id is not None else max(vistas.values(), default=0) + 1
    nuevas = []
    for _ in range(z):
        for _ in range(intentos_por_combo):
            c = combinacion_azar(rng, m, p, q, pesos_m, pesos_p, pesos_q)
            f = _firma(c)
            if f not in vistas:
                vistas[f] = siguiente
                nuevas.append((siguiente, c))
                siguiente += 1
                break
        else:
            print(f"  espacio de combinaciones agotado tras {len(nuevas)}/{z}: ya se probo todo lo posible")
            break
    return nuevas


def escalada(rng, m, p, q, z, vistas: dict, evaluar_combo, lote=10, intentos_sin_mejora=10, arranques=1,
             pesos_m=None, pesos_p=None, pesos_q=None, base_id=None):
    """Hill-climbing local para UNA tarea (--escalada), en vez de puro azar: un lote inicial de hasta 'lote'
    combinaciones nuevas (sesgadas si hay pesos_*, via combinaciones_nuevas) y, desde ahi, prueba vecinos
    (vecino(): un solo elemento agregado/quitado) -- si uno mejora se mueve ahi y sigue escalando, si no lo
    descarta y prueba otro, hasta 'intentos_sin_mejora' vecinos seguidos sin mejorar o hasta agotar el
    presupuesto de ese arranque. vistas: se muta in-place igual que combinaciones_nuevas. evaluar_combo(
    escenario, combo) -> accuracy: la inyecta main() (aca no se sabe nada de sklearn).

    arranques (multi-arranque, >1 --arranques): en vez de escalar solo desde LA mejor del lote, se queda con
    las 'arranques' mejores y escala UNA cadena de vecinos independiente desde CADA UNA, repartiendo lo que
    queda del presupuesto ('z' menos el lote) entre ellas a partes iguales -- distinto punto de partida =
    distinto optimo local al que puede llegar cada una, asi que el mejor de todas suele ser mas robusto que
    escalar desde un solo punto (que puede quedar pegado en el primer optimo que encuentra). Las cadenas
    comparten 'vistas': ninguna re-explora un vecino que otra ya probo. arranques=1 (default) = comportamiento
    de siempre, una sola cadena con todo el presupuesto.

    Devuelve (mejor_combo, mejor_score) de TODAS las cadenas -- None, -1.0 si el lote no encontro ninguna
    combinacion nueva (espacio agotado desde el primer intento)."""
    presupuesto = z
    iniciales = combinaciones_nuevas(rng, m, p, q, min(lote, presupuesto), vistas,
                                      pesos_m=pesos_m, pesos_p=pesos_p, pesos_q=pesos_q, base_id=base_id)
    presupuesto -= len(iniciales)

    evaluadas = [(evaluar_combo(escenario, combo), combo) for escenario, combo in iniciales]
    if not evaluadas:
        return None, -1.0
    evaluadas.sort(key=lambda t: t[0], reverse=True)   # estable: ante empate, la primera vista del lote gana

    k = max(1, min(arranques, len(evaluadas)))
    semillas = evaluadas[:k]
    por_arranque = [presupuesto // k] * k
    for i in range(presupuesto % k):   # el resto de la division se reparte entre las primeras cadenas
        por_arranque[i] += 1

    mejor_combo, mejor_score = semillas[0][1], semillas[0][0]
    for (score0, combo0), presupuesto_cadena in zip(semillas, por_arranque):
        actual, actual_score, sin_mejora = combo0, score0, 0
        while presupuesto_cadena > 0 and sin_mejora < intentos_sin_mejora:
            c = vecino(rng, actual, m, p, q)
            f = _firma(c)
            if f in vistas:   # ya se probo (por esta cadena, otro arranque, u otra tarea en una corrida anterior)
                sin_mejora += 1
                continue
            eid = max(vistas.values()) + 1   # sigue la numeracion donde se quedo el lote/bloque de esta tarea
            vistas[f] = eid
            presupuesto_cadena -= 1
            score = evaluar_combo(eid, c)
            if score > actual_score:
                actual, actual_score, sin_mejora = c, score, 0
            else:
                sin_mejora += 1
        if actual_score > mejor_score:
            mejor_combo, mejor_score = actual, actual_score
    return mejor_combo, mejor_score


def vector(ds, idx_pts, idx_metric):
    """(n_clips, F): por cuadro, los ejes x,y,z de los kpoints elegidos + las metricas elegidas, concatenados."""
    P = ds["points"][:, :, idx_pts, :]
    M = ds["metrics"][:, :, idx_metric]
    n = P.shape[0]
    return np.concatenate([P.reshape(n, -1), M.reshape(n, -1)], axis=1)


def modelos():
    """El catalogo COMPLETO -- los mismos ~14 modelos que compara el panel Entrenamiento (src/entrenamiento/
    modelos.py), copiado aqui a mano porque este script es standalone (no puede hacer 'from src...' en el
    cluster). lightgbm/catboost/xgboost se suman solo si estan instalados, igual que alla."""
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    from sklearn.ensemble import (
        AdaBoostClassifier,
        ExtraTreesClassifier,
        GradientBoostingClassifier,
        HistGradientBoostingClassifier,
        RandomForestClassifier,
    )
    from sklearn.linear_model import LogisticRegression, RidgeClassifier, SGDClassifier
    from sklearn.naive_bayes import GaussianNB
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.neural_network import MLPClassifier
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.svm import SVC
    from sklearn.tree import DecisionTreeClassifier

    def escalado(est):
        return make_pipeline(StandardScaler(), est)

    out = [
        ("random_forest", RandomForestClassifier(n_estimators=200, random_state=42)),
        ("extra_trees", ExtraTreesClassifier(n_estimators=200, random_state=42)),
        ("gradient_boosting", GradientBoostingClassifier(n_estimators=150, random_state=42)),
        ("hist_gradient_boosting", HistGradientBoostingClassifier(min_samples_leaf=2, random_state=42)),
        ("adaboost", AdaBoostClassifier(n_estimators=150, random_state=42)),
        ("logistic", escalado(LogisticRegression(max_iter=2000))),
        ("sgd_logistico", escalado(SGDClassifier(loss="log_loss", random_state=42))),
        ("ridge", escalado(RidgeClassifier())),
        ("lda", escalado(LinearDiscriminantAnalysis(solver="lsqr", shrinkage="auto"))),
        ("svm", escalado(SVC(probability=True, random_state=42))),
        ("knn", escalado(KNeighborsClassifier(n_neighbors=3))),
        ("decision_tree", DecisionTreeClassifier(random_state=42)),
        ("mlp", escalado(MLPClassifier(hidden_layer_sizes=(32,), max_iter=2000, random_state=42))),
        ("naive_bayes", GaussianNB()),
    ]
    try:
        from lightgbm import LGBMClassifier
        out.append(("lightgbm", LGBMClassifier(n_estimators=200, num_leaves=15, min_child_samples=1,
                                                 verbose=-1, random_state=42)))
    except ImportError:
        pass
    try:
        from catboost import CatBoostClassifier
        out.append(("catboost", CatBoostClassifier(iterations=200, depth=4, verbose=0, random_seed=42, allow_writing_files=False)))
    except ImportError:
        pass
    try:
        from xgboost import XGBClassifier
        out.append(("xgboost", XGBClassifier(n_estimators=200, max_depth=4, eval_metric="logloss", random_state=42)))
    except ImportError:
        pass
    return out


def evaluar(nombre, est, X, y, skf):
    from sklearn.metrics import f1_score
    from sklearn.model_selection import cross_val_predict
    try:
        pred = cross_val_predict(est, X, y, cv=skf, groups=GRUPOS)
    except Exception as e:
        return {"modelo": nombre, "accuracy": None, "f1_macro": None, "error": str(e)[:150]}
    return {"modelo": nombre, "accuracy": round(float((pred == y).mean()), 4),
            "f1_macro": round(float(f1_score(y, pred, average="macro", zero_division=0)), 4), "error": ""}


def campos(m, p, q):
    """Nombres de columna del .csv -- todo codificado (nada de texto: los nombres de kpoints/angulos/
    proporciones ya estan en el .npz/tabla SQL de origen, aca solo van sus POSICIONES). K/A/P van en el
    mismo orden que point_names/metric_types de ese ejercicio -- por eso el ancho cambia segun el ejercicio."""
    return (["llave", "type", "modelo", "escenario"] + [f"K{j + 1:02d}" for j in range(m)]
            + [f"A{j + 1:02d}" for j in range(p)] + [f"P{j + 1:02d}" for j in range(q)]
            + ["accuracy", "f1_macro", "error"])


def _fila(escenario, idx_pts, idx_ang, idx_pro, ds, m, p, q, r):
    """llave = escenario*100 + codigo_modelo: identifica esta fila SIN coordinar entre las tareas paralelas
    del array (cada una calcula su propia llave sola, y nunca choca con la de otra) -- alcanza con que
    escenario ya sea unico (lo garantiza cargar_historial/combinaciones_nuevas). -1/-1 para la linea base."""
    modelo_cod = MODELOS_CODIGO.get(r["modelo"], -1)
    llave = -1 if escenario == -1 else escenario * 100 + modelo_cod
    fila = {"llave": llave, "type": ds["tipo"], "modelo": modelo_cod, "escenario": escenario}
    fila.update({f"K{j + 1:02d}": int(j in idx_pts) for j in range(m)})
    fila.update({f"A{j + 1:02d}": int(j in idx_ang) for j in range(p)})
    fila.update({f"P{j + 1:02d}": int(j in idx_pro) for j in range(q)})
    fila["accuracy"] = r["accuracy"]
    fila["f1_macro"] = r["f1_macro"]
    fila["error"] = r["error"]
    return fila


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dataset", required=True, help=".npz de scripts/exportar_dataset_slurm.py")
    ap.add_argument("--z", type=int, default=200, help="limite de combinaciones NUEVAS a probar en esta corrida (no exhaustivo)")
    ap.add_argument("--semilla", type=int, default=0, help="misma semilla = mismo orden de sorteo (el historial igual evita repetir)")
    ap.add_argument("--test-pct", type=int, default=20)
    ap.add_argument("--salida", default="resultados_busqueda.csv")
    ap.add_argument("--historial", default="", help="default: <dataset>.historial.json -- combinaciones ya probadas, para no repetirlas")
    ap.add_argument("--tarea-id", type=int, default=0, help="SLURM array: indice de esta tarea (0-based)")
    ap.add_argument("--n-tareas", type=int, default=1, help="SLURM array: cuantas tareas en total")
    ap.add_argument("--heuristico", action="store_true",
                     help="sesga el sorteo hacia lo que mas mueve el accuracy en vez de azar puro -- entrena una "
                          "referencia extra (no cuenta contra --z), ver docstring")
    ap.add_argument("--escalada", action=argparse.BooleanOptionalAction, default=ESCALADA_POR_DEFECTO,
                     help="cada tarea hace su propio hill-climbing local (lote inicial + vecinos del mejor "
                          "encontrado) en vez de solo evaluar combinaciones al azar -- ver docstring. Con "
                          "--escalada (default), --z es el presupuesto POR TAREA (con --no-escalada, es el "
                          "total de la corrida repartido entre tareas)")
    ap.add_argument("--lote", type=int, default=None,
                     help=f"--escalada: tamano del lote inicial al azar por tarea, antes de escalar (default: "
                          f"{LOTE_PCT_POR_DEFECTO:.0%} de --z, ver PARAMETROS POR DEFECTO)")
    ap.add_argument("--intentos-sin-mejora", type=int, default=INTENTOS_SIN_MEJORA_POR_DEFECTO,
                     help="--escalada: cuantos vecinos seguidos sin mejorar antes de que esa cadena se detenga")
    ap.add_argument("--arranques", type=int, default=None,
                     help=f"--escalada (multi-arranque): en vez de escalar solo desde LA mejor del lote inicial, "
                          f"escala desde las N mejores (una cadena de vecinos independiente por cada una), "
                          f"repartiendo el presupuesto restante entre ellas -- mas robusto contra quedarse en "
                          f"un optimo local (default: {ARRANQUES_PCT_POR_DEFECTO:.0%} del lote inicial, ver "
                          f"PARAMETROS POR DEFECTO)")
    ap.add_argument("--modelo", default="", help="nombre de MODELOS_CODIGO (arriba del archivo, ej. "
                     "random_forest/svm/xgboost): evalua SOLO ese modelo en vez del catalogo completo (~18). "
                     "Para repartir el paralelismo POR MODELO en vez de por --n-tareas: --array=0-(N_MODELOS-1) "
                     "con un modelo distinto por tarea (ver slurm_busqueda_features.sbatch) en vez de --array=0-71 "
                     "-- cada tarea entrena UN modelo nomas, mucho mas liviano; evita que el cluster corte una "
                     "corrida que intenta los ~18 modelos juntos en muchas tareas en paralelo")
    args = ap.parse_args(argv)
    if args.escalada:
        args.lote, args.arranques = _lote_y_arranques(args.z, args.lote, args.arranques)

    ds = cargar(args.dataset)
    from sklearn.model_selection import StratifiedGroupKFold
    global GRUPOS
    GRUPOS = np.array([grupo_de(c) for c in ds["clips"]])
    m = len(ds["point_names"])
    idx_metric_ang = [i for i, t in enumerate(ds["metric_types"]) if t == "angle"]
    idx_metric_pro = [i for i, t in enumerate(ds["metric_types"]) if t in ("proporcion", "distance_ratio")]
    p, q = len(idx_metric_ang), len(idx_metric_pro)
    print(f"{ds['ejercicio']}: {len(ds['clips'])} clips, {m} kpoints, {p} angulos, {q} proporciones")
    if not m:
        raise SystemExit("El dataset no tiene kpoints: nada que combinar")

    y = ds["y"]
    k = elegir_k(y, args.test_pct, GRUPOS)
    skf = StratifiedGroupKFold(n_splits=k, shuffle=True, random_state=42)
    cat = modelos()
    if args.modelo:
        cat = [(n, e) for n, e in cat if n == args.modelo]
        if not cat:
            raise SystemExit(f"--modelo {args.modelo!r} no es un modelo conocido (ver MODELOS_CODIGO en este archivo)")
    print(f"{len(cat)} modelos: {', '.join(n for n, _ in cat)}")

    hist_ruta = historial_de(args)

    # --escalada + varias tareas: cada tarea descubre SUS PROPIAS combinaciones (dependen de sus resultados,
    # no se pueden precalcular igual para todas como en el modo normal) -- cada una guarda su propio
    # <hist_ruta>.tN.json para no pisarse al escribir, y al arrancar junta el de TODAS (propio.glob) para no
    # repetir combinaciones que ya encontro otra tarea en una corrida anterior.
    if args.escalada and args.n_tareas > 1:
        propia_ruta = hist_ruta.with_name(hist_ruta.stem + f".t{args.tarea_id}.json")
        vistas_globales = {}
        for p_hist in sorted(hist_ruta.parent.glob(hist_ruta.stem + ".t*.json")):
            vistas_globales.update(json.loads(p_hist.read_text(encoding="utf-8")))
        propio = cargar_historial(propia_ruta)
    else:
        propia_ruta = hist_ruta
        vistas_globales = cargar_historial(hist_ruta)
        propio = vistas_globales
    print(f"historial: {len(vistas_globales)} combinaciones ya probadas en corridas anteriores ({hist_ruta.name})")

    pesos_m = pesos_p = pesos_q = None
    if args.heuristico:
        print("--heuristico: entrenando referencia (RandomForest, todo activado) para pesar el sorteo...")
        pesos_m, pesos_p, pesos_q = importancias(ds, idx_metric_ang, idx_metric_pro)

    if not args.escalada:
        # + len(vistas): sin esto, repetir el mismo --semilla sobre un historial que YA tiene combinaciones
        # (por ejemplo, volver a correr el mismo comando) reproduce EXACTAMENTE la misma secuencia de sorteo
        # que la genero la primera vez -- todas colisionan con 'vistas' de entrada y se agota
        # intentos_por_combo antes de llegar a una combinacion nueva. Sumar cuantas ya hay corre el punto de
        # partida del sorteo.
        rng = random.Random(args.semilla + len(vistas_globales))
        combos = combinaciones_nuevas(rng, m, p, q, args.z, vistas_globales, pesos_m=pesos_m, pesos_p=pesos_p, pesos_q=pesos_q)
        if args.tarea_id == 0:   # ya tiene la lista completa de esta corrida (todas las tareas la generan igual): la deja anotada
            guardar_historial(hist_ruta, vistas_globales)
        # sharding por posicion LOCAL (j), no por escenario_id -- el id ya es global y no sirve para repartir parejo
        mias = [(eid, c) for j, (eid, c) in enumerate(combos) if j % args.n_tareas == args.tarea_id]
        print(f"tarea {args.tarea_id}/{args.n_tareas}: {len(mias)} de {len(combos)} combinaciones nuevas, k={k}-fold")

    # se escribe cada fila apenas se calcula (no todo junto al final): si el job se corta por tiempo, lo ya
    # calculado queda en el .csv en vez de perderse. 'top5' (resumen impreso al final) se guarda aparte en
    # memoria nomas -- no afecta lo que ya esta en disco.
    salida = Path(args.salida)
    top5 = []
    n_filas = 0

    # avance/estado (ver guardar_estado): 'objetivo' es un TECHO, no una promesa -- en modo normal es cuanto
    # le toco a esta tarea (mias), en --escalada es el presupuesto (puede terminar antes si converge o si se
    # agota el espacio de combinaciones).
    objetivo = args.z if args.escalada else len(mias)
    estado_ruta = salida.with_suffix(".estado.json")
    guardar_estado(estado_ruta, tarea=args.tarea_id, n_tareas=args.n_tareas, combos=0, objetivo=objetivo,
                    filas=0, pct=0.0, terminado=False, error="")

    # .avance.txt: igual que estado.json pero en texto plano y cada 5 min nomas (ver guardar_avance_txt) --
    # tambien deja inicio/fin de ESTA tarea (con --modelo, de ese modelo puntual) para saber cuanto demoro.
    avance_ruta = salida.with_suffix(".avance.txt")
    t_inicio_wall = time.time()
    inicio_iso = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(t_inicio_wall))
    ultimo_avance = t_inicio_wall
    guardar_avance_txt(avance_ruta, modelo=args.modelo or "todos", avance=f"0/{objetivo}", inicio=inicio_iso)
    with salida.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos(m, p, q))
        w.writeheader()

        if args.tarea_id == 0:   # referencia: todo activado, con un clasificador que no aprende nada (siempre la clase mas frecuente)
            from sklearn.dummy import DummyClassifier
            todo = (list(range(m)), list(range(p)), list(range(q)))
            r = evaluar("linea_base", DummyClassifier(strategy="most_frequent"), vector(ds, todo[0], idx_metric_ang + idx_metric_pro), y, skf)
            fila = _fila(-1, *todo, ds, m, p, q, r)
            w.writerow(fila)
            f.flush()
            n_filas += 1

        mejor_acc = -1.0   # avisa en vivo cada vez que una combinacion sube el accuracy en >= 1 punto porcentual
        combos_hechos = 0

        def evaluar_combo(escenario, combo):
            """Entrena/mide el catalogo COMPLETO de modelos sobre 'combo', escribe una fila por modelo (con
            el aviso de 'nuevo mejor' en vivo) y devuelve el mejor accuracy visto en esa combinacion -- lo
            que usa --escalada para decidir si un vecino mejora el punto actual o no."""
            nonlocal n_filas, mejor_acc, combos_hechos, ultimo_avance
            idx_pts, idx_ang, idx_pro = combo
            idx_metric = [idx_metric_ang[a] for a in idx_ang] + [idx_metric_pro[a] for a in idx_pro]
            X = vector(ds, idx_pts, idx_metric)
            n_elem = len(idx_pts) + len(idx_ang) + len(idx_pro)
            mejor_de_esta_combo = -1.0
            for nombre, est in cat:
                r = evaluar(nombre, est, X, y, skf)
                fila = _fila(escenario, idx_pts, idx_ang, idx_pro, ds, m, p, q, r)
                w.writerow(fila)
                f.flush()
                n_filas += 1
                if fila["f1_macro"] is not None:
                    top5.append((fila["f1_macro"], fila["accuracy"], nombre, escenario, n_elem))
                    top5.sort(key=lambda t: t[0], reverse=True)
                    del top5[5:]
                if fila["accuracy"] is not None:
                    mejor_de_esta_combo = max(mejor_de_esta_combo, fila["accuracy"])
                    if fila["accuracy"] >= mejor_acc + 0.01:
                        mejor_acc = fila["accuracy"]
                        print(f"  ** nuevo mejor acc={fila['accuracy']:.3f} ({nombre})  escenario={escenario}  "
                              f"K={[kk + 1 for kk in idx_pts]} A={[a + 1 for a in idx_ang]} P={[a + 1 for a in idx_pro]}")
            combos_hechos += 1
            guardar_estado(estado_ruta, tarea=args.tarea_id, n_tareas=args.n_tareas, combos=combos_hechos,
                            objetivo=objetivo, filas=n_filas, pct=round(100 * combos_hechos / objetivo, 1) if objetivo else 100.0,
                            terminado=False, error="")
            ahora = time.time()
            if ahora - ultimo_avance >= 300:   # cada 5 min nomas, no en cada combinacion (ver guardar_avance_txt)
                ultimo_avance = ahora
                guardar_avance_txt(avance_ruta, modelo=args.modelo or "todos", avance=f"{combos_hechos}/{objetivo}",
                                    inicio=inicio_iso)
            return mejor_de_esta_combo

        t0 = time.time()
        if args.escalada:
            rng = random.Random(args.semilla + args.tarea_id)   # cada tarea escala DESDE UN PUNTO DISTINTO -- semilla propia
            base_id = max(vistas_globales.values(), default=0) + args.tarea_id * RESERVA_ESCENARIOS_POR_TAREA + 1
            vistas_tarea = dict(vistas_globales)
            antes = set(vistas_tarea)
            mejor_combo, mejor_score = escalada(rng, m, p, q, args.z, vistas_tarea, evaluar_combo,
                                                 lote=args.lote, intentos_sin_mejora=args.intentos_sin_mejora,
                                                 arranques=args.arranques,
                                                 pesos_m=pesos_m, pesos_p=pesos_p, pesos_q=pesos_q, base_id=base_id)
            descubiertas = {f: eid for f, eid in vistas_tarea.items() if f not in antes}
            propio.update(descubiertas)
            guardar_historial(propia_ruta, propio)
            print(f"tarea {args.tarea_id}/{args.n_tareas}: {len(descubiertas)} combinaciones nuevas exploradas "
                  f"(escalada, mejor score={mejor_score:.3f})" if mejor_combo else
                  f"tarea {args.tarea_id}/{args.n_tareas}: sin combinaciones nuevas (espacio agotado desde el lote inicial)")
        else:
            for j, (escenario, combo) in enumerate(mias):
                evaluar_combo(escenario, combo)
                if (j + 1) % 10 == 0:
                    print(f"  combo {j + 1}/{len(mias)}: {n_filas} filas, {time.time() - t0:.0f}s")

    guardar_estado(estado_ruta, tarea=args.tarea_id, n_tareas=args.n_tareas, combos=combos_hechos,
                    objetivo=objetivo, filas=n_filas, pct=round(100 * combos_hechos / objetivo, 1) if objetivo else 100.0,
                    terminado=True, error="")
    t_fin_wall = time.time()
    guardar_avance_txt(avance_ruta, modelo=args.modelo or "todos", avance=f"{combos_hechos}/{objetivo}",
                        inicio=inicio_iso, fin=time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(t_fin_wall)),
                        duracion_seg=round(t_fin_wall - t_inicio_wall, 1))

    print(f"\n{n_filas} filas -> {salida}")
    for f1, acc, nombre, escenario, n_elem in top5:
        print(f"  {nombre:14s} f1={f1:.3f} acc={acc:.3f}  escenario={escenario} elementos={n_elem}")


if __name__ == "__main__":
    main()
