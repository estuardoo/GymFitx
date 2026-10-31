# `src/interfaz/api/ahpc.py`

```text
AHPC: modulo independiente para armar, con los datos ya generados (table_frames_fix en SQL), el paquete
completo para correr la busqueda de features en un cluster/supercomputador: el .npz autocontenido de cada
ejercicio elegido + el script standalone scripts/hpc/busqueda_features_slurm.py (sin SQL, sin FastAPI, sin el
resto de GYMFITX) + un .sbatch por ejercicio ya apuntando a su dataset. Se sube el .zip al cluster, se
descomprime y se corre "sbatch slurm_<ejercicio>.sbatch" ahi mismo. No genera datos nuevos: solo empaqueta
lo que ya esta en las tablas SQL.
```

## Constantes

`SCRIPT`, `RESUMEN_SCRIPT`, `ESTADO_SCRIPT`, `DIAGNOSTICO_SCRIPT`, `SBATCH_PLANTILLA`, `RESUMEN_SBATCH_PLANTILLA`, `LANZADOR_PLANTILLA`, `LEEME`

## `_sbatch_para`

`def _sbatch_para(ejercicio: str) -> str`

```text
La plantilla de ejemplo, con --dataset/--job-name puestos para este ejercicio.
```

## `_resumen_sbatch_para`

`def _resumen_sbatch_para(ejercicio: str) -> str`

```text
sbatch del resumen SOLO (sin la busqueda), para cuando ya tenes todos los .csv en resultados/ (la
busqueda termino, o se corto pero alcanza lo que hay) y queres correr/actualizar el resumen como un job
aparte en vez de a mano en el login node -- ver LEEME.txt.
```

## `_lanzar_para`

`def _lanzar_para(ejercicio: str) -> str`

```text
La plantilla del lanzador (arma busqueda + resumen en 2 sbatch encadenados con --dependency, ver
scripts/hpc/lanzar_busqueda_slurm.sh), con el nombre del ejercicio puesto en todos los placeholders.
```

## `_config_json`

`def _config_json(ejercicios: list[str], codigos_por_ejercicio: dict[str, list[str]]) -> str`

```text
Un solo config.json para todo el paquete (las carpetas y los codigos de modelo son iguales para
cualquier ejercicio) -- SIN nombres de kpoints/angulos/proporciones: eso ya esta en tu tabla SQL, aca
solo las rutas y las leyendas que no existen en otro lado (codigo de cada modelo, y K0N -> codigo
universal de landmark de cada ejercicio, para no confundirlos al leer resultados).
```

## `ahpc_ejercicios`

`def ahpc_ejercicios()`

Ruta: **GET /api/ahpc/ejercicios**

```text
Un ejercicio por fila: cuantos clips tiene en el manifest (bien/mal, sin 'base') y si ya tiene
catalogo de kpoints (si no, no se puede exportar).
```

## class `ExportarPedido`

_sin docstring_

## `ahpc_exportar`

`def ahpc_exportar(body: ExportarPedido)`

Ruta: **POST /api/ahpc/exportar**

```text
body: {ejercicios: [nombre, ...]}. Arma un .zip con el .npz de cada ejercicio (rehecho con lo que hay
ahora mismo en SQL), el script standalone busqueda_features_slurm.py y un .sbatch por ejercicio ya
apuntando a su dataset -- listo para subir al cluster y correr sbatch ahi. Los ejercicios que fallen
(sin datos, sin catalogo) van en la cabecera X-Ahpc-Errores y no rompen el zip de los demas.
```

