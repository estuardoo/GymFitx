# `scripts/reprocesar.py`

```text
Reprocesa una grabacion por el mismo pipeline, sin camara.

    python scripts/reprocesar.py --video input/raw/2026-08-25/073012_mano_apertura_serie.mp4
    python scripts/reprocesar.py --video ... --exercise mano_apertura --modo grabar

Para esto se archivan los videos crudos. Sirve para:
  - recalibrar la plantilla con otros umbrales sobre la MISMA ejecucion
  - reevaluar sesiones viejas despues de cambiar el YAML del ejercicio
  - comparar como te movias hace un mes contra hoy

Como VideoSource y CameraSource comparten interfaz, el pipeline no nota la
diferencia: se ejecuta exactamente el mismo codigo que en vivo.
```

## `ejercicio_del_video`

`def ejercicio_del_video(video: Path) -> str | None`

_sin docstring_

## `main`

`def main() -> int`

_sin docstring_

