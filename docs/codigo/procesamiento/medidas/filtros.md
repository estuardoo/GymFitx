# `src/procesamiento/medidas/filtros.py`

```text
One Euro Filter vectorizado y consciente de las unidades.

Por que no una media movil: mete un retardo constante que desplaza la señal en
el tiempo y desalinea el DTW, que es justo lo que estamos midiendo. El One Euro
adapta su frecuencia de corte a la velocidad: filtra fuerte cuando estas quieto
(donde el ruido molesta) y casi no filtra cuando te mueves rapido (donde el
retardo molesta).

Detalle que suele hacerse mal: beta multiplica la velocidad de la señal, asi que
su valor depende de las UNIDADES. Un angulo se mueve a ~60 grados/s y una razon
de distancia a ~0.8/s; con un beta unico, la razon quedaria sobrefiltrada y con
retardo. Aqui la velocidad se divide primero por el rango tipico de cada feature,
de modo que beta es adimensional y significa lo mismo para todas.
```

## Constantes

`DOS_PI`, `RANGO`

## `_alpha`

`def _alpha(cutoff: np.ndarray | float, dt: float) -> np.ndarray`

_sin docstring_

## class `OneEuroFilter`

_sin docstring_

### `OneEuroFilter.__init__`

`def __init__(self, size: int, units: list[str] | None=None, min_cutoff: float=2.5, beta: float=27.0, d_cutoff: float=1.0) -> None`

_sin docstring_

### `OneEuroFilter.reset`

`def reset(self) -> None`

_sin docstring_

### `OneEuroFilter.update`

`def update(self, x: np.ndarray, t_ms: int) -> np.ndarray`

_sin docstring_

