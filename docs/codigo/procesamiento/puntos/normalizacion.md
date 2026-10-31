# `src/procesamiento/puntos/normalizacion.py`

```text
Normalizacion de un clip de puntos y remuestreo a N cuadros. Modo "formula" (el de cada ejercicio, se define en Kpoints ->
Normalizacion): x' = (K - origen) / escala, con origen y escala como formulas entre kpoints (ver formula.py).
Modos antiguos "rectangulo" (caja 100x100) y "punto": solo para modelos ya entrenados y ejercicios sin kpoints de referencia.

La usan igual el dataset (SQL) y el clasificador en vivo.
```

## Constantes

`EPS_ESCALA`, `DEFAULT_CFG`, `LADO_LIENZO`

## class `NormalizacionInvalida`

```text
El clip no se puede normalizar con esta formula (escala 0 o sin datos, kpoint ausente): se marca y no entra.
```

## `cfg_para`

`def cfg_para(point_names, cfg_guardada: dict | None=None) -> dict`

```text
Config efectiva con defaults razonables para estos puntos.
```

## `guia`

`def guia(cfg: dict) -> str`

```text
Descriptor corto de la normalizacion (table_file.guia_fix).
```

## `firma`

`def firma(nombres, angulos) -> str`

```text
Firma corta de QUE puntos/angulos trae el clip.
```

## `resamplear`

`def resamplear(fijo: np.ndarray, n_frames_fijo: int) -> np.ndarray`

```text
(T,N,C) -> (n,N,C). Interpola solo sobre cuadros con dato (NaN = no detectado).
```

## `resamplear_angulos`

`def resamplear_angulos(angulos: np.ndarray, n_frames_fijo: int) -> np.ndarray`

_sin docstring_

## `codigos_de`

`def codigos_de(kpoints) -> dict[int, str]`

```text
{codigo C: nombre del kpoint} de los puntos del cuerpo marcados en el ejercicio. C = landmark de MediaPipe + 1: fijo en todos los
ejercicios (C24 = cadera izquierda siempre). Los derivados no tienen codigo C: se arman en la formula con medio().
```

## `formulas_defecto`

`def formulas_defecto(kpoints) -> tuple[str, str] | None`

```text
(origen, escala) por defecto si el ejercicio trae hombros y caderas: origen = medio de caderas,
escala = largo del tronco (medio de hombros -> medio de caderas). None si faltan.
```

## `k_a_c`

`def k_a_c(texto, kpoints) -> str`

```text
Formulas guardadas con K<n> (posicion en la lista, formato viejo) -> C<nn> fijo, segun el catalogo actual del ejercicio.
```

## `escala_del_clip`

`def escala_del_clip(valores) -> float`

```text
Mediana de la escala sobre los cuadros validos (finitos y > 0): una escala por clip, estable ante un cuadro malo.
```

## `valores_formula`

`def valores_formula(points, point_names, cfg) -> tuple[np.ndarray, np.ndarray]`

```text
(origen (T,2) por cuadro, escala (T,) por cuadro) de la formula de cfg sobre los puntos del clip.
```

## `_normalizar_formula`

`def _normalizar_formula(points, point_names, cfg)`

```text
(K - origen) / escala en x e y; z solo se divide por la escala (el origen es 2D). origen por cuadro, escala una por clip.
```

## `_normalizar_punto`

`def _normalizar_punto(points, point_names, cfg)`

_sin docstring_

## `_normalizar_rectangulo`

`def _normalizar_rectangulo(points, indices_caja=None)`

```text
Caja envolvente del clip completo -> lienzo fijo de 100x100 con un solo
factor de escala (no deforma). Si se dan indices_caja, la caja sale solo
de esos puntos pero la transformacion se aplica a todos.
```

## `normalizar`

`def normalizar(points, point_names, cfg: dict) -> np.ndarray`

```text
(T,N,3) crudo -> (n_frames_fijo,N,3) segun cfg (ya resuelta con cfg_para).
```

## `normalizacion_de`

`def normalizacion_de(exercise)`

```text
Normalizacion del ejercicio (guide.json -> normalizacion): {origen, escala, n_frames, propia}. Lo que falte sale del
defecto (hombros/caderas del catalogo; n_frames de config.json formato.n_frames_defecto). propia=False: la formula es la propuesta, nunca se guardo.
```

## `validar_normalizacion`

`def validar_normalizacion(norm, kpoints)`

```text
Valida {origen, escala, n_frames} contra el catalogo; ValueError con mensaje para el panel. -> dict limpio.
```

## `cfg_de_normalizacion`

`def cfg_de_normalizacion(origen, escala, n_frames, kpoints)`

```text
cfg de modo 'formula' para estas formulas; ValueError si nombran un punto que el ejercicio no tiene marcado.
```

## `cfg_normalizacion`

`def cfg_normalizacion(exercise)`

```text
La cfg de normalizacion lista para procesamiento/puntos (la misma para gold, SQL, entrenamiento y modelo en vivo).
Sin formula posible (ejercicio sin hombros/caderas y sin configurar) cae al modo antiguo 'rectangulo'.
```

