# `src/nucleo/definicion.py`

```text
Definicion de cada ejercicio: UNA sola fuente, parameters/ (antes ejercicios/<slug>.yaml + un espejo numerado).

    parameters/exercise.json       numero -> nombre, slug, fuente (source), sql_tipo, activo
    parameters/<n>/kpoints.json    los puntos del ejercicio
    parameters/<n>/angles.json     angulos / proporciones (features, con 'activo')
    parameters/<n>/guide.json      el resto: description, segmentation, signal, reglas, base_clip, clasificador...

leer() junta todo en el dict de siempre ({name, description, source, features, kpoints, ...}); guardar() lo reparte.
Un ejercicio archivado queda con su numero (reservado) pero inactivo: ya no aparece en slugs().
```

## Constantes

`SCHEMA`, `_APARTE`

## `_dir`

`def _dir(ej: int) -> Path`

_sin docstring_

## `_json`

`def _json(p: Path, defecto=None)`

_sin docstring_

## `_fila`

`def _fila(slug: str) -> tuple[int, dict] | None`

_sin docstring_

## `slugs`

`def slugs() -> list[str]`

```text
Ejercicios activos que tienen definicion.
```

## `existe`

`def existe(slug: str) -> bool`

_sin docstring_

## `leer`

`def leer(slug: str) -> dict | None`

```text
La definicion completa del ejercicio (None si no existe).
```

## `_escribir`

`def _escribir(ruta: Path, obj) -> None`

_sin docstring_

## `guardar`

`def guardar(slug: str, data: dict) -> int`

```text
Escribe la definicion completa; guarda antes una copia de la anterior en sistema/respaldos/. -> numero del ejercicio.
```

## `archivar`

`def archivar(slug: str) -> None`

```text
Lo saca de la lista (sigue con su numero y sus archivos; crear otro con el mismo nombre lo reactiva).
```

