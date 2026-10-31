# `scripts/grabar.py`

```text
Graba el movimiento base de un ejercicio y calibra su plantilla.

    python scripts/grabar.py --exercise mano_apertura

Haz 5 o mas repeticiones lentas y completas, volviendo siempre al punto de
partida. Al pulsar 'q' el sistema segmenta la toma, elige la repeticion medoide
y deriva umbrales, normalizacion y tau. Nada de eso se escribe a mano.

La toma queda archivada en input/raw/ (video + features), asi que siempre se
puede volver a calibrar sobre la misma grabacion con scripts/reprocesar.py.
```

## `main`

`def main() -> int`

_sin docstring_

