# `src/preparacion/documentar.py`

```text
Documentos que genera el pipeline (nunca a mano, para que no se desincronicen):
  - diccionario de datos: una fila por columna de la tabla final -> docs/diccionario/<ej>.csv y .md
  - informe de limpieza en Markdown -> reportes/<n>/limpieza.md (el .json lo escribe la etapa limpiar)
Sin marcas de tiempo ni nada que cambie de una corrida a otra: mismas entradas, mismos bytes.
```

## Constantes

`UNIDAD`

## `_escribir`

`def _escribir(ruta, texto: str) -> None`

_sin docstring_

## `columnas`

`def columnas(spec: dict, nombres: list[str]) -> list[dict]`

```text
Las columnas del vector, en el MISMO orden que `vectorizar.aplanar`: por cuadro, primero x/y/z de cada kpoint y
luego las metricas activas (angulos / proporciones). `nombres` = kpoints que traen los clips (el orden del vector).
```

## `escribir_diccionario`

`def escribir_diccionario(ejercicio: str, spec: dict, filas: list[dict], n_features: int) -> None`

```text
CSV + Markdown. Falla si las columnas descritas no son exactamente las de la tabla final (criterio: 100 %).
```

## `ruta_reporte`

`def ruta_reporte(ejercicio: str, nombre: str)`

```text
output/reportes/<n>/<nombre>: los informes de un ejercicio, en su carpeta numerada.
```

## `escribir_limpieza_md`

`def escribir_limpieza_md(inf: dict) -> None`

_sin docstring_

