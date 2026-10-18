# `src/interfaz/api/publicar.py`

```text
API del boton "Publicar en internet" (tunel Cloudflare, apagado por defecto). La logica vive en interfaz/tunel.py.
```

## class `Publicar`

_sin docstring_

## `publicar_estado`

`async def publicar_estado() -> dict`

Ruta: **GET /api/publicar/estado**

_sin docstring_

## `publicar_iniciar`

`async def publicar_iniciar(cfg: Publicar) -> dict`

Ruta: **POST /api/publicar/iniciar**

_sin docstring_

## `publicar_detener`

`async def publicar_detener() -> dict`

Ruta: **POST /api/publicar/detener**

_sin docstring_

## `publicar_nueva_clave`

`async def publicar_nueva_clave() -> dict`

Ruta: **POST /api/publicar/nueva_clave**

```text
Genera otra clave (la anterior deja de servir) y la muestra UNA vez.
```

