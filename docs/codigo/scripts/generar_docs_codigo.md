# `scripts/generar_docs_codigo.py`

```text
Genera docs/codigo/: la documentacion de TODO el codigo, leida del propio codigo (docstrings, firmas, rutas, imports,
parametros) para que nunca quede desactualizada. Solo libreria estandar.

    python scripts/generar_docs_codigo.py            # reescribe docs/codigo/
    python scripts/generar_docs_codigo.py --revisar  # no escribe: sale con error si docs/codigo/ esta desactualizada

Salida (sin fechas: mismas fuentes, mismos bytes):
    INDICE.md            que hay en cada rama y modulo
    dependencias.md      matriz de quien importa a quien (el arbol de capas)
    api_rutas.md         todas las rutas REST/WebSocket
    parametros.md        cada clave de params.yaml y los modulos que la usan
    <rama>/<modulo>.md   clases, funciones y constantes con su docstring (src/), scripts/ y la web (js)
```

## Constantes

`RAIZ`, `METODOS`

## `_orden`

`def _orden(raiz: Path) -> list[str]`

```text
El ORDEN de ramas de tests/test_capas.py (unica fuente de la regla del arbol).
```

## `_fuentes`

`def _fuentes(raiz: Path) -> list[Path]`

_sin docstring_

## `_rel`

`def _rel(p: Path, raiz: Path) -> str`

_sin docstring_

## `_destino`

`def _destino(rel: str) -> str`

```text
src/nucleo/config.py -> nucleo/config.md · scripts/x.py -> scripts/x.md · .../web/js/a.js -> web/js/a.md
```

## `_firma`

`def _firma(n: ast.AST) -> str`

_sin docstring_

## `_doc`

`def _doc(texto: str | None) -> str`

_sin docstring_

## `_resumen`

`def _resumen(texto: str | None) -> str`

_sin docstring_

## `_ruta_de`

`def _ruta_de(dec: ast.AST) -> tuple[str, str] | None`

```text
@router.get("/api/x") -> ("GET", "/api/x")
```

## `_importados`

`def _importados(arbol: ast.AST) -> list[str]`

_sin docstring_

## `_doc_py`

`def _doc_py(rel: str, texto: str)`

```text
-> (markdown, resumen, rutas, imports, parametros usados)
```

## `_doc_js`

`def _doc_js(rel: str, texto: str)`

_sin docstring_

## `generar`

`def generar(raiz: Path=RAIZ) -> dict[str, str]`

```text
-> {ruta relativa dentro de docs/codigo: contenido}
```

## `escribir`

`def escribir(salida: Path, docs: dict[str, str]) -> None`

_sin docstring_

## `desactualizados`

`def desactualizados(salida: Path, docs: dict[str, str]) -> list[str]`

_sin docstring_

## `main`

`def main(argv=None) -> int`

_sin docstring_

