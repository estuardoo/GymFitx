"""Genera docs/codigo/: la documentacion de TODO el codigo, leida del propio codigo (docstrings, firmas, rutas, imports,
parametros) para que nunca quede desactualizada. Solo libreria estandar.

    python scripts/generar_docs_codigo.py            # reescribe docs/codigo/
    python scripts/generar_docs_codigo.py --revisar  # no escribe: sale con error si docs/codigo/ esta desactualizada

Salida (sin fechas: mismas fuentes, mismos bytes):
    INDICE.md            que hay en cada rama y modulo
    dependencias.md      matriz de quien importa a quien (el arbol de capas)
    api_rutas.md         todas las rutas REST/WebSocket
    parametros.md        cada clave de parameters/config.json y los modulos que la usan
    <rama>/<modulo>.md   clases, funciones y constantes con su docstring (src/), scripts/ y la web (js)"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
METODOS = {"get", "post", "put", "delete", "patch", "websocket"}


def _orden(raiz: Path) -> list[str]:
    """El ORDEN de ramas de tests/test_capas.py (unica fuente de la regla del arbol)."""
    for n in ast.parse((raiz / "tests" / "test_capas.py").read_text("utf-8")).body:
        if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "ORDEN" for t in n.targets):
            return list(ast.literal_eval(n.value))
    return []


def _fuentes(raiz: Path) -> list[Path]:
    py = [p for base in ("src", "scripts") for p in sorted((raiz / base).rglob("*.py")) if "__pycache__" not in p.parts]
    js = sorted((raiz / "src" / "interfaz" / "web" / "js").glob("*.js"))
    return [*py, *js]


def _rel(p: Path, raiz: Path) -> str:
    return p.relative_to(raiz).as_posix()


def _destino(rel: str) -> str:
    """src/nucleo/config.py -> nucleo/config.md · scripts/x.py -> scripts/x.md · .../web/js/a.js -> web/js/a.md"""
    partes = rel.split("/")
    if partes[0] == "src" and "web" in partes:
        partes = ["web", *partes[partes.index("web") + 1:]]
    elif partes[0] == "src":
        partes = partes[1:]
    return "/".join(partes).rsplit(".", 1)[0] + ".md"


def _firma(n: ast.AST) -> str:
    ret = f" -> {ast.unparse(n.returns)}" if n.returns else ""
    return f"{'async ' if isinstance(n, ast.AsyncFunctionDef) else ''}def {n.name}({ast.unparse(n.args)}){ret}"


def _doc(texto: str | None) -> str:
    return f"```text\n{texto.strip()}\n```\n" if texto and texto.strip() else "_sin docstring_\n"


def _resumen(texto: str | None) -> str:
    return (texto or "").strip().split("\n")[0].replace("|", "/")


def _ruta_de(dec: ast.AST) -> tuple[str, str] | None:
    """@router.get("/api/x") -> ("GET", "/api/x")"""
    if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute) and dec.func.attr in METODOS and dec.args \
            and isinstance(dec.args[0], ast.Constant) and isinstance(dec.args[0].value, str):
        return dec.func.attr.upper(), dec.args[0].value
    return None


def _importados(arbol: ast.AST) -> list[str]:
    salida = []
    for n in ast.walk(arbol):
        if isinstance(n, ast.ImportFrom) and n.module and n.module.startswith("src."):
            salida.append(n.module)
        elif isinstance(n, ast.Import):
            salida += [a.name for a in n.names if a.name.startswith("src.")]
    return salida


def _doc_py(rel: str, texto: str):
    """-> (markdown, resumen, rutas, imports, parametros usados)"""
    arbol = ast.parse(texto)
    modulo = ast.get_docstring(arbol)
    md = [f"# `{rel}`", "", _doc(modulo)]
    consts = [t.id for n in arbol.body if isinstance(n, ast.Assign) for t in n.targets if isinstance(t, ast.Name) and t.id.isupper()]
    if consts:
        md += ["## Constantes", "", ", ".join(f"`{c}`" for c in consts), ""]
    rutas, funciones, clases = [], 0, 0
    for n in arbol.body:
        if isinstance(n, ast.ClassDef):
            clases += 1
            md += [f"## class `{n.name}`", "", _doc(ast.get_docstring(n))]
            for m in n.body:
                if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    md += [f"### `{n.name}.{m.name}`", "", f"`{_firma(m)}`", "", _doc(ast.get_docstring(m))]
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funciones += 1
            md += [f"## `{n.name}`", "", f"`{_firma(n)}`", ""]
            for d in n.decorator_list:
                r = _ruta_de(d)
                if r:
                    rutas.append((r[0], r[1], n.name, _resumen(ast.get_docstring(n))))
                    md += [f"Ruta: **{r[0]} {r[1]}**", ""]
            md += [_doc(ast.get_docstring(n))]
    parametros = sorted(set(re.findall(r'params\("(\w+)"\)', texto)))
    return "\n".join(md), _resumen(modulo), rutas, _importados(arbol), parametros, (funciones, clases)


def _doc_js(rel: str, texto: str):
    cab = re.match(r"\s*/\*+\s*(.*?)\*/", texto, re.S)
    cabecera = " ".join(cab.group(1).split()) if cab else ""
    funcs = sorted(set(re.findall(r"^(?:async\s+)?function\s+(\w+)", texto, re.M)))
    md = [f"# `{rel}`", "", f"> {cabecera or '_sin comentario de cabecera_'}", "", "## Funciones", ""]
    md += [f"- `{f}`" for f in funcs] or ["_ninguna_"]
    return "\n".join(md), cabecera.split(". ")[0][:140], len(funcs)


def generar(raiz: Path = RAIZ) -> dict[str, str]:
    """-> {ruta relativa dentro de docs/codigo: contenido}"""
    docs: dict[str, str] = {}
    indice: dict[str, list] = {}
    rutas_api, imports, usan = [], Counter(), {}
    for fuente in _fuentes(raiz):
        rel, texto = _rel(fuente, raiz), fuente.read_text("utf-8")
        destino = _destino(rel)
        if fuente.suffix == ".js":
            md, resumen, n = _doc_js(rel, texto)
            info = f"{n} funciones"
        else:
            md, resumen, rutas, imps, parametros, (nf, nc) = _doc_py(rel, texto)
            info = f"{nc} clases, {nf} funciones"
            rama = rel.split("/")[1] if rel.startswith("src/") and rel.count("/") > 1 else None
            rutas_api += [(m, r, f, d, rel) for m, r, f, d in rutas]
            for i in imps:
                if rama and i.split(".")[1] != rama:
                    imports[(rama, i.split(".")[1])] += 1
            for p in parametros:
                usan.setdefault(p, []).append(rel)
        docs[destino] = md + "\n"
        carpeta = destino.split("/")[0] if "/" in destino else "(raiz)"
        indice.setdefault(carpeta, []).append((rel, destino, resumen, info))

    idx = ["# Documentacion del codigo", "",
           "Generada por `scripts/generar_docs_codigo.py` desde los docstrings, firmas e imports (no se edita a mano; "
           "`python scripts/generar_docs_codigo.py` la regenera y `dvc repro documentar_codigo` la deja registrada).", "",
           "Otras vistas: [dependencias entre ramas](dependencias.md) · [rutas de la API](api_rutas.md) · [parametros](parametros.md).", ""]
    for carpeta in sorted(indice):
        idx += [f"## {carpeta}", "", "| Archivo | Que hace | Contenido |", "|---|---|---|"]
        idx += [f"| [{rel}]({dest}) | {res} | {info} |" for rel, dest, res, info in indice[carpeta]]
        idx.append("")
    docs["INDICE.md"] = "\n".join(idx) + "\n"

    visibles = {a for a, _ in imports} | {b for _, b in imports}
    ramas = [r for r in _orden(raiz) if r in visibles] + sorted(visibles - set(_orden(raiz)))
    mat = ["# Dependencias entre ramas de `src/`", "",
           "Cada celda = cuantos imports hay desde la rama de la FILA hacia la rama de la COLUMNA. La regla del arbol "
           "(`tests/test_capas.py`): solo se importa del tronco o de ramas anteriores del pipeline, asi que todo cae bajo la diagonal.", "",
           "| desde \\ hacia | " + " | ".join(ramas) + " |", "|---|" + "---|" * len(ramas)]
    mat += [f"| **{a}** | " + " | ".join(str(imports.get((a, b), "")) for b in ramas) + " |" for a in ramas]
    docs["dependencias.md"] = "\n".join(mat) + "\n"

    api = ["# Rutas de la API", "", f"{len(rutas_api)} rutas. Detalle y docstring en el modulo de cada una.", "",
           "| Metodo | Ruta | Funcion | Que hace | Archivo |", "|---|---|---|---|---|"]
    api += [f"| {m} | `{r}` | `{f}` | {d} | {a} |" for m, r, f, d, a in sorted(rutas_api, key=lambda x: (x[1], x[0]))]
    docs["api_rutas.md"] = "\n".join(api) + "\n"

    par = ["# Parametros (`parameters/config.json`)", "", "Cada seccion de `parameters/config.json` y los modulos que la leen con `params(\"seccion\")`. "
           "La decision que la origina esta en `docs/decisiones/`.", "", "| Seccion | Usada en |", "|---|---|"]
    par += [f"| `{p}` | {', '.join(f'`{f}`' for f in sorted(set(fs)))} |" for p, fs in sorted(usan.items())]
    docs["parametros.md"] = "\n".join(par) + "\n"
    return docs


def escribir(salida: Path, docs: dict[str, str]) -> None:
    for rel, texto in docs.items():
        destino = salida / rel
        destino.parent.mkdir(parents=True, exist_ok=True)
        with open(destino, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(texto)
    for viejo in salida.rglob("*.md"):   # modulos que ya no existen
        if viejo.relative_to(salida).as_posix() not in docs:
            viejo.unlink()


def desactualizados(salida: Path, docs: dict[str, str]) -> list[str]:
    def leer(p: Path) -> str:
        return p.read_text("utf-8").replace("\r\n", "\n") if p.exists() else ""
    faltan = [r for r, t in docs.items() if leer(salida / r) != t]
    sobran = [p.relative_to(salida).as_posix() for p in salida.rglob("*.md") if p.relative_to(salida).as_posix() not in docs] if salida.exists() else []
    return sorted(faltan + sobran)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--revisar", action="store_true", help="no escribe: falla si docs/codigo esta desactualizada")
    a = ap.parse_args(argv)
    salida, docs = RAIZ / "docs" / "codigo", generar()
    if a.revisar:
        malos = desactualizados(salida, docs)
        print("docs/codigo al dia" if not malos else "desactualizados:\n  " + "\n  ".join(malos))
        return 1 if malos else 0
    escribir(salida, docs)
    print(f"docs/codigo: {len(docs)} archivos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
