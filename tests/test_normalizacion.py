"""Normalizacion por ejercicio (Kpoints -> Normalizacion): parser de formulas, (K - origen) / escala, n_frames, gold y SQL."""
import json

import numpy as np
import pytest
from test_preparacion import EJ, datos  # noqa: F401  (fixture: clips sinteticos de 'zancada')

from src.etiquetado import editor_puntos as PUNTOS
from src.nucleo import config as C
from src.nucleo import inputs as INP
from src.preparacion import etapas as E
from src.preparacion import tabla as T
from src.procesamiento.puntos import formula as FORM
from src.procesamiento.puntos import normalizacion as NORM
from src.procesamiento.puntos import vectorizar

SUBIR_REAL = E._subir_sql   # conftest lo reemplaza en cada test; este es el verdadero

K = {1: np.array([[0.0, 0.0], [1.0, 1.0]]), 2: np.array([[2.0, 0.0], [3.0, 1.0]]), 3: np.array([[0.0, 4.0], [1.0, 5.0]])}


def test_formulas_validas():
    assert np.allclose(FORM.evaluar("medio(C1,C2)", K, "p"), [[1, 0], [2, 1]])
    assert np.allclose(FORM.evaluar("dist(C1,C2)", K, "n"), [2, 2])
    assert np.allclose(FORM.evaluar("dist(medio(C1,C2), C3)", K, "n"), [np.hypot(1, 4)] * 2)
    assert np.allclose(FORM.evaluar("max(dist(C1,C2), dist(C1,C3))", K, "n"), [4, 4])
    assert np.allclose(FORM.evaluar("prom(C1,C2,C3)", K, "p"), [[2 / 3, 4 / 3], [5 / 3, 7 / 3]])
    assert np.allclose(FORM.evaluar("(C2 - C1) / dist(C1,C2) * 2", K, "p"), [[2, 0], [2, 0]])
    assert FORM.usados("dist(medio(C12,C13), c2)") == [2, 12, 13]


@pytest.mark.parametrize("texto,tipo", [
    ("__import__('os').system('x')", "n"), ("C1.x", "n"), ("abs(C1)", "n"), ("C1 * C2", "p"), ("C1 + 2", "p"),
    ("dist(C1)", "n"), ("medio(C1,C2)", "n"), ("dist(C1,C2)", "p"), ("C9", "p"), ("", "p"), ("C1 +", "p"),
    ("C1 / C2", "p"), ("[C1]", "p"), ("dist(C1,C2) if 1 else 2", "n"), ("x" * 200, "p"),
    ("K1", "p"), ("dist(K1,K2)", "n"),       # K<n> (posicion en la lista) ya no se acepta en formulas nuevas
])
def test_formulas_rechazadas(texto, tipo):
    with pytest.raises(ValueError):
        FORM.validar(texto, tipo, [1, 2, 3])


def _clip(desp=(0.0, 0.0), k=1.0, frames=20):
    """Cuerpo de 4 puntos que se agacha: caderas (0.4/0.6, 0.8), hombros (0.4/0.6, 0.4) -> tronco = 0.4."""
    t = np.linspace(0, 1, frames)[:, None]
    base = np.array([[0.4, 0.4, 0.1], [0.6, 0.4, 0.1], [0.4, 0.8, 0.0], [0.6, 0.8, 0.0]])
    pts = np.repeat(base[None], frames, axis=0)
    pts[:, :, 1] += 0.1 * np.sin(t * np.pi)          # todo el cuerpo sube/baja
    pts[:, :2, 0] += 0.02 * t                         # un hombro se mueve
    pts[:, :, :2] = pts[:, :, :2] * k + np.array(desp)
    return pts.astype(np.float32), ["LS", "RS", "LH", "RH"]


CFG = {"modo": "formula", "origen": "medio(C3,C4)", "escala": "dist(medio(C1,C2), medio(C3,C4))", "n_frames_fijo": 10,
       "puntos": {"1": "LS", "2": "RS", "3": "LH", "4": "RH"}}


