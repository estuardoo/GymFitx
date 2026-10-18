"""Parecido de un clip contra el clip base, punto por punto: R2 (%) tras alinear posicion/escala y tiempo (DTW).

Lo usan la Descomposicion y la tabla table_indicator."""

from __future__ import annotations

import numpy as np

from src.evaluacion.comparadores.dtw import dtw_band

DTW_VERSION = 2  # v2: usa src.evaluacion.comparadores.dtw.dtw_band (antes una copia propia en Python puro)


def _dtw_alinear(base_pts, otro_pts):
    """Alinea 'otro_pts' a los indices de tiempo de 'base_pts' con DTW (banda
    Sakoe-Chiba de +/-15 %, la MISMA implementacion que puntua las
    repeticiones en vivo: src.evaluacion.comparadores.dtw.dtw_band). La banda evita que un DTW
    libre "persiga" puntos sueltos y maquille un movimiento distinto como
    identico. Devuelve, para cada frame del base, el promedio de los puntos
    de 'otro' que le tocaron en el camino optimo."""
    A = np.asarray(base_pts, dtype=np.float64)
    B = np.asarray(otro_pts, dtype=np.float64)
    C = ((A[:, None, :] - B[None, :, :]) ** 2).sum(axis=2)
    _, camino = dtw_band(C, 0.15)
    suma = np.zeros_like(A)
    cuenta = np.zeros(len(A))
    for i, j in camino:
        suma[i] += B[j]
        cuenta[i] += 1
    sin_par = cuenta == 0               # no deberia pasar (camino continuo), por si acaso
    suma[sin_par] = B[np.minimum(np.nonzero(sin_par)[0], len(B) - 1)]
    cuenta[sin_par] = 1
    return [tuple(p) for p in suma / cuenta[:, None]]


def alinear(base_kp, otro_kp):
    """Alinea 'otro_kp' al 'base_kp' en (x,y), en dos pasos (ver indicador()
    para el porque de cada uno): 1. posicion + escala (mismo promedio y mismo
    rango que el base, sin deformar la proporcion) y 2. tiempo (DTW). Devuelve
    'otro' ya en los MISMOS instantes de tiempo que 'base' (una tupla (x,y)
    por frame de base) -- lo que usa SIM para animar los 2 esqueletos en
    sincronia. None si no hay datos ('base_kp'/'otro_kp' vacios)."""
    xb, yb = base_kp["x"], base_kp["y"]
    x, y = otro_kp["x"], otro_kp["y"]
    if not xb or not x:
        return None
    mxb, myb = sum(xb) / len(xb), sum(yb) / len(yb)
    mx, my = sum(x) / len(x), sum(y) / len(y)
    rango = lambda serie: max(serie) - min(serie)
    rb_x, rb_y, r_x, r_y = rango(xb), rango(yb), rango(x), rango(y)
    factores = []
    if r_x > 1e-6 and rb_x > 1e-6:
        factores.append(rb_x / r_x)
    if r_y > 1e-6 and rb_y > 1e-6:
        factores.append(rb_y / r_y)
    escala = min(factores) if factores else 1.0
    otro_alineado = [((x[i] - mx) * escala + mxb, (y[i] - my) * escala + myb) for i in range(len(x))]
    base_pts = list(zip(xb, yb))
    return _dtw_alinear(base_pts, otro_alineado)


def indicador(base_kp, otro_kp):
    """Que tan parecido es 'otro_kp' al 'base_kp' en (x,y), como un R^2 vuelto
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
    None si el base no se movio en ese punto (SStot ~ 0, nada con que comparar)."""
    xb, yb = base_kp["x"], base_kp["y"]
    if not xb:
        return None
    mxb, myb = sum(xb) / len(xb), sum(yb) / len(yb)
    ss_tot = sum((xb[i] - mxb) ** 2 + (yb[i] - myb) ** 2 for i in range(len(xb)))
    if ss_tot < 1e-9:
        return None
    otro_dtw = alinear(base_kp, otro_kp)
    if otro_dtw is None:
        return None
    ss_res = sum((otro_dtw[i][0] - xb[i]) ** 2 + (otro_dtw[i][1] - yb[i]) ** 2 for i in range(len(xb)))
    return round(max(0.0, 1 - ss_res / ss_tot) * 100, 2)
