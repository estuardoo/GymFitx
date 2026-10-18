"""Verifica src/evaluacion/comparadores/: los modelos intercambiables de comparacion.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent

from src.evaluacion import comparadores as scorers  # noqa: E402
from src.evaluacion.plantilla import Template  # noqa: E402


def _plantilla(T=20, F=3) -> Template:
    rng = np.random.default_rng(0)
    data = rng.normal(size=(T, F)).astype(np.float32) * 10 + 90
    return Template(
        exercise="test", names=[f"f{i}" for i in range(F)], units=["deg"] * F,
        data=data, mu=data.mean(axis=0), sigma=data.std(axis=0) + 1.0,
        low=0.2, high=0.8, tau=5.0, n_reps=5,
    )


def _segmento_identico(t: Template):
    from src.nucleo.tipos import Segment
    return Segment(start_ms=0, end_ms=500, data=t.data.copy(), valid=np.ones_like(t.data, dtype=bool))


def test_dtw_biomec_y_angulos_directo_dan_100_contra_si_misma():
    t = _plantilla()
    seg = _segmento_identico(t)
    for clave, m in scorers.MODELOS.items():
        score = m["fn"](seg, t)
        assert score.total > 99.0, f"{clave} deberia dar ~100 contra su propia plantilla"


def test_comparar_todos_corre_todos_los_modelos_y_mide_tiempo():
    t = _plantilla()
    seg = _segmento_identico(t)
    resultados = scorers.comparar_todos(seg, t)
    assert set(resultados) == set(scorers.MODELOS)
    for r in resultados.values():
        assert r["score"].total > 99.0
        assert r["latencia_ms"] >= 0.0


def test_angulos_directo_tolera_duracion_distinta_por_remuestreo():
    t = _plantilla(T=20)
    from src.nucleo.tipos import Segment
    # Misma forma, el doble de cuadros: _resample debe alinear igual a ~100.
    largo = np.repeat(t.data, 2, axis=0)
    seg = Segment(start_ms=0, end_ms=500, data=largo, valid=np.ones_like(largo, dtype=bool))
    score = scorers._angulos_directo(seg, t)
    assert score.total > 95.0


def test_default_model_existe_en_el_registro():
    assert scorers.DEFAULT_MODEL in scorers.MODELOS

