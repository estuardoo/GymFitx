# `src/etiquetado/depurar.py`

```text
Quitar por completo un ejercicio archivado: manifest, cortes, seleccion de entrenamiento y SQL.

Archivar un ejercicio (Panel -> Rutina -> 🗑) saca su .yaml de ejercicios/; esto limpia el resto para que sus
clips ya no cuenten (entrenamiento, tablas, totales). Nada se borra en el disco: clips, grabaciones y plantilla
pasan a datos/archivados/<ejercicio>_<fecha>/ (recuperable). En SQL si se borra todo lo del 'type'; el numero del
type queda reservado en sql_tipos.json para no reutilizarlo. Es idempotente: si algo falla (SQL caido, un archivo
en uso) el ejercicio sigue figurando como pendiente y se reintenta.
```

## Constantes

`ARCHIVO_DIR`, `PENDIENTES_PATH`, `DEPURADOS_PATH`, `SIN_EJERCICIO`, `TABLAS_DEL_TIPO`

## `_leer`

`def _leer(path, defecto)`

_sin docstring_

## `_escribir`

`def _escribir(path, datos)`

_sin docstring_

## `_contar`

`def _contar(carpeta)`

_sin docstring_

## `_pendiente`

`def _pendiente(slug, si)`

_sin docstring_

## `_depurado`

`def _depurado(slug, si)`

_sin docstring_

## `huerfanos`

`def huerfanos()`

```text
Ejercicios que ya no estan en ejercicios/ pero aun dejan algo: clips en el manifest o en carpetas, una limpieza
pendiente, o datos en SQL (su type en sql_tipos.json, mientras no se haya depurado).
```

## `plan`

`def plan()`

```text
Que se quitaria de cada ejercicio archivado (para confirmar antes). sql_archivos=None si SQL no responde.
```

## `_purgar_sql`

`def _purgar_sql(tipo)`

_sin docstring_

## `depurar`

`def depurar(slug)`

```text
Deja el ejercicio 'slug' (ya archivado) fuera del manifest, los cortes, la seleccion y SQL.
```

## `depurar_todos`

`def depurar_todos(slugs=None)`

```text
Los ejercicios archivados que aun dejan datos (o solo los de 'slugs').
```

