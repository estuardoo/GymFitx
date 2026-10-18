# `src/evaluacion/similitud.py`

```text
Parecido de un clip contra el clip base, punto por punto: R2 (%) tras alinear posicion/escala y tiempo (DTW).

Lo usan la Descomposicion y la tabla table_indicator.
```

## Constantes

`DTW_VERSION`

## `_dtw_alinear`

`def _dtw_alinear(base_pts, otro_pts)`

```text
Alinea 'otro_pts' a los indices de tiempo de 'base_pts' con DTW (banda
Sakoe-Chiba de +/-15 %, la MISMA implementacion que puntua las
repeticiones en vivo: src.evaluacion.comparadores.dtw.dtw_band). La banda evita que un DTW
libre "persiga" puntos sueltos y maquille un movimiento distinto como
identico. Devuelve, para cada frame del base, el promedio de los puntos
de 'otro' que le tocaron en el camino optimo.
```

## `alinear`

`def alinear(base_kp, otro_kp)`

```text
Alinea 'otro_kp' al 'base_kp' en (x,y), en dos pasos (ver indicador()
para el porque de cada uno): 1. posicion + escala (mismo promedio y mismo
rango que el base, sin deformar la proporcion) y 2. tiempo (DTW). Devuelve
'otro' ya en los MISMOS instantes de tiempo que 'base' (una tupla (x,y)
por frame de base) -- lo que usa SIM para animar los 2 esqueletos en
sincronia. None si no hay datos ('base_kp'/'otro_kp' vacios).
```

## `indicador`

`def indicador(base_kp, otro_kp)`

```text
Que tan parecido es 'otro_kp' al 'base_kp' en (x,y), como un R^2 vuelto
porcentaje: 100 = identico, 0 = tan distinto como si no se hubiera movido.

Antes de comparar, 'otro' se ALINEA al 'base' (ver alinear()) en dos pasos:
1. Posicion + escala (desplazamiento y un solo factor para x/y, sin
   deformar la proporcion): mismo promedio y mismo rango que el base.
   Sin esto, un movimiento con la misma FORMA no calificaba bien solo
   porque se grabo con la mano en otra parte del cuadro o un poco mas
   grande/chico (camara, persona, encuadre) -- ruido de grabacion, no
   una diferencia real de movimiento.
2. Tiempo (Dynamic Time Warping, ver _dtw_alinear): dos grabaciones del
   mismo gesto rara vez tienen el mismo ritmo interno frame a frame
   (una pausa, un tramo mas lento) aunque se hayan remuestreado al mismo
   numero de frames -- DTW busca la correspondencia que minimiza el
   error en vez de comparar siempre frame i contra frame i.

    SSres = sum_frames[(x_alineado_dtw-xbase)^2 + (y_alineado_dtw-ybase)^2]
    SStot = sum_frames[(xbase-mean(xbase))^2 + (ybase-mean(ybase))^2]
    indicador = 100 * max(0, 1 - SSres/SStot)

Se autocalibra solo (SStot es la propia variacion del base, no un numero
inventado): un ejercicio con mucho movimiento no queda en desventaja
frente a uno con poco. Negativo (peor que no moverse) se recorta a 0.
None si el base no se movio en ese punto (SStot ~ 0, nada con que comparar).
```

