"""Validacion por grabacion: ningun video (ni sus copias _2/_3 ni sus ventanas 'fuera') queda en entrenar y en probar a la vez."""
import numpy as np
from sklearn.dummy import DummyClassifier

from src.entrenamiento import datos as DATOS
from src.entrenamiento import validacion as VALID


def test_grupo_de():
    assert DATOS.grupo_de("zancada/bien/100747b_zancada_frontal_bien_s01_bien.mp4") == "100747b_zancada_frontal_bien"
    assert DATOS.grupo_de("zancada/bien/100747b_zancada_frontal_bien_s01_bien_2.mp4") == "100747b_zancada_frontal_bien"
    assert DATOS.grupo_de("cuerpo_completo/base/cuerpo_completo__2026-08-25__205448_base_s02_base_r0.mp4") == \
        "cuerpo_completo__2026-08-25__205448_base"
    assert DATOS.grupo_de("fuera/cuerpo_completo/2026-08-25/205448_base.mp4@3.5") == "cuerpo_completo__2026-08-25__205448_base"


def _datos():
    clips = [f"z/{c}/v{v}_s{i:02d}_{c}{sufijo}.mp4" for c, vs in (("bien", range(4)), ("mal", range(4, 10)))
             for v in vs for i in range(4) for sufijo in ("", "_2")]
    y = np.array([0 if "/bien/" in c else 1 for c in clips])
    return clips, y, np.random.default_rng(0).normal(size=(len(clips), 5))


def test_por_grabacion_no_parte_un_video_y_k_respeta_las_grabaciones():
    clips, y, X = _datos()
    g = [DATOS.grupo_de(c) for c in clips]
    assert VALID.grupos_por_clase(y, g) == 4
    assert VALID.elegir_k(20, {0: 32, 1: 48}, [0, 1], len(y), 4) == 4
    skf = VALID.PorGrabacion(4, g, 42)
    for tr, te in skf.split(X, y):
        assert not {g[i] for i in tr} & {g[i] for i in te}
    r = VALID.evaluar("base", DummyClassifier(strategy="most_frequent"), X, y, skf)
    assert "accuracy" in r
    an = VALID.cv_anidada([("d", DummyClassifier(strategy="most_frequent"))], X, y, skf)
    assert an is not None and an["elegidos"] == {"d": 4}


def test_script_slurm_agrupa_igual_que_el_panel():
    import importlib.util
    from pathlib import Path
    ruta = Path(__file__).resolve().parent.parent / "scripts" / "busqueda_features_slurm.py"
    spec = importlib.util.spec_from_file_location("slurm_busqueda", ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    clips, y, X = _datos()
    assert all(mod.grupo_de(c) == DATOS.grupo_de(c) for c in clips)
    g = [mod.grupo_de(c) for c in clips]
    assert mod.elegir_k(np.array(y), 20, g) == 4
    from sklearn.model_selection import StratifiedGroupKFold, cross_val_predict
    pred = cross_val_predict(DummyClassifier(strategy="most_frequent"), X, y, cv=StratifiedGroupKFold(4, shuffle=True, random_state=42), groups=np.array(g))
    assert len(pred) == len(y)
