"""Modulo AHPC (interfaz/api/ahpc.py): listar ejercicios y armar el paquete listo para el cluster
(.npz + script standalone + .sbatch por ejercicio), sin cortar ni recalcular nada -- ver
src/entrenamiento/exportar_slurm.py para el detalle del formato del .npz."""

from __future__ import annotations

import json
import zipfile
from io import BytesIO
from pathlib import Path

from test_swap_sink import _instalar_stub_mediapipe  # noqa: E402

_instalar_stub_mediapipe()

from fastapi.testclient import TestClient  # noqa: E402

from src.interfaz.api import ahpc  # noqa: E402
from src.interfaz.app import app  # noqa: E402

client = TestClient(app)

FILAS = [{"clip": f"{'bien' if i % 2 else 'mal'}/c{i}.mp4", "clase": "bien" if i % 2 else "mal",
         "type": 1, "exercise": "sentadilla", "origen": f"x/{i}.mp4"} for i in range(4)]
FILAS.append({"clip": "base/b.mp4", "clase": "base", "type": 1, "exercise": "sentadilla", "origen": "x"})


def _falso_exportar(ejercicio, out):
    import numpy as np
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    np.savez(out, points=np.zeros((2, 3, 2, 3), dtype="float32"), point_names=["a", "b"],
             metrics=np.zeros((2, 3, 1), dtype="float32"), metric_names=["ang"], metric_types=["angle"],
             clips=["c0.mp4", "c1.mp4"], y=["bien", "mal"], ejercicio=ejercicio, tipo=1)
    return {"archivo": str(out), "clips": 2, "frames_por_clip": 3, "kpoints": 2, "metricas": 1,
            "clases": {"bien": 1, "mal": 1}, "point_codes": ["C11", "C12"]}


def test_lista_ejercicios_con_su_conteo_y_si_tiene_catalogo(monkeypatch):
    monkeypatch.setattr(ahpc, "_manifest", lambda: FILAS)
    monkeypatch.setattr(ahpc, "puntos_de_ejercicio", lambda ej: ["a", "b"])
    r = client.get("/api/ahpc/ejercicios")
    assert r.status_code == 200
    assert r.json() == [{"ejercicio": "sentadilla", "clips": 4, "listo": True}]   # 'base' no cuenta


def test_exportar_arma_zip_con_npz_script_y_sbatch(monkeypatch, tmp_path):
    monkeypatch.setattr(ahpc, "SLURM_DIR", tmp_path)
    monkeypatch.setattr(ahpc, "exportar", _falso_exportar)
    r = client.post("/api/ahpc/exportar", json={"ejercicios": ["sentadilla"]})
    assert r.status_code == 200 and r.headers["content-disposition"].endswith('"ahpc_slurm.zip"')
    z = zipfile.ZipFile(BytesIO(r.content))
    nombres = set(z.namelist())
    assert nombres == {"input/sentadilla.npz", "slurm_sentadilla.sbatch", "slurm_resumen_sentadilla.sbatch",
                       "lanzar_sentadilla.sh", "busqueda_features_slurm.py", "resumen_busqueda_slurm.py",
                       "estado_busqueda_slurm.py", "diagnostico_hpc.sh", "LEEME.txt", "config.json"}
    lanzador = z.read("lanzar_sentadilla.sh").decode()
    assert "slurm_sentadilla.sbatch" in lanzador and "gymfit_resumen_sentadilla" in lanzador
    assert "--dependency=" in lanzador and "afterany" in lanzador
    sbatch = z.read("slurm_sentadilla.sbatch").decode()
    assert "input/sentadilla.npz" in sbatch and "gymfit_sentadilla" in sbatch
    assert "--partition=standard" in sbatch and "--time=04:00:00" in sbatch   # tuneado para el cluster real (diagnostico_hpc.sh)
    resumen_sbatch = z.read("slurm_resumen_sentadilla.sbatch").decode()
    assert "gymfit_resumen_sentadilla" in resumen_sbatch and "resumen_sentadilla/" in resumen_sbatch
    assert "resumen_busqueda_slurm.py" in resumen_sbatch
    import numpy as np
    d = np.load(BytesIO(z.read("input/sentadilla.npz")))
    assert list(d["point_names"]) == ["a", "b"]
    config = json.loads(z.read("config.json"))
    assert config["ejercicios"] == ["sentadilla"]
    assert config["modelos_codigo"] == ahpc.MODELOS_CODIGO
    assert config["kpoints_codigo"] == {"sentadilla": {"K01": "C11", "K02": "C12"}}


def test_exportar_varios_lista_los_que_fallaron_en_cabecera(monkeypatch, tmp_path):
    def falla_o_exporta(ejercicio, out):
        if ejercicio == "mala":
            raise ValueError("sin datos")
        return _falso_exportar(ejercicio, out)
    monkeypatch.setattr(ahpc, "SLURM_DIR", tmp_path)
    monkeypatch.setattr(ahpc, "exportar", falla_o_exporta)
    r = client.post("/api/ahpc/exportar", json={"ejercicios": ["sentadilla", "mala"]})
    assert r.status_code == 200
    assert json.loads(r.headers["x-ahpc-errores"]) == {"mala": "sin datos"}
    z = zipfile.ZipFile(BytesIO(r.content))
    assert "input/sentadilla.npz" in z.namelist() and "input/mala.npz" not in z.namelist()


def test_sql_caido_devuelve_error_claro(monkeypatch):
    from src.almacenamiento import dataset_sql as SQL

    def revienta(ejercicio, out):
        raise SQL.SQLServerNoDisponible("sin servidor")
    monkeypatch.setattr(ahpc, "exportar", revienta)
    r = client.post("/api/ahpc/exportar", json={"ejercicios": ["sentadilla"]})
    assert r.status_code == 400 and "SQL Server" in r.json()["error"]
