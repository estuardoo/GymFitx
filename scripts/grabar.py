"""Graba el movimiento base de un ejercicio y calibra su plantilla.

    python scripts/grabar.py --exercise mano_apertura

Haz 5 o mas repeticiones lentas y completas, volviendo siempre al punto de
partida. Al pulsar 'q' el sistema segmenta la toma, elige la repeticion medoide
y deriva umbrales, normalizacion y tau. Nada de eso se escribe a mano.

La toma queda archivada en input/raw/ (video + features), asi que siempre se
puede volver a calibrar sobre la misma grabacion con scripts/reprocesar.py.
"""

from __future__ import annotations

import argparse

from scripts._comun import (
    agregar_flags_comunes,
    avisar_archivo,
    camara,
    cargar_ejercicio,
    con_archivo,
    correr_con_ventana,
)
from src.evaluacion.plantilla import template_path
from src.nucleo.config import TEMPLATES_DIR
from src.sesion.pipeline import Pipeline, Recorder


def main() -> int:
    ap = argparse.ArgumentParser(description="Grabar movimiento base")
    ap.add_argument("--exercise", required=True)
    agregar_flags_comunes(ap)
    args = ap.parse_args()

    ex = cargar_ejercicio(args.exercise)
    salida = template_path(TEMPLATES_DIR, ex.slug)

    print(f"Ejercicio: {ex.name}")
    print(f"{ex.description.strip()}\n")
    print("Haz al menos 5 repeticiones lentas y completas. Pulsa 'q' para cerrar.\n")

    base = Recorder(salida)
    sink = con_archivo(base, archivar=not args.no_archivo,
                   video=not args.sin_video, max_width=args.video_ancho,
                   codec=args.video_codec)
    pipe = Pipeline(ex, camara(args), sink)
    correr_con_ventana(pipe, f"GYMFITX · grabando base · {ex.name}")

    if base.error:
        print(f"\nNo se pudo construir la plantilla: {base.error}")
        avisar_archivo(sink)
        print("\nLa toma quedo archivada: puedes reintentar la calibracion con")
        print(f"  python scripts/reprocesar.py --video <ruta del mp4> --exercise {ex.slug} --modo grabar")
        return 1

    t = base.template
    print(f"\nPlantilla guardada en {salida}")
    print(f"  repeticiones detectadas : {t.n_reps}")
    print(f"  referencia (medoide)    : {t.data.shape[0]} cuadros, {t.duration_ms} ms")
    print(f"  umbrales de histeresis  : low={t.low:.2f}  high={t.high:.2f}")
    print(f"  tau calibrado           : {t.tau:.3f}  (una rep tipica tuya = 90 puntos)")
    avisar_archivo(sink)
    print(f"\nYa puedes entrenar:  python scripts/evaluar.py --exercise {ex.slug}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
