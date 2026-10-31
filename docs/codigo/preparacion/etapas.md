# `src/preparacion/etapas.py`

```text
Las 5 tareas de la etapa 3 de CRISP-DM como etapas ejecutables (las llama dvc.yaml, una por ejercicio):

    python -m src.preparacion.etapas <seleccionar|limpiar|construir|integrar|formatear|todo> <ejercicio>

    3.1 seleccionar  qué clips entran y por qué los que no          -> output/reportes/<n>/seleccion.json
    3.2 limpiar      calidad de cada clip contra parameters/config.json -> output/reportes/<n>/limpieza.json|.md
    3.3 construir    variables derivadas (angulos/proporciones) y registros generados (ventanas "fuera") -> input/plate/<n>/
    3.4 integrar     une clip + clase + grabacion de origen (grupo para la validacion)
    3.5 formatear    normaliza, remuestrea y aplana: un vector por clip -> input/gold/<n>/<id>.npy + docs/diccionario/<ej>.csv|.md

<n> es el numero del ejercicio (parameters/exercise.json) y <id> el del clip: bronze, plate y gold comparten numeracion.
Cada etapa lee la salida de la anterior desde input/plate/<n>/ (nada en memoria entre etapas), asi dvc puede
saltarse las que no cambiaron. Salidas deterministas: sin fechas, sin aleatoriedad.
```

## Constantes

`ETAPAS`

## `_plate`

`def _plate(ejercicio)`

_sin docstring_

## `_gold`

`def _gold(ejercicio)`

_sin docstring_

## `_json_w`

`def _json_w(ruta, obj) -> None`

_sin docstring_

## `_json_r`

`def _json_r(ruta)`

_sin docstring_

## `seleccionar`

`def seleccionar(ejercicio: str) -> list[dict]`

_sin docstring_

## `limpiar`

`def limpiar(ejercicio: str) -> dict`

_sin docstring_

## `construir`

`def construir(ejercicio: str) -> int`

```text
Escribe en input/plate/<n>/ los puntos (<id>.p.npy) y angulos (<id>.a.npy) de cada clip limpio, y los de las ventanas
"fuera" generadas (f000001...). construido.json = registro de lo escrito.
```

## `integrar`

`def integrar(ejercicio: str) -> dict`

_sin docstring_

## `_subir_sql`

`def _subir_sql(ejercicio: str) -> dict`

```text
Copia la tabla normalizada a SQL (table_frames_fix; guia_fix = la formula). Sin conexion queda pendiente: el siguiente
respaldo (cortar / entrenar / «Copiar ahora») la sube porque la guia de esos clips ya no coincide. Nunca lanza.
```

## `formatear`

`def formatear(ejercicio: str, subir_sql: bool=True) -> dict`

_sin docstring_

## `todo`

`def todo(ejercicio: str) -> dict`

```text
Las 5 etapas seguidas (boton «Generar documentacion» de Sistema).
```

## `_resumen`

`def _resumen(r)`

_sin docstring_

## `main`

`def main(argv=None) -> None`

_sin docstring_

