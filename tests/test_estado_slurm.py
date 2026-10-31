"""scripts/estado_busqueda_slurm.py: junta los <salida>.estado.json que cada tarea de busqueda_features_slurm.py
va sobreescribiendo sola, en una tabla de avance (por tarea: cuanto hizo, %, si termino o fallo)."""

from __future__ import annotations

import csv
import json

from scripts.hpc import estado_busqueda_slurm as EST


def _estado(ruta, **campos):
    base = {"tarea": 0, "n_tareas": 2, "combos": 3, "objetivo": 6, "filas": 20, "pct": 50.0,
            "terminado": False, "error": "", "actualizado": "2026-09-29T00:00:00"}
    base.update(campos)
    ruta.write_text(json.dumps(base), encoding="utf-8")


def test_leer_estados_junta_y_ordena_por_tarea(tmp_path):
    _estado(tmp_path / "res_1.estado.json", tarea=1, combos=6, objetivo=6, pct=100.0, terminado=True)
    _estado(tmp_path / "res_0.estado.json", tarea=0, combos=3, objetivo=6, pct=50.0, terminado=False)

    filas = EST.leer_estados(tmp_path)
    assert [f["tarea"] for f in filas] == [0, 1]
    assert filas[0]["terminado"] is False and filas[1]["terminado"] is True


def test_main_imprime_tabla_y_puede_guardar_csv(tmp_path, capsys):
    _estado(tmp_path / "res_0.estado.json", tarea=0, combos=6, objetivo=6, pct=100.0, terminado=True)
    _estado(tmp_path / "res_1.estado.json", tarea=1, combos=2, objetivo=6, pct=33.3, terminado=False, error="MemoryError: boom")

    salida_csv = tmp_path / "estado.csv"
    EST.main(["--resultados", str(tmp_path), "--csv", str(salida_csv)])

    out = capsys.readouterr().out
    assert "terminado" in out and "ERROR: MemoryError: boom" in out
    assert "1/2 tareas terminadas, 1 con error" in out

    with salida_csv.open(encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    assert len(filas) == 2 and {f["tarea"] for f in filas} == {"0", "1"}


def test_main_sin_estado_json_avisa_en_vez_de_reventar(tmp_path):
    import pytest

    with pytest.raises(SystemExit, match="Sin \\*.estado.json"):
        EST.main(["--resultados", str(tmp_path)])
