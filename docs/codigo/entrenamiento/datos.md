# `src/entrenamiento/datos.py`

```text
Etapa 6a: que clips entran al entrenamiento (seleccion manual) y armar X / y desde SQL.
```

## Constantes

`CLASES_NO_ENTRENABLES`

## `guardar_seleccion`

`def guardar_seleccion(cambios, tipo=None)`

```text
cambios: {clip: bool}. Se guarda en la tabla `clips` (campo `usar`); por defecto todo clip nuevo SI se usa.
Espejo en SQL (table_file.usar) si responde.
```

## `clips_entrenamiento`

`def clips_entrenamiento(tipo=None)`

```text
Para la tabla 'Clips para entrenar': todos los clips del manifest de
este type con su clase y si estan marcados para usarse.
```

## `armar`

`def armar(rows, tipo, features, tipos=None, vectores=None, personas=None)`

```text
X, y (clase) y clips de este type, mas lo que se dejo afuera y por que. `vectores` = {clip: vector} armado desde
el disco (src/preparacion/etapas.py, lo normal); sin el se leen de table_frames_fix en SQL. `personas` = lista de
personas (P1, P2...) que entran; None = todas. ValueError con un mensaje para el panel si no alcanza para entrenar.
```

