# `src/evaluacion/comparadores/dtw.py`

```text
Capa 6: comparacion de una repeticion contra la plantilla.

Dos decisiones que definen la calidad del resultado:

1. z-score por feature contra mu/sigma de la plantilla. Sin esto los angulos
   (rango 0-180) aplastarian a las razones de distancia (rango 0-2) en la
   distancia total, y una falla del meñique casi no moveria el puntaje.
2. DTW con banda de Sakoe-Chiba. Alinea en el tiempo dos ejecuciones a
   velocidades distintas (hacerlo mas lento no es hacerlo mal), y la banda
   ademas impide alineamientos degenerados donde un solo cuadro se estira
   sobre media repeticion.
```

## Constantes

`INF`

## `zscore`

`def zscore(data: np.ndarray, mu: np.ndarray, sigma: np.ndarray) -> np.ndarray`

_sin docstring_

## `cost_matrix`

`def cost_matrix(A: np.ndarray, B: np.ndarray) -> np.ndarray`

```text
(T,S) distancia media absoluta por par de cuadros, ignorando NaN.
```

## `dtw_band`

`def dtw_band(C: np.ndarray, radius_frac: float=0.15) -> tuple[float, list[tuple[int, int]]]`

```text
DTW sobre la matriz de costos, restringido a una banda diagonal.

Devuelve (costo medio por paso, camino). El costo se divide por la
longitud del camino para que no dependa de cuantos cuadros duro la rep.
```

## `compare`

`def compare(segment: Segment, template) -> Score`

```text
Repeticion vs plantilla -> Score 0-100 con desglose por feature.
```

## `pairwise_errors`

`def pairwise_errors(reps: list[np.ndarray], mu, sigma, radius_frac: float) -> np.ndarray`

```text
Matriz (n,n) de error DTW entre repeticiones. Base de la autocalibracion.
```

