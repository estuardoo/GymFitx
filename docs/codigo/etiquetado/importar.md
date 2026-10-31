# `src/etiquetado/importar.py`

```text
Subir clips ya cortados (bien / mal) a un ejercicio, sin pasar por grabacion + etiquetado.

Cada clip queda como si lo hubiera exportado el panel: una fila en la tabla `clips` (parameters/inputs.json, etiqueta 1/0 y
persona si se sabe) y sus archivos input/bronze/<n del ejercicio>/<id>.mp4 + .npz con los puntos del catalogo. Si el SQL
Server responde, registro en SQL (poblar_desde_manifest); si no, el clip queda local y "Sistema -> Generar tablas" lo sube
despues. Un clip sin video fuente (raw_id vacio) lleva su propia persona.
```

## Constantes

`CLASES`, `_VIDEO`, `PROGRESO`

## `_nombre`

`def _nombre(original: str) -> str`

_sin docstring_

## `_duracion`

`def _duracion(mp4: Path) -> float`

_sin docstring_

## `_quitar_clip`

`def _quitar_clip(row)`

_sin docstring_

## `_fila`

`def _fila(cid)`

_sin docstring_

## `_una`

`def _una(slug, clase, nombre_original, src: Path, extras=None)`

```text
Un archivo: transcodifica, detecta puntos, registra el clip y devuelve su fila (o lanza).
```

## `importar_clips`

`def importar_clips(slug, clase, archivos, reemplazar=False, avance=None)`

```text
archivos: [(nombre_original, ruta_temporal[, extras])]; extras (persona, vista, fecha...) van a la fila del clip.
`reemplazar` ya no hace nada (no hay clip base que reemplazar). Devuelve {"ok": [clips], "errores": [str],
"sql": resumen|None, "sql_error": str|None}.
```

## `guardar_subidas`

`def guardar_subidas(subidas)`

```text
[(nombre, file-like)] -> (carpeta temporal a cerrar, [(nombre, ruta)]).
```

## `_natural`

`def _natural(txt)`

_sin docstring_

## `listar_carpeta`

`def listar_carpeta(carpeta)`

```text
[(clase, nombre, ruta, extras)] ordenado por clase, persona (P1, P2, ... P10) y nombre.
```

## `_unir`

`def _unir(clips, destino)`

```text
Concatena mp4 (mismo origen, mismos parametros) en uno solo: copia directa; si no cuadra, re-codifica.
```

## `_npz_unido`

`def _npz_unido(clips, durs, destino)`

```text
npz del video reconstruido = los puntos de cada clip, uno detras de otro con su tiempo desplazado (no se
vuelve a detectar). Sin 'points' en algun clip no hay npz (el panel lo detecta al exportar).
```

## `_clip_de`

`def _clip_de(t, clase, nombre, persona)`

```text
Fila de `clips` importada con ese nombre y clase (la de esa persona, o la que aun no tiene persona).
```

## `reconstruir_originales`

`def reconstruir_originales(slug, carpeta)`

```text
Con el indice.csv de la carpeta (video_origen, inicio_s...) arma, por cada video original, UN video con sus
clips unidos en orden (los tramos entre cortes no existen: el original no se tiene), lo deja en
input/raw/<n>/<id>.mp4 con su .npz/.json, registra sus cortes en la tabla `raw` (pestana Cut/Edit) y apunta los
clips a el. Agrega al indice.csv video_reconstruido / ini_rec_s / fin_rec_s. Repetible: lo ya reconstruido se salta.
```

## `_ya_importados`

`def _ya_importados(slug)`

```text
Claves (clase, nombre, persona) de los clips ya importados de este ejercicio.
```

## `_asignar_personas`

`def _asignar_personas(slug, todos)`

```text
Un clip importado antes SIN persona que ahora aparece en la carpeta con persona la recibe (en vez de duplicarse).
```

## `importar_carpeta`

`def importar_carpeta(slug, carpeta, reemplazar_base=True)`

```text
Importa una carpeta entera, incremental: lo que ya esta importado (misma clase, nombre y persona) se salta, asi que
repetirlo solo suma lo nuevo; los ya importados sin persona reciben la de la carpeta. Devuelve
{"ok", "saltados", "errores", "sql_error", "por_clase", "personas_asignadas"}.
```

## `iniciar_carpeta`

`def iniciar_carpeta(slug, carpeta)`

```text
Lanza importar_carpeta en un hilo (son minutos: re-codifica y detecta puntos clip por clip).
El avance se lee de PROGRESO; al terminar queda el resultado ahi.
```

