# `scripts/hpc/estado_busqueda_slurm.py`

```text
Tabla de avance de una corrida de busqueda_features_slurm.py -- lee los <salida>.estado.json que cada
tarea del array va sobreescribiendo sola (uno por tarea, actualizado cada vez que termina una combinacion) y
arma una tabla: cuanto avanzo cada tarea, si ya termino o si fallo. Standalone a proposito, solo libreria
estandar (nada de numpy/sklearn) -- se puede correr en el login node del cluster en cualquier momento,
incluso con el job todavia corriendo, aunque el modulo de python/scikit-learn este roto.

    python estado_busqueda_slurm.py --resultados resultados/

'terminado' en false para una tarea que ya no aparece en squeue/sacct = fallo (revisa su .err); en false y
sigue en squeue = normal, todavia corriendo.
```

## `leer_estados`

`def leer_estados(carpeta: Path) -> list[dict]`

_sin docstring_

## `main`

`def main(argv=None)`

_sin docstring_

