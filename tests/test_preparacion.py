"""Las 5 etapas de preparacion con clips sinteticos: salidas completas, deterministas y coherentes con lo que lee el entrenamiento."""
import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

from src.nucleo import config as C
from src.nucleo import inputs as INP
from src.nucleo.landmarks import POSE_LANDMARKS
from src.preparacion import documentar as DOC
from src.preparacion import etapas as E
from src.preparacion import tabla as T

EJ = "zancada"


def _clip(t, nombre, semilla, etiqueta, raw=None, seg=1, copia=False, frames=40, nan=0.0):
    """Registra un clip en la tabla y escribe su npz en input/bronze/<n>/<id>.npz."""
    rng = np.random.default_rng(semilla)
    pts = np.cumsum(rng.normal(0, 0.01, (frames, 33, 3)), axis=0).astype(np.float32) + rng.uniform(0.2, 0.8, (1, 33, 3)).astype(np.float32)
    if nan:
        pts[rng.random((frames, 33)) < nan] = np.nan
    c = INP.registrar_clip(t, EJ, etiqueta=etiqueta, t_ini_ms=0, t_fin_ms=1000, raw_id=raw["id"] if raw else None, seg=seg,
                           copia=copia, persona="P1", origen_viejo=f"x/{nombre}.mp4")
    np.savez(INP.ruta_clip(c["ej"], c["id"], "npz"), points=pts, point_names=np.array(POSE_LANDMARKS), t_ms=np.arange(frames) * 33)
    return c


@pytest.fixture
def datos(tmp_path, monkeypatch):
    desmarcado = None
    with INP.editar() as t:
        for etiqueta, base in ((1, 10), (0, 20)):
            for v in range(2):   # 2 grabaciones por clase
                raw = INP.registrar_raw(t, EJ, persona="P1")
                for sg in range(1, 4):
                    c = _clip(t, f"v{base + v}_s{sg}", base * 10 + v * 3 + sg, etiqueta, raw, sg)
                    if etiqueta == 1 and v == 0 and sg == 2:
                        desmarcado = INP.clave(c)
                    if v == 0 and sg == 1:
                        _clip(t, f"v{base}_s1_2", base, etiqueta, raw, sg, copia=True)   # copia de un ciclo
        _clip(t, "corto", 99, 1, frames=5)
        _clip(t, "ruidoso", 98, 0, nan=0.9)
    INP.guardar_seleccion({desmarcado: False})
    monkeypatch.setattr(DOC, "DICCIONARIO_DIR", tmp_path / "docs" / "diccionario")
    return tmp_path


def _huellas(datos):
    raices = [C.PLATE_DIR, C.GOLD_DIR, C.REPORTES_DIR, datos / "docs"]
    return {str(p): hashlib.md5(p.read_bytes()).hexdigest() for r in raices for p in sorted(r.rglob("*")) if p.is_file()}


def _final():
    d = C.GOLD_DIR / str(INP.id_de(EJ))
    meta = json.loads((d / "meta.json").read_text())
    return meta, np.stack([np.load(d / f"{f['key']}.npy") for f in meta["filas"]])


def test_cinco_etapas_salidas_y_motivos(datos):
    r = E.todo(EJ)
    sel = json.loads((C.REPORTES_DIR / str(INP.id_de(EJ)) / "seleccion.json").read_text())
    assert sel["incluidos"] == 15 and {e["motivo"] for e in sel["excluidos"]} == {"desmarcado a mano en el panel"}
    lim = json.loads((C.REPORTES_DIR / str(INP.id_de(EJ)) / "limpieza.json").read_text())
    por = {c["clip"]: c["motivos"] for c in lim["clips"]}
    assert sum(any("muy corto" in m for m in ms) for ms in por.values()) == 1
    assert sum(any("sin detectar" in m for m in ms) for ms in por.values()) == 1
    assert lim["salen"] == 2 and lim["copias"] == 2 and "Informe de limpieza" in (C.REPORTES_DIR / str(INP.id_de(EJ)) / "limpieza.md").read_text()
    assert r["integrar"]["grabaciones"] == 4 and r["integrar"]["por_clase"] == {"bien": 6, "mal": 7}

    meta, X = _final()
    assert X.shape == (len(meta["filas"]), meta["n_features"]) and len(meta["columnas"]) == meta["n_features"]
    assert {f["key"] for f in meta["filas"]} == {Path(f["clip"]).stem for f in meta["filas"]}   # gold lleva el numero del clip
    dic = (datos / "docs" / "diccionario" / f"{EJ}.csv").read_text().splitlines()
    assert len(dic) - 1 == meta["n_features"] and dic[1].split(",")[0] == "f01_LEFT_SHOULDER_x"   # 100 % de las columnas, en orden


def test_mismas_entradas_mismos_bytes(datos):
    E.todo(EJ)
    antes = _huellas(datos)
    E.todo(EJ)
    assert _huellas(datos) == antes   # criterio 1: la anotacion (md5) no cambia al rehacer


def test_el_entrenamiento_lee_lo_mismo_que_la_tabla_final(datos):
    E.todo(EJ)
    meta, X = _final()
    vec = T.vectores(EJ, T.spec_de(EJ))
    for fila, x in zip(meta["filas"], X):
        if not fila["generado"]:
            assert np.allclose(vec[fila["clip"]], x)
    assert len(vec) == 14   # 16 clips menos corto y ruidoso (limpieza); el desmarcado a mano lo filtra la seleccion del entrenamiento


def test_gold_se_rehace_si_cambia_la_normalizacion(datos):
    E.todo(EJ)
    spec = T.spec_de(EJ)
    d = C.GOLD_DIR / str(INP.id_de(EJ))
    antes = {p.name for p in d.glob("0*.npy")}
    assert antes
    T.vectores(EJ, {**spec, "cfg": {**spec["cfg"], "n_frames_fijo": spec["cfg"].get("n_frames_fijo", 30) + 5}})
    meta = json.loads((d / "meta.json").read_text())
    assert meta["hash"] != T.hash_gold(spec)   # el cache de gold se invalida con el hash


def test_diccionario_falla_si_no_coincide(datos):
    with pytest.raises(ValueError, match="describe"):
        DOC.escribir_diccionario(EJ, T.spec_de(EJ), [{"columna": "a"}], 2)