def test_normaliza_por_formula():
    pts, nombres = _clip()
    out = NORM.normalizar(pts, nombres, CFG)
    assert out.shape == (10, 4, 3)
    # el medio de las caderas es el origen (0,0); los hombros quedan a un tronco (0.4/0.4 = 1) hacia arriba (y negativa en imagen)
    assert np.allclose(out[:, 2:, :2].mean(axis=1), 0, atol=1e-5)
    assert np.allclose(out[:, :2, 1].mean(axis=1), -1, atol=2e-3)     # (el tronco varia un poco: un hombro se mueve)
    assert np.allclose(out[:, 3, 0] - out[:, 2, 0], 0.2 / 0.4, atol=2e-3)    # caderas separadas 0.2 = 0.5 troncos
    assert np.allclose(out[..., 2], pts[0, :, 2][None] / 0.4, atol=2e-3)    # z solo se divide por la escala


def test_invariante_a_posicion_y_tamano():
    a = NORM.normalizar(*_clip(), CFG)
    b = NORM.normalizar(*_clip(desp=(0.3, -0.2), k=2.5), CFG)
    assert np.allclose(a[..., :2], b[..., :2], atol=1e-4)


def test_escala_mediana_ignora_cuadros_malos():
    pts, nombres = _clip()
    pts[3, 0, :2] = np.nan                    # un hombro no detectado en un cuadro
    pts[5, :2, :] = pts[5, 2:, :]             # y otro cuadro con tronco 0
    assert NORM.escala_del_clip(NORM.valores_formula(pts, nombres, CFG)[1]) == pytest.approx(0.4, abs=0.02)


def test_clip_sin_escala_se_marca():
    pts = np.zeros((12, 4, 3), dtype=np.float32)       # todo en el mismo punto: escala 0
    with pytest.raises(NORM.NormalizacionInvalida):
        NORM.normalizar(pts, ["LS", "RS", "LH", "RH"], CFG)
    prep = (pts, ["LS", "RS", "LH", "RH"], np.zeros((12, 0), np.float32), [])
    assert vectorizar.vector_de_prep(prep, {"cfg": CFG, "features": "puntos"}).size == 0   # vector vacio = el clip no entra


def test_misma_formula_en_vivo_y_entrenamiento():
    pts, nombres = _clip()
    spec = {"point_names": nombres, "kpoints": [], "cfg": CFG, "features": "puntos", "features_def": []}
    assert np.allclose(vectorizar.vector_de_clip(pts, nombres, spec), vectorizar.vector_de_prep((pts, nombres, np.zeros((20, 0), np.float32), []), spec))
    assert vectorizar.vector_de_clip(pts, nombres, spec).size == 10 * 4 * 3     # 'puntos' = x,y,z de cada kpoint por cuadro


# ---------------------------------------------------------------- por ejercicio
def test_defecto_por_ejercicio_y_n_frames(datos):  # noqa: F811
    n = NORM.normalizacion_de(EJ)
    assert n["origen"] == "medio(C24,C25)" and n["escala"] == "dist(medio(C12,C13), medio(C24,C25))"   # caderas / tronco: codigos fijos
    assert n["n_frames"] == C.params("formato")["n_frames_defecto"] and not n["propia"]
    cfg = NORM.cfg_normalizacion(EJ)
    assert cfg["modo"] == "formula" and cfg["puntos"] == {"12": "LEFT_SHOULDER", "13": "RIGHT_SHOULDER", "24": "LEFT_HIP", "25": "RIGHT_HIP"}


def test_guardar_y_validar(datos):  # noqa: F811
    with pytest.raises(ValueError, match="C33"):
        PUNTOS.guardar_normalizacion(EJ, {"origen": "C33", "escala": "dist(C12,C13)", "n_frames": 20})
    with pytest.raises(ValueError, match="punto"):
        PUNTOS.guardar_normalizacion(EJ, {"origen": "dist(C12,C13)", "escala": "dist(C12,C13)", "n_frames": 20})
    with pytest.raises(ValueError, match="n_frames"):
        PUNTOS.guardar_normalizacion(EJ, {"origen": "C24", "escala": "dist(C12,C24)", "n_frames": 1})
    r = PUNTOS.guardar_normalizacion(EJ, {"origen": "C24", "escala": "dist(C12,C24)", "n_frames": 20})
    assert r["cambio"] and PUNTOS.guardar_normalizacion(EJ, {"origen": "C24", "escala": "dist(C12,C24)", "n_frames": 20})["cambio"] is False
    n = PUNTOS.leer_ejercicio(EJ)["normalizacion"]
    assert n["origen"] == "C24" and n["n_frames"] == 20 and n["propia"] and n["error"] is None
    assert NORM.cfg_normalizacion(EJ)["n_frames_fijo"] == 20
    assert "normalizacion" in json.loads((C.PARAMETROS_DIR / str(INP.id_de(EJ)) / "guide.json").read_text("utf-8"))


