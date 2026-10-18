# `src/preparacion/etapas.py`

```text
Las 5 tareas de la etapa 3 de CRISP-DM como etapas ejecutables (las llama dvc.yaml, una por ejercicio):

    python -m src.preparacion.etapas <seleccionar|limpiar|construir|integrar|formatear|todo> <ejercicio>

    3.1 seleccionar  qué clips entran y por qué los que no          -> reportes/seleccion_<ej>.json
    3.2 limpiar      calidad de cada clip contra params.yaml        -> reportes/limpieza_<ej>.json|.md
    3.3 construir    variables derivadas (angulos/proporciones) y registros generados (ventanas "fuera")
    3.4 integrar     une clip + clase + grabacion de origen (grupo para la validacion)
    3.5 formatear    normaliza, remuestrea y aplana -> datos/final/<ej>/X.npy + docs/diccionario/<ej>.csv|.md

Cada etapa lee la salida de la anterior desde datos/intermedio/<ej>/ (nada en memoria entre etapas), asi dvc puede
saltarse las que no cambiaron. Salidas deterministas: sin fechas, sin aleatoriedad.
```

## Constantes

`ETAPAS`

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

_sin docstring_

## `integrar`

`def integrar(ejercicio: str) -> dict`

_sin docstring_

## `formatear`

`def formatear(ejercicio: str) -> dict`

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

