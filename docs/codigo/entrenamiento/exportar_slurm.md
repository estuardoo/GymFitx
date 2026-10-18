# `src/entrenamiento/exportar_slurm.py`

```text
Exporta, para UN ejercicio, los datos crudos por video y por cuadro (puntos x,y,z de cada kpoint y las
metricas -- angulos y proporciones activados -- ya normalizadas 0..1) a un .npz AUTOCONTENIDO: para leerlo
despues no hace falta SQL Server ni el resto de GYMFITX, solo numpy.

Pensado para copiarlo a un cluster/supercomputador y correr ahi scripts/busqueda_features_slurm.py (ver ese
archivo para el flujo completo). Se corre en la PC que SI tiene acceso a SQL Server:

    python scripts/exportar_dataset_slurm.py --ejercicio manguito_rotador

Repetible para cualquier ejercicio: solo cambia --ejercicio.
```

## `exportar`

`def exportar(ejercicio: str, out) -> dict`

```text
Arma y guarda el .npz de 'ejercicio' en 'out'. -> resumen para mostrar en consola.
```

