# `src/preparacion/tabla.py`

```text
Nucleo de la preparacion: lo comparten el entrenamiento y las 5 etapas ejecutables (etapas.py).

Todo sale del DISCO (input/bronze, input/raw y las tablas de parameters/inputs.json); SQL Server es solo una copia de respaldo.
Los umbrales vienen de parameters/config.json (src/nucleo/config.py: params()).
Capas: bronze (clip) -> plate (puntos y angulos sin normalizar) -> gold (vector normalizado); cada una usa el id del clip.
```

## Constantes

`CLASES_CICLO`, `_LOCK`

## `seleccion`

`def seleccion() -> dict`

```text
{clip: false} = desmarcado a mano en el panel (no usar para entrenar).
```

## `grupo_de`

`def grupo_de(clip: str) -> str`

```text
Grabacion de la que sale un clip (o una ventana "fuera"): todos los ciclos, copias y ventanas de un mismo
video comparten grupo, para que la validacion nunca ponga unos en entrenar y otros en probar (fuga de datos).
```

## `cfg_formato`

`def cfg_formato(ejercicio: str) -> dict`

```text
Normalizacion espacial y temporal del ejercicio: la formula (origen / escala) y los cuadros que se definen en Kpoints.
```

## `spec_de`

`def spec_de(ejercicio: str, features: str | None=None, tipo: int | None=None) -> dict`

```text
La 'spec' del vector (la misma que guarda el modelo): que puntos, que medidas y como se normalizan.
```

## `clips_de`

`def clips_de(ejercicio: str) -> list[dict]`

```text
Clips de este ejercicio (tabla `clips` de parameters/inputs.json; sin pasar por SQL).
```

## `ruta_npz`

`def ruta_npz(row: dict) -> Path`

_sin docstring_

## `leer_clip`

`def leer_clip(row: dict, spec: dict) -> dict`

```text
{cuadros, nan_pct, prep}: tamaño del clip, % de puntos sin deteccion (solo los del ejercicio) y las medidas derivadas
(angulos / proporciones) listas para normalizar. prep = None si el clip no trae datos.
```

## `carpeta`

`def carpeta(base: Path, ejercicio: str) -> Path`

```text
input/<capa>/<numero del ejercicio>/ (se crea).
```

## `_sha`

`def _sha(obj) -> str`

_sin docstring_

## `hash_plate`

`def hash_plate(spec: dict) -> str`

_sin docstring_

## `hash_gold`

`def hash_gold(spec: dict) -> str`

```text
Todo lo que cambia el vector final: si cambia (normalizacion, componentes, limpieza...) el gold se rehace.
```

## `_guardar_json`

`def _guardar_json(ruta: Path, obj) -> None`

_sin docstring_

## `llave`

`def llave(row: dict) -> str`

_sin docstring_

## `plates`

`def plates(filas: list[dict], spec: dict) -> dict[str, dict]`

```text
{clip: {cuadros, nan_pct, prep}} desde input/plate (se regenera lo que cambio: el clip o el catalogo de puntos).
prep = (puntos, nombres, angulos, nombres_ang) o None si el clip no trae datos.
```

## `motivos_limpieza`

`def motivos_limpieza(cuadros: int, nan_pct: float) -> list[str]`

_sin docstring_

## `vectores`

`def vectores(ejercicio: str, spec: dict) -> dict[str, np.ndarray]`

```text
{clip: vector final} de los clips del disco que pasan la limpieza -- lo que lee el entrenamiento (en vez de SQL).
Pasa por plate y gold: lo que ya esta calculado y al dia se lee tal cual.
```

## `previa_normalizacion`

`def previa_normalizacion(nombre, norm, clip=None)`

```text
Prueba la formula en un clip (por numero; sin numero, el del medio) SIN guardar: valores de origen y escala y
donde quedan los kpoints que usa. ValueError con mensaje para el panel si la formula o el clip no sirven.
```

## `_iou`

`def _iou(a0, a1, b0, b1)`

_sin docstring_

## `ventanas_crudas`

`def ventanas_crudas(exercise, tope, paso=None, iou_max=None)`

```text
Ventanas del largo de un ciclo tomadas de los tramos de las grabaciones fuente que no estan cortados como
bien/mal/base: (lista de (puntos, nombres, 'fuera/<video>@<seg>'), ventana_ms). ([], None) si no hay.
```

## `ventanas_fuera`

`def ventanas_fuera(exercise, spec, tope, paso=None, iou_max=None)`

```text
Ejemplos de la clase "fuera" ya vectorizados, para que el modelo aprenda a decir "aqui no hay ciclo" (lo que permite
contar en vivo con ventana deslizante). -> (vectores, nombres, ventana_ms); ([], [], None) si no hay grabaciones.
```

