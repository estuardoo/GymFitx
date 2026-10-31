# `src/interfaz/api/entrenamiento.py`

```text
API de entrenamiento: clips a usar, entrenar, corridas, modelos y descomposicion.

Rutas sync ("def", no "async def"): FastAPI las corre en su threadpool, asi
que cortar/entrenar (CPU) no bloquea el websocket ni el video de la camara.
```

## `dataset_entrenar_clips`

`def dataset_entrenar_clips(tipo: str | None=None)`

Ruta: **GET /api/entrenar/clips**

_sin docstring_

## `dataset_entrenamientos`

`def dataset_entrenamientos()`

Ruta: **GET /api/entrenamientos**

_sin docstring_

## `dataset_modelos`

`def dataset_modelos()`

Ruta: **GET /api/modelos**

_sin docstring_

## `modelos_matriz`

`def modelos_matriz()`

Ruta: **GET /api/modelos/matriz**

```text
epocas / max_iter / parar de cada modelo que itera (la matriz de src/nucleo/config.py + lo guardado).
```

## `modelos_matriz_guardar`

`def modelos_matriz_guardar(body: dict)`

Ruta: **POST /api/modelos/matriz**

_sin docstring_

## class `EntrenarPedido`

_sin docstring_

## class `SeleccionPedido`

_sin docstring_

## `dataset_entrenar`

`def dataset_entrenar(body: EntrenarPedido)`

Ruta: **POST /api/entrenar**

_sin docstring_

## `dataset_entrenar_seleccion`

`def dataset_entrenar_seleccion(body: SeleccionPedido)`

Ruta: **POST /api/entrenar/seleccion**

_sin docstring_

## `dataset_descomp_opciones`

`def dataset_descomp_opciones(body: dict)`

Ruta: **POST /api/descomp/opciones**

_sin docstring_

## `dataset_descomp_analizar`

`def dataset_descomp_analizar(body: dict)`

Ruta: **POST /api/descomp/analizar**

_sin docstring_

## `dataset_descomp_ranking`

`def dataset_descomp_ranking(body: dict)`

Ruta: **POST /api/descomp/ranking**

_sin docstring_

