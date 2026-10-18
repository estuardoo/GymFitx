# `src/preparacion/tabla.py`

```text
Nucleo de la preparacion: lo comparten el entrenamiento y las 5 etapas ejecutables (etapas.py).

Todo sale del DISCO (datos/clips, manifest.json, etiquetas.json, grabaciones); SQL Server es solo una copia de respaldo.
Los umbrales vienen de params.yaml (src/nucleo/config.py: params()).
```

## Constantes

`CLASES_CICLO`, `COPIA`

## `seleccion`

`def seleccion() -> dict`

```text
{clip: false} = desmarcado a mano en el panel (no usar para entrenar).
```

## `grupo_de`

`def grupo_de(clip: str) -> str`

```text
Grabacion de la que sale un clip (o una ventana "fuera"): todos los ciclos, copias (_2, _3) y ventanas de un mismo
video comparten grupo, para que la validacion nunca ponga unos en entrenar y otros en probar (fuga de datos).
```

## `cfg_formato`

`def cfg_formato(ejercicio: str) -> dict`

```text
Normalizacion espacial y temporal: defaults de normalizacion.py + params.yaml (formato, y formato.por_ejercicio).
```

## `spec_de`

`def spec_de(ejercicio: str, features: str | None=None, tipo: int | None=None) -> dict`

```text
La 'spec' del vector (la misma que guarda el modelo): que puntos, que medidas y como se normalizan.
```

## `clips_de`

`def clips_de(ejercicio: str) -> list[dict]`

```text
Filas del manifest.json de este ejercicio (sin pasar por SQL).
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

## `motivos_limpieza`

`def motivos_limpieza(cuadros: int, nan_pct: float) -> list[str]`

_sin docstring_

## `vectores`

`def vectores(ejercicio: str, spec: dict) -> dict[str, np.ndarray]`

```text
{clip: vector final} de los clips del disco que pasan la limpieza -- lo que lee el entrenamiento (en vez de SQL).
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

