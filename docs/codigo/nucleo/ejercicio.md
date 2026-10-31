# `src/nucleo/ejercicio.py`

```text
Carga y validacion del ejercicio (su definicion vive en parameters/<n>/, ver nucleo/definicion.py).

Un ejercicio NO es codigo: es un dato que declara que articulaciones
mirar y como reconocer una repeticion. Agregar manguito rotador o flexion de
tobillo es crear su definicion, nunca tocar el motor.

Todo lo que se puede validar se valida al cargar. Un error de dedo en un nombre
de landmark revienta antes de encender la camara, no a mitad de la serie.
```

## Constantes

`VALID_SOURCES`, `VALID_TYPES`, `VALID_REDUCE`, `VALID_DIRECTION`, `UNIDAD_POR_TIPO`

## class `Exercise`

_sin docstring_

### `Exercise.feature_names`

`def feature_names(self) -> list[str]`

_sin docstring_

### `Exercise.unit_of`

`def unit_of(self, name: str) -> str`

_sin docstring_

### `Exercise.to_dict`

`def to_dict(self) -> dict`

_sin docstring_

## `_reglas`

`def _reglas(slug, data)`

_sin docstring_

## `load_exercise`

`def load_exercise(slug: str) -> Exercise`

_sin docstring_

## `construir`

`def construir(slug: str, data: dict) -> Exercise`

```text
Valida una definicion (leida o por guardar) y arma el Exercise.
```

## `load_all`

`def load_all() -> dict[str, Exercise]`

```text
Todos los ejercicios activos, indexados por slug.
```

## `leer_def`

`def leer_def(exercise)`

```text
La definicion del ejercicio (dict) o None.
```

## `kpoints_de_ejercicio`

`def kpoints_de_ejercicio(exercise)`

```text
El catalogo 'kpoints' de la definicion (lista vacia si no tiene).
```

## `resolver_features`

`def resolver_features(features, kpoints)`

```text
Un feature de la definicion puede nombrar un landmark crudo (LEFT_ELBOW) aunque el ejercicio tenga catalogo de
kpoints con otro nombre: se traduce al nombre del kpoint que lo representa.
Sin esto, esos angulos no se encuentran en los datos.
```

## `features_de_ejercicio`

`def features_de_ejercicio(exercise)`

```text
Los angulos y proporciones ACTIVADOS de la definicion, con sus puntos ya traducidos a kpoints (lista vacia si no tiene).
```

## `puntos_de_ejercicio`

`def puntos_de_ejercicio(exercise: str) -> list[str] | None`

```text
Los puntos que le importan a este ejercicio, en orden. Si la definicion ya
tiene catalogo de 'kpoints' (editor de Puntos), son ESOS nombres -- es lo
que src/procesamiento/offline.py guarda en el .npz. Si no, los landmarks que aparecen en
'points'/'reference' de sus features, en orden de aparicion.
None si no se pudo leer la definicion -- quien llama debe caer entonces a la
lista completa que trae el .npz (mejor eso que perder datos).
```

