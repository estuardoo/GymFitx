# `src/entrenamiento/descomposicion.py`

```text
Descomposicion: cada clip contra el clip 'base' de su ejercicio, punto por
punto (indicador tipo R2 con DTW, calculado en src/almacenamiento/dataset_sql.py).
```

## `_rows_de_tipo`

`def _rows_de_tipo(tipo)`

_sin docstring_

## `descomp_opciones`

`def descomp_opciones(tipo)`

```text
Para el panel: que clips hay por clase (base/bien/mal) y los kpoints de
este ejercicio -- en el mismo orden que su numero (point) real en
table_kpoints, para que 'K1, K2...' en la interfaz sea el mismo punto que
calcula el indicador. Si SQL no responde, cae al catalogo derivado del
.npz+definicion (mismo orden en la practica, pero no es la fuente de verdad).
```

## `descomp_analizar`

`def descomp_analizar(tipo, base, bien, mal, activos=None)`

```text
Series x(frame)/y(frame) por kpoint (solo los 'activos', para las
graficas) + el indicador de cada kpoint contra el 'base' (todos, para la
tabla-matriz) -- ver indicador() para la formula.
```

## `descomp_ranking`

`def descomp_ranking(tipo)`

```text
Ranking de TODOS los clips de este ejercicio contra su 'base', ya
autocalculado en table_indicator al generar/actualizar tablas SQL --
de mayor a menor KG (promedio de indicador entre kpoints). Ver
SQL.ranking_indicadores().
```

