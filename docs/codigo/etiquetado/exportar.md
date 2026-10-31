# `src/etiquetado/exportar.py`

```text
Etapa 4: exportar cada segmento etiquetado como clip (.mp4 + .npz con sus kpoints) al disco y, si Sistema lo pide
(respaldo_sql.al_cortar), copiarlo a SQL.

Cada clip es una fila de la tabla `clips` (parameters/inputs.json) y vive en input/bronze/<ej>/<id>.{mp4,npz}. Un corte que ya
tenia clip (mismo video y numero de corte) conserva su id al volver a exportar. Salta los videos cuyos cortes no cambiaron
(hash por video en sistema/export_estado.json).
```

## Constantes

`ESTADO`, `_EXPORT_LOCK`, `PROGRESO`, `_CONTAR`

## `recorta_npz`

`def recorta_npz(src, ini, fin, dst)`

```text
Recorta values/t_ms del npz hermano al rango [ini,fin] en segundos.
Si el npz del video fuente ya trae keypoints crudos (points/point_names/
-- grabaciones nuevas de GYMFITX), los recorta igual y los copia al
clip: sin esto, table_frames/table_frames_fix en SQL quedaban siempre
vacias aunque el video fuente si tuviera los puntos.
```

## `_quitar_archivos`

`def _quitar_archivos(ej, cid)`

_sin docstring_

## `_hash`

`def _hash(segmentos, tiene_puntos=False)`

_sin docstring_

## `_npz_tiene_puntos`

`def _npz_tiene_puntos(mp4_path)`

```text
Sin correr deteccion: firma de los puntos crudos que YA trae el .npz
hermano ('' si no tiene). Si cambia el catalogo de puntos cambia la firma
y los clips se vuelven a recortar con los puntos nuevos.
```

## `_avanzar`

`def _avanzar(vid)`

_sin docstring_

## `_videos_a_cortar`

`def _videos_a_cortar(labels)`

_sin docstring_

## `exportar`

`def exportar(labels, todo=False, subir_sql=None)`

```text
Un solo export a la vez: dos clics seguidos (o 'Generar cortes' + 'Generar
tablas') corrian en paralelo e insertaban el mismo clip dos veces en SQL
(UNIQUE KEY UQ_table_file_type_archivo, visto en cortador.log).
```

## `_planear`

`def _planear(vid, segs, exercise)`

```text
Dentro de la tabla: un clip por corte bien/mal (reusa el id del corte que ya tenia) y fuera los que sobran.
-> (ej, [(seg, clip_row)], ids_sobrantes) o None si el video no esta en la tabla `raw`.
```

## `_exportar`

`def _exportar(labels, todo, subir_sql)`

_sin docstring_

## `estado_export`

`def estado_export()`

_sin docstring_

## `sql_generar`

`def sql_generar()`

```text
Boton manual de Sistema → Tablas del dataset. No lee la tabla de clips y ya -- eso solo
veria los clips como quedaron la ULTIMA vez que se corto, y un clip
cortado antes de tener deteccion de puntos se quedaria "omitido_sin_puntos"
para siempre por mas veces que le des click. Por eso reusa exportar():
si a un video le faltan puntos los detecta y re-recorta antes de subir a
SQL (exportar ya se salta los que no cambiaron, via el hash).
```

