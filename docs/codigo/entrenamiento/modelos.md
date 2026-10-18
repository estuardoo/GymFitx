# `src/entrenamiento/modelos.py`

```text
Catalogo de clasificadores a comparar (sklearn siempre; lightgbm/xgboost si estan instalados).
```

## Constantes

`SEMILLA`

## `catalogo`

`def catalogo()`

```text
Catalogo de clasificadores a comparar. sklearn siempre disponible (14 modelos);
lightgbm/xgboost/catboost se agregan solo si estan instalados (import tolerante), igual que
el patron usado en SUBVALUACION/ML/src/registry.py (solo se leyo ese proyecto, no se edito).
```

## `modelos_disponibles`

`def modelos_disponibles()`

_sin docstring_

## `tope`

`def tope(nombre)`

```text
El tope de iteraciones configurado para este modelo (epocas o max_iter), o None si no itera.
```

## `iteraciones_usadas`

`def iteraciones_usadas(est)`

```text
Cuantas iteraciones hizo de verdad un modelo YA ajustado (puede frenar antes del tope por convergencia
o early stopping). None si el modelo no itera o la libreria no lo expone.
```

