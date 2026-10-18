# `src/interfaz/api/etiquetado.py`

```text
API de etiquetado: videos para cortar, etiquetas, overlay de puntos, exportar clips, tablas SQL y editor de puntos.

Rutas sync ("def", no "async def"): FastAPI las corre en su threadpool, asi
que cortar/entrenar (CPU) no bloquea el websocket ni el video de la camara.
```

## `dataset_data`

`def dataset_data(name: str)`

Ruta: **GET /data/{name:path}**

_sin docstring_

## `dataset_config`

`def dataset_config()`

Ruta: **GET /api/config**

_sin docstring_

## `dataset_labels_get`

`def dataset_labels_get()`

Ruta: **GET /api/labels**

_sin docstring_

## `dataset_labels_post`

`def dataset_labels_post(body: dict)`

Ruta: **POST /api/labels**

_sin docstring_

## `dataset_overlay`

`def dataset_overlay(file: str)`

Ruta: **GET /api/overlay**

_sin docstring_

## `dataset_export_estado`

`def dataset_export_estado()`

Ruta: **GET /api/export_estado**

_sin docstring_

## `dataset_export_progreso`

`def dataset_export_progreso()`

Ruta: **GET /api/export_progreso**

_sin docstring_

## `dataset_export`

`def dataset_export(body: dict, todo: bool=False)`

Ruta: **POST /api/export**

_sin docstring_

## `dataset_tipos`

`def dataset_tipos()`

Ruta: **GET /api/tipos**

_sin docstring_

## `dataset_sql_estado`

`def dataset_sql_estado(tipo: str | None=None)`

Ruta: **GET /api/sql/estado**

_sin docstring_

## `dataset_sql_config`

`def dataset_sql_config(body: dict, tipo: str | None=None)`

Ruta: **POST /api/sql/config**

_sin docstring_

## `dataset_sql_blanquear`

`def dataset_sql_blanquear()`

Ruta: **POST /api/sql/blanquear**

_sin docstring_

## `dataset_sql_generar`

`def dataset_sql_generar()`

Ruta: **POST /api/sql/generar**

_sin docstring_

## `dataset_puntos_ejercicios`

`def dataset_puntos_ejercicios()`

Ruta: **GET /api/puntos/ejercicios**

_sin docstring_

## `dataset_puntos_tipos`

`def dataset_puntos_tipos()`

Ruta: **GET /api/puntos/tipos**

_sin docstring_

## `_figura_png`

`def _figura_png() -> bytes`

```text
El mismo esqueleto del video (sesion/overlay.py) sobre el catalogo de puntos, de fondo del diagrama.
```

## `dataset_puntos_figura`

`def dataset_puntos_figura()`

Ruta: **GET /api/puntos/figura.png**

_sin docstring_

## `dataset_puntos_catalogo`

`def dataset_puntos_catalogo(source: str='pose')`

Ruta: **GET /api/puntos/catalogo**

_sin docstring_

## `dataset_puntos_yaml_get`

`def dataset_puntos_yaml_get(ejercicio: str='')`

Ruta: **GET /api/puntos/yaml**

_sin docstring_

## `dataset_puntos_crear`

`def dataset_puntos_crear(body: dict)`

Ruta: **POST /api/puntos/crear**

_sin docstring_

## `dataset_puntos_sincronizar`

`def dataset_puntos_sincronizar(ejercicio: str='')`

Ruta: **GET /api/puntos/sincronizar**

_sin docstring_

## `dataset_puntos_modificar`

`def dataset_puntos_modificar(body: dict)`

Ruta: **POST /api/puntos/modificar**

_sin docstring_

## `dataset_puntos_eliminar`

`def dataset_puntos_eliminar(body: dict)`

Ruta: **POST /api/puntos/eliminar**

_sin docstring_

## `archivados_plan`

`def archivados_plan()`

Ruta: **GET /api/archivados/plan**

```text
Ejercicios archivados que aun dejan clips o datos en SQL (lo que quitaria el boton de Sistema).
```

## `archivados_depurar`

`def archivados_depurar(body: dict)`

Ruta: **POST /api/archivados/depurar**

_sin docstring_

## `ejercicio_base_clip`

`def ejercicio_base_clip(body: dict)`

Ruta: **POST /api/ejercicio/base-clip**

```text
Rehace la base del ejercicio desde un clip (por defecto el primero de 'bien'). Reinicia la camara para tomarla.
```

## `dataset_puntos_reglas`

`def dataset_puntos_reglas(body: dict)`

Ruta: **POST /api/puntos/reglas**

_sin docstring_

## `dataset_puntos_yaml_post`

`def dataset_puntos_yaml_post(body: dict)`

Ruta: **POST /api/puntos/yaml**

_sin docstring_

## `ejercicio_clips`

`def ejercicio_clips(slug: str)`

Ruta: **GET /api/ejercicio/clips**

```text
Cuantos clips bien/mal/base tiene el ejercicio (para el dialogo de subida).
```

## `ejercicio_importar_carpeta`

`def ejercicio_importar_carpeta(body: dict)`

Ruta: **POST /api/ejercicio/clips/carpeta**

```text
Importa una carpeta Base/Bien/Mal/P1..Pn del disco del servidor (segundo plano; avance en .../progreso).
```

## `ejercicio_importar_progreso`

`def ejercicio_importar_progreso()`

Ruta: **GET /api/ejercicio/clips/carpeta/progreso**

_sin docstring_

## `_subir_clips`

`def _subir_clips(slug, clase, reemplazar, archivos)`

_sin docstring_

