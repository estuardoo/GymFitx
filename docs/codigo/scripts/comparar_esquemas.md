# `scripts/comparar_esquemas.py`

```text
Compara esquemas (YAML) y modelos (src/evaluacion/comparadores/) sobre las MISMAS
grabaciones -- sin volver a prender la camara.

    python scripts/comparar_esquemas.py --movimiento manguito_rotador \
        --base datos/grabaciones/manguito_rotador/2026-09-01/070000_base.mp4 \
        --eval datos/grabaciones/manguito_rotador/2026-09-02/071500_serie.mp4

Que hace:
  1. Busca todos los YAML de ejercicios/ que empiezan con "<movimiento>" o
     "<movimiento>__..." (ver src.evaluacion.esquemas.grupo_de) -- cada uno es un
     esquema distinto del mismo movimiento real.
  2. Para cada esquema, reprocesa --base para calibrar SU plantilla (mismo
     video para todos, solo cambia que features mira).
  3. Para cada esquema y cada modelo de src/evaluacion/comparadores/, reprocesa cada
     --eval y junta los puntajes por repeticion.
  4. Imprime la tabla comparativa: promedio/desvio por (esquema, modelo) y
     la correlacion entre todos -- que tan de acuerdo estan entre si.

Para agregar un esquema nuevo: copia un YAML de ejercicios/ a
"<movimiento>__algo.yaml" y cambia su lista de "features" (que
articulaciones/regiones mide). No hace falta grabar de nuevo: este script
reusa --base y --eval con el nuevo esquema tal cual.

Nota: esto compara modelos y esquemas ENTRE SI (correlacion), no contra un
puntaje "correcto" -- para eso (matriz de confusion, MAE) hace falta
etiquetar las repeticiones a mano primero, que todavia no existe en el panel.
```

## `_construir_base`

`def _construir_base(video: Path, exercise)`

_sin docstring_

## `_evaluar_video`

`def _evaluar_video(video: Path, exercise, template, modelo: str) -> list[float]`

_sin docstring_

## `main`

`def main() -> int`

_sin docstring_

