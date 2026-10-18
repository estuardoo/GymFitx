"""Etapa 6c: lo que queda de cada corrida en datos/entrenamientos/run_N/ (graficas, meta.json) y su listado."""

from __future__ import annotations

import json

from src.nucleo.config import ENTRENAMIENTOS_DIR

ENTR = ENTRENAMIENTOS_DIR


def _plt():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    return plt


def nueva_corrida():
    """(numero, carpeta) de la proxima datos/entrenamientos/run_N/."""
    ENTR.mkdir(exist_ok=True)
    numero = 1 + max([int(p.name[4:]) for p in ENTR.glob("run_*") if p.name[4:].isdigit()], default=0)
    out = ENTR / f"run_{numero}"
    out.mkdir(parents=True)
    return numero, out


def grafico_comparacion(out, numero, resultados, linea_base, mejor):
    """Dispersion F1 macro (Y) vs Accuracy (X) de todos los modelos, con su nombre al lado -- arriba a la
    derecha es mejor. Los que fallaron (sin 'accuracy') se listan aparte, no se pueden ubicar en el plano."""
    plt = _plt()
    todos = resultados + [linea_base]
    validos = [r for r in todos if "accuracy" in r]
    errores = [r["nombre"] for r in todos if "accuracy" not in r]
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    ax.plot([0, 1], [0, 1], ls=":", lw=1, color="#c7ccd6", zorder=1)   # referencia: F1 == accuracy
    for r in validos:
        es_mejor = r["nombre"] == mejor["nombre"]
        es_base = r["nombre"] == "linea_base"
        color = "#2f6feb" if es_mejor else ("#b0b6c0" if es_base else "#5a6273")
        ax.scatter(r["accuracy"], r["f1_macro"], s=95 if es_mejor else 55, color=color,
                  zorder=3, edgecolors="white", linewidths=0.6)
        ax.annotate(r["nombre"], (r["accuracy"], r["f1_macro"]), textcoords="offset points",
                   xytext=(6, 4), fontsize=8, color="#333", fontweight="bold" if es_mejor else "normal")
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    ax.set_xlabel("Accuracy")
    ax.set_ylabel("F1 macro")
    titulo = f"Comparacion de modelos #{numero}"
    ax.set_title(titulo + (f"  ({len(errores)} sin entrenar)" if errores else ""))
    fig.tight_layout()
    fig.savefig(out / "comparacion.png", dpi=110)
    plt.close(fig)


def grafico_confusion(out, numero, y, y_pred, clases, nombre):
    from sklearn.metrics import confusion_matrix
    plt = _plt()
    cm = confusion_matrix(y, y_pred, labels=range(len(clases)))
    fig, ax = plt.subplots(figsize=(4.5, 4))
    ax.imshow(cm, cmap="Blues")
    ax.set_xticks(range(len(clases)))
    ax.set_xticklabels(clases, rotation=45, ha="right")
    ax.set_yticks(range(len(clases)))
    ax.set_yticklabels(clases)
    ax.set_xlabel("Prediccion")
    ax.set_ylabel("Real")
    ax.set_title(f"Matriz de confusion #{numero} ({nombre})")
    for i in range(len(clases)):
        for j in range(len(clases)):
            ax.text(j, i, cm[i, j], ha="center", va="center", color="white" if cm[i, j] > cm.max() / 2 else "black")
    fig.tight_layout()
    fig.savefig(out / "confusion.png", dpi=110)
    plt.close(fig)


def grafico_roc(out, numero, y, y_proba, clases, nombre):
    import numpy as np
    from sklearn.metrics import auc, roc_curve
    from sklearn.preprocessing import label_binarize
    plt = _plt()
    fig, ax = plt.subplots(figsize=(5, 4.5))
    if y_proba is not None:
        y_bin = label_binarize(y, classes=range(len(clases)))
        if len(clases) == 2:
            y_bin = np.hstack([1 - y_bin, y_bin])
        for i, cl in enumerate(clases):
            fpr, tpr, _ = roc_curve(y_bin[:, i], y_proba[:, i])
            ax.plot(fpr, tpr, label=f"{cl} (AUC={auc(fpr, tpr):.2f})")
        ax.legend(fontsize=8)
    ax.plot([0, 1], [0, 1], "--", color="#999")
    ax.set_xlabel("FPR")
    ax.set_ylabel("TPR")
    ax.set_title(f"ROC #{numero} ({nombre})")
    fig.tight_layout()
    fig.savefig(out / "roc.png", dpi=110)
    plt.close(fig)


def matriz_iteraciones(numero, modelos):
    """Tabla de texto para el log: por modelo, F1 y cuantas iteraciones uso contra su tope ('frenó' = paró antes)."""
    filas = [f"entrenar run_{numero}: iteraciones por modelo (media de los folds)",
             f"  {'modelo':<24}{'f1':>7}{'tope':>7}{'min':>7}{'media':>8}{'max':>7}  freno"]
    for m in sorted(modelos, key=lambda m: m.get("f1_macro") or -1, reverse=True):
        it = m.get("iteraciones")
        if m.get("error"):
            filas.append(f"  {m['nombre']:<24}{'error':>7}")
        elif it:
            filas.append(f"  {m['nombre']:<24}{m['f1_macro']:>7.3f}{it['tope']:>7}{it['min']:>7}{it['media']:>8}{it['max']:>7}  "
                         f"{'si' if it['freno'] else 'no (llego al tope)'}")
        else:
            filas.append(f"  {m['nombre']:<24}{m['f1_macro']:>7.3f}{'-':>7}{'-':>7}{'-':>8}{'-':>7}  (no itera)")
    return "\n".join(filas)


