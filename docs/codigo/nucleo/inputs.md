# `src/nucleo/inputs.py`

```text
Que video es cual: las tablas `raw` (grabaciones) y `clips` (recortes) en parameters/inputs.json, y la tabla de
ejercicios numerados en parameters/exercise.json. Todo lo demas (cortes, exportar, entrenar, panel) pregunta aqui.

    raw    {id, ej, persona, fecha, archivos, segmentos, origen_viejo}        input/raw/<ej>/<id>.mp4|npz|json
    clips  {id, ej, raw_id, seg, t_ini_ms, t_fin_ms, etiqueta 1|0|null, usar, persona, rev, copia}   input/bronze/<ej>/<id>.mp4|npz

La persona vive en el raw (un cambio llega a todos sus clips); un clip sin raw (importado suelto) trae la suya.
Los ids nunca se reutilizan (contadores). Los nombres de ejercicio solo existen en exercise.json.
```

## Constantes

`SCHEMA`, `LOCK`, `CLASE_DE`, `ETIQUETA_DE`, `EXPORTABLES`, `SIN_ETIQUETA`, `_COPIA`

## `_leer`

`def _leer(path, defecto)`

_sin docstring_

## `_escribir`

`def _escribir(path, obj) -> None`

_sin docstring_

## `ejercicios`

`def ejercicios() -> dict[int, dict]`

_sin docstring_

## `id_de`

`def id_de(slug: str) -> int | None`

_sin docstring_

## `slug_de`

`def slug_de(ej) -> str`

_sin docstring_

## `asegurar_ejercicio`

`def asegurar_ejercicio(slug: str, nombre: str | None=None) -> int`

```text
El numero del ejercicio; si no tiene, le asigna el siguiente (los numeros no se reutilizan).
```

## `desactivar_ejercicio`

`def desactivar_ejercicio(slug: str) -> None`

```text
Ejercicio archivado: sigue con su numero (reservado) pero inactivo.
```

## `_vacia`

`def _vacia() -> dict`

_sin docstring_

## `tabla`

`def tabla() -> dict`

```text
Copia de la tabla (se relee solo si el archivo cambio).
```

## `_leer_tabla`

`def _leer_tabla() -> dict`

_sin docstring_

## `editar`

`def editar()`

```text
with editar() as t: ...  -> lee, deja modificar y guarda al salir (si no hubo error). Un solo escritor a la vez.
```

## `_nuevo_id`

`def _nuevo_id(t: dict, cual: str) -> int`

_sin docstring_

## `ruta_raw`

`def ruta_raw(ej, rid, ext='mp4') -> Path`

_sin docstring_

## `ruta_clip`

`def ruta_clip(ej, cid, ext='mp4') -> Path`

_sin docstring_

## `vid_de`

`def vid_de(raw: dict) -> str`

```text
El identificador de un video para el panel: ruta relativa a input/raw ('1/000007.mp4').
```

## `clave`

`def clave(clip: dict) -> str`

```text
El identificador de un clip: ruta relativa a input/bronze ('1/000123.mp4').
```

## `_partes`

`def _partes(ruta: str)`

_sin docstring_

## `raw_de_vid`

`def raw_de_vid(vid: str, t: dict | None=None) -> dict | None`

_sin docstring_

## `clip_de_clave`

`def clip_de_clave(cl: str, t: dict | None=None) -> dict | None`

_sin docstring_

## `registrar_raw`

`def registrar_raw(t: dict, slug: str, *, fecha: str | None=None, persona: str | None=None, archivos=('mp4', 'npz', 'json'), origen_viejo: str | None=None, segmentos: list | None=None) -> dict`

```text
Fila nueva en `raw` (no crea archivos: los escribe quien graba). Dentro de `with editar() as t`.
```

## `registrar_clip`

`def registrar_clip(t: dict, slug: str, *, etiqueta, t_ini_ms: int, t_fin_ms: int, raw_id: int | None=None, seg: int | None=None, reps: int=0, persona: str | None=None, origen_viejo: str | None=None, copia: bool=False) -> dict`

_sin docstring_

## `es_copia`

`def es_copia(nombre: str) -> bool`

```text
'..._bien_2' = copia del mismo ciclo (riesgo de fuga entre entrenar y probar).
```

## `persona_de`

`def persona_de(clip: dict, raws: dict) -> str | None`

_sin docstring_

## `filas`

`def filas(t: dict | None=None) -> list[dict]`

```text
Los clips con la forma que el resto del codigo siempre uso (clip, npz, origen, clase, ini, fin, exercise, persona...).
```

## `grupo_de_vid`

`def grupo_de_vid(vid: str, t: dict | None=None) -> str`

```text
Grupo de validacion de un video: todos sus ciclos y ventanas comparten grupo (sin fuga entre entrenar y probar).
```

## `grupo_de_clip`

`def grupo_de_clip(cl: str, t: dict | None=None) -> str`

_sin docstring_

## `leer_labels`

`def leer_labels() -> dict`

```text
{vid: {"segmentos": [...], ...}} de los raw que tienen cortes.
```

## `guardar_labels`

`def guardar_labels(body: dict) -> None`

```text
Mezcla (no reemplaza): un video no mencionado conserva sus cortes.
```

## `asignar_persona`

`def asignar_persona(raw_id: int, persona: str | None) -> dict`

_sin docstring_

## `seleccion`

`def seleccion() -> dict`

```text
{clip: False} = desmarcado a mano en el panel (no usar para entrenar).
```

## `guardar_seleccion`

`def guardar_seleccion(cambios: dict) -> int`

_sin docstring_

