# `src/evaluacion/plantilla.py`

```text
La plantilla: el movimiento base y TODO lo que se deriva de el.

Aqui vive la autocalibracion, que es lo que elimina los numeros magicos del
sistema. De una sola grabacion de N repeticiones salen:

  mu / sigma    normalizacion de las features        -> compare
  low / high    umbrales de histeresis               -> segmenter
  data          la repeticion de referencia (medoide)-> compare
  tau           severidad del puntaje                -> compare

El medoide (la repeticion mas parecida a todas las demas) es mejor referencia
que el promedio: promediar en el dominio del tiempo emborrona los picos y
produce una plantilla que nadie puede reproducir.

tau se fija para que una repeticion tan buena como tu promedio puntue 90:
    100 * exp(-err/tau) = 90   =>   tau = err / 0.10536
Asi el puntaje es comparable entre dias y entre ejercicios distintos.
```

## Constantes

`LN_090`

## class `Template`

_sin docstring_

### `Template.save`

`def save(self, path: str | Path) -> Path`

_sin docstring_

### `Template.load`

`def load(cls, path: str | Path) -> Template`

_sin docstring_

### `Template.to_dict`

`def to_dict(self) -> dict`

_sin docstring_

## `template_path`

`def template_path(templates_dir: str | Path, slug: str) -> Path`

_sin docstring_

## `build_template`

`def build_template(frames: list[FeatureVec], exercise, extractor, radius_frac: float=0.15) -> Template`

```text
De una toma continua de N repeticiones a una plantilla calibrada.

Se segmenta OFFLINE, con umbrales derivados de la propia toma: en el
momento de grabar todavia no existen umbrales que aplicar.
```

