# `src/etiquetado/manifest.py`

```text
Rutas e indice del dataset: que video es cual, que clips se exportaron (manifest.json) y de que ejercicio.

Lo comparten cortes, exportar, tablas y entrenamiento.
```

## `_slug`

`def _slug(vid: str) -> str`

```text
Identificador plano y unico para nombrar clips/preview de un video, a
partir de su ruta relativa a DATA (ej. 'sentadilla/2026-08-25/073012_serie.mp4'
-> 'sentadilla__2026-08-25__073012_serie'). Hace falta desde que DATA paso
a ser datos/grabaciones/ (anidada por ejercicio/fecha): el nombre pelado del
archivo ya no identifica un video sin ambiguedad -- dos grabaciones de
dias distintos pueden compartir el mismo HHMMSS_modo.mp4.
```

## `_ruta_video`

`def _ruta_video(vid: str) -> Path`

```text
Del identificador que maneja el panel (ruta relativa a DATA, ej.
'sentadilla/2026-08-25/073012_serie.mp4') al archivo real, validando que
no se escape de datos/grabaciones/ -- mismo criterio que src.sesion.grabacion.resolver_json.
```

## `_leer_json`

`def _leer_json(path, defecto)`

_sin docstring_

## `_manifest`

`def _manifest() -> list[dict]`

```text
manifest.json con 'exercise' y 'type' ya resueltos en cada fila (antes
se releia y completaba igual en 7 funciones distintas).
```

## `_tipo_o_primero`

`def _tipo_o_primero(tipo, rows=None)`

```text
El type pedido por el panel, o el del primer clip si no se paso.
```

## `_exercise_de`

`def _exercise_de(mp4_path)`

```text
El ejercicio del video (mismo nombre que su ejercicios/*.yaml),
leido del .json que graba GYMFITX -- de eso depende el 'type' en SQL y
que puntos le importan a table_kpoints (ver nucleo/ejercicio.puntos_de_ejercicio).
```

