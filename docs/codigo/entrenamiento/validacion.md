# `src/entrenamiento/validacion.py`

```text
Etapa 6b: como se mide un modelo (k-fold estratificado, F1 macro, CV anidada).
```

## `grupos_por_clase`

`def grupos_por_clase(y, grupos) -> int`

```text
Grabaciones distintas de la clase que menos tiene (cada fold necesita al menos una de cada clase).
```

## `elegir_k`

`def elegir_k(test_pct, conteo, clases, n, min_grupos=None)`

```text
Folds del k-fold: ~100/test_pct, sin pasar de la clase mas chica, de n/2 ni de las grabaciones de la clase mas chica.
```

## class `PorGrabacion`

```text
Reemplaza al StratifiedKFold: .split(X, y) estratificado sin partir una grabacion entre entrenar y probar.
Las copias (_2, _3) y los ciclos del mismo video van juntos; antes se mezclaban y el F1 salia inflado.
`estratos` (p.ej. clase+persona) reparte cada estrato entre los folds: el azar queda condicionado a la persona,
asi cada fold de prueba tiene clips de todas las personas en vez de tocar solo a una.
```

### `PorGrabacion.__init__`

`def __init__(self, k, grupos, semilla, estratos=None)`

_sin docstring_

### `PorGrabacion.split`

`def split(self, X, y)`

_sin docstring_

## `evaluar`

`def evaluar(nombre, est, X, y, skf)`

```text
Un modelo con CV: una sola pasada por fold (la prediccion sale del argmax de predict_proba).
De paso anota cuantas iteraciones uso de verdad en cada fold ('iteraciones': tope y min/media/max).
```

## `composicion_folds`

`def composicion_folds(skf, X, y, personas)`

```text
Por fold: cuantos clips de cada persona van a prueba y cuantos a entrenar. Sirve para ver que el azar
reparte entre todas las personas (y no toma solo de una).
```

## `por_persona`

`def por_persona(y, y_pred, personas, clases)`

```text
Lo que acierta el modelo en los clips de cada persona, con las predicciones que ya salieron de los folds
(no reentrena nada). Sirve para comparar P1 contra P2: con pocos clips una persona puede no decir mucho.
```

## `sin_privados`

`def sin_privados(r)`

_sin docstring_

## `cv_anidada`

`def cv_anidada(catalogo, X, y, skf)`

```text
Estimacion honesta del procedimiento completo "probar N modelos y
quedarse con el mejor": en cada fold externo se elige el modelo con CV
interna SOLO sobre la parte de entrenamiento y se mide en la de prueba.
Sin esto, el % reportado es optimista (se elige y se mide con los mismos
datos). None si hay muy pocos clips para una CV interna.
```

