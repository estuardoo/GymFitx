"""src/nucleo/migrar.py: copia los datos del proyecto viejo sin tocarlo, sin pisar
nada y una sola vez."""

import json
import tempfile
from pathlib import Path

from src.nucleo.migrar import migrar


def _viejo(base: Path) -> Path:
    v = base / "GYMFITX"
    for rel, contenido in {
        "recordings/cuerpo_completo/2026-08-25/1_base.mp4": "video",
        "templates/mano.npz": "npz",
        "models/pose_landmarker.task": "modelo",
        "fgml/dataset/bien/c1.npz": "clip",
        "fgml/entrenamientos/run_1/meta.json": "{}",
        "fgml/labels.json": '{"a": 1}',
        "fgml/.export_estado.json": "{}",
        "fgml/pipeline.yaml": "cortes: {}",
        "fgml/data/viejo.mp4": "no se copia",
        "fgml/cortador.py": "codigo",
        "exercises/cuerpo_completo.yaml": "name: editado",
    }.items():
        p = v / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(contenido)
    return v


def test_copia_todo_al_lugar_nuevo_y_no_toca_el_viejo():
    with tempfile.TemporaryDirectory() as d:
        base = Path(d)
        viejo = _viejo(base)
        raiz = base / "GYMFIT"
        datos = raiz / "datos"
        (raiz / "ejercicios").mkdir(parents=True)
        (raiz / "ejercicios" / "cuerpo_completo.yaml").write_text("name: del codigo")
        (datos / "etiquetas.json").parent.mkdir(parents=True)
        (datos / "etiquetas.json").write_text('{"ya": "estaba"}')   # no se pisa

        r = migrar(viejo, raiz, datos)
        assert r["hecho"]
        assert (datos / "grabaciones/cuerpo_completo/2026-08-25/1_base.mp4").read_text() == "video"
        assert (datos / "plantillas/mano.npz").exists()
        assert (raiz / "modelos/pose_landmarker.task").exists()
        assert (datos / "clips/bien/c1.npz").exists()
        assert (datos / "entrenamientos/run_1/meta.json").exists()
        assert (datos / "export_estado.json").exists()
        assert (datos / "ajustes.yaml").read_text() == "cortes: {}"
        assert json.loads((datos / "etiquetas.json").read_text()) == {"ya": "estaba"}
        assert (raiz / "ejercicios/cuerpo_completo.yaml").read_text() == "name: editado"
        assert not any(p.name == "viejo.mp4" for p in raiz.rglob("*"))
        assert not any(p.name == "cortador.py" for p in raiz.rglob("*"))
        assert (viejo / "fgml/labels.json").exists()                  # el viejo queda igual

        assert migrar(viejo, raiz, datos)["hecho"] is False          # una sola vez


def test_sin_proyecto_viejo_no_hace_nada():
    with tempfile.TemporaryDirectory() as d:
        r = migrar(Path(d) / "no_existe", Path(d) / "GYMFIT", Path(d) / "GYMFIT/datos")
        assert r["hecho"] is False and "no hay proyecto viejo" in r["motivo"]
