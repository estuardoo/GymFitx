# `src/captura/deteccion/tracker.py`

```text
Capa 2: cuadro -> landmarks. Unico archivo del proyecto que importa mediapipe.

Si manana cambiamos de motor (MoveNet, YOLO-pose, lo que sea), solo se
reescribe este archivo: el resto del pipeline habla en Landmarks, no en
estructuras de MediaPipe.
```

## Constantes

`MODEL_URLS`

## `ensure_model`

`def ensure_model(source: str) -> Path`

```text
Descarga el modelo la primera vez. Despues el sistema corre offline.
```

## `_to_array`

`def _to_array(points) -> np.ndarray`

_sin docstring_

## class `_BaseTracker`

_sin docstring_

### `_BaseTracker.detect`

`def detect(self, frame: Frame) -> list[Landmarks]`

_sin docstring_

### `_BaseTracker.close`

`def close(self) -> None`

_sin docstring_

### `_BaseTracker.__enter__`

`def __enter__(self)`

_sin docstring_

### `_BaseTracker.__exit__`

`def __exit__(self, *exc) -> None`

_sin docstring_

### `_BaseTracker._mp_image`

`def _mp_image(frame: Frame) -> mp.Image`

```text
BGR -> mp.Image, UNA vez por cuadro aunque lo pidan varios trackers
(varios trackers en paralelo): se cachea el ultimo cuadro convertido.
```

## class `PoseTracker`

_sin docstring_

### `PoseTracker.__init__`

`def __init__(self, min_confidence: float=0.5) -> None`

_sin docstring_

### `PoseTracker.detect`

`def detect(self, frame: Frame) -> list[Landmarks]`

_sin docstring_

## `build_tracker`

`def build_tracker(exercise) -> _BaseTracker`

```text
Enruta segun lo que declare el ejercicio. El pipeline no elige, obedece.
```

