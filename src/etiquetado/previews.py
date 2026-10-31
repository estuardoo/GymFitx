"""Copia H.264 liviana de cada grabacion para el <video> del navegador (sistema/previews/)."""

from __future__ import annotations

import subprocess

from src.etiquetado.manifest import DATA, _slug
from src.nucleo.config import PREVIEWS_DIR


def ffmpeg_exe():
    """ffmpeg del sistema; si no hay (PC nueva), el que trae imageio-ffmpeg.
    Sin esto la vista previa daba error 500 (WinError 2) en una maquina sin ffmpeg."""
    import shutil
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        raise RuntimeError("No encuentro ffmpeg: instala con 'winget install Gyan.FFmpeg' "
                           "o 'pip install imageio-ffmpeg'") from None


PREVIEW = PREVIEWS_DIR


def preview_de(src):
    """El navegador no decodifica mp4v (fourcc de OpenCV); cachea una copia H.264 para poder verla."""
    PREVIEW.mkdir(exist_ok=True)
    # nombre plano por ruta relativa a DATA, no src.name: dos grabaciones de
    # dias distintos pueden compartir el mismo HHMMSS_modo.mp4 (ver _slug).
    dst = PREVIEW / (_slug(src.relative_to(DATA).as_posix()) + src.suffix)
    if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
        subprocess.run([ffmpeg_exe(), "-y", "-hide_banner", "-loglevel", "error", "-i", str(src),
                        "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                        "-movflags", "+faststart", "-an", str(dst)], check=True)
    return dst


def limpiar_preview_huerfanos() -> int:
    """Borra de sistema/previews las copias H.264 que ya no corresponden a
    ninguna grabacion (p.ej. las de nombre viejo '205448_base.mp4', de antes
    de _slug). Se regeneran solas al abrir el video. Devuelve cuantas borro."""
    if not PREVIEW.exists():
        return 0
    vigentes = {_slug(mp4.relative_to(DATA).as_posix()) for mp4 in DATA.rglob("*.mp4")}
    borrados = 0
    for f in PREVIEW.glob("*.mp4"):
        if f.stem not in vigentes:
            try:
                f.unlink()
                borrados += 1
            except OSError:
                pass
    return borrados
