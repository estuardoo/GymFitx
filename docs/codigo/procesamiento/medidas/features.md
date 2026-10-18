# `src/procesamiento/medidas/features.py`

```text
Capa 3: landmarks -> vector de features invariantes.

Dos reglas que sostienen todo el proyecto:

1. Nunca comparamos coordenadas crudas. Comparamos angulos articulares
   (invariantes a posicion, escala y distancia a la camara) y razones de
   distancia divididas por un segmento del propio cuerpo.
2. Los angulos salen de los *world landmarks* (metros, origen en la entidad),
   no de las coordenadas de pantalla: eso elimina la perspectiva.

Optimizacion: el YAML se compila UNA vez a arrays de indices. En caliente no
hay lookups de diccionario ni bucles de Python, solo operaciones numpy sobre
todas las features a la vez.
```

## Constantes

`ESCALA_TIPO`

## `angle_deg`

`def angle_deg(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float`

```text
Angulo interior A-B-C en grados, con vertice en B.
```

## `distance`

`def distance(a: np.ndarray, b: np.ndarray) -> float`

_sin docstring_

## `_nombres_de`

`def _nombres_de(spec: dict) -> list[str]`

_sin docstring_

## `_angulos_deg`

`def _angulos_deg(P: np.ndarray, idx: np.ndarray) -> np.ndarray`

```text
(K,3) indices de A-B-C -> (K,) angulos en grados. NaN si A o C caen sobre B.
```

## class `_Banco`

```text
Un grupo de features del YAML compilado a arrays de indices. 'indice' traduce el nombre
de un punto a su fila en P: los landmarks crudos de una fuente, o los kpoints del catalogo.
```

### `_Banco.__init__`

`def __init__(self, entradas, indice) -> None`

_sin docstring_

### `_Banco.medir`

`def medir(self, P: np.ndarray, out: np.ndarray) -> None`

```text
P (N,3) -> escribe en 'out' las features de este grupo (NaN = no medible).
```

## class `FeatureExtractor`

```text
Compilado desde un Exercise. Inmutable una vez construido.

Cada feature se mide de una de dos formas:
  - CRUDA: todos sus puntos son landmarks de MediaPipe de la fuente del ejercicio (camino de siempre).
  - DE KPOINTS: algun punto es un kpoint del catalogo (p.ej. un punto derivado). Se mide sobre los
    kpoints resueltos por cuadro con la misma funcion que el dataset (procesamiento/puntos/kpoints.py).
```

### `FeatureExtractor.__init__`

`def __init__(self, exercise) -> None`

_sin docstring_

### `FeatureExtractor.from_points`

`def from_points(self, P: np.ndarray) -> np.ndarray`

```text
P: (N, 3) world landmarks -> (F,) valores de las features CRUDAS. NaN = no medible
(tambien las de kpoints, que salen de extract()).
```

### `FeatureExtractor.select`

`def select(self, detections: list[Landmarks]) -> Landmarks | None`

```text
Elige que entidad medir cuando hay varias.
```

### `FeatureExtractor.extract`

`def extract(self, detections: list[Landmarks], t_ms: int) -> FeatureVec | None`

_sin docstring_

### `FeatureExtractor.signal`

`def signal(self, values: np.ndarray) -> float`

```text
Proyeccion 1-D declarada en el YAML. Es lo que cuenta repeticiones.
```

## `medibles`

`def medibles(nombres, features) -> list[dict]`

```text
Los features (activos) cuyos puntos existen todos en 'nombres', en el orden del yaml.
```

## `medir_clip`

`def medir_clip(points, nombres, features)`

```text
points (T,N,3) + nombres de sus N puntos -> ((T,F) float32 crudo, [nombres de feature], [tipos]).
Mide EXACTAMENTE los angulos y proporciones activados del ejercicio, tal como salen (sin normalizar).
```

## `normalizar_metricas`

`def normalizar_metricas(valores, tipos)`

```text
(n,F) crudo -> (n,F) en 0..1 segun el tipo de cada columna (sin tipos: todo angulo /180).
```

## `compute_features`

`def compute_features(points: np.ndarray, specs: list[dict], source: str='pose') -> dict`

```text
Camino escalar, usado por los tests. Misma matematica que la version compilada.
```

