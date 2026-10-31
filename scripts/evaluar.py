"""Evalua repeticiones en vivo contra el movimiento base.

    python scripts/evaluar.py --exercise mano_apertura

Cada sesion queda archivada en input/raw/ (video crudo + features + metadatos).
"""

from __future__ import annotations

import argparse

import numpy as np

from scripts._comun import (
    agregar_flags_comunes,
    avisar_archivo,
    camara,
    cargar_ejercicio,
    cargar_plantilla,
    con_archivo,
    correr_con_ventana,
)
from src.almacenamiento.historial import Storage
from src.nucleo.config import DB_PATH
from src.sesion.grabacion import VideoLogger
from src.sesion.pipeline import Evaluator, Pipeline


def main() -> int:
    ap = argparse.ArgumentParser(description="Evaluar repeticiones en vivo")
    ap.add_argument("--exercise", required=True)
    ap.add_argument("--reps", type=int, default=0, help="meta de repeticiones (0 = libre)")
    ap.add_argument("--no-save", action="store_true", help="no registrar en la base de datos")
    agregar_flags_comunes(ap)
    args = ap.parse_args()

    ex = cargar_ejercicio(args.exercise)
    plantilla = cargar_plantilla(ex.slug)

    store = None if args.no_save else Storage(DB_PATH)
    ses_id = store.open_session(ex.slug, "serie") if store else None

    base = Evaluator(plantilla, storage=store, target_reps=args.reps, session_id=ses_id)
    sink = con_archivo(base, archivar=not args.no_archivo,
                   video=not args.sin_video, max_width=args.video_ancho,
                   codec=args.video_codec)
    pipe = Pipeline(ex, camara(args), sink, template=plantilla)

    pipe.bus.subscribe(lambda e: (
        print(f"  rep {e['n']:>2}  {e['score']['total']:5.1f} puntos   "
              f"(peor: {e['peor'][0]['feature']})")
        if e["type"] == "rep" else None
    ))

    print(f"Ejercicio: {ex.name}   base: {plantilla.n_reps} reps, tau={plantilla.tau:.3f}")
    print("Pulsa 'q' para terminar.\n")
    correr_con_ventana(pipe, f"GYMFITX · {ex.name}")

    if base.scores:
        print(f"\nSerie: {len(base.scores)} reps   "
              f"promedio {np.mean(base.scores):.1f}   mejor {max(base.scores):.1f}")
    else:
        print("\nNo se completo ninguna repeticion.")

    avisar_archivo(sink)
    if store:
        vl = pipe.sink_of(VideoLogger)
        if vl is not None and ses_id is not None:
            store.close_session(ses_id, vl.meta, vl.rutas)
        store.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
