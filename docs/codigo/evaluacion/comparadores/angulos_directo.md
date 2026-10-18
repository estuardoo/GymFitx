# `src/evaluacion/comparadores/angulos_directo.py`

```text
Comparador sin DTW: remuestrea la repeticion al largo de la plantilla y compara cuadro a cuadro.

Sirve de control para medir cuanto aporta el DTW.
```

## `_resample`

`def _resample(data: np.ndarray, n: int) -> np.ndarray`

```text
(T,F) -> (n,F) por interpolacion lineal en el indice de tiempo.
```

## `_angulos_directo`

`def _angulos_directo(segment: Segment, template) -> Score`

```text
Arquitectura 2 del documento de referencia: distancia angular directa,
sin DTW. Remuestrea la repeticion a la duracion de la plantilla y compara
frame a frame.
```

