# `src/etiquetado/importar.py`

```text
Subir clips ya cortados (bien / mal / base) a un ejercicio, sin pasar por grabacion + etiquetado.

Cada clip queda como si lo hubiera exportado el panel: datos/clips/<ejercicio>/<clase>/<nombre>.mp4
+ .npz con los puntos del catalogo, fila en manifest.json y, si el SQL Server responde, registro en
SQL (poblar_desde_manifest). Si SQL no responde el clip queda local y "Sistema -> Generar tablas"
lo sube despues (estas filas tienen 'origen' fuera de labels, exportar() las conserva).
```

## Constantes

`CLASES`, `_VIDEO`, `PROGRESO`

## `_nombre`

`def _nombre(original: str) -> str`

_sin docstring_

## `_unico`

`def _unico(carpeta: Path, stem: str) -> str`

_sin docstring_

## `_duracion`

`def _duracion(mp4: Path) -> float`

_sin docstring_

## `_quitar_clip`

`def _quitar_clip(row)`

_sin docstring_

## `_borrar_en_sql`

`def _borrar_en_sql(type_, archivo)`

```text
Quita un clip de SQL (indicadores, frames, fila); los indicadores se recalculan al registrar el nuevo.
```

## `_una`

`def _una(slug, clase, nombre_original, src: Path)`

```text
Un archivo: transcodifica, detecta puntos, devuelve la fila de manifest (o lanza).
```

## `importar_clips`

`def importar_clips(slug, clase, archivos, reemplazar=False, avance=None)`

```text
archivos: [(nombre_original, ruta_temporal[, extras])]; extras (persona, vista, fecha...) van a la fila del manifest. Devuelve {"ok": [clips], "errores": [str],
"sql": resumen|None, "sql_error": str|None, "base_reemplazada": bool}.
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

## `reconstruir_originales`

`def reconstruir_originales(slug, carpeta)`

```text
Con el indice.csv de la carpeta (video_origen, inicio_s...) arma, por cada video original, UN video con sus
clips unidos en orden (los tramos entre cortes no existen: el original no se tiene), lo deja en
datos/grabaciones/<slug>/<fecha>/<persona>_<origen>.mp4 con su .npz/.json, registra sus cortes en
etiquetas.json (pestana Cut/Edit) y apunta los clips del manifest a el. Agrega al indice.csv
video_reconstruido / ini_rec_s / fin_rec_s. Repetible: lo ya reconstruido se salta.
```

## `importar_carpeta`

`def importar_carpeta(slug, carpeta, reemplazar_base=True)`

```text
Importa una carpeta entera, incremental: lo que ya esta en datos/clips/<slug>/<clase>/ se salta, asi que
repetirlo solo suma lo nuevo. Devuelve {"ok", "saltados", "errores", "sql_error", "por_clase"}.
```

## `iniciar_carpeta`

`def iniciar_carpeta(slug, carpeta)`

```text
Lanza importar_carpeta en un hilo (son minutos: re-codifica y detecta puntos clip por clip).
El avance se lee de PROGRESO; al terminar queda el resultado ahi.
```

