# `src/etiquetado/exportar.py`

```text
Etapa 4: exportar cada segmento etiquetado como clip (.mp4 + .npz con sus kpoints) al disco y, si Sistema lo pide
(respaldo_sql.al_cortar), copiarlo a SQL.

Salta los videos cuyos cortes no cambiaron (hash por video en export_estado.json).
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

## `limpiar_previos`

`def limpiar_previos(labels)`

```text
Borra los clips ya exportados de estos videos antes de recortar de nuevo (evita huerfanos si cambiaste la cantidad o clase de los cortes).
```

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

## `_exportar`

`def _exportar(labels, todo, subir_sql)`

_sin docstring_

## `estado_export`

`def estado_export()`

_sin docstring_

## `sql_generar`

`def sql_generar()`

```text
Boton manual de Sistema → Tablas del dataset. No lee manifest.json y ya -- eso solo
veria los clips como quedaron la ULTIMA vez que se corto, y un clip
cortado antes de tener deteccion de puntos se quedaria "omitido_sin_puntos"
para siempre por mas veces que le des click. Por eso reusa exportar():
si a un video le faltan puntos los detecta y re-recorta antes de subir a
SQL (exportar ya se salta los que no cambiaron, via el hash).
```

