# `scripts/_comun.py`

```text
Utilidades compartidas por los scripts de linea de comandos.

Existe para que record, evaluate, replay y serve no dupliquen el armado del
pipeline: la unica diferencia real entre ellos es el sumidero y la fuente.
```

## `cargar_ejercicio`

`def cargar_ejercicio(slug: str)`

_sin docstring_

## `cargar_plantilla`

`def cargar_plantilla(slug: str) -> Template`

_sin docstring_

## `con_archivo`

`def con_archivo(principal: Sink, archivar: bool=True, video: bool=True, max_width: int=0, codec: str='mp4v') -> Sink`

```text
Compone el sumidero principal con el archivador de la sesion.

Toda sesion queda archivada salvo que se pida lo contrario: los videos
y las features sirven despues para reanalizar, reentrenar o comparar
contra el pasado, y no se pueden recuperar si no se guardaron.
```

## `correr_con_ventana`

`def correr_con_ventana(pipe: Pipeline, titulo: str) -> None`

```text
Corre el pipeline en un hilo y muestra su ultimo cuadro anotado.
```

## `camara`

`def camara(args) -> CameraSource`

_sin docstring_

## `agregar_flags_comunes`

`def agregar_flags_comunes(ap) -> None`

_sin docstring_

## `avisar_archivo`

`def avisar_archivo(sink) -> None`

_sin docstring_

