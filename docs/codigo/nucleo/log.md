# `src/nucleo/log.py`

```text
Log del proyecto: un archivo por sesion en datos/logs/ (antes habia uno solo,
gymfitx.log, que rotaba y se perdia el rastro de en que arranque paso cada error).

    from gymfitx.log import logger
    log = logger("dataset")        # -> lineas "2026-09-23 10:00:00  [dataset] mensaje"

SESSION_LOG_PATH es el archivo de ESTA sesion (panel de Sistema lo muestra).
Solo se guardan las ultimas MAX_SESIONES para no llenar el disco.
```

## Constantes

`_RAIZ`, `MAX_SESIONES`, `SESSION_LOG_PATH`

## `_podar_sesiones_viejas`

`def _podar_sesiones_viejas() -> None`

_sin docstring_

## class `_Prefijo`

_sin docstring_

### `_Prefijo.format`

`def format(self, record: logging.LogRecord) -> str`

_sin docstring_

## `_configurar`

`def _configurar() -> logging.Logger`

_sin docstring_

## `logger`

`def logger(nombre: str | None=None) -> logging.Logger`

_sin docstring_

