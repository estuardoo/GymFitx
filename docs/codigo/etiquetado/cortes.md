# `src/etiquetado/cortes.py`

```text
Etapa 3: cortar y etiquetar grabaciones (bien / mal / base / descarte por segmento).

datos/etiquetas.json es la UNICA fuente del etiquetado y se guarda por mezcla.
```

## Constantes

`CFG`, `_OVERLAY_LOCK`

## `videos`

`def videos()`

_sin docstring_

## `estado_config`

`def estado_config()`

_sin docstring_

## `leer_labels`

`def leer_labels()`

_sin docstring_

## `guardar_labels`

`def guardar_labels(body)`

_sin docstring_

## `overlay_de`

`def overlay_de(file)`

```text
Puntos en coordenadas de pantalla (0-1) por cuadro, para dibujar el esqueleto
sobre el video mientras se reproduce. Si el video aun no tiene la
deteccion con el catalogo actual, se corre aqui (la primera vez tarda).
```

