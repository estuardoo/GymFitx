# `src/evaluacion/segmentador.py`

```text
Capa 5: recorta repeticiones del flujo continuo de features.

Maquina de estados sobre una señal 1-D con histeresis de dos umbrales. La
histeresis es lo que evita que un temblor en la zona de cambio dispare veinte
repeticiones falsas.

Los dos umbrales NO se escriben a mano en ningun lado: salen de los percentiles
de la propia grabacion base (ver template.build_template). Cero numeros magicos.

Truco para no duplicar logica: 'up_down' se resuelve invirtiendo el signo de la
señal y de los umbrales, y reusando exactamente el mismo codigo de 'down_up'.
```

## Constantes

`ESPERANDO_ALTO`, `EN_ALTO`, `BAJANDO`, `EN_BAJO`

## class `RepSegmenter`

_sin docstring_

### `RepSegmenter.__init__`

`def __init__(self, n_features: int, signal_idx: np.ndarray, reduce: str, low: float, high: float, direction: str='down_up', min_duration_ms: int=600, max_duration_ms: int=8000, capacity: int=600, fin: float | None=None) -> None`

_sin docstring_

### `RepSegmenter.signal_of`

`def signal_of(self, values: np.ndarray) -> float`

_sin docstring_

### `RepSegmenter.reset`

`def reset(self) -> None`

_sin docstring_

### `RepSegmenter._push`

`def _push(self, fv: FeatureVec) -> bool`

_sin docstring_

### `RepSegmenter._emit`

`def _emit(self) -> Segment`

_sin docstring_

### `RepSegmenter.update`

`def update(self, fv: FeatureVec) -> Segment | None`

```text
Devuelve un Segment el cuadro en que se cierra una repeticion.
```

