"""Las 5 etapas de preparacion con clips sinteticos: salidas completas, deterministas y coherentes con lo que lee el entrenamiento."""
import hashlib
import json

import numpy as np
import pytest

from src.nucleo.landmarks import POSE_LANDMARKS
from src.preparacion import documentar as DOC
from src.preparacion import etapas as E
from src.preparacion import tabla as T

EJ = "zancada"


def _clip(carpeta, nombre, semilla, frames=40, nan=0.0):
    rng = np.random.default_rng(semilla)
    pts = np.cumsum(rng.normal(0, 0.01, (frames, 33, 3)), axis=0).astype(np.float32) + rng.uniform(0.2, 0.8, (1, 33, 3)).astype(np.float32)
    if nan:
        pts[rng.random((frames, 33)) < nan] = np.nan
    np.savez(carpeta / f"{nombre}.npz", points=pts, point_names=np.array(POSE_LANDMARKS), t_ms=np.arange(frames) * 33)
    return {"clip": f"{EJ}/{carpeta.name}/{nombre}.mp4", "npz": f"{nombre}.npz", "clase": carpeta.name, "exercise": EJ}


@pytest.fixture
def datos(tmp_path, monkeypatch):
    clips = tmp_path / "clips"
    filas = []
    for clase, base in (("bien", 10), ("mal", 20)):
        d = clips / EJ / clase
        d.mkdir(parents=True)
        for v in range(2):   # 2 grabaciones por clase
            for s in range(1, 4):
                filas.append(_clip(d, f"v{base + v}_{EJ}_s{s:02d}_{clase}", base * 10 + v * 3 + s))
        filas.append(_clip(d, f"v{base}_{EJ}_s01_{clase}_2", base))   # copia _2 de un ciclo
    filas.append(_clip(clips / EJ / "bien", "corto_s01_bien", 99, frames=5))
    filas.append(_clip(clips / EJ / "mal", "ruidoso_s01_mal", 98, nan=0.9))
    (tmp_path / "manifest.json").write_text(json.dumps(filas))
    (tmp_path / "sel.json").write_text(json.dumps({f"{EJ}/bien/v10_{EJ}_s02_bien.mp4": False}))
    for mod, nombre, valor in ((T, "CLIPS_DIR", clips), (T, "MANIFEST_PATH", tmp_path / "manifest.json"), (T, "SELECCION_PATH", tmp_path / "sel.json"),
                               (E, "INTERMEDIO", tmp_path / "datos" / "intermedio"), (E, "FINAL", tmp_path / "datos" / "final"),
                               (E, "REPORTES_DIR", tmp_path / "reportes"), (DOC, "REPORTES_DIR", tmp_path / "reportes"),
                               (DOC, "DICCIONARIO_DIR", tmp_path / "docs" / "diccionario")):
        monkeypatch.setattr(mod, nombre, valor)
    monkeypatch.setattr(T, "_leer_json", lambda p, d: json.loads(p.read_text()) if p == tmp_path / "manifest.json" else d)
    return tmp_path


def _huellas(raiz):
    return {str(p.relative_to(raiz)): hashlib.md5(p.read_bytes()).hexdigest() for p in sorted(raiz.rglob("*")) if p.is_file() and p.name != "sel.json"}


def test_cinco_etapas_salidas_y_motivos(datos):
    r = E.todo(EJ)
    sel = json.loads((datos / "reportes" / f"seleccion_{EJ}.json").read_text())
    assert sel["incluidos"] == 15 and {e["motivo"] for e in sel["excluidos"]} == {"desmarcado a mano en el panel"}
    lim = json.loads((datos / "reportes" / f"limpieza_{EJ}.json").read_text())
    por = {c["clip"].split("/")[-1]: c["motivos"] for c in lim["clips"]}
    assert any("muy corto" in m for m in por["corto_s01_bien.mp4"]) and any("sin detectar" in m for m in por["ruidoso_s01_mal.mp4"])
    assert lim["salen"] == 2 and lim["copias"] == 2 and "Informe de limpieza" in (datos / "reportes" / f"limpieza_{EJ}.md").read_text()
    assert r["integrar"]["grabaciones"] == 4 and r["integrar"]["por_clase"] == {"bien": 6, "mal": 7}

    meta = json.loads((datos / "datos" / "final" / EJ / "meta.json").read_text())
    X = np.load(datos / "datos" / "final" / EJ / "X.npy")
    assert X.shape == (len(meta["filas"]), meta["n_features"]) and len(meta["columnas"]) == meta["n_features"]
    dic = (datos / "docs" / "diccionario" / f"{EJ}.csv").read_text().splitlines()
    assert len(dic) - 1 == meta["n_features"] and dic[1].split(",")[0] == "f01_LEFT_SHOULDER_x"   # 100 % de las columnas, en orden


def test_mismas_entradas_mismos_bytes(datos):
    E.todo(EJ)
    antes = _huellas(datos)
    E.todo(EJ)
    assert _huellas(datos) == antes   # criterio 1: la anotacion (md5) no cambia al rehacer


def test_el_entrenamiento_lee_lo_mismo_que_la_tabla_final(datos):
    E.todo(EJ)
    meta = json.loads((datos / "datos" / "final" / EJ / "meta.json").read_text())
    X = np.load(datos / "datos" / "final" / EJ / "X.npy")
    vec = T.vectores(EJ, T.spec_de(EJ))
    for fila, x in zip(meta["filas"], X):
        if not fila["generado"]:
            assert np.allclose(vec[fila["clip"]], x)
    assert not any("corto" in c or "ruidoso" in c for c in vec)   # la limpieza tambien aplica al entrenar


def test_diccionario_falla_si_no_coincide(datos):
    with pytest.raises(ValueError, match="describe"):
        DOC.escribir_diccionario(EJ, T.spec_de(EJ), [{"columna": "a"}], 2)
