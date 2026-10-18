"""Comparar corridas de entrenamiento: mejoro / empeoro / igual y que parametros cambiaron."""


from src.entrenamiento import reportes as R


def _run(n, f1, acc=0.9, frames=30, features="ambos", clips=None, tipo=1):
    return {"numero": n, "tipo": tipo, "f1_macro": f1, "accuracy": acc, "features": features,
            "config": {"n_frames_fijo": frames, "modo": "rectangulo"}, "test_pct": 20,
            "clases": ["bien", "mal"], "conteo_clases": clips or {"bien": 10, "mal": 10}}


def test_veredicto_y_cambios():
    a, b = _run(1, 0.80), _run(2, 0.86, frames=45, clips={"bien": 12, "mal": 10})
    v = R.comparar(b, a)
    assert v["veredicto"] == "mejoro" and v["delta_f1"] == 0.06 and v["contra"] == 1
    assert "frames 30→45" in v["cambios"] and any(c.startswith("clips 12/10") for c in v["cambios"])
    assert R.comparar(_run(3, 0.70), a)["veredicto"] == "empeoro"
    assert R.comparar(_run(3, 0.805), a)["veredicto"] == "igual"   # menos de 1 punto: ruido
    assert R.comparar(a, None) is None


def test_el_umbral_sube_cuando_los_folds_son_ruidosos():
    a, b = _run(1, 0.80), _run(2, 0.86)
    assert R.comparar(b, a)["veredicto"] == "mejoro"              # sin folds: piso de 1 punto
    a.update(f1_std=0.20, k=4), b.update(f1_std=0.20, k=4)         # error estandar combinado ~0.14
    v = R.comparar(b, a)
    assert v["veredicto"] == "igual" and v["ruido"] > 0.12 and v["delta_f1"] == 0.06


def test_corrida_vieja_sin_kpoints_ni_angulos_no_inventa_cambios():
    assert R.comparar(_run(2, 0.9), _run(1, 0.8))["cambios"] == []
