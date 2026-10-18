# `src/entrenamiento/datos.py`

```text
Etapa 6a: que clips entran al entrenamiento (seleccion manual) y armar X / y desde SQL.
```

## Constantes

`SELECCION`, `CLASES_NO_ENTRENABLES`

## `guardar_seleccion`

`def guardar_seleccion(cambios, tipo=None)`

```text
cambios: {clip: bool}. Se guarda solo lo que se excluye (por defecto,
todo clip nuevo SI se usa). Espejo en SQL (table_file.usar) si responde.
```

## `clips_entrenamiento`

`def clips_entrenamiento(tipo=None)`

```text
Para la tabla 'Clips para entrenar': todos los clips del manifest de
este type con su clase y si estan marcados para usarse.
```

## `armar`

`def armar(rows, tipo, features, tipos=None, vectores=None)`

```text
X, y (clase) y clips de este type, mas lo que se dejo afuera y por que. `vectores` = {clip: vector} armado desde
el disco (src/preparacion/etapas.py, lo normal); sin el se leen de table_frames_fix en SQL. ValueError con un
mensaje para el panel si no alcanza para entrenar.
```

