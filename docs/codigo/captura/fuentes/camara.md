# `src/captura/fuentes/camara.py`

```text
Webcam: abrir (DSHOW/MSMF, MJPG), listar camaras y entregar cuadros tolerando fallos sueltos.
```

## Constantes

`FALLOS_TOLERADOS_S`

## `_backends`

`def _backends() -> list[int]`

_sin docstring_

## `_abrir`

`def _abrir(index: int)`

```text
Prueba cada backend hasta encontrar uno que de un cuadro real.

Devuelve (cap_abierto, ultimo_cuadro) o (None, None) si ninguno respondio.
El primer cuadro tras abrir suele salir negro o fallar del todo en varias
camaras USB, por eso los reintentos con una pausa corta antes de descartar
el indice.
```

## `_abrir_url`

`def _abrir_url(url: str)`

```text
Abre un flujo de video por red (DroidCam); None si no responde con un cuadro real a tiempo.
```

## `nombres_camaras_windows`

`def nombres_camaras_windows() -> list[str]`

```text
Camaras que Windows mismo ve conectadas (PnP), sin pasar por OpenCV.

Sirve para distinguir "no hay camara" de "hay camara pero OpenCV no
pudo abrirla" (permisos de Windows, en uso por otra app, driver): si
esto encuentra nombres y list_cameras() no encuentra nada, el problema
esta en el acceso, no en el hardware.
```

## `nombres_dshow`

`def nombres_dshow() -> list[str]`

```text
Nombres reales de camara, EN EL MISMO ORDEN que cv2.CAP_DSHOW les
asigna indice (consulta el mismo grafo DirectShow que usa OpenCV, a
diferencia de nombres_camaras_windows() que lee el PnP general y puede
no coincidir en orden). Es lo que deja mostrar "Logitech C920" en vez
de "Camara 0" en el selector del panel.
```

## `list_cameras`

`def list_cameras(max_index: int=8) -> list[dict]`

```text
Prueba los indices 0..max_index-1 y devuelve los que responden con imagen.

Usado tanto por scripts/camara.py como por el endpoint /api/cameras del
panel: un solo lugar que sabe como sondear camaras, sin duplicar la logica
entre la CLI y el servidor.
```

## class `CameraSource`

_sin docstring_

### `CameraSource.__init__`

`def __init__(self, index: int=0, width: int=1280, height: int=720, mirror: bool=True, fps: int=30, url: str | None=None) -> None`

_sin docstring_

### `CameraSource.frames`

`def frames(self) -> Iterator[Frame]`

_sin docstring_

### `CameraSource.set_fps`

`def set_fps(self, fps: int) -> bool`

```text
Pide un nuevo FPS a la camara YA ABIERTA, sin reabrirla (evita el
corte visible de apagar+prender). Devuelve si el driver acepto el
pedido -- no siempre lo respeta de verdad; el FPS real siempre se ve
en el overlay del video, asi que un valor que no aplica se nota ahi.
```

### `CameraSource.close`

`def close(self) -> None`

_sin docstring_

