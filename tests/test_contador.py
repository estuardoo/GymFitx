"""Vista previa con modelo: el Contador cuenta/clasifica cada rep sin guardar y no cuenta como 'grabando'."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from test_scorers import _plantilla, _segmento_identico  # noqa: E402

from src.nucleo.tipos import Score  # noqa: E402
from src.sesion.sumideros import Contador, EventBus, Sink  # noqa: E402


class _Clf:
    run, nombre = "run_7", "knn"

    def __init__(self, clases):
        self.clases = iter(clases)

    def puntuar(self, seg, tpl):
        return Score(total=90.0, error_z=float("nan"), per_feature=[], feature_names=[],
                     duration_ms=seg.duration_ms, clase=next(self.clases))


class _Pipe:
    def __init__(self):
        self.bus, self.last_score = EventBus(), 0.0
        self.eventos = []
        self.bus.subscribe(self.eventos.append)

        class _Ex:
            slug = "test"
        self.exercise = _Ex()


def test_contador_clasifica_cada_rep_y_no_es_grabando():
    t = _plantilla()
    c = Contador(t, _Clf(["bien", "mal"]))
    pipe = _Pipe()
    for _ in range(2):
        c.on_rep(pipe, _segmento_identico(t))
    reps = [e for e in pipe.eventos if e["type"] == "rep"]
    assert [e["n"] for e in reps] == [1, 2]
    assert [e["clasificador"]["clase"] for e in reps] == ["bien", "mal"]
    assert reps[0]["clasificador"]["run"] == "run_7" and reps[0]["modelo"] == "clasificador"
    assert c.es_contador and not Sink.es_contador


def test_pipeline_con_contador_no_esta_grabando():
    from test_gesto import _pipeline
    p = _pipeline()
    p.swap_sink(Contador(_plantilla(), _Clf([])))
    assert p.grabando is False


# ---- conteo solo con el modelo: clase "fuera" + ventana deslizante ----
import numpy as np  # noqa: E402

from src.procesamiento.puntos import vectorizar  # noqa: E402
from src.sesion.sumideros import ContadorModelo  # noqa: E402


class _ClfVentana:
    """Modelo de juguete: ve 'ciclo' si la ventana trae movimiento (media del vector alta)."""
    run, nombre, clases = "run_9", "toy", ["bien", "fuera", "mal"]
    spec = {"ventana_ms": 1000, "n_features": 1}
    point_names = ["a"]

    class modelo:   # noqa: N801
        @staticmethod
        def predict_proba(X):
            p_ciclo = float(np.clip(X[0, 0], 0, 1))
            return np.array([[0.9 * p_ciclo, 1 - p_ciclo, 0.1 * p_ciclo]])


def test_detector_cuenta_un_ciclo_por_cada_subida_y_bajada(monkeypatch):
    monkeypatch.setattr(vectorizar, "vector_de_clip",
                        lambda pts, names, spec: np.array([np.mean(pts)], np.float32))
    c = ContadorModelo(_ClfVentana())
    pipe = _Pipe()

    class _Fv:
        def __init__(self, t, v):
            self.t_ms, self.kpoints = t, np.full((2, 3), v, np.float32)

    # 2 ciclos de 1 s separados por 1.5 s de reposo, a 30 ms por cuadro
    for t in range(0, 8000, 30):
        activo = (1000 <= t < 2000) or (3500 <= t < 4500)
        c.on_frame(pipe, None, _Fv(t, 1.0 if activo else 0.0))
    reps = [e for e in pipe.eventos if e["type"] == "rep"]
    assert len(reps) == 2 and all(e["clasificador"]["clase"] == "bien" for e in reps)


def test_ventanas_fuera_solo_toma_tramos_sin_corte(monkeypatch):
    from src.nucleo import inputs as INP
    from src.preparacion import tabla as D
    t = np.arange(0, 20000, 100)   # 20 s a 10 fps
    with INP.editar() as tab:
        raw = INP.registrar_raw(tab, "ej", segmentos=[{"ini": 2, "fin": 4, "clase": "bien"}, {"ini": 6, "fin": 8, "clase": "mal"}])
    np.savez(INP.ruta_raw(raw["ej"], raw["id"], "npz"), points=np.ones((len(t), 2, 3), np.float32), point_names=np.array(["a", "b"]),
             points_t_ms=t, t_ms=t, values=np.zeros((len(t), 1)), names=np.array(["x"]), units=np.array(["deg"]))
    monkeypatch.setattr(vectorizar, "vector_de_clip", lambda pts, names, spec: np.ones(3, np.float32))
    vecs, nombres, ventana = D.ventanas_fuera("ej", {"n_features": 3}, tope=100)
    assert ventana == 2000 and len(vecs) == len(nombres) > 5
    for n in nombres:   # ninguna ventana se parece (IoU>=0.3) a un corte
        ini = float(n.split("@")[1])
        assert all(D._iou(ini, ini + 2, i, f) < 0.3 for i, f in [(2, 4), (6, 8)])
    assert len(D.ventanas_fuera("ej", {"n_features": 3}, tope=3)[0]) == 3


def test_n_conteo_una_sola_cifra():
    """El video, el contador del panel y el evento de estado leen la misma cifra: la del sumidero."""
    from src.sesion.sumideros import Evaluator, Sink
    assert Sink().n is None
    ev = Evaluator.__new__(Evaluator)
    ev.scores = [50.0, 60.0]
    assert ev.n == 2


def test_ciclo_que_empieza_a_mitad_del_movimiento_no_cuenta(monkeypatch):
    """Al prender la camara en pleno movimiento, el primer tramo no es una rep completa: no debe contar."""
    monkeypatch.setattr(vectorizar, "vector_de_clip",
                        lambda pts, names, spec: np.array([np.mean(pts)], np.float32))
    c = ContadorModelo(_ClfVentana())
    pipe = _Pipe()

    class _Fv:
        def __init__(self, t, v):
            self.t_ms, self.kpoints = t, np.full((2, 3), v, np.float32)

    # movimiento 0-1 s (sin inicio), reposo, luego un ciclo completo 2.5-3.5 s
    for t in range(0, 4500, 30):
        activo = t < 1000 or 2500 <= t < 3500
        c.on_frame(pipe, None, _Fv(t, 1.0 if activo else 0.0))
    reps = [e for e in pipe.eventos if e["type"] == "rep"]
    assert len(reps) == 1
