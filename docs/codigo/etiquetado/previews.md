# `src/etiquetado/previews.py`

```text
Copia H.264 liviana de cada grabacion para el <video> del navegador (sistema/previews/).
```

## Constantes

`PREVIEW`

## `ffmpeg_exe`

`def ffmpeg_exe()`

```text
ffmpeg del sistema; si no hay (PC nueva), el que trae imageio-ffmpeg.
Sin esto la vista previa daba error 500 (WinError 2) en una maquina sin ffmpeg.
```

## `preview_de`

`def preview_de(src)`

```text
El navegador no decodifica mp4v (fourcc de OpenCV); cachea una copia H.264 para poder verla.
```

## `limpiar_preview_huerfanos`

`def limpiar_preview_huerfanos() -> int`

```text
Borra de sistema/previews las copias H.264 que ya no corresponden a
ninguna grabacion (p.ej. las de nombre viejo '205448_base.mp4', de antes
de _slug). Se regeneran solas al abrir el video. Devuelve cuantas borro.
```

