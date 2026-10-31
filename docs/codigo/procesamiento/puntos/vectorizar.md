# `src/procesamiento/puntos/vectorizar.py`

```text
Clip de puntos -> vector de largo fijo para el clasificador.

Es la MISMA transformacion para entrenar y para puntuar en vivo:
  - src/almacenamiento/dataset_sql.py la usa para llenar table_frames / table_frames_fix
    (lo que lee entrenar()).
  - src/evaluacion/comparadores/ la usa para convertir una repeticion en vivo en el
    mismo vector que vio el modelo al entrenar.
Si cambia algo aqui, cambia en los dos lados a la vez: no pueden divergir.

Pasos:
  1. filtrar los puntos al catalogo del ejercicio y descartar cuadros sin dato
  2. angulos de la mano (src/procesamiento/medidas/angulos.py, convencion flexion)
  3. normalizar el espacio (formula entre kpoints del ejercicio; antes "rectangulo"/"punto") y remuestrear a
     n_frames_fijo cuadros (interpolacion lineal)
  4. por cuadro: [x1,y1,z1, x2,y2,z2, ..., angulos...], concatenado; NaN -> 0
```

## `preparar`

`def preparar(points, point_names, deseados=None, kpoints=None, features=None)`

```text
Paso 1+2: filtra al catalogo, quita cuadros sin dato y calcula angulos.
Devuelve (points (T,N,3), nombres, angulos (T,A), nombres_angulos) o None
si no queda ningun cuadro con dato.
```

## `fijo`

`def fijo(points, nombres, angulos, cfg, features=None)`

```text
Paso 3: (puntos normalizados (n,N,3), angulos (n,A)), redondeados igual
que se guardan en SQL (2 y 4 decimales) para que vivo == entrenamiento. Las metricas (angulos,
proporciones) se llevan a 0..1 por tipo: es la tabla normalizada; la cruda va en table_frames.
```

## `aplanar`

`def aplanar(pts_fix: np.ndarray, ang_fix: np.ndarray, usar: str='ambos', tipos=None) -> np.ndarray`

```text
Paso 4: el vector final. usar: ver componentes(); tipos = tipo de cada columna de ang_fix (None = angulos).
```

## `vector_de_prep`

`def vector_de_prep(prep, spec: dict) -> np.ndarray`

```text
Pasos 3+4 sobre lo que devolvio preparar(): normaliza, remuestrea y aplana con la 'spec' del modelo.
```

## `vector_de_clip`

`def vector_de_clip(points, point_names, spec: dict) -> np.ndarray | None`

```text
Todo junto, con la 'spec' que guarda entrenar() en el modelo:
{"point_names": [...], "kpoints": [...], "cfg": {...}, "features": "ambos"}.
```

