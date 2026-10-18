"""Gesto de control: mantener una muneca en la esquina superior izquierda inicia/detiene la grabacion."""

from __future__ import annotations

from src.nucleo.landmarks import POSE_LANDMARKS

# Se usa la pose de 33 puntos que ya se calcula (cero costo extra): una muneca
# dentro de la esquina GESTO_MANTENER_MS seguidos = un disparo. Hay que salir
# de la zona para poder volver a disparar. (El modelo de pose no ve los dedos,
# por eso no es un "puno cerrado".)
_IDX_MUNECAS = (POSE_LANDMARKS.index("LEFT_WRIST"), POSE_LANDMARKS.index("RIGHT_WRIST"))

GESTO_RECORTE = 0.318         # esquina superior izquierda: lado = frac del cuadro
# ponytail: umbrales fijos (no calibrados por persona/camara)
GESTO_MANTENER_MS = 1000      # tiempo dentro de la zona para disparar
GESTO_ENFRIAMIENTO_MS = 1500  # tras un disparo, ignora otro por este tiempo
GESTO_OLVIDO_MS = 600         # si la muneca se pierde menos que esto, no cuenta como salida


class Gesto:
    """Muneca sostenida en la esquina = un disparo."""

    def __init__(self, al_disparar) -> None:
        self.estado: str | None = None   # "dentro" mientras hay una muneca en la zona, si no None
        self._al_disparar = al_disparar
        self._desde_ms: int | None = None
        self._armado = True              # False tras disparar, hasta que salga de la zona
        self._ultimo_disparo_ms: int | None = None
        self._ultima_vista_ms: int | None = None

    @staticmethod
    def en_zona(detecciones) -> bool:
        for d in detecciones:
            if d.source != "pose":
                continue
            for i in _IDX_MUNECAS:
                x, y = d.screen[i][:2]
                if 0 <= x < GESTO_RECORTE and 0 <= y < GESTO_RECORTE:
                    return True
        return False

    def evaluar(self, detecciones, t_ms: int) -> None:
        if self.avanzar(self.en_zona(detecciones), t_ms):
            self._al_disparar()

    def avanzar(self, dentro: bool, t_ms: int) -> bool:
        """Logica pura: True justo en el cuadro en que se cumple el tiempo dentro de la zona."""
        if not dentro:
            if self._ultima_vista_ms is None or t_ms - self._ultima_vista_ms > GESTO_OLVIDO_MS:
                self.estado, self._desde_ms, self._armado = None, None, True
            return False
        self._ultima_vista_ms = t_ms
        self.estado = "dentro"
        if self._desde_ms is None:
            self._desde_ms = t_ms
        if not self._armado or t_ms - self._desde_ms < GESTO_MANTENER_MS:
            return False
        if self._ultimo_disparo_ms is not None and t_ms - self._ultimo_disparo_ms < GESTO_ENFRIAMIENTO_MS:
            return False
        self._ultimo_disparo_ms, self._armado = t_ms, False
        return True

    def close(self) -> None:
        pass
