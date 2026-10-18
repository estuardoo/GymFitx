# `src/procesamiento/puntos/normalizacion.py`

```text
Normalizacion de un clip de puntos: caja 100x100 (o punto de referencia) y remuestreo a N cuadros.

La usan igual el dataset (SQL) y el clasificador en vivo.
```

## Constantes

`DEFAULT_CFG`, `LADO_LIENZO`

## `cfg_para`

`def cfg_para(point_names, cfg_guardada: dict | None=None) -> dict`

```text
Config efectiva con defaults razonables para estos puntos.
```

## `guia`

`def guia(cfg: dict) -> str`

```text
Descriptor corto de la normalizacion (table_file.guia_fix).
```

## `firma`

`def firma(nombres, angulos) -> str`

```text
Firma corta de QUE puntos/angulos trae el clip.
```

## `resamplear`

`def resamplear(fijo: np.ndarray, n_frames_fijo: int) -> np.ndarray`

```text
(T,N,C) -> (n,N,C). Interpola solo sobre cuadros con dato (NaN = no detectado).
```

## `resamplear_angulos`

`def resamplear_angulos(angulos: np.ndarray, n_frames_fijo: int) -> np.ndarray`

_sin docstring_

## `_normalizar_punto`

`def _normalizar_punto(points, point_names, cfg)`

_sin docstring_

## `_normalizar_rectangulo`

`def _normalizar_rectangulo(points, indices_caja=None)`

```text
Caja envolvente del clip completo -> lienzo fijo de 100x100 con un solo
factor de escala (no deforma). Si se dan indices_caja, la caja sale solo
de esos puntos pero la transformacion se aplica a todos.
```

## `normalizar`

`def normalizar(points, point_names, cfg: dict) -> np.ndarray`

```text
(T,N,3) crudo -> (n_frames_fijo,N,3) segun cfg (ya resuelta con cfg_para).
```

