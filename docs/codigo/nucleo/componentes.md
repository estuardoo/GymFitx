# `src/nucleo/componentes.py`

```text
Que entra al vector del modelo: letras x, y, z (ejes de cada kpoint), a (angulos), p (proporciones y razones).

Los nombres de antes siguen valiendo: puntos=xyz, angulos=ap, ambos=xyzap. Lo comparten el SQL (al leer los
vectores), el vectorizador (vivo) y el entrenamiento, para que los tres armen exactamente lo mismo.
```

## Constantes

`_LEGADO`

## `componentes`

`def componentes(usar: str)`

```text
-> (indices de ejes, angulos?, proporciones?)
```

## `mascara_metricas`

`def mascara_metricas(tipos, usar: str, n: int) -> list[bool]`

```text
Que columnas de metricas entran: proporciones y razones cuentan como 'p'; lo demas, angulos (sin tipos: angulos).
```