def guardar_meta(out, meta):
    (out / "meta.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False), "utf-8")


UMBRAL_IGUAL = 0.01  # piso: menos de 1 punto de F1 macro siempre es "igual"; con folds ruidosos el umbral sube (ver _ruido)


def parametros(m):
    """Lo que definio una corrida (para comparar). None = la corrida vieja no lo guardo."""
    conteo = m.get("conteo_clases") or {c: int(r["support"]) for c, r in (m.get("reporte") or {}).items()
                                        if isinstance(r, dict) and c in (m.get("clases") or [])}
    return {"frames": (m.get("config") or {}).get("n_frames_fijo"), "features": m.get("features"),
            "kpoints": m.get("kpoints_usados"), "angulos": m.get("angulos"),
            "modo": (m.get("config") or {}).get("modo"), "test_pct": m.get("test_pct"), "clips": conteo or None,
            "matriz": m.get("matriz_modelos")}


def _cambios(a, b):
    """Que parametros difieren entre la corrida anterior (a) y esta (b), en texto."""
    out = []
    for k, etiqueta in (("frames", "frames"), ("features", "features"), ("modo", "normalizacion"),
                        ("test_pct", "test %")):
        if a[k] is not None and b[k] is not None and a[k] != b[k]:
            out.append(f"{etiqueta} {a[k]}→{b[k]}")
    for k, etiqueta in (("kpoints", "kpoints"), ("angulos", "angulos")):
        if a[k] is not None and b[k] is not None and len(a[k]) != len(b[k]):
            out.append(f"{etiqueta} {len(a[k])}→{len(b[k])}")
        elif a[k] is not None and b[k] is not None and a[k] != b[k]:
            out.append(f"{etiqueta} distintos")
    if a.get("matriz") and b.get("matriz"):   # solo los modelos que estuvieron en las dos corridas
        for n in sorted(set(a["matriz"]) & set(b["matriz"])):
            for k in ("epocas", "max_iter", "parar", "paciencia", "tol"):
                if a["matriz"][n].get(k) != b["matriz"][n].get(k):
                    out.append(f"{n}.{k} {a['matriz'][n].get(k)}→{b['matriz'][n].get(k)}")
    if a["clips"] and b["clips"] and a["clips"] != b["clips"]:
        out.append("clips " + "/".join(str(b["clips"].get(c, 0)) for c in sorted(b["clips"])) + " (antes "
                   + "/".join(str(a["clips"].get(c, 0)) for c in sorted(b["clips"])) + ")")
    return out


def _ruido(m, previa):
    """Cuanto puede moverse el F1 solo por azar entre dos corridas: error estandar de cada una
    (desviacion entre folds / raiz(k)) combinados. Sin datos de folds (corrida vieja) = solo el piso."""
    se = [(r["f1_std"] / r["k"] ** 0.5) ** 2 for r in (m, previa) if r.get("f1_std") is not None and r.get("k")]
    return max(UMBRAL_IGUAL, round(sum(se) ** 0.5, 4)) if len(se) == 2 else UMBRAL_IGUAL


def comparar(m, previa):
    """Veredicto de la corrida m contra la anterior del mismo ejercicio: mejoro / empeoro / igual."""
    if not previa or m.get("f1_macro") is None or previa.get("f1_macro") is None:
        return None
    d = round(m["f1_macro"] - previa["f1_macro"], 4)
    anid = (m.get("anidado") or {}).get("f1_macro"), (previa.get("anidado") or {}).get("f1_macro")
    ruido = _ruido(m, previa)
    return {"contra": previa["numero"], "delta_f1": d, "ruido": ruido, "delta_accuracy": round(m["accuracy"] - previa["accuracy"], 4),
            "delta_anidado": round(anid[0] - anid[1], 4) if None not in anid else None,
            "veredicto": "igual" if abs(d) < ruido else ("mejoro" if d > 0 else "empeoro"),
            "cambios": _cambios(parametros(previa), parametros(m))}


def entrenamientos():
    """Todas las corridas, cada una con 'parametros' y 'vs_anterior' (contra la corrida
    anterior del mismo ejercicio; se calcula al leer, asi tambien sirve para corridas viejas)."""
    if not ENTR.exists():
        return []
    out, ultima = [], {}
    for p in sorted(ENTR.glob("run_*"), key=lambda p: int(p.name[4:]) if p.name[4:].isdigit() else 0):
        mp = p / "meta.json"
        if mp.exists():
            m = json.loads(mp.read_text("utf-8"))
            m["parametros"] = parametros(m)
            m["vs_anterior"] = comparar(m, ultima.get(m.get("tipo")))
            ultima[m.get("tipo")] = m
            out.append(m)
    return out
