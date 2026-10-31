# `src/evaluacion/comparadores/clasificador.py`

```text
Comparador con el modelo entrenado (output/models/<n>/run_NNN/modelo.joblib).

Convierte los kpoints de la repeticion en el MISMO vector que vio al entrenar
(procesamiento/puntos/vectorizar.py); el puntaje es P(bien) 0-100.
```

## class `Clasificador`

```text
Modelo de output/models/<n>/run_NNN cargado para puntuar en vivo.
```

### `Clasificador.__init__`

`def __init__(self, ruta: Path) -> None`

_sin docstring_

### `Clasificador.puntuar`

`def puntuar(self, segment: Segment, template) -> Score`

_sin docstring_

### `Clasificador.to_dict`

`def to_dict(self) -> dict`

_sin docstring_

## class `DetectorCiclos`

```text
Cuenta ciclos solo con el modelo: ventana deslizante del largo de un ciclo (spec['ventana_ms']) sobre los
kpoints en vivo. P(ciclo) = 1 - P(fuera); un ciclo se cuenta cuando sube de ALTO y vuelve a bajar de BAJO.
```

### `DetectorCiclos.__init__`

`def __init__(self, clf: Clasificador) -> None`

_sin docstring_

### `DetectorCiclos.update`

`def update(self, t_ms: int, kp) -> dict | None`

```text
kp = kpoints (K,3) de este cuadro. Devuelve {"clase","p_bien","p_ciclo"} al cerrar un ciclo, o None.
```

## `buscar_clasificador`

`def buscar_clasificador(exercise: str, base_dir: Path=ENTRENAMIENTOS_DIR) -> Path | None`

```text
El modelo.joblib mas reciente entrenado con clips de 'exercise' y con
spec (los entrenados antes de esta version no la tienen). Corridas en output/models/<n del ejercicio>/run_NNN.
```

## `cargar_clasificador`

`def cargar_clasificador(exercise: str) -> Clasificador | None`

_sin docstring_

