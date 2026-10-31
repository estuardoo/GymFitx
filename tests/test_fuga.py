"""Validacion por grabacion: ningun video (ni sus copias _2/_3 ni sus ventanas 'fuera') queda en entrenar y en probar a la vez."""
import numpy as np
from sklearn.dummy import DummyClassifier

from src.entrenamiento import datos as DATOS
from src.entrenamiento import validacion as VALID


def _tabla(n_videos=10, ciclos=4):
    """Una tabla con `n_videos` videos (los 4 primeros bien, el resto mal), cada uno con `ciclos` clips y sus copias."""
    from src.nucleo import inputs as INP
    claves = []
    with INP.editar() as t:
        for v in range(n_videos):
            raw = INP.registrar_raw(t, "z", persona=f"P{v % 2 + 1}")
            for i in range(ciclos):
                for copia in (False, True):
                    c = INP.registrar_clip(t, "z", etiqueta=1 if v < 4 else 0, t_ini_ms=i * 1000, t_fin_ms=i * 1000 + 900,
                                           raw_id=raw["id"], seg=i, copia=copia)
                    claves.append(INP.clave(c))
    return claves


def test_grupo_de():
    from src.nucleo import inputs as INP
    claves = _tabla(2, 2)
    assert len({DATOS.grupo_de(c) for c in claves}) == 2           # un grupo por video, con ciclos y copias dentro
    assert DATOS.grupo_de(claves[0]) == DATOS.grupo_de(claves[3]) != DATOS.grupo_de(claves[4])
    raw0 = INP.tabla()["raw"][0]
    assert DATOS.grupo_de(f"fuera/{INP.vid_de(raw0)}@3.5") == DATOS.grupo_de(claves[0])   # ventana 'fuera' = su video


def _datos():
    clips = _tabla()
    y = np.array([0 if i < 32 else 1 for i in range(len(clips))])
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
    ruta = Path(__file__).resolve().parent.parent / "scripts" / "hpc" / "busqueda_features_slurm.py"
    spec = importlib.util.spec_from_file_location("slurm_busqueda", ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    clips, y, X = _datos()
    g = [DATOS.grupo_de(c) for c in clips]   # el exportador los guarda en el npz ("grupos"); el script ya no los deduce del nombre
    assert mod.elegir_k(np.array(y), 20, g) == 4
    from sklearn.model_selection import StratifiedGroupKFold, cross_val_predict
    pred = cross_val_predict(DummyClassifier(strategy="most_frequent"), X, y, cv=StratifiedGroupKFold(4, shuffle=True, random_state=42), groups=np.array(g))
    assert len(pred) == len(y)
