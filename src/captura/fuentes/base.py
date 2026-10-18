"""Interfaz comun de las fuentes de cuadros: el pipeline no distingue camara de video."""

from __future__ import annotations

from collections.abc import Iterator

from src.nucleo.tipos import Frame


class BaseSource:
    # en_vivo=True: el pipeline captura en un hilo propio y procesa siempre el
    # cuadro mas reciente (descarta los que no alcanza a procesar). False:
    # procesa TODOS los cuadros en orden (videos, tests: resultado repetible).
    en_vivo = False
    motivo_fin: str | None = None   # por que termino frames() (si no fue un stop pedido)

    def frames(self) -> Iterator[Frame]:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, *exc) -> None:
        self.close()
