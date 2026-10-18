"""Reproduce un archivo como fuente de cuadros (tests, reprocesar sin camara)."""

from __future__ import annotations

import time
from collections.abc import Iterator
from pathlib import Path

import cv2

from src.captura.fuentes.base import BaseSource
from src.nucleo.tipos import Frame


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
