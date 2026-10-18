"""Utilidades compartidas por los scripts de linea de comandos.

Existe para que record, evaluate, replay y serve no dupliquen el armado del
pipeline: la unica diferencia real entre ellos es el sumidero y la fuente.
"""

from __future__ import annotations

import threading

import cv2

from src.captura.fuentes.camara import CameraSource
from src.evaluacion.plantilla import Template, template_path
from src.nucleo.config import EXERCISES_DIR, RECORDINGS_DIR, TEMPLATES_DIR
from src.nucleo.ejercicio import load_exercise
from src.sesion.grabacion import VideoLogger
from src.sesion.pipeline import MultiSink, Pipeline, Sink


def cargar_ejercicio(slug: str):
    ruta = EXERCISES_DIR / f"{slug}.yaml"
    if not ruta.exists():
        disponibles = ", ".join(sorted(p.stem for p in EXERCISES_DIR.glob("*.yaml")))
        raise SystemExit(f"No existe el ejercicio '{slug}'. Disponibles: {disponibles}")
    return load_exercise(ruta)


def cargar_plantilla(slug: str) -> Template:
    ruta = template_path(TEMPLATES_DIR, slug)
    if not ruta.exists():
        raise SystemExit(
            f"'{slug}' todavia no tiene movimiento base.\n"
            f"Grabalo con:  python scripts/grabar.py --exercise {slug}"
        )
    return Template.load(ruta)


def con_archivo(principal: Sink, archivar: bool = True, video: bool = True,
                max_width: int = 0, codec: str = "mp4v") -> Sink:
    """Compone el sumidero principal con el archivador de la sesion.

    Toda sesion queda archivada salvo que se pida lo contrario: los videos
    y las features sirven despues para reanalizar, reentrenar o comparar
    contra el pasado, y no se pueden recuperar si no se guardaron.
    """
    if not archivar:
        return principal
    return MultiSink(principal,
                     VideoLogger(RECORDINGS_DIR, guardar_video=video,
                                 max_width=max_width, codec=codec))


def correr_con_ventana(pipe: Pipeline, titulo: str) -> None:
    """Corre el pipeline en un hilo y muestra su ultimo cuadro anotado."""
    detener = threading.Event()
    hilo = threading.Thread(target=pipe.run, args=(detener.is_set,), daemon=True)
    hilo.start()
    try:
        while hilo.is_alive():
            img = pipe.latest_frame
            if img is not None:
                cv2.imshow(titulo, img)
            if (cv2.waitKey(15) & 0xFF) in (ord("q"), 27):
                detener.set()
                break
    finally:
        detener.set()
        hilo.join(timeout=10)
        cv2.destroyAllWindows()


def camara(args) -> CameraSource:
    return CameraSource(
        index=args.camera, width=args.width, height=args.height, mirror=not args.no_mirror
    )


def agregar_flags_comunes(ap) -> None:
    ap.add_argument("--camera", type=int, default=0)
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--height", type=int, default=720)
    ap.add_argument("--no-mirror", action="store_true")
    ap.add_argument("--no-archivo", action="store_true",
                    help="no archivar esta sesion (ni video ni features)")
    ap.add_argument("--sin-video", action="store_true",
                    help="archivar features y metadatos, pero no el video")
    ap.add_argument("--video-ancho", type=int, default=0, metavar="PX",
                    help="reducir el video archivado a este ancho (0 = resolucion de captura)")
    ap.add_argument("--video-codec", default="mp4v", metavar="FOURCC",
                    help="mp4v (por defecto, siempre disponible) o avc1 (pesa ~3x menos)")


def avisar_archivo(sink) -> None:
    vl = sink.find(VideoLogger) if isinstance(sink, MultiSink) else None
    if vl is None:
        return
    if vl.video_path:
        mb = vl.video_path.stat().st_size / 1e6 if vl.video_path.exists() else 0
        print("\nSesion archivada:")
        print(f"  video    {vl.video_path}  ({mb:.1f} MB, {vl.codec}, "
              f"{vl._tam[0]}x{vl._tam[1]})")
    else:
        print("\nSesion archivada (sin video):")
    print(f"  features {vl.npz_path}")
    print(f"  metadatos{'':1} {vl.json_path}")
