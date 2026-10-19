"""Reprocesa una grabacion por el mismo pipeline, sin camara.

    python apps/replay.py --video recordings/2026-08-25/073012_mano_apertura_serie.mp4
    python apps/replay.py --video ... --exercise mano_apertura --modo grabar

Para esto se archivan los videos crudos. Sirve para:
  - recalibrar la plantilla con otros umbrales sobre la MISMA ejecucion
  - reevaluar sesiones viejas despues de cambiar el YAML del ejercicio
  - comparar como te movias hace un mes contra hoy

Como VideoSource y CameraSource comparten interfaz, el pipeline no nota la
diferencia: se ejecuta exactamente el mismo codigo que en vivo.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import _bootstrap  # noqa: F401
import numpy as np
from _common import cargar_ejercicio, cargar_plantilla, correr_con_ventana

from core.config import TEMPLATES_DIR
from core.pipeline import Evaluator, Pipeline, Recorder
from core.source import VideoSource
from core.template import template_path


def ejercicio_del_video(video: Path) -> str | None:
    meta = video.with_suffix(".json")
    if meta.exists():
        try:
            return json.loads(meta.read_text(encoding="utf-8"))["exercise"]
        except Exception:
            return None
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Reprocesar una grabacion")
    ap.add_argument("--video", required=True)
    ap.add_argument("--exercise", help="por defecto, el que diga el .json de la grabacion")
    ap.add_argument("--modo", choices=["evaluar", "grabar"], default="evaluar")
    ap.add_argument("--realtime", action="store_true", help="reproducir a velocidad real")
    ap.add_argument("--sin-ventana", action="store_true")
    args = ap.parse_args()

    video = Path(args.video)
    if not video.exists():
        raise SystemExit(f"No existe el video: {video}")

    slug = args.exercise or ejercicio_del_video(video)
    if not slug:
        raise SystemExit("No pude deducir el ejercicio. Pasa --exercise.")
    ex = cargar_ejercicio(slug)

    plantilla = None
    if args.modo == "evaluar":
        plantilla = cargar_plantilla(slug)
        sink = Evaluator(plantilla, storage=None)   # un reproceso no ensucia el historial
    else:
        sink = Recorder(template_path(TEMPLATES_DIR, slug))

    fuente = VideoSource(video, mirror=False, realtime=args.realtime)
    pipe = Pipeline(ex, fuente, sink, template=plantilla, annotate=not args.sin_ventana)
    pipe.bus.subscribe(lambda e: (
        print(f"  rep {e['n']:>2}  {e['score']['total']:5.1f} puntos")
        if e["type"] == "rep" else None
    ))

    print(f"Reprocesando {video.name}  ->  {ex.name}  (modo {args.modo})\n")
    if args.sin_ventana:
        pipe.run()
    else:
        correr_con_ventana(pipe, f"GYMFITX · replay · {video.name}")

    if args.modo == "evaluar":
        if sink.scores:
            print(f"\n{len(sink.scores)} reps   promedio {np.mean(sink.scores):.1f}   "
                  f"mejor {max(sink.scores):.1f}")
        else:
            print("\nNo se detectaron repeticiones completas en la grabacion.")
    elif sink.error:
        print(f"\nNo se pudo construir la plantilla: {sink.error}")
        return 1
    else:
        t = sink.template
        print(f"\nPlantilla recalibrada: {t.n_reps} reps, low={t.low:.2f} high={t.high:.2f} "
              f"tau={t.tau:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
