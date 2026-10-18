# `src/nucleo/landmarks.py`

```text
Nombres, indices y conexiones de los landmarks de MediaPipe.

Un solo lugar con los nombres permite que los YAML de ejercicio se escriban en
lenguaje humano ("LEFT_ELBOW") en vez de numeros magicos, y que un nombre mal
escrito falle al arrancar y no a mitad de la sesion.
```

## Constantes

`POSE_LANDMARKS`, `POSE_CONNECTIONS`, `POSE_CONNECTIONS_MANO`, `POSE_CONNECTIONS_NOMBRES`, `_INDEX`, `N_POINTS`

## `regiones_de_puntos`

`def regiones_de_puntos(nombres: list[str]) -> list[str]`

```text
Que regiones de POSE_REGIONES tocan al menos uno de estos landmarks.

Se usa para marcar por defecto, en el selector del panel, las zonas que
un ejercicio realmente necesita (segun los puntos que declara su YAML) --
el usuario despues puede ajustarlo a mano.
```

## `region_indices`

`def region_indices(nombres: list[str] | None) -> set[int] | None`

```text
Traduce nombres de region a indices de POSE_LANDMARKS.

None = sin filtro (todas las regiones, el comportamiento de siempre).
Una lista (incluso vacia) = solo la union de esas regiones.
```

## `es_landmark`

`def es_landmark(name: str, source: str) -> bool`

```text
True si 'name' es un landmark crudo de MediaPipe de esa fuente (y no el nombre de un kpoint).
```

## `resolve`

`def resolve(name: str, source: str='pose') -> int`

```text
Nombre de landmark -> indice. Falla fuerte y con mensaje util.
```

