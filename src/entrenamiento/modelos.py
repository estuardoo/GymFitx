"""Catalogo de clasificadores a comparar (sklearn siempre; lightgbm/xgboost si estan instalados)."""

from __future__ import annotations

from src.nucleo.config import matriz_modelos, params

SEMILLA = params("entrenamiento")["semilla"]   # params.yaml


def catalogo():
    """Catalogo de clasificadores a comparar. sklearn siempre disponible (14 modelos);
    lightgbm/xgboost/catboost se agregan solo si estan instalados (import tolerante), igual que
    el patron usado en SUBVALUACION/ML/src/registry.py (solo se leyo ese proyecto, no se edito)."""
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

    def escalado(est):   # los modelos sensibles a la escala (distancias, gradientes) llevan su propio StandardScaler
        return make_pipeline(StandardScaler(), est)

    M = matriz_modelos()   # epocas / max_iter / parar de cada modelo (src/nucleo/config.py, editable desde Entrenamiento)
    out = [
        ("random_forest", RandomForestClassifier(n_estimators=M["random_forest"]["epocas"], random_state=SEMILLA)),
        ("extra_trees", ExtraTreesClassifier(n_estimators=M["extra_trees"]["epocas"], random_state=SEMILLA)),
        ("gradient_boosting", GradientBoostingClassifier(
            n_estimators=M["gradient_boosting"]["epocas"], random_state=SEMILLA, tol=M["gradient_boosting"]["tol"],
            n_iter_no_change=M["gradient_boosting"]["paciencia"] if M["gradient_boosting"]["parar"] else None)),
        ("hist_gradient_boosting", HistGradientBoostingClassifier(
            max_iter=M["hist_gradient_boosting"]["max_iter"], early_stopping=M["hist_gradient_boosting"]["parar"],
            n_iter_no_change=M["hist_gradient_boosting"]["paciencia"], tol=M["hist_gradient_boosting"]["tol"],
            min_samples_leaf=2, random_state=SEMILLA)),
        ("adaboost", AdaBoostClassifier(n_estimators=M["adaboost"]["epocas"], random_state=SEMILLA)),
        ("logistic", escalado(LogisticRegression(max_iter=M["logistic"]["max_iter"], tol=M["logistic"]["tol"]))),
        ("sgd_logistico", escalado(SGDClassifier(loss="log_loss", max_iter=M["sgd_logistico"]["max_iter"],
                                                 early_stopping=M["sgd_logistico"]["parar"],
                                                 n_iter_no_change=M["sgd_logistico"]["paciencia"],
                                                 tol=M["sgd_logistico"]["tol"], random_state=SEMILLA))),
        ("ridge", escalado(RidgeClassifier())),
        ("lda", escalado(LinearDiscriminantAnalysis(solver="lsqr", shrinkage="auto"))),
        ("svm", escalado(SVC(probability=True, random_state=SEMILLA))),
        ("knn", escalado(KNeighborsClassifier(n_neighbors=3))),
        ("decision_tree", DecisionTreeClassifier(random_state=SEMILLA)),
        ("mlp", escalado(MLPClassifier(hidden_layer_sizes=(32,), max_iter=M["mlp"]["max_iter"],
                                                early_stopping=M["mlp"]["parar"], n_iter_no_change=M["mlp"]["paciencia"],
                                                tol=M["mlp"]["tol"], random_state=SEMILLA))),
        ("naive_bayes", GaussianNB()),
    ]
    try:
        from lightgbm import LGBMClassifier
        out.append(("lightgbm", LGBMClassifier(n_estimators=M["lightgbm"]["epocas"], num_leaves=15, min_child_samples=1,
                                                 verbose=-1, random_state=SEMILLA)))
    except ImportError:
        pass
    try:
        from catboost import CatBoostClassifier
        out.append(("catboost", CatBoostClassifier(iterations=M["catboost"]["epocas"], depth=4, verbose=0, random_seed=SEMILLA, allow_writing_files=False)))
    except ImportError:
        pass
    try:
        from xgboost import XGBClassifier
        out.append(("xgboost", XGBClassifier(n_estimators=M["xgboost"]["epocas"], max_depth=4, eval_metric="logloss", random_state=SEMILLA)))
    except ImportError:
        pass
    return out


def modelos_disponibles():
    try:
        return [n for n, _ in catalogo()]
    except ImportError:
        return []


def tope(nombre):
    """El tope de iteraciones configurado para este modelo (epocas o max_iter), o None si no itera."""
    f = matriz_modelos().get(nombre)
    return (f["epocas"] or f["max_iter"]) if f else None


def iteraciones_usadas(est):
    """Cuantas iteraciones hizo de verdad un modelo YA ajustado (puede frenar antes del tope por convergencia
    o early stopping). None si el modelo no itera o la libreria no lo expone."""
    est = est[-1] if hasattr(est, "steps") else est   # Pipeline: el estimador final
    for attr in ("n_iter_", "n_estimators_"):
        v = getattr(est, attr, None)
        if v is not None:
            try:
                return int(max(v)) if hasattr(v, "__len__") else int(v)   # logistic: array por clase
            except (TypeError, ValueError):
                pass
    for attr in ("estimators_", "tree_count_"):       # bosques / adaboost / catboost
        v = getattr(est, attr, None)
        if v is not None:
            return int(v if isinstance(v, int) else len(v))
    if hasattr(est, "get_booster"):                   # xgboost
        return int(est.get_booster().num_boosted_rounds())
    if hasattr(est, "best_iteration_") and est.best_iteration_:   # lightgbm
        return int(est.best_iteration_)
    return None
