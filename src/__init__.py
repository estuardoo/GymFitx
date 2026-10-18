"""GYMFITX: coach de movimiento por camara.

Un solo sistema, una rama por funcion (ver docs/ARQUITECTURA.md):
nucleo -> almacenamiento -> captura -> procesamiento -> evaluacion -> sesion -> etiquetado -> entrenamiento -> interfaz.
Cada rama solo importa de las anteriores (tests/test_capas.py)."""
