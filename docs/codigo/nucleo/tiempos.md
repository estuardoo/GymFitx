# `src/nucleo/tiempos.py`

```text
Tiempos por proceso, en matriz. Complementa el log de sesion (datos/logs/gymfitx_*.log):
- cada proceso medido con medir("nombre") queda en una fila (n, ultima, media, p95, max, inicio, hilo)
- la matriz se guarda en datos/logs/tiempos_<sesion>.log y se ve en  GET /api/tiempos
- lo que pasa de LENTO_S tambien deja una linea [tiempos] en el log de sesion
```

## Constantes

`LENTO_S`, `MUESTRAS`, `RUTA`, `T0`

## `registrar`

`def registrar(nombre: str, inicio: float, dur: float) -> None`

```text
inicio = perf_counter() al empezar; dur en segundos.
```

## `medir`

`def medir(nombre: str)`

_sin docstring_

## `filas`

`def filas() -> list[dict]`

```text
Una fila por proceso, en orden de primera aparicion en el tiempo.
```

## `matriz`

`def matriz() -> str`

_sin docstring_

## `escribir`

`def escribir(forzar: bool=False) -> None`

```text
Reescribe la matriz de la sesion si hubo cambios (se llama al arrancar, cada 30 s y al cerrar).
```

