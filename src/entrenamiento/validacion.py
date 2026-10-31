"""Etapa 6b: como se mide un modelo (k-fold estratificado, F1 macro, CV anidada)."""

from __future__ import annotations


def grupos_por_clase(y, grupos) -> int:
    """Grabaciones distintas de la clase que menos tiene (cada fold necesita al menos una de cada clase)."""
    return min(len({g for g, c in zip(grupos, y) if c == clase}) for clase in set(y))


def elegir_k(test_pct, conteo, clases, n, min_grupos=None):
    """Folds del k-fold: ~100/test_pct, sin pasar de la clase mas chica, de n/2 ni de las grabaciones de la clase mas chica."""
    tope = min(conteo[c] for c in clases)
    return max(2, min(round(100 / test_pct), tope, n // 2, min_grupos or tope))


class PorGrabacion:
    """Reemplaza al StratifiedKFold: .split(X, y) estratificado sin partir una grabacion entre entrenar y probar.
    Las copias (_2, _3) y los ciclos del mismo video van juntos; antes se mezclaban y el F1 salia inflado.
    `estratos` (p.ej. clase+persona) reparte cada estrato entre los folds: el azar queda condicionado a la persona,
    asi cada fold de prueba tiene clips de todas las personas en vez de tocar solo a una."""

    def __init__(self, k, grupos, semilla, estratos=None):
        import numpy as np
        self.k, self.grupos, self.semilla = k, np.asarray(grupos), semilla
        self.estratos = None if estratos is None else np.asarray(estratos)

    def split(self, X, y):
        from sklearn.model_selection import StratifiedGroupKFold
        y_est = y if self.estratos is None else self.estratos
        return StratifiedGroupKFold(self.k, shuffle=True, random_state=self.semilla).split(X, y_est, self.grupos)


def evaluar(nombre, est, X, y, skf):
    """Un modelo con CV: una sola pasada por fold (la prediccion sale del argmax de predict_proba).
    De paso anota cuantas iteraciones uso de verdad en cada fold ('iteraciones': tope y min/media/max)."""
    import time

    import numpy as np
    from sklearn.base import clone
    from sklearn.metrics import f1_score

    from src.entrenamiento import modelos as MODELOS
    t0 = time.time()
    y_pred = np.empty_like(y)
    y_proba = np.zeros((len(y), len(set(y))))
    con_proba, usadas = True, []
    try:
        for tr, te in skf.split(X, y):
            m = clone(est).fit(X[tr], y[tr])
            it = MODELOS.iteraciones_usadas(m)
            if it is not None:
                usadas.append(it)
            try:
                y_proba[te] = m.predict_proba(X[te])
            except Exception:   # modelos sin predict_proba (ridge...): solo la prediccion
                con_proba = False
            y_pred[te] = m.predict(X[te])
    except Exception as e:
        return {"nombre": nombre, "error": str(e)[:200]}
    if con_proba:
        y_pred = y_proba.argmax(axis=1)
    tope = MODELOS.tope(nombre)
    r = {"nombre": nombre, "accuracy": round(float((y_pred == y).mean()), 4),
         "f1_macro": round(float(f1_score(y, y_pred, average="macro", zero_division=0)), 4),
         "tiempo_seg": round(time.time() - t0, 2),
         "_est": est, "_y_pred": y_pred, "_y_proba": y_proba if con_proba else None}
    if tope and usadas:   # sin tope configurado (svm...) el numero no tiene contra que compararse
        r["iteraciones"] = {"tope": int(tope), "min": min(usadas), "media": round(float(np.mean(usadas)), 1),
                            "max": max(usadas), "freno": max(usadas) < tope}
    return r


def composicion_folds(skf, X, y, personas):
    """Por fold: cuantos clips de cada persona van a prueba y cuantos a entrenar. Sirve para ver que el azar
    reparte entre todas las personas (y no toma solo de una)."""
    import numpy as np
    personas = np.asarray(personas)
    nombres = sorted(set(personas.tolist()))
    out = []
    for i, (tr, te) in enumerate(skf.split(X, y)):
        out.append({"fold": i + 1,
                    "prueba": {p: int((personas[te] == p).sum()) for p in nombres},
                    "entreno": {p: int((personas[tr] == p).sum()) for p in nombres}})
    return out


def por_persona(y, y_pred, personas, clases):
    """Lo que acierta el modelo en los clips de cada persona, con las predicciones que ya salieron de los folds
    (no reentrena nada). Sirve para comparar P1 contra P2: con pocos clips una persona puede no decir mucho."""
    import numpy as np
    personas = np.asarray(personas)
    out = {}
    for p in sorted(set(personas.tolist())):
        m = personas == p
        reales = {c: int((y[m] == i).sum()) for i, c in enumerate(clases) if (y[m] == i).any()}
        out[p] = {"clips": int(m.sum()), "reales": reales,
                  "accuracy": round(float((y_pred[m] == y[m]).mean()), 4)}
    return out


def sin_privados(r):
    return {k: v for k, v in r.items() if not k.startswith("_")}


def cv_anidada(catalogo, X, y, skf):
    """Estimacion honesta del procedimiento completo "probar N modelos y
    quedarse con el mejor": en cada fold externo se elige el modelo con CV
    interna SOLO sobre la parte de entrenamiento y se mide en la de prueba.
    Sin esto, el % reportado es optimista (se elige y se mide con los mismos
    datos). None si hay muy pocos clips para una CV interna."""
    import numpy as np
    from sklearn.base import clone
    from sklearn.metrics import f1_score
    from sklearn.model_selection import StratifiedGroupKFold, StratifiedKFold, cross_val_score
    y_pred = np.empty_like(y)
    elegidos = []
    grupos = getattr(skf, "grupos", None)   # con grupos (PorGrabacion) la CV interna tampoco parte una grabacion
    for tr, te in skf.split(X, y):
        minimo = np.bincount(y[tr]).min() if len(set(y[tr])) == len(set(y)) else 0
        if grupos is not None and minimo:
            minimo = grupos_por_clase(y[tr], grupos[tr])
        if minimo < 2:
            return None
        n_int = min(3, int(minimo))
        semilla = getattr(skf, "semilla", getattr(skf, "random_state", 0))
        interna = (StratifiedGroupKFold(n_int, shuffle=True, random_state=semilla) if grupos is not None
                   else StratifiedKFold(n_splits=n_int, shuffle=True, random_state=semilla))
        g_tr = None if grupos is None else grupos[tr]
        mejor, mejor_f1 = None, -1.0
        for nombre, est in catalogo:
            try:
                f1 = float(np.mean(cross_val_score(clone(est), X[tr], y[tr], cv=interna, scoring="f1_macro", groups=g_tr)))
            except Exception:
                continue
            if f1 > mejor_f1:
                mejor, mejor_f1 = (nombre, est), f1
        if mejor is None:
            return None
        elegidos.append(mejor[0])
        y_pred[te] = clone(mejor[1]).fit(X[tr], y[tr]).predict(X[te])
    from collections import Counter
    return {"accuracy": round(float((y_pred == y).mean()), 4),
            "f1_macro": round(float(f1_score(y, y_pred, average="macro", zero_division=0)), 4),
            "elegidos": dict(Counter(elegidos))}
