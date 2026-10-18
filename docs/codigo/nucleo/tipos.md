# `src/nucleo/tipos.py`

```text
Contratos de datos del pipeline. Cero logica, solo estructura.

Todo lo que viaja entre capas pasa por aqui. Si un modulo necesita un campo
que no esta en estos tipos, la responsabilidad esta mal repartida.
```

## class `Frame`

```text
Un cuadro crudo de la fuente.
```

## class `Landmarks`

```text
Puntos detectados en un cuadro (el cuerpo, 33 puntos).
```

## class `FeatureVec`

```text
El vector de features de un cuadro. Nada aguas abajo conoce los pixeles.

raw/label son opcionales y no alteran el scoring (que sigue viviendo por
completo en 'values', los angulos/razones invariantes): solo van de
pasada para quien quiera archivar los landmarks crudos (ver videolog.py),
por ejemplo para reconstruir un dataset de puntos (x,y,z) por separado.
```

### `FeatureVec.any_valid`

`def any_valid(self) -> bool`

_sin docstring_

## class `Segment`

```text
Una repeticion recortada del flujo.
```

### `Segment.duration_ms`

`def duration_ms(self) -> int`

_sin docstring_

### `Segment.n_frames`

`def n_frames(self) -> int`

_sin docstring_

## class `Score`

```text
Resultado de comparar una repeticion contra la plantilla.
```

### `Score.worst`

`def worst(self, n: int=2) -> list[tuple[str, float]]`

```text
Las n features con mayor desviacion. Es lo que el panel muestra como consejo.
```

### `Score.to_dict`

`def to_dict(self) -> dict`

_sin docstring_

