# `src/interfaz/api/grabaciones.py`

```text
API de grabaciones: listar, descargar features en CSV y usar una toma como nueva base.
```

## class `UsarComoBase`

_sin docstring_

## `recordings`

`def recordings(limit: int=40, exercise: str | None=None) -> dict`

Ruta: **GET /api/recordings**

_sin docstring_

## `recording_csv`

`def recording_csv(ruta_relativa: str) -> Response`

Ruta: **GET /api/recordings/csv**

```text
Descarga en CSV las features (movimientos) ya guardadas en el .npz de
una grabación -- los ángulos y proporciones del ejercicio, que ya se
archivan automáticamente al terminar cada sesión.
```

## `use_as_base`

`def use_as_base(cfg: UsarComoBase) -> dict`

Ruta: **POST /api/recordings/use_as_base**

```text
Recalibra la plantilla de un ejercicio a partir de una grabacion archivada.

No hace falta redecodificar el video: las features de cada cuadro ya
quedaron guardadas en el .npz cuando se archivo la sesion, asi que esto
corre en milisegundos, sea cual sea el largo del video.
```

