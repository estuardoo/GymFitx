# `src/evaluacion/base_clip.py`

```text
Base (plantilla) a partir de UN clip ya cortado: el primer clip "bien" del ejercicio (o el que se indique).

Sirve para que el ejercicio cuente repeticiones en vivo sin tener que grabar una base aparte.
Los umbrales salen del propio clip: a = P10 y b = P90 de la señal; low = a + 0.3 (b - a), high = a + 0.5 (b - a)
(la banda es estrecha y esta en el medio del recorrido, asi cada ciclo se cuenta una sola vez); la rep se cuenta al volver
a `fin` = 70 % del recorrido, o sea en la posicion inicial y no a mitad de la subida.
tau (severidad del puntaje) sale del error DTW contra los demas clips "bien" si los hay.
```

## Constantes

`_B`, `TAU_DEFECTO`, `MAX_OTROS`

## `_natural`

`def _natural(s: str)`

_sin docstring_

## `_valores`

`def _valores(ex, ext: FeatureExtractor, npz: Path) -> np.ndarray`

```text
(T, F) features crudas del clip, medidas con la misma matematica del vivo.
```

## `_originales`

`def _originales(d: Path) -> list[Path]`

```text
.npz de la carpeta en orden natural de nombre, sin los duplicados (_2, _3...) si hay originales.
```

## `primer_clip`

`def primer_clip(slug: str, clase: str='bien') -> Path | None`

_sin docstring_

## `plantilla_de_clip`

`def plantilla_de_clip(ex, npz: Path, otros: list[Path] | None=None) -> Template`

_sin docstring_

## `base_desde_clip`

`def base_desde_clip(ex, clip: str | None=None, clase: str='bien') -> dict`

```text
Crea datos/plantillas/<slug>.npz desde `clip` (nombre o ruta; por defecto el primero de la clase).
```

