"""Fuentes de cuadros. Camara y archivo comparten interfaz a proposito.

Esa igualdad es lo que permite desarrollar y probar el comparador entero sin
webcam: grabas un video una vez y lo reproduces, con resultados identicos en
cada corrida. Sin esto, cada prueba del DTW exigiria pararse frente a la camara.
"""

from __future__ import annotations

import subprocess
import sys
import time
from collections.abc import Iterator
from pathlib import Path

import cv2

from .types import Frame


def _backends() -> list[int]:
    # DSHOW arranca rapido (~1s) pero algunos drivers USB le devuelven cuadros
    # en negro o no abren; MSMF es mas lento pero suele abrir lo que DSHOW no
    # puede. Se prueban los dos, en ese orden, y se usa el primero que sirva.
    if sys.platform.startswith("win"):
        return [cv2.CAP_DSHOW, cv2.CAP_MSMF]
    return [cv2.CAP_ANY]


def _abrir(index: int):
    """Prueba cada backend hasta encontrar uno que de un cuadro real.

    Devuelve (cap_abierto, ultimo_cuadro) o (None, None) si ninguno respondio.
    El primer cuadro tras abrir suele salir negro o fallar del todo en varias
    camaras USB, por eso los reintentos con una pausa corta antes de descartar
    el indice.
    """
    for backend in _backends():
        cap = cv2.VideoCapture(index, backend)
        if not cap.isOpened():
            cap.release()
            continue
        ok, frame = False, None
        for _ in range(4):
            ok, frame = cap.read()
            if ok:
                break
            time.sleep(0.1)
        if ok:
            return cap, frame
        cap.release()
    return None, None


def nombres_camaras_windows() -> list[str]:
    """Camaras que Windows mismo ve conectadas (PnP), sin pasar por OpenCV.

    Sirve para distinguir "no hay camara" de "hay camara pero OpenCV no
    pudo abrirla" (permisos de Windows, en uso por otra app, driver): si
    esto encuentra nombres y list_cameras() no encuentra nada, el problema
    esta en el acceso, no en el hardware.
    """
    if not sys.platform.startswith("win"):
        return []
    try:
        r = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Get-CimInstance Win32_PnPEntity | "
             "Where-Object { $_.PNPClass -eq 'Camera' -or $_.PNPClass -eq 'Image' } | "
             "Select-Object -ExpandProperty Name"],
            capture_output=True, text=True, timeout=6,
        )
        return [n.strip() for n in r.stdout.splitlines() if n.strip()]
    except Exception:
        return []


def nombres_dshow() -> list[str]:
    """Nombres reales de camara, EN EL MISMO ORDEN que cv2.CAP_DSHOW les
    asigna indice (consulta el mismo grafo DirectShow que usa OpenCV, a
    diferencia de nombres_camaras_windows() que lee el PnP general y puede
    no coincidir en orden). Es lo que deja mostrar "Logitech C920" en vez
    de "Camara 0" en el selector del panel.
    """
    if not sys.platform.startswith("win"):
        return []
    try:
        from pygrabber.dshow_graph import FilterGraph
        return FilterGraph().get_input_devices()
    except Exception:
        return []


def list_cameras(max_index: int = 8) -> list[dict]:
    """Prueba los indices 0..max_index-1 y devuelve los que responden con imagen.

    Usado tanto por check_camera.py como por el endpoint /api/cameras del
    panel: un solo lugar que sabe como sondear camaras, sin duplicar la logica
    entre la CLI y el servidor.
    """
    nombres = nombres_dshow()
    encontradas: list[dict] = []
    for i in range(max_index):
        cap, frame = _abrir(i)
        if cap is None:
            continue
        h, w = frame.shape[:2]
        nombre = nombres[i] if i < len(nombres) else f"Cámara {i}"
        encontradas.append({"index": i, "width": w, "height": h, "name": nombre})
        cap.release()
    return encontradas


class BaseSource:
    def frames(self) -> Iterator[Frame]:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, *exc) -> None:
        self.close()


class CameraSource(BaseSource):
    def __init__(
        self,
        index: int = 0,
        width: int = 1280,
        height: int = 720,
        mirror: bool = True,
        fps: int = 30,
    ) -> None:
        self._cap, _ = _abrir(index)
        if self._cap is None:
            raise RuntimeError(
                f"No se pudo abrir la camara {index}. "
                f"Corre 'python check_camera.py' para ver cual responde."
            )
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        # No todos los drivers respetan esto (algunos ignoran el pedido y se
        # quedan en su fps nativo); el FPS real siempre se ve en el overlay
        # del video, asi que es facil notar si la camara no lo soporta.
        self._cap.set(cv2.CAP_PROP_FPS, fps)
        self._cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.mirror = mirror
        self.index = index

    def frames(self) -> Iterator[Frame]:
        t0 = time.perf_counter()
        last_ms = -1
        i = 0
        while True:
            ok, image = self._cap.read()
            if not ok:
                return
            if self.mirror:
                image = cv2.flip(image, 1)
            # MediaPipe exige timestamps estrictamente crecientes.
            t_ms = max(int((time.perf_counter() - t0) * 1000), last_ms + 1)
            last_ms = t_ms
            yield Frame(image=image, t_ms=t_ms, index=i)
            i += 1

    def set_fps(self, fps: int) -> bool:
        """Pide un nuevo FPS a la camara YA ABIERTA, sin reabrirla (evita el
        corte visible de apagar+prender). Devuelve si el driver acepto el
        pedido -- no siempre lo respeta de verdad; el FPS real siempre se ve
        en el overlay del video, asi que un valor que no aplica se nota ahi.
        """
        return bool(self._cap.set(cv2.CAP_PROP_FPS, fps))

    def close(self) -> None:
        self._cap.release()


class VideoSource(BaseSource):
    """Reproduce un archivo. Usado por los tests y para depurar sin camara."""

    def __init__(self, path: str | Path, mirror: bool = False, realtime: bool = False) -> None:
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(self.path)
        self._cap = cv2.VideoCapture(str(self.path))
        self.mirror = mirror
        self.realtime = realtime

    def frames(self) -> Iterator[Frame]:
        last_ms = -1
        i = 0
        wall0 = time.perf_counter()
        while True:
            ok, image = self._cap.read()
            if not ok:
                return
            if self.mirror:
                image = cv2.flip(image, 1)
            t_ms = max(int(self._cap.get(cv2.CAP_PROP_POS_MSEC)), last_ms + 1)
            last_ms = t_ms
            if self.realtime:
                espera = t_ms / 1000.0 - (time.perf_counter() - wall0)
                if espera > 0:
                    time.sleep(espera)
            yield Frame(image=image, t_ms=t_ms, index=i)
            i += 1

    def close(self) -> None:
        self._cap.release()
