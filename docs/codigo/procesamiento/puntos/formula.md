# `src/procesamiento/puntos/formula.py`

```text
Formulas entre kpoints para normalizar (Kpoints -> Normalizacion): `medio(C24,C25)`, `dist(medio(C12,C13), medio(C24,C25))`.

C<nn> = el punto del cuerpo con ese codigo FIJO, igual en todos los ejercicios (landmark de MediaPipe + 1: C01 nariz, C12/C13 hombros,
C24/C25 caderas...). Tiene que estar marcado en los kpoints del ejercicio. (K<n> = la posicion en la lista de un ejercicio: formato viejo,
solo se lee para modelos ya entrenados; las formulas nuevas no lo aceptan.) Dos tipos de valor:
  punto  (x,y por cuadro)      C24 · medio(a,b) · prom(a,b,..) · punto±punto · punto*numero · punto/numero
  numero (un valor por cuadro) dist(a,b) · max(n,..) · min(n,..) · numero (2, 0.5) · numero±*/ numero
Solo x e y. Se lee el texto con `ast` y se camina el arbol permitido: nunca se ejecuta codigo (no hay eval).
```

## Constantes

`_K`, `LARGO_MAX`, `_FUNCIONES`

## `_arbol`

`def _arbol(texto: str)`

_sin docstring_

## `usados`

`def usados(texto: str) -> list[int]`

```text
Numeros de punto (C<nn>) que nombra la formula (sin repetir, en orden).
```

## `_ev`

`def _ev(n, K)`

```text
-> ('p'|'n', array): 'p' (T,2) punto, 'n' (T,1) numero (las constantes (1,1) se difunden).
```

## `validar`

`def validar(texto: str, tipo: str, numeros) -> None`

```text
ValueError con un mensaje para el panel. tipo: 'p' (origen) o 'n' (escala); numeros = kpoints que existen.
```

## `evaluar`

`def evaluar(texto: str, K: dict[int, np.ndarray], tipo: str) -> np.ndarray`

```text
K = {numero: (T,2)} -> (T,2) para 'p' o (T,) para 'n'. NaN donde falte un punto.
```

