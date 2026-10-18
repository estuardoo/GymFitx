"""Compara esquemas (YAML) y modelos (src/evaluacion/comparadores/) sobre las MISMAS
grabaciones -- sin volver a prender la camara.

    python scripts/comparar_esquemas.py --movimiento manguito_rotador \\
        --base datos/grabaciones/manguito_rotador/2026-09-01/070000_base.mp4 \\
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
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from src.captura.fuentes.video import VideoSource
from src.evaluacion import comparadores as scorers
from src.evaluacion.esquemas import esquemas_de, tabla_comparacion
from src.evaluacion.plantilla import template_path
from src.nucleo.config import EXERCISES_DIR, TEMPLATES_DIR
from src.nucleo.ejercicio import load_all
from src.sesion.pipeline import Evaluator, Pipeline, Recorder


def _construir_base(video: Path, exercise):
    fuente = VideoSource(video, mirror=False, realtime=False)
    rec = Recorder(template_path(TEMPLATES_DIR, exercise.slug))
    pipe = Pipeline(exercise, fuente, rec, template=None, annotate=False)
    pipe.run()
    if rec.error:
        raise RuntimeError(f"'{exercise.slug}': {rec.error}")
    return rec.template


def _evaluar_video(video: Path, exercise, template, modelo: str) -> list[float]:
    fuente = VideoSource(video, mirror=False, realtime=False)
    ev = Evaluator(template, storage=None, modelo=modelo)
    pipe = Pipeline(exercise, fuente, ev, template=template, annotate=False)
    pipe.run()
    return list(ev.scores)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--movimiento", required=True,
                     help="prefijo compartido por los YAML a comparar (ver src.evaluacion.esquemas.grupo_de)")
    ap.add_argument("--base", required=True, help="video para calibrar cada esquema")
    ap.add_argument("--eval", nargs="+", required=True, help="uno o mas videos a puntuar")
    args = ap.parse_args()

    esquemas = esquemas_de(args.movimiento, load_all(EXERCISES_DIR))
    if not esquemas:
        raise SystemExit(
            f"Ningun ejercicio en ejercicios/ pertenece al grupo '{args.movimiento}'. "
            f"Para comparar esquemas, copia un YAML existente a "
            f"'{args.movimiento}__otro.yaml' con otra lista de 'features'."
        )

    base = Path(args.base)
    videos_eval = [Path(v) for v in args.eval]
    resultados: dict[tuple[str, str], list[float]] = {}

    for slug, ex in esquemas.items():
        print(f"\n== esquema: {slug} ==")
        template = _construir_base(base, ex)
        print(f"   base calibrada: {template.n_reps} reps, tau={template.tau:.3f}")
        for modelo in scorers.MODELOS:
            todos: list[float] = []
            for video in videos_eval:
                todos += _evaluar_video(video, ex, template, modelo)
            resultados[(slug, modelo)] = todos
            resumen = f"promedio {np.mean(todos):.1f}" if todos else "sin repeticiones detectadas"
            print(f"   {modelo:16s} {len(todos):3d} reps  {resumen}")

    tabla = tabla_comparacion(resultados)
    print("\n=== comparacion (esquema, modelo) ===")
    for (slug, modelo), fila in tabla["filas"].items():
        print(f"  {slug:28s} {modelo:16s} "
              f"promedio={fila['promedio']}  desvio={fila['desvio']}  n={fila['n']}")

    print("\n=== correlacion -- que tan de acuerdo estan entre si ===")
    if not tabla["correlacion"]:
        print("  (hacen falta al menos 2 repeticiones y 2 columnas para correlacionar)")
    for par, r in tabla["correlacion"].items():
        print(f"  {par}: {r}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
