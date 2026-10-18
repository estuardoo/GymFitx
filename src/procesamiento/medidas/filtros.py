"""One Euro Filter vectorizado y consciente de las unidades.

Por que no una media movil: mete un retardo constante que desplaza la señal en
el tiempo y desalinea el DTW, que es justo lo que estamos midiendo. El One Euro
adapta su frecuencia de corte a la velocidad: filtra fuerte cuando estas quieto
(donde el ruido molesta) y casi no filtra cuando te mueves rapido (donde el
retardo molesta).

Detalle que suele hacerse mal: beta multiplica la velocidad de la señal, asi que
su valor depende de las UNIDADES. Un angulo se mueve a ~60 grados/s y una razon
de distancia a ~0.8/s; con un beta unico, la razon quedaria sobrefiltrada y con
retardo. Aqui la velocidad se divide primero por el rango tipico de cada feature,
de modo que beta es adimensional y significa lo mismo para todas.
"""

from __future__ import annotations

import numpy as np

DOS_PI = 2.0 * np.pi

# Rango tipico de cada tipo de feature, usado para adimensionalizar la velocidad.
RANGO = {"deg": 180.0, "ratio": 2.0}


def _alpha(cutoff: np.ndarray | float, dt: float) -> np.ndarray:
    tau = 1.0 / (DOS_PI * np.asarray(cutoff, dtype=np.float32))
    return 1.0 / (1.0 + tau / dt)


class OneEuroFilter:
    def __init__(
        self,
        size: int,
        units: list[str] | None = None,
        min_cutoff: float = 2.5,
        beta: float = 27.0,
        d_cutoff: float = 1.0,
    ) -> None:
        self.min_cutoff = float(min_cutoff)
        self.beta = float(beta)
        self.d_cutoff = float(d_cutoff)
        self.scale = np.array(
            [RANGO.get(u, 1.0) for u in (units or ["deg"] * size)], dtype=np.float32
        )
        self._x_prev = np.full(size, np.nan, dtype=np.float32)
        self._dx_prev = np.zeros(size, dtype=np.float32)
        self._t_prev: int | None = None

    def reset(self) -> None:
        self._x_prev[:] = np.nan
        self._dx_prev[:] = 0.0
        self._t_prev = None

    def update(self, x: np.ndarray, t_ms: int) -> np.ndarray:
        x = x.astype(np.float32, copy=False)
        if self._t_prev is None:
            self._t_prev = t_ms
            self._x_prev = x.copy()
            return x

        dt = max((t_ms - self._t_prev) / 1000.0, 1e-3)
        self._t_prev = t_ms

        # Un NaN nuevo no debe contaminar el estado: se arrastra el ultimo valido.
        nuevo = np.isnan(self._x_prev) & ~np.isnan(x)
        self._x_prev = np.where(nuevo, x, self._x_prev)

        dx = (x - self._x_prev) / dt
        a_d = _alpha(self.d_cutoff, dt)
        self._dx_prev = np.where(np.isnan(dx), self._dx_prev,
                                 a_d * dx + (1 - a_d) * self._dx_prev).astype(np.float32)

        # Velocidad adimensional: asi beta significa lo mismo en grados y en razones.
        cutoff = self.min_cutoff + self.beta * np.abs(self._dx_prev) / self.scale
        a = _alpha(cutoff, dt)

        self._x_prev = np.where(np.isnan(x), self._x_prev,
                                a * x + (1 - a) * self._x_prev).astype(np.float32)
        return self._x_prev.copy()
