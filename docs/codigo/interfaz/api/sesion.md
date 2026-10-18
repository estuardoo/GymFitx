# `src/interfaz/api/sesion.py`

```text
API de la sesion en vivo: camaras, estado, rutina, historial, encender/grabar/detener, video MJPEG y WebSocket.
```

## Constantes

`VIDEO_ANCHO_MAX`

## `_encolar`

`def _encolar(evento: dict) -> None`

_sin docstring_

## `_al_bus`

`def _al_bus(evento: dict) -> None`

_sin docstring_

## `_difusor`

`async def _difusor() -> None`

_sin docstring_

## `iniciar_difusor`

`def iniciar_difusor()`

```text
Lo llama el ciclo de vida de la app: crea la cola y la tarea que reparte eventos.
```

## class `RutinaItem`

_sin docstring_

## class `EncenderCamara`

_sin docstring_

## class `OverlayRegiones`

_sin docstring_

## class `CambiarFps`

_sin docstring_

## class `SeleccionarModelo`

_sin docstring_

## class `SeleccionarEntrenamiento`

_sin docstring_

## class `CambiarEjercicio`

_sin docstring_

## `cameras`

`def cameras(max: int=8) -> dict`

Ruta: **GET /api/cameras**

_sin docstring_

## `state`

`def state() -> dict`

Ruta: **GET /api/state**

_sin docstring_

## `history`

`def history(days: int=14) -> dict`

Ruta: **GET /api/history**

_sin docstring_

## `set_routine`

`def set_routine(items: list[RutinaItem]) -> dict`

Ruta: **POST /api/routine**

_sin docstring_

## `session_camera_on`

`def session_camera_on(cfg: EncenderCamara) -> dict`

Ruta: **POST /api/session/camera_on**

_sin docstring_

## `session_overlay`

`def session_overlay(cfg: OverlayRegiones) -> dict`

Ruta: **POST /api/session/overlay**

_sin docstring_

## `session_fps`

`def session_fps(cfg: CambiarFps) -> dict`

Ruta: **POST /api/session/fps**

_sin docstring_

## `session_modelo`

`def session_modelo(cfg: SeleccionarModelo) -> dict`

Ruta: **POST /api/session/modelo**

_sin docstring_

## `session_clasificador`

`def session_clasificador(cfg: SeleccionarEntrenamiento) -> dict`

Ruta: **POST /api/session/clasificador**

_sin docstring_

## `session_exercise`

`def session_exercise(cfg: CambiarEjercicio) -> dict`

Ruta: **POST /api/session/exercise**

_sin docstring_

## `session_grabar`

`def session_grabar() -> dict`

Ruta: **POST /api/session/grabar**

_sin docstring_

## `session_grabar_detener`

`def session_grabar_detener() -> dict`

Ruta: **POST /api/session/grabar_detener**

_sin docstring_

## `session_stop`

`def session_stop() -> dict`

Ruta: **POST /api/session/stop**

_sin docstring_

## `session_pause`

`def session_pause() -> dict`

Ruta: **POST /api/session/pause**

_sin docstring_

## `session_resume`

`def session_resume() -> dict`

Ruta: **POST /api/session/resume**

_sin docstring_

## `_jpeg`

`def _jpeg(img)`

_sin docstring_

## `video`

`async def video() -> StreamingResponse`

Ruta: **GET /video**

```text
MJPEG. El JPEG se codifica en un hilo (antes bloqueaba el event loop
del servidor en cada cuadro) y solo cuando hay un cuadro NUEVO.
```

## `ws_endpoint`

`async def ws_endpoint(ws: WebSocket) -> None`

Ruta: **WEBSOCKET /ws**

_sin docstring_

