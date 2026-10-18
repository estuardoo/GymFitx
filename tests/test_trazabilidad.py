"""Criterio 'cobertura de decisiones' de CRISP-DM: decision -> parametro -> etapa -> doc, sin eslabones sueltos."""

import re
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
DECISIONES = RAIZ / "docs" / "decisiones"
EN_EJECUCION = {"entrenamiento", "base_clip", "ejercicios"}   # params que no entran a una etapa de dvc.yaml (se leen al entrenar/en vivo)


def _dvc():
    return yaml.safe_load((RAIZ / "dvc.yaml").read_text("utf-8"))["stages"]


def _etapas():
    return [(n, e.get("do", e)) for n, e in _dvc().items()]


def test_cada_etapa_cita_una_decision_que_existe():
    for nombre, e in _etapas():
        citado = re.findall(r"docs/decisiones/[\w\-.]+\.md", e.get("desc", ""))
        assert citado, f"{nombre}: su desc no apunta a docs/decisiones/"
        for c in citado:
            assert (RAIZ / c).exists(), f"{nombre}: {c} no existe"


def test_los_params_de_las_etapas_existen():
    params = yaml.safe_load((RAIZ / "params.yaml").read_text("utf-8"))
    for nombre, e in _etapas():
        for p in e.get("params", []):
            assert p in params, f"{nombre}: params.yaml no tiene la seccion '{p}'"


def test_cada_seccion_de_params_esta_justificada_en_una_decision():
    params = yaml.safe_load((RAIZ / "params.yaml").read_text("utf-8"))
    texto = " ".join(p.read_text("utf-8") for p in DECISIONES.glob("0*.md"))
    sin = [s for s in params if s not in EN_EJECUCION and f"`{s}" not in texto] + \
          [s for s in params if s in EN_EJECUCION and s != "ejercicios" and f"`{s}" not in texto]
    assert not sin, f"secciones de params.yaml sin decision que las cite: {sin}"


def test_el_indice_de_decisiones_lista_todas():
    indice = (DECISIONES / "README.md").read_text("utf-8")
    for p in DECISIONES.glob("0*.md"):
        assert p.name in indice, f"{p.name} no esta en docs/decisiones/README.md"


def test_documentacion_del_codigo_al_dia():
    sys.path.insert(0, str(RAIZ / "scripts"))
    import generar_docs_codigo as G
    malos = G.desactualizados(RAIZ / "docs" / "codigo", G.generar(RAIZ))
    assert not malos, "docs/codigo desactualizada; corre: python scripts/generar_docs_codigo.py\n" + "\n".join(malos[:10])
