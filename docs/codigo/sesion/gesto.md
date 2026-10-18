# `src/sesion/gesto.py`

```text
Gesto de control: mantener una muneca en la esquina superior izquierda inicia/detiene la grabacion.
```

## Constantes

`_IDX_MUNECAS`, `GESTO_RECORTE`, `GESTO_MANTENER_MS`, `GESTO_ENFRIAMIENTO_MS`, `GESTO_OLVIDO_MS`

## class `Gesto`

```text
Muneca sostenida en la esquina = un disparo.
```

### `Gesto.__init__`

`def __init__(self, al_disparar) -> None`

_sin docstring_

### `Gesto.en_zona`

`def en_zona(detecciones) -> bool`

_sin docstring_

### `Gesto.evaluar`

`def evaluar(self, detecciones, t_ms: int) -> None`

_sin docstring_

### `Gesto.avanzar`

`def avanzar(self, dentro: bool, t_ms: int) -> bool`

```text
Logica pura: True justo en el cuadro en que se cumple el tiempo dentro de la zona.
```

### `Gesto.close`

`def close(self) -> None`

_sin docstring_

