"""Que entra al vector del modelo: letras x, y, z (ejes de cada kpoint), a (angulos), p (proporciones y razones).

Los nombres de antes siguen valiendo: puntos=xyz, angulos=ap, ambos=xyzap. Lo comparten el SQL (al leer los
vectores), el vectorizador (vivo) y el entrenamiento, para que los tres armen exactamente lo mismo."""

from __future__ import annotations

_LEGADO = {"puntos": "xyz", "angulos": "ap", "ambos": "xyzap"}


def componentes(usar: str):
    """-> (indices de ejes, angulos?, proporciones?)"""
    u = _LEGADO.get(usar, usar or "")
    return [i for i, c in enumerate("xyz") if c in u], "a" in u, "p" in u


def mascara_metricas(tipos, usar: str, n: int) -> list[bool]:
    """Que columnas de metricas entran: proporciones y razones cuentan como 'p'; lo demas, angulos (sin tipos: angulos)."""
    _, con_ang, con_pro = componentes(usar)
    tipos = tipos or ["angle"] * n
    return [con_pro if t in ("proporcion", "distance_ratio") else con_ang for t in tipos]
