"""Tests de la capa de persistencia. Base temporal, no toca la real."""

import sys
import tempfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.storage import Storage   # noqa: E402
from core.types import Score       # noqa: E402


def _score(total: float) -> Score:
    return Score(total=total, error_z=0.1,
                 per_feature=np.array([1.0, 2.0], np.float32),
                 feature_names=["a", "b"], duration_ms=1500)


def _store() -> tuple[Storage, tempfile.TemporaryDirectory]:
    d = tempfile.TemporaryDirectory()
    return Storage(Path(d.name) / "t.db"), d


def test_registra_y_agrega():
    st, d = _store()
    for v in (80.0, 90.0, 100.0):
        st.log_rep("mano_apertura", _score(v))
    hoy = st.today()
    assert len(hoy) == 1
    assert hoy[0]["reps"] == 3
    assert abs(hoy[0]["avg_score"] - 90.0) < 0.05
    assert hoy[0]["best"] == 100.0
    st.close(); d.cleanup()


def test_rutina_se_reemplaza_completa():
    st, d = _store()
    st.set_routine([{"exercise": "a", "target_reps": 5}, {"exercise": "b", "target_reps": 8}])
    st.set_routine([{"exercise": "b", "target_reps": 12}])
    r = st.routine()
    assert len(r) == 1 and r[0]["exercise"] == "b" and r[0]["target_reps"] == 12
    st.close(); d.cleanup()


def test_racha_y_recientes():
    st, d = _store()
    assert st.streak() == 0
    st.log_rep("x", _score(70.0))
    assert st.streak() == 1
    assert st.recent(5)[0]["exercise"] == "x"
    assert len(st.daily(14)) == 1
    st.close(); d.cleanup()


if __name__ == "__main__":
    fallos = 0
    for nombre, fn in sorted(globals().items()):
        if nombre.startswith("test_") and callable(fn):
            try:
                fn(); print(f"  OK    {nombre}")
            except Exception as e:
                fallos += 1; print(f"  FALLA {nombre}: {e}")
    print("\nTodo bien." if not fallos else f"\n{fallos} test(s) fallaron.")
    raise SystemExit(1 if fallos else 0)
