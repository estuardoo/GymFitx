"""Reglas de postura (verde/rojo) y base desde un clip: el conteo sin entrenamiento."""
import numpy as np
import pytest

from src.evaluacion import base_clip as B
from src.evaluacion.segmentador import RepSegmenter
from src.nucleo import reglas as R
from src.nucleo.ejercicio import load_exercise
from src.nucleo.tipos import FeatureVec
from src.procesamiento.medidas.features import FeatureExtractor

REGLA = {"nombre": "Espalda", "a": ["C01"], "b": ["C24", "C25"], "angulo": 90, "tolerancia": 8, "unidad": "pct"}


def _cuerpo(dx):
    s = np.zeros((33, 3))
    s[0] = (0.5 + dx, 0.2, 0)        # nariz
    s[23] = s[24] = (0.5, 0.6, 0)    # caderas
    return s


def test_regla_recta_verde_e_inclinada_roja():
    r = R.validar([REGLA])
    assert R.evaluar(r, _cuerpo(0.0), 100, 100)[0]["ok"]
    assert R.evaluar(r, _cuerpo(0.02), 100, 100)[0]["ok"]       # ~2.9 grados < 7.2
    mal = R.evaluar(r, _cuerpo(0.1), 100, 100)[0]               # ~14 grados
    assert not mal["ok"] and mal["desvio"] > 7.2


def test_regla_invalida():
    with pytest.raises(ValueError):
        R.validar([{**REGLA, "a": ["C99"]}])
    assert R.tolerancia_deg(R.validar([{**REGLA, "unidad": "deg", "tolerancia": 5}])[0]) == 5


def test_base_desde_clip_cuenta_una_vez(tmp_path, monkeypatch):
    ex = load_exercise("zancada_reglas")
    npz = next(iter(B._originales("zancada", "bien")), None)
    if npz is None:
        pytest.skip("sin clips de zancada")
    tpl = B.plantilla_de_clip(ex, npz)
    ext = FeatureExtractor(ex)
    v, t = B._valores(ex, ext, npz), dict(np.load(npz))["t_ms"]
    seg = RepSegmenter(n_features=v.shape[1], signal_idx=ext.signal_idx, reduce=ext.signal_reduce, low=tpl.low,
                       high=tpl.high, direction=ex.direction, min_duration_ms=ex.min_duration_ms,
                       max_duration_ms=ex.max_duration_ms, capacity=len(v) + 2)
    n = sum(seg.update(FeatureVec(values=x, valid=~np.isnan(x), t_ms=int(m), raw=None, label="")) is not None
            for x, m in zip(v, t))
    assert n == 1


def test_clip_con_pocos_puntos(tmp_path):
    """Los clips viejos guardan solo sus kpoints (12, 23...): se miden igual por nombre."""
    ex = load_exercise("zancada_reglas")
    ext = FeatureExtractor(ex)
    nombres = ["LEFT_SHOULDER", "RIGHT_SHOULDER", "LEFT_ELBOW", "RIGHT_ELBOW", "LEFT_WRIST", "RIGHT_WRIST", "LEFT_HIP",
               "RIGHT_HIP", "LEFT_KNEE", "RIGHT_KNEE", "LEFT_ANKLE", "RIGHT_ANKLE"]
    pts = np.random.default_rng(0).normal(size=(5, 12, 3)).astype(np.float32)
    np.savez(tmp_path / "c.npz", points=pts, point_names=np.array(nombres), t_ms=np.arange(5) * 33)
    v = B._valores(ex, ext, tmp_path / "c.npz")
    assert v.shape == (5, ext.size) and np.isfinite(v[:, ext.names.index("rodilla_izq")]).all()


def _lunge(front_left=True):
    """Vista lateral: hombros sobre caderas, pierna delantera (rodilla mas alta) flexionada."""
    s = np.full((33, 3), 0.5)
    s[11] = s[12] = (0.5, 0.2, 0)      # hombros
    s[23] = s[24] = (0.5, 0.5, 0)      # caderas
    fr, tr = (25, 26) if front_left else (26, 25)
    s[fr], s[tr] = (0.7, 0.62, 0), (0.35, 0.8, 0)    # rodillas: delantera mas alta
    s[fr + 2], s[tr + 2] = (0.7, 0.9, 0), (0.2, 0.9, 0)
    return s


def test_reglas_de_zancada():
    ex = load_exercise("zancada_reglas")
    activas = {r["nombre"] for r in ex.reglas if r["activo"]}
    assert activas == {"Espalda recta", "Tronco", "Cadera delantera", "Brazo izq", "Brazo der"}
    angs = []
    for izq in (True, False):   # da igual cual pierna va delante
        res = {r["nombre"]: r for r in R.evaluar(ex.reglas, _lunge(izq), 100, 100)}
        assert res["Tronco"]["ok"] and "pc" in res["Cadera delantera"]
        angs.append(res["Cadera delantera"]["angulo"])
    assert angs[0] == pytest.approx(angs[1])
    # tronco inclinado 45 grados: roja con mensaje
    mal = _lunge()
    mal[11] = mal[12] = (0.8, 0.25, 0)
    r = {x["nombre"]: x for x in R.evaluar(ex.reglas, mal, 100, 100)}["Tronco"]
    assert not r["ok"] and r["mensaje"]
    # fase arriba: las reglas "abajo" no se evaluan
    assert "Cadera delantera" not in {x["nombre"] for x in R.evaluar(ex.reglas, _lunge(), 100, 100, fases=("siempre",))}


def test_brazos_doblados_al_bajar_en_rojo():
    ex = load_exercise("zancada_reglas")
    rectos = _lunge()
    rectos[13] = (0.5, 0.35, 0)   # codo izq
    rectos[15] = (0.5, 0.5, 0)    # muneca izq: brazo recto (hombro-codo-muneca alineados)
    doblados = rectos.copy()
    doblados[15] = (0.65, 0.35, 0)   # antebrazo horizontal: codo a 90 grados
    ok = {r["nombre"]: r for r in R.evaluar(ex.reglas, rectos, 100, 100, fases=("siempre", "bajando"))}["Brazo izq"]
    mal = {r["nombre"]: r for r in R.evaluar(ex.reglas, doblados, 100, 100, fases=("siempre", "bajando"))}["Brazo izq"]
    assert ok["ok"] and not mal["ok"] and "brazos" in mal["mensaje"]


def test_segmenter_cuenta_al_volver_al_inicio():
    from src.evaluacion.segmentador import RepSegmenter
    seg = RepSegmenter(n_features=1, signal_idx=np.array([0]), reduce="mean", low=100, high=130, fin=150, min_duration_ms=100)
    cuentas = []
    for i, v in enumerate([170, 120, 90, 90, 120, 140, 155, 170]):   # baja, sube: 140 no cuenta, 155 si
        cuentas.append(seg.update(FeatureVec(values=np.array([v], dtype=np.float32), valid=np.array([True]),
                                             t_ms=i * 100, raw=None, label="")) is not None)
    assert cuentas.index(True) == 6 and sum(cuentas) == 1