def test_kpoint_quitado_se_avisa(datos):  # noqa: F811
    PUNTOS.guardar_normalizacion(EJ, {"origen": "C24", "escala": "dist(C12,C24)", "n_frames": 20})
    d = PUNTOS._definicion_de(EJ)
    d["kpoints"] = [k for k in d["kpoints"] if k["nombre"] != "LEFT_HIP"]
    PUNTOS.DEF.guardar(EJ, d)
    assert "C24" in PUNTOS.leer_ejercicio(EJ)["normalizacion"]["error"]
    with pytest.raises(ValueError, match="C24"):
        NORM.cfg_normalizacion(EJ)


def test_previa_en_un_clip(datos):  # noqa: F811
    r = T.previa_normalizacion(EJ, {"origen": "medio(C24,C25)", "escala": "dist(medio(C12,C13), medio(C24,C25))", "n_frames": 30})
    assert r["cuadros"] > 0 and r["escala"] > 0 and set(r["ejemplo"]) == {"LEFT_SHOULDER", "RIGHT_SHOULDER", "LEFT_HIP", "RIGHT_HIP"}
    assert r["clip"] in r["clips"] and T.previa_normalizacion(EJ, {"origen": "C24", "escala": "dist(C12,C24)", "n_frames": 5}, r["clips"][0])["clip"] == r["clips"][0]


def test_gold_sigue_a_la_formula_y_a_n_frames(datos):  # noqa: F811
    E.todo(EJ)
    d = C.GOLD_DIR / str(INP.id_de(EJ))
    meta = json.loads((d / "meta.json").read_text())
    h0, n0 = meta["hash"], meta["n_features"]
    assert meta["normalizacion"].startswith("formula:o=medio(C24,C25)")
    PUNTOS.guardar_normalizacion(EJ, {"origen": "medio(C24,C25)", "escala": "dist(C12,C24)", "n_frames": 12})
    r = E.formatear(EJ)
    meta = json.loads((d / "meta.json").read_text())
    assert meta["hash"] != h0 and meta["n_features"] != n0 and "dist(C12,C24)" in meta["normalizacion"]
    assert r["sql"]["estado"] == "pendiente" and np.load(d / f"{meta['filas'][0]['key']}.npy").size == meta["n_features"]
    assert T.spec_de(EJ)["cfg"]["n_frames_fijo"] == 12


def test_subir_sql_llama_a_respaldar_solo_con_los_clips_del_ejercicio(datos, monkeypatch):  # noqa: F811
    from src.etiquetado import tablas
    visto = {}
    monkeypatch.setattr(tablas, "respaldar_sql", lambda rows: visto.update(ejs={r["exercise"] for r in rows}, n=len(rows)) or {"resumen": {"frames_fix": 1}, "error": None})
    r = SUBIR_REAL(EJ)
    assert r["estado"] == "subido" and visto["ejs"] <= {EJ}
    monkeypatch.setattr(tablas, "respaldar_sql", lambda rows: {"resumen": None, "error": "sin conexion"})
    assert SUBIR_REAL(EJ)["estado"] == "pendiente"
    monkeypatch.setattr(tablas, "respaldar_sql", lambda rows: (_ for _ in ()).throw(RuntimeError("boom")))
    assert SUBIR_REAL(EJ)["estado"] == "pendiente"       # nunca lanza


def test_formulas_viejas_con_k_se_convierten_a_c(datos):  # noqa: F811
    d = PUNTOS._definicion_de(EJ)
    d["normalizacion"] = {"origen": "medio(K7,K8)", "escala": "dist(medio(K1,K2), medio(K7,K8))", "n_frames": 20}   # K = posicion en la lista
    PUNTOS.DEF.guardar(EJ, d)
    n = NORM.normalizacion_de(EJ)
    assert n["origen"] == "medio(C24,C25)" and n["escala"] == "dist(medio(C12,C13), medio(C24,C25))" and n["n_frames"] == 20


def test_codigo_c_es_fijo_entre_ejercicios():
    a = [{"nombre": "X", "origen": {"tipo": "landmark", "fuente": "pose", "landmark": "LEFT_HIP"}}]
    b = [{"nombre": "Y", "numero": 3, "origen": {"tipo": "landmark", "fuente": "pose", "landmark": "LEFT_HIP"}}]
    assert NORM.codigos_de(a) == {24: "X"} and NORM.codigos_de(b) == {24: "Y"}
