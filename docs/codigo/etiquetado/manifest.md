# `src/etiquetado/manifest.py`

```text
Rutas e indice del dataset: que video es cual, que clips se exportaron (tabla `clips` de parameters/inputs.json) y de que
ejercicio. Lo comparten cortes, exportar, tablas y entrenamiento.
```

## `_slug`

`def _slug(vid: str) -> str`

```text
Identificador plano y unico de un video, a partir de su ruta relativa a DATA
(ej. '1/000007.mp4' -> '1__000007'): sirve de nombre para sus previews.
```

## `_ruta_video`

`def _ruta_video(vid: str) -> Path`

```text
Del identificador que maneja el panel (ruta relativa a DATA, ej.
'1/000007.mp4') al archivo real, validando que
no se escape de input/raw/ -- mismo criterio que src.sesion.grabacion.resolver_json.
```

## `_leer_json`

`def _leer_json(path, defecto)`

_sin docstring_

## `_manifest`

`def _manifest() -> list[dict]`

```text
Los clips (tabla `clips`) con 'exercise' y 'type' ya resueltos en cada fila.
```

## `_tipo_o_primero`

`def _tipo_o_primero(tipo, rows=None)`

```text
El type pedido por el panel, o el del primer clip si no se paso.
```

## `_exercise_de`

`def _exercise_de(mp4_path)`

```text
El ejercicio del video: su carpeta es el numero (input/raw/<n>/), que exercise.json traduce a nombre. Si el video
esta fuera de esa estructura se lee del .json que graba GYMFITX.
```

