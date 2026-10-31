# `src/evaluacion/esquemas.py`

```text
Comparar 'esquemas' (que features/regiones del cuerpo se miden) y modelos
(como se compara) entre si, sobre las MISMAS grabaciones.

Un esquema es, en este proyecto, simplemente OTRA definicion de ejercicio
que describe el mismo movimiento real con otro conjunto de features/regiones
-- ver parameters/<n>/ y src/nucleo/ejercicio.py. No hace falta un concepto nuevo:
dos definiciones que empiezan igual ya son dos variantes del mismo movimiento.

Convencion de nombres: 'manguito_rotador' y 'manguito_rotador__hombro'
pertenecen los dos al grupo 'manguito_rotador' (todo antes de '__'). Una definicion
sin '__' es su propio grupo de un solo esquema.

Por que se pueden compartir los MISMOS videos entre esquemas sin volver a
grabar: cada sesion ya archiva el video crudo, sin anotar (ver
src/sesion/grabacion.py). scripts/reprocesar.py ya sabe reprocesar ese video con OTRO
ejercicio adjunto -- el pipeline no distingue camara de video. Este
modulo solo automatiza ese reproceso para muchos esquemas x muchos modelos
a la vez y arma la tabla comparativa.

Lo que este modulo NO hace todavia (ver matriz de pendientes): matriz de
confusion y MAE contra una etiqueta humana -- hace falta la herramienta de
etiquetado, que todavia no existe.
```

## `grupo_de`

`def grupo_de(slug: str) -> str`

```text
'manguito_rotador__hombro' -> 'manguito_rotador'. Sin '__', el slug
entero es su propio grupo (un solo esquema).
```

## `esquemas_de`

`def esquemas_de(movimiento: str, ejercicios: dict) -> dict`

```text
Todos los ejercicios (slug -> Exercise) que son esquemas del mismo
movimiento, ordenados por slug para que la salida sea reproducible.
```

## `tabla_comparacion`

`def tabla_comparacion(resultados: dict[tuple[str, str], list[float]]) -> dict`

```text
resultados: {(esquema, modelo): [score_rep1, score_rep2, ...]}, todas
sobre el MISMO video y en el mismo orden de repeticion.

Devuelve promedio/desvio por celda (esquema, modelo) y una matriz de
correlacion entre todas las celdas -- que tan de acuerdo estan entre si
modelos y esquemas sobre las mismas repeticiones. No necesita ninguna
etiqueta humana: es acuerdo entre modelos, no acierto contra la verdad.
```

