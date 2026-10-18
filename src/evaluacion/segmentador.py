"""Capa 5: recorta repeticiones del flujo continuo de features.

Maquina de estados sobre una señal 1-D con histeresis de dos umbrales. La
histeresis es lo que evita que un temblor en la zona de cambio dispare veinte
repeticiones falsas.

Los dos umbrales NO se escriben a mano en ningun lado: salen de los percentiles
de la propia grabacion base (ver template.build_template). Cero numeros magicos.

Truco para no duplicar logica: 'up_down' se resuelve invirtiendo el signo de la
señal y de los umbrales, y reusando exactamente el mismo codigo de 'down_up'.
"""

from __future__ import annotations

import numpy as np

from src.nucleo.tipos import FeatureVec, Segment

ESPERANDO_ALTO = "esperando_alto"
EN_ALTO = "en_alto"
BAJANDO = "bajando"
EN_BAJO = "en_bajo"


class RepSegmenter:
    def __init__(
        self,
        n_features: int,
        signal_idx: np.ndarray,
        reduce: str,
        low: float,
        high: float,
        direction: str = "down_up",
        min_duration_ms: int = 600,
        max_duration_ms: int = 8000,
        capacity: int = 600,
        fin: float | None = None,
    ) -> None:
        if high <= low:
            raise ValueError(f"Umbrales invalidos: low={low} high={high}")
        self.flip = -1.0 if direction == "up_down" else 1.0
        self.low = low * self.flip if self.flip > 0 else -high
        self.high = high * self.flip if self.flip > 0 else -low
        # la rep se cuenta al volver a la posicion inicial (`fin`, >= high); solo down_up
        self.fin = max(fin, self.high) if fin is not None and self.flip > 0 else self.high
        self.signal_idx = signal_idx
        self.reduce = reduce
        self.min_duration_ms = min_duration_ms
        self.max_duration_ms = max_duration_ms

        # Buffer preasignado: cero allocaciones por cuadro.
        self._buf = np.empty((capacity, n_features), dtype=np.float32)
        self._t = np.empty(capacity, dtype=np.int64)
        self._n = 0
        self.capacity = capacity
        self._kp: list = [None] * capacity   # kpoints por cuadro (None si el cuadro no los trae)

        self.state = ESPERANDO_ALTO
        self.last_signal = float("nan")
        self.reps = 0

    def signal_of(self, values: np.ndarray) -> float:
        sub = values[self.signal_idx]
        if np.all(np.isnan(sub)):
            return float("nan")
        with np.errstate(invalid="ignore"):
            if self.reduce == "min":
                s = float(np.nanmin(sub))
            elif self.reduce == "max":
                s = float(np.nanmax(sub))
            else:
                s = float(np.nanmean(sub))
        return s

    def reset(self) -> None:
        self._n = 0
        self.state = ESPERANDO_ALTO

    def _push(self, fv: FeatureVec) -> bool:
        if self._n >= self.capacity:
            return False
        self._buf[self._n] = fv.values
        self._t[self._n] = fv.t_ms
        self._kp[self._n] = fv.kpoints
        self._n += 1
        return True

    def _emit(self) -> Segment:
        data = self._buf[: self._n].copy()
        kps = [k for k in self._kp[: self._n] if k is not None]
        seg = Segment(
            start_ms=int(self._t[0]),
            end_ms=int(self._t[self._n - 1]),
            data=data,
            valid=~np.isnan(data),
            kpoints=np.stack(kps) if kps and len({k.shape for k in kps}) == 1 else None,
        )
        self._n = 0
        self.reps += 1
        return seg

    def update(self, fv: FeatureVec) -> Segment | None:
        """Devuelve un Segment el cuadro en que se cierra una repeticion."""
        s_raw = self.signal_of(fv.values)
        self.last_signal = s_raw
        if np.isnan(s_raw):
            return None
        s = s_raw * self.flip

        if self.state == ESPERANDO_ALTO:
            if s >= self.high:
                self.state = EN_ALTO
            return None

        if self.state == EN_ALTO:
            if s < self.high:
                self._n = 0
                self._push(fv)
                self.state = BAJANDO
            return None

        # A partir de aqui hay una repeticion en curso.
        if not self._push(fv):
            self.reset()          # se paso del buffer: descarta y rearma
            return None

        transcurrido = int(self._t[self._n - 1] - self._t[0])
        if transcurrido > self.max_duration_ms:
            self.reset()
            return None

        if self.state == BAJANDO:
            if s <= self.low:
                self.state = EN_BAJO
            elif s >= self.high:   # subio sin llegar abajo: intento descartado, se rearma
                self.reset()
                self.state = EN_ALTO
            return None

        if self.state == EN_BAJO and s >= self.fin:
            if transcurrido < self.min_duration_ms:
                self.reset()      # movimiento demasiado brusco para ser una rep
                self.state = EN_ALTO
                return None
            seg = self._emit()
            self.state = EN_ALTO
            return seg

        return None
