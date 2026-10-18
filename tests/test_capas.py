"""El arbol funcional se respeta: cada rama de src/ solo importa del tronco o de
ramas ANTERIORES del pipeline. Si alguien hace que captura/ importe de interfaz/,
esto falla y dice que archivo y que import."""

import ast
from pathlib import Path

PAQUETE = Path(__file__).resolve().parent.parent / "src"
ORDEN = ["nucleo", "almacenamiento", "captura", "procesamiento", "evaluacion",
         "sesion", "etiquetado", "preparacion", "entrenamiento", "interfaz"]


def _rama(modulo: str) -> str:
    return modulo.split(".")[1]


def test_todas_las_ramas_estan_en_el_orden():
    ramas = {p.name for p in PAQUETE.iterdir() if p.is_dir() and (p / "__init__.py").exists()}
    assert ramas == set(ORDEN)
    assert [p.name for p in PAQUETE.glob("*.py")] == ["__init__.py"]   # nada suelto en la raiz


def test_ninguna_rama_importa_de_una_posterior():
    violaciones = []
    for archivo in PAQUETE.rglob("*.py"):
        rel = archivo.relative_to(PAQUETE)
        if len(rel.parts) == 1:
            continue
        propia = ORDEN.index(rel.parts[0])
        for n in ast.walk(ast.parse(archivo.read_text(encoding="utf-8"))):
            nombres = ([n.module] if isinstance(n, ast.ImportFrom) and n.module else
                       [a.name for a in n.names] if isinstance(n, ast.Import) else [])
            for m in nombres:
                if m.startswith("src.") and ORDEN.index(_rama(m)) > propia:
                    violaciones.append(f"{rel}:{n.lineno} importa {m}")
    assert not violaciones, "\n".join(violaciones)
