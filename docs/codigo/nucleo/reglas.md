# `src/nucleo/reglas.py`

```text
Reglas de postura: un angulo medido en el cuadro contra un valor y una tolerancia. Dentro = verde, fuera = rojo.

Dos formas (segun lleve `c`):
  - sin `c`: la recta B->A contra la horizontal; 90 = recta (A justo encima de B).
  - con `c`: el angulo en el vertice B entre las rectas B->A y B->C (p. ej. hombro-cadera-rodilla).
Cada extremo es un punto o el promedio de varios. Codigos: C01..C33 = landmark MediaPipe + 1 (C01 = nariz, C24/C25 =
caderas), medidos sobre los 33 puntos del cuadro (no hace falta tenerlos en el catalogo de kpoints). D## / T##
= ese punto de la pierna DELANTERA / TRASERA (## = codigo de la pierna izquierda: D26 = rodilla delantera); la delantera es
la de la rodilla mas alta en la imagen. El angulo se mide en pixeles (corrige el aspecto del cuadro).
`lado`: ambos (|ang - angulo| <= tol), min (ang >= angulo - tol), max (ang <= angulo + tol). `fase: abajo` = solo se
evalua en la parte baja de la repeticion; `bajando` = durante el descenso y abajo (repeticion en curso). En el .yaml: `reglas:` [{nombre, a, b, c?, angulo, tolerancia, unidad, lado,
fase, mensaje, activo}].
```

## Constantes

`_COD`, `UNIDADES`, `LADOS`, `FASES`

## `_parte`

`def _parte(codigo)`

_sin docstring_

## `indice`

`def indice(codigo, izq_delante: bool=True) -> int`

```text
Indice MediaPipe (0..32). D/T dependen de que pierna va delante.
```

## `_puntos`

`def _puntos(v)`

_sin docstring_

## `validar`

`def validar(reglas) -> list[dict]`

```text
Normaliza y valida; ValueError con un mensaje para el panel.
```

## `tolerancia_deg`

`def tolerancia_deg(r) -> float`

_sin docstring_

## `_punto`

`def _punto(pts, codigos, izq_delante, tam)`

_sin docstring_

## `evaluar`

`def evaluar(reglas, screen, ancho, alto, fases=FASES) -> list[dict]`

```text
screen: (N,>=2) normalizado 0-1. Devuelve por regla activa {nombre, angulo, desvio, ok, mensaje, pa, pb[, pc]}
(puntos en pixeles, para dibujar); las que no se pueden medir o no son de una de las `fases` activas se omiten.
```

