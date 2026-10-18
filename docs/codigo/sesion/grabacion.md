# `src/sesion/grabacion.py`

```text
Registro en disco de cada sesion: video crudo + features + metadatos.

Se guarda el video SIN anotaciones a proposito. Las anotaciones se pueden
regenerar en cualquier momento reproduciendo el archivo con VideoSource por el
mismo pipeline (scripts/reprocesar.py); los pixeles originales, no. Guardar el video
limpio deja la puerta abierta a reprocesar con otro modelo, otro YAML o otros
umbrales dentro de un año, que es justamente para lo que sirve archivarlos.

Estructura en disco -- cada ejercicio en su propia carpeta, y dentro por dia:

    datos/grabaciones/<ejercicio>/<AAAA-MM-DD>/<HHMMSS>_<modo>.mp4
    datos/grabaciones/<ejercicio>/<AAAA-MM-DD>/<HHMMSS>_<modo>.npz
    datos/grabaciones/<ejercicio>/<AAAA-MM-DD>/<HHMMSS>_<modo>.json

Junto al .mp4 quedan:
  .npz   la serie de features ya extraida  -> reanalisis sin volver a trackear,
         y es lo que usa el panel para recalibrar la plantilla desde una
         grabacion vieja sin tener que redecodificar el video
  .json  metadatos de la sesion            -> que ejercicio, cuando, con que

Detalle de precision temporal: la camara entrega cuadros a un ritmo irregular
(20-30 fps con saltos, y con huecos cuando la sesion se pausa). Escribir esos
cuadros a una tasa nominal fija produciria un video que corre mas rapido o mas
lento que la realidad. Aqui cada cuadro se escribe tantas veces como haga
falta para llenar su lugar en una linea de tiempo de 30 fps: el video
resultante dura exactamente lo que duro la sesion (sin contar las pausas, que
el pipeline ya descuenta antes de que estos cuadros lleguen aqui).
```

## Constantes

`FPS_SALIDA`, `CODEC_POR_DEFECTO`

## class `VideoLogger`

```text
Sumidero que archiva la sesion. Se combina con Recorder o Evaluator.
```

### `VideoLogger.__init__`

`def __init__(self, base_dir: Path | str, guardar_video: bool=True, max_width: int=0, codec: str=CODEC_POR_DEFECTO) -> None`

_sin docstring_

### `VideoLogger.on_start`

`def on_start(self, pipe) -> None`

_sin docstring_

### `VideoLogger.on_frame`

`def on_frame(self, pipe, frame, fv) -> None`

```text
Cuadros PROCESADOS (con deteccion): guarda las features.
```

### `VideoLogger.on_raw_frame`

`def on_raw_frame(self, pipe, frame) -> None`

```text
TODOS los cuadros de la camara (hilo de captura): escribe el video.
Antes el video se escribia desde el hilo de deteccion (~7 fps) y cada
cuadro se repetia ~4 veces: 70 % de cuadros congelados. Ahora el video
lleva los cuadros reales de la camara y solo rellena huecos reales.
```

### `VideoLogger.on_rep`

`def on_rep(self, pipe, seg) -> None`

_sin docstring_

### `VideoLogger.on_stop`

`def on_stop(self, pipe) -> None`

_sin docstring_

### `VideoLogger.rutas`

`def rutas(self) -> dict`

_sin docstring_

## `listar_grabaciones`

`def listar_grabaciones(base_dir: Path | str, limite: int=40, exercise: str | None=None) -> list[dict]`

```text
Las sesiones archivadas, mas recientes primero. Lee los .json, no los videos.

exercise: si se pasa, solo las de ese slug (equivalente a listar esa
subcarpeta) -- es lo que usa el panel para el filtro por ejercicio.
```

## `uso_en_disco`

`def uso_en_disco(base_dir: Path | str) -> dict`

_sin docstring_

## `features_a_csv`

`def features_a_csv(npz_path: Path | str) -> str`

```text
El contenido del .npz de una grabacion, como texto CSV (t_ms + cada feature).

Los "movimientos" (angulos de cada dedo, apertura, etc.) ya se guardan
solos en el .npz al terminar cualquier sesion -- de mano o de cuerpo
completo. Esto solo los pasa a un formato que se abre en Excel/Sheets en
vez del binario de numpy, para el boton "Movimientos (CSV)" del panel.
```

## `resolver_json`

`def resolver_json(base_dir: Path | str, ruta_relativa: str) -> Path`

```text
De la ruta relativa que maneja el panel (ej. 'slug/2026-08-25/073012_serie.mp4')
al .json de metadatos correspondiente, validando que no se escape de datos/grabaciones/.
```

