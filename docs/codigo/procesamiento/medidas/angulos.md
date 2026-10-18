# `src/procesamiento/medidas/angulos.py`

```text
Geometria de angulos entre vectores/puntos (grados).

VERSION: subirla si cambia la definicion de algun angulo (fuerza a recalcular en SQL).
```

## Constantes

`VERSION`

## `angulo_entre`

`def angulo_entre(u: np.ndarray, v: np.ndarray) -> np.ndarray`

```text
(...,3),(...,3) -> (...) grados entre vectores; NaN si alguno es ~0.
```

## `angulo_interior`

`def angulo_interior(a, b, c) -> np.ndarray`

```text
Angulo A-B-C con vertice en B, en grados (acepta lotes (...,3)).
```

