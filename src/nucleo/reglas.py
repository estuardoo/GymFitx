"""Reglas de postura: un angulo medido en el cuadro contra un valor y una tolerancia. Dentro = verde, fuera = rojo.

Dos formas (segun lleve `c`):
  - sin `c`: la recta B->A contra la horizontal; 90 = recta (A justo encima de B).
  - con `c`: el angulo en el vertice B entre las rectas B->A y B->C (p. ej. hombro-cadera-rodilla).
Cada extremo es un punto o el promedio de varios. Codigos: C01..C33 = landmark MediaPipe + 1 (C01 = nariz, C24/C25 =
caderas), medidos sobre los 33 puntos del cuadro (no hace falta tenerlos en el catalogo de kpoints). D## / T##
= ese punto de la pierna DELANTERA / TRASERA (## = codigo de la pierna izquierda: D26 = rodilla delantera); la delantera es
la de la rodilla mas alta en la imagen. El angulo se mide en pixeles (corrige el aspecto del cuadro).
`lado`: ambos (|ang - angulo| <= tol), min (ang >= angulo - tol), max (ang <= angulo + tol). `fase: abajo` = solo se
evalua en la parte baja de la repeticion; `bajando` = durante el descenso y abajo (repeticion en curso). En la definicion: `reglas:` [{nombre, a, b, c?, angulo, tolerancia, unidad, lado,
fase, mensaje, activo}]."""

from __future__ import annotations

import math
import re

import numpy as np

_COD = re.compile(r"^([CDT])(\d{1,2})$", re.I)
UNIDADES = ("pct", "deg")
LADOS = ("ambos", "min", "max")
FASES = ("siempre", "bajando", "abajo")
RODILLA_IZQ, RODILLA_DER = 25, 26   # indices MediaPipe: definen cual pierna va delante


def _parte(codigo):
    m = _COD.match(str(codigo).strip())
    if not m or not 1 <= int(m.group(2)) <= 33:
        raise ValueError(f"punto invalido '{codigo}': usa C01..C33 (C01 = nariz), D## o T##")
    letra, n = m.group(1).upper(), int(m.group(2))
    if letra != "C" and not (12 <= n <= 32 and n % 2 == 0):
        raise ValueError(f"'{codigo}': D/T llevan el codigo del lado izquierdo (par, de C12 a C32)")
    return letra, n


def indice(codigo, izq_delante: bool = True) -> int:
    """Indice MediaPipe (0..32). D/T dependen de que pierna va delante."""
    letra, n = _parte(codigo)
    if letra == "C":
        return n - 1
    izq = izq_delante if letra == "D" else not izq_delante
    return n - 1 if izq else n


def _puntos(v):
    if isinstance(v, str):
        v = [p for p in re.split(r"[,\s]+", v) if p]
    v = [f"{_parte(p)[0]}{_parte(p)[1]:02d}" for p in v]
    if not 1 <= len(v) <= 4:
        raise ValueError("cada extremo lleva de 1 a 4 puntos (se promedian)")
    return v


def validar(reglas) -> list[dict]:
    """Normaliza y valida; ValueError con un mensaje para el panel."""
    out = []
    for i, r in enumerate(reglas or [], 1):
        nombre = str(r.get("nombre") or "").strip()
        if not nombre:
            raise ValueError(f"regla {i}: falta el nombre")
        unidad, lado, fase = r.get("unidad", "pct"), r.get("lado") or "ambos", r.get("fase") or "siempre"
        for v, ok, campo in ((unidad, UNIDADES, "unidad"), (lado, LADOS, "lado"), (fase, FASES, "fase")):
            if v not in ok:
                raise ValueError(f"regla '{nombre}': {campo} debe ser {' o '.join(ok)}")
        try:
            angulo, tol = float(r.get("angulo", 90)), float(r.get("tolerancia", 8))
        except (TypeError, ValueError):
            raise ValueError(f"regla '{nombre}': angulo y tolerancia deben ser numeros") from None
        if not 0 <= angulo <= 180 or tol < 0 or (tol == 0 and lado == "ambos"):
            raise ValueError(f"regla '{nombre}': angulo 0-180 y tolerancia mayor que 0 (0 solo con lado min/max)")
        try:
            a, b = _puntos(r.get("a")), _puntos(r.get("b"))
            c = _puntos(r["c"]) if r.get("c") else []
        except ValueError as e:
            raise ValueError(f"regla '{nombre}': {e}") from None
        out.append({"nombre": nombre, "a": a, "b": b, "c": c, "angulo": angulo, "tolerancia": tol, "unidad": unidad,
                    "lado": lado, "fase": fase, "mensaje": str(r.get("mensaje") or "").strip(),
                    "activo": r.get("activo") is not False})
    return out


def tolerancia_deg(r) -> float:
    return r["tolerancia"] * r["angulo"] / 100.0 if r["unidad"] == "pct" else r["tolerancia"]


def _punto(pts, codigos, izq_delante, tam):
    return pts[[indice(c, izq_delante) for c in codigos], :2].mean(axis=0) * tam


def evaluar(reglas, screen, ancho, alto, fases=FASES) -> list[dict]:
    """screen: (N,>=2) normalizado 0-1. Devuelve por regla activa {nombre, angulo, desvio, ok, mensaje, pa, pb[, pc]}
    (puntos en pixeles, para dibujar); las que no se pueden medir o no son de una de las `fases` activas se omiten."""
    out = []
    pts = np.asarray(screen, dtype=np.float64)
    izq_delante = bool(pts[RODILLA_IZQ, 1] <= pts[RODILLA_DER, 1])   # y de imagen: menor = mas alta = delante
    tam = (ancho, alto)
    for r in reglas or []:
        if r.get("activo") is False or (r.get("fase", "siempre") != "siempre" and r["fase"] not in fases):
            continue
        a, b = _punto(pts, r["a"], izq_delante, tam), _punto(pts, r["b"], izq_delante, tam)
        c = _punto(pts, r["c"], izq_delante, tam) if r.get("c") else None
        if not all(np.isfinite(p).all() for p in (a, b) if p is not None) or (c is not None and not np.isfinite(c).all()):
            continue
        if np.allclose(a, b) or (c is not None and np.allclose(c, b)):
            continue
        if c is None:
            ang = math.degrees(math.atan2(b[1] - a[1], a[0] - b[0]))   # y de imagen crece hacia abajo
            dif = (ang - r["angulo"] + 180.0) % 360.0 - 180.0
        else:
            va, vc = a - b, c - b
            ang = math.degrees(math.acos(float(np.clip(va @ vc / (np.linalg.norm(va) * np.linalg.norm(vc)), -1, 1))))
            dif = ang - r["angulo"]
        tol, lado = tolerancia_deg(r), r.get("lado", "ambos")
        ok = dif >= -tol if lado == "min" else dif <= tol if lado == "max" else abs(dif) <= tol
        e = {"nombre": r["nombre"], "angulo": round(ang, 1), "desvio": round(abs(dif), 1), "ok": bool(ok),
             "mensaje": r.get("mensaje", ""), "pa": (int(a[0]), int(a[1])), "pb": (int(b[0]), int(b[1]))}
        if c is not None:
            e["pc"] = (int(c[0]), int(c[1]))
        out.append(e)
    return out
