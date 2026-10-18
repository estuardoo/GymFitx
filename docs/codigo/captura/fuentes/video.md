# `src/captura/fuentes/video.py`

```text
Reproduce un archivo como fuente de cuadros (tests, reprocesar sin camara).
```

## class `VideoSource`

```text
Reproduce un archivo. Usado por los tests y para depurar sin camara.
```

### `VideoSource.__init__`

`def __init__(self, path: str | Path, mirror: bool=False, realtime: bool=False) -> None`

_sin docstring_

### `VideoSource.frames`

`def frames(self) -> Iterator[Frame]`

_sin docstring_

### `VideoSource.close`

`def close(self) -> None`

_sin docstring_

