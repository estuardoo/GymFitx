# `src/interfaz/app.py`

```text
Servidor local del panel de control.

    python -m src.interfaz       ->  http://127.0.0.1:8000

Tres canales hacia el navegador:
  REST       estado y configuracion           interfaz/api/*.py
  WebSocket  eventos del pipeline en vivo      interfaz/api/sesion.py
  MJPEG      el video anotado                  interfaz/api/sesion.py

Este archivo solo arma la app: middleware del tunel, ciclo de vida, routers y carpetas estaticas.
```

## `_sincronizar_kpoints`

`async def _sincronizar_kpoints() -> None`

```text
Al arrancar trae de SQL lo que difiera y despues, cada 30 s, sube lo guardado sin conexion.
```

## `_ciclo_de_vida`

`async def _ciclo_de_vida(_app)`

_sin docstring_

## `_log_error_no_manejado`

`async def _log_error_no_manejado(request: Request, exc: Exception) -> JSONResponse`

```text
Sin esto un error de ruta (ej. pyodbc) solo se veia en la consola del .bat,
nunca en gymfitx.log -- quedaba invisible en cuanto se cerraba esa ventana.
```

## `_sin_cache`

`async def _sin_cache(request: Request, call_next)`

```text
La interfaz (index y /static) no se cachea: un cambio de JS llega con recargar, sin Ctrl+F5.
```

## `_medir_http`

`async def _medir_http(request: Request, call_next)`

```text
Tiempo hasta tener la respuesta de cada ruta (los streams largos se saltan). Ver /api/tiempos.
```

## `tiempos_api`

`def tiempos_api() -> dict`

Ruta: **GET /api/tiempos**

```text
Matriz de tiempos por proceso de esta sesion (tambien en sistema/logs/tiempos_*.log).
```

## `index`

`async def index() -> FileResponse`

Ruta: **GET /**

_sin docstring_

## `main`

`def main() -> None`

_sin docstring_

