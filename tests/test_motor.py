"""Tests del motor completo, sin camara y sin mediapipe.
"""

from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent

from synth import a_framevecs, rep_sintetica, toma  # noqa: E402

from src.evaluacion.comparadores.dtw import compare, cost_matrix, dtw_band  # noqa: E402
from src.evaluacion.plantilla import Template, build_template  # noqa: E402
from src.evaluacion.segmentador import RepSegmenter  # noqa: E402
from src.nucleo.ejercicio import load_all, load_exercise  # noqa: E402
from src.nucleo.landmarks import POSE_LANDMARKS, resolve  # noqa: E402
from src.nucleo.tipos import Segment  # noqa: E402
from src.procesamiento.medidas.features import FeatureExtractor, angle_deg, compute_features  # noqa: E402
from src.procesamiento.medidas.filtros import OneEuroFilter  # noqa: E402

EJ = load_exercise(ROOT / "tests" / "data" / "sintetico.yaml")
EXT = FeatureExtractor(EJ)


# ---------------------------------------------------------------- geometria
def test_angulo_recto():
    assert abs(angle_deg(np.array([1., 0, 0]), np.zeros(3), np.array([0., 1, 0])) - 90) < 1e-4


def test_angulo_invariante_a_escala_y_traslacion():
    a, b, c = np.array([1., 0, 0]), np.zeros(3), np.array([0., 2, 0])
    off = np.array([5., -3, 12])
    assert abs(angle_deg(a, b, c) - angle_deg(a*7+off, b*7+off, c*7+off)) < 1e-3


def test_landmarks_de_pose():
    assert len(POSE_LANDMARKS) == 33
    assert resolve("RIGHT_ELBOW", "pose") == 14


def test_extractor_compilado_igual_al_escalar():
    """La version vectorizada no puede diferir de la matematica de referencia."""
    rng = np.random.default_rng(3)
    P = rng.normal(scale=0.05, size=(33, 3)).astype(np.float32)
    rapido = EXT.from_points(P)
    lento = compute_features(P, EJ.features, EJ.source)
    for i, nombre in enumerate(EXT.names):
        assert abs(rapido[i] - lento[nombre]) < 1e-3, nombre


def test_todos_los_ejercicios_cargan():
    todos = load_all(ROOT / "ejercicios")
    assert "cuerpo_completo" in todos and "manguito_rotador" in todos
    for ex in todos.values():
        FeatureExtractor(ex)          # compila sin error = nombres validos


# ---------------------------------------------------------------- filtro
def test_one_euro_baja_el_ruido_sin_meter_retardo():
    """Debe mejorar el error contra la señal limpia, no solo suavizar la curva.

    Un filtro con retardo 'se ve' mas suave pero se aleja de la verdad; por eso
    la prueba mide error contra la señal limpia y no varianza.
    """
    limpio = np.vstack([rep_sintetica(n_frames=120) for _ in range(3)])   # ritmo de rehab: 4 s/rep
    rng = np.random.default_rng(1)
    escala = np.array([1, 1, 1, 1, 1, 2.0 / 180.0])
    ruidoso = limpio + rng.normal(scale=2.0, size=limpio.shape) * escala

    f = OneEuroFilter(6, ["deg"] * 5 + ["ratio"])
    salida = np.array([f.update(fila.astype(np.float32), int(i * 33))
                       for i, fila in enumerate(ruidoso)])

    antes = np.abs(ruidoso - limpio).mean(axis=0)
    despues = np.abs(salida - limpio).mean(axis=0)
    assert (despues < antes).all(), f"antes={antes.round(3)} despues={despues.round(3)}"


def test_one_euro_trata_igual_grados_y_razones():
    """La correccion por unidades: la razon no puede quedar peor tratada que el angulo."""
    limpio = np.vstack([rep_sintetica(n_frames=120) for _ in range(3)])
    rng = np.random.default_rng(4)
    escala = np.array([1, 1, 1, 1, 1, 2.0 / 180.0])
    ruidoso = limpio + rng.normal(scale=2.0, size=limpio.shape) * escala
    f = OneEuroFilter(6, ["deg"] * 5 + ["ratio"])
    salida = np.array([f.update(fila.astype(np.float32), int(i * 33))
                       for i, fila in enumerate(ruidoso)])
    mejora = (np.abs(ruidoso - limpio).mean(axis=0) / np.abs(salida - limpio).mean(axis=0))
    assert mejora.min() > 1.05
    assert mejora.max() / mejora.min() < 1.6, f"trato desparejo entre unidades: {mejora.round(2)}"


# ---------------------------------------------------------------- segmentador
def test_segmentador_cuenta_las_repeticiones():
    frames = toma(n_reps=6)
    señal = np.array([EXT.signal(f.values) for f in frames])
    low, high = np.percentile(señal, [20, 80])
    seg = RepSegmenter(6, EXT.signal_idx, "mean", float(low), float(high),
                       "down_up", 600, 8000, capacity=400)
    reps = [s for f in frames if (s := seg.update(f)) is not None]
    assert 4 <= len(reps) <= 6, f"detecto {len(reps)} reps"


