# `src/etiquetado/tablas.py`

```text
Etapa 5: llevar los clips exportados a las tablas SQL (crudo, normalizado e indicador vs base).

Aqui esta la logica; almacenamiento/dataset_sql.py solo guarda y lee.
```

## Constantes

`RESUMEN_VACIO`

## `cfg_de_tipo`

`def cfg_de_tipo(type_, point_names)`

```text
Normalizacion efectiva del type: la del ejercicio (Kpoints -> Normalizacion, parameters/<n>/guide.json).
Es la MISMA con la que entrena el modelo, asi la copia en SQL no diverge del disco.
```

## `poblar_desde_manifest`

`def poblar_desde_manifest(manifest_rows, dataset_dir, type_=1)`

```text
Por cada clip del manifest con .npz que ya trae 'points': registra el
archivo, el catalogo de puntos (una vez) y sus frames crudos y normalizados.
Si la 'guia' (parametros de normalizacion + firma de puntos) no cambio para
un archivo que ya tiene datos, se deja tal cual. Al final recalcula
table_indicator contra el clip 'base'.
```

## `respaldar_sql`

`def respaldar_sql(rows)`

```text
Copia a SQL Server los clips que ya estan en disco (el disco manda; SQL es respaldo y alimenta Descomposicion /
Ranking). -> {"resumen": contadores | None, "error": texto | None}. Nunca lanza: si SQL no responde solo lo cuenta.
```

## `_actualizar_indicadores`

`def _actualizar_indicadores(cx, type_)`

```text
table_indicator de cada clip contra el clip 'base' de su type. La llave
(archivo base + su guia_fix + version del DTW) evita recalcular lo que no cambio.
```

## `catalogo_puntos_disponible`

`def catalogo_puntos_disponible(manifest_rows, dataset_dir)`

```text
Nombres de puntos del primer clip que ya tenga 'points', filtrados por
la definicion de su ejercicio -- para los <select> del panel sin conectarse a SQL.
```

## `sql_estado`

`def sql_estado(tipo=None)`

```text
Para Sistema → Tablas del dataset: conexion + puntos disponibles + config del ejercicio
('tipo') elegido en el selector (antes siempre el del primer clip).
```

## `tipos_disponibles`

`def tipos_disponibles()`

_sin docstring_

