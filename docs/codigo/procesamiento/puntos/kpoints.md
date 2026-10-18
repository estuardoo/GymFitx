# `src/procesamiento/puntos/kpoints.py`

```text
Catalogo de 'kpoints' de un ejercicio -> puntos por cuadro.

UNA sola implementacion para los dos caminos:
  - offline: src/procesamiento/offline.py re-decodifica el video grabado (30 fps reales)
    y arma el dataset de entrenamiento.
  - en vivo: src/sesion/pipeline.py arma los mismos puntos por cuadro para que el
    clasificador entrenado (src/evaluacion/comparadores/) puntue cada repeticion.

Cada kpoint del .yaml: {"numero", "nombre", "origen"} con
  origen = {"tipo": "landmark", "fuente": "pose", "landmark": NOMBRE}
         o {"tipo": "derivado", "de": [numero_a, numero_b]}  (punto medio de dos kpoints previos)
```

## Constantes

`FUENTES_KPOINT`, `VERSION_DETECCION`, `_NAN3`

## `nombres`

`def nombres(kpoints) -> list[str]`

_sin docstring_

## `resolver`

`def resolver(kpoints, detecciones)`

```text
Detecciones (Landmarks de pose) de UN cuadro -> (world (K,3), screen (K,2)) en el orden del
catalogo; NaN donde el punto no se vio. None si no se vio ningun punto del catalogo (cuadro sin dato).
```