def test_segmentador_ignora_el_reposo():
    """Quieto en la posicion alta: cero repeticiones, ni una falsa."""
    quieto = np.tile(rep_sintetica(n_frames=1)[0], (200, 1))
    quieto += np.random.default_rng(2).normal(scale=0.4, size=quieto.shape)
    seg = RepSegmenter(6, EXT.signal_idx, "mean", 100.0, 160.0, "down_up", 600, 8000)
    assert sum(seg.update(f) is not None for f in a_framevecs(quieto)) == 0


def test_histeresis_evita_rebotes():
    """Oscilar justo debajo del umbral alto no debe contar repeticiones."""
    t = np.linspace(0, 20 * np.pi, 400)
    datos = np.tile(rep_sintetica(n_frames=1)[0], (400, 1))
    datos[:, 1:5] = (150 + 4 * np.sin(t))[:, None]
    seg = RepSegmenter(6, EXT.signal_idx, "mean", 90.0, 160.0, "down_up", 600, 8000)
    assert sum(seg.update(f) is not None for f in a_framevecs(datos)) == 0


# ---------------------------------------------------------------- DTW
def test_dtw_alinea_velocidades_distintas():
    lento = rep_sintetica(n_frames=90)
    rapido = rep_sintetica(n_frames=30)
    mismo, _ = dtw_band(cost_matrix(lento, lento))
    distinto, _ = dtw_band(cost_matrix(lento, rapido))
    assert mismo < 1e-6
    assert distinto < 3.0, f"el DTW no absorbio el cambio de velocidad: {distinto}"


def test_dtw_penaliza_forma_distinta():
    base = rep_sintetica(n_frames=45)
    torcido = rep_sintetica(n_frames=45, sesgo_menique=45.0)
    igual, _ = dtw_band(cost_matrix(base, base))
    peor, _ = dtw_band(cost_matrix(base, torcido))
    assert peor > igual + 5.0


# ---------------------------------------------------------------- plantilla
def _plantilla():
    return build_template(toma(n_reps=6, ruido=1.2), EJ, EXT)


def test_plantilla_se_autocalibra():
    t = _plantilla()
    assert t.n_reps >= 4
    assert t.high > t.low
    assert t.tau > 0
    assert t.data.shape[1] == 6
    assert np.all(t.sigma > 0)


def test_repeticion_tipica_puntua_cerca_de_90():
    """La calibracion de tau se define para que esto sea cierto."""
    t = _plantilla()
    d = rep_sintetica(n_frames=45, ruido=1.2, semilla=99)
    s = compare(Segment(0, 1500, d, ~np.isnan(d)), t)
    assert 70 <= s.total <= 100, f"puntaje fuera de rango: {s.total:.1f}"


def test_movimiento_incompleto_puntua_menos():
    t = _plantilla()
    buena = rep_sintetica(n_frames=45, ruido=1.2, semilla=7)
    corta = rep_sintetica(n_frames=45, amplitud=40.0, ruido=1.2, semilla=7)  # no cierra la mano
    s_buena = compare(Segment(0, 1500, buena, ~np.isnan(buena)), t).total
    s_corta = compare(Segment(0, 1500, corta, ~np.isnan(corta)), t).total
    assert s_buena > s_corta + 10, f"buena={s_buena:.1f} corta={s_corta:.1f}"


def test_score_señala_la_feature_culpable():
    t = _plantilla()
    d = rep_sintetica(n_frames=45, ruido=0.5, sesgo_menique=45.0, semilla=5)
    s = compare(Segment(0, 1500, d, ~np.isnan(d)), t)
    assert s.worst(1)[0][0] == "curl_menique", s.worst(3)


def test_velocidad_distinta_no_castiga():
    """Hacerlo mas lento no es hacerlo mal: el puntaje debe aguantar."""
    t = _plantilla()
    normal = rep_sintetica(n_frames=45, ruido=1.0, semilla=11)
    lenta = rep_sintetica(n_frames=90, ruido=1.0, semilla=11)
    s_n = compare(Segment(0, 1500, normal, ~np.isnan(normal)), t).total
    s_l = compare(Segment(0, 3000, lenta, ~np.isnan(lenta)), t).total
    assert abs(s_n - s_l) < 20, f"normal={s_n:.1f} lenta={s_l:.1f}"


def test_plantilla_ida_y_vuelta_a_disco(tmp=None):
    import tempfile
    t = _plantilla()
    with tempfile.TemporaryDirectory() as d:
        p = t.save(Path(d) / "x.npz")
        t2 = Template.load(p)
    assert t2.exercise == t.exercise and t2.names == t.names
    assert np.allclose(t2.data, t.data) and abs(t2.tau - t.tau) < 1e-9


def test_toma_sin_repeticiones_falla_con_mensaje_util():
    quieto = np.tile(rep_sintetica(n_frames=1)[0], (120, 1))
    try:
        build_template(a_framevecs(quieto), EJ, EXT)
    except ValueError as e:
        assert "señal" in str(e).lower() or "repeticiones" in str(e).lower()
    else:
        raise AssertionError("deberia haber fallado")

