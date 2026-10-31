# `src/entrenamiento/reportes.py`

```text
Etapa 6c: lo que queda de cada corrida en output/models/<ejercicio>/run_NNN/ (graficas, meta.json) y su listado.
```

## Constantes

`ENTR`, `UMBRAL_IGUAL`

## `_plt`

`def _plt()`

_sin docstring_

## `nueva_corrida`

`def nueva_corrida(ejercicio_id)`

```text
(numero, carpeta) de la proxima output/models/<ejercicio_id>/run_NNN/ (el numero cuenta por ejercicio).
```

## `dir_de`

`def dir_de(ejercicio_id, numero) -> str`

```text
Como se nombra una corrida para el panel y las rutas web: '1/run_001'.
```

## `grafico_comparacion`

`def grafico_comparacion(out, numero, resultados, linea_base, mejor)`

```text
Dispersion F1 macro (Y) vs Accuracy (X) de todos los modelos, con su nombre al lado -- arriba a la
derecha es mejor. Los que fallaron (sin 'accuracy') se listan aparte, no se pueden ubicar en el plano.
```

## `grafico_confusion`

`def grafico_confusion(out, numero, y, y_pred, clases, nombre)`

_sin docstring_

## `grafico_roc`

`def grafico_roc(out, numero, y, y_proba, clases, nombre)`

_sin docstring_

## `matriz_iteraciones`

`def matriz_iteraciones(numero, modelos)`

```text
Tabla de texto para el log: por modelo, F1 y cuantas iteraciones uso contra su tope ('frenó' = paró antes).
```

## `guardar_meta`

`def guardar_meta(out, meta)`

_sin docstring_

## `parametros`

`def parametros(m)`

```text
Lo que definio una corrida (para comparar). None = la corrida vieja no lo guardo.
```

## `_cambios`

`def _cambios(a, b)`

```text
Que parametros difieren entre la corrida anterior (a) y esta (b), en texto.
```

## `_ruido`

`def _ruido(m, previa)`

```text
Cuanto puede moverse el F1 solo por azar entre dos corridas: error estandar de cada una
(desviacion entre folds / raiz(k)) combinados. Sin datos de folds (corrida vieja) = solo el piso.
```

## `comparar`

`def comparar(m, previa)`

```text
Veredicto de la corrida m contra la anterior del mismo ejercicio: mejoro / empeoro / igual.
```

## `entrenamientos`

`def entrenamientos()`

```text
Todas las corridas, cada una con 'parametros', 'dir' y 'vs_anterior' (contra la corrida anterior del mismo
ejercicio; se calcula al leer, asi tambien sirve para corridas viejas). En orden cronologico.
```

