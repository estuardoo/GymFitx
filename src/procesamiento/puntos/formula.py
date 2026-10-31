"""Formulas entre kpoints para normalizar (Kpoints -> Normalizacion): `medio(C24,C25)`, `dist(medio(C12,C13), medio(C24,C25))`.

C<nn> = el punto del cuerpo con ese codigo FIJO, igual en todos los ejercicios (landmark de MediaPipe + 1: C01 nariz, C12/C13 hombros,
C24/C25 caderas...). Tiene que estar marcado en los kpoints del ejercicio. (K<n> = la posicion en la lista de un ejercicio: formato viejo,
solo se lee para modelos ya entrenados; las formulas nuevas no lo aceptan.) Dos tipos de valor:
  punto  (x,y por cuadro)      C24 · medio(a,b) · prom(a,b,..) · punto±punto · punto*numero · punto/numero
  numero (un valor por cuadro) dist(a,b) · max(n,..) · min(n,..) · numero (2, 0.5) · numero±*/ numero
Solo x e y. Se lee el texto con `ast` y se camina el arbol permitido: nunca se ejecuta codigo (no hay eval)."""

from __future__ import annotations

import ast
import re

import numpy as np

_K = re.compile(r"^[CcKk](\d{1,3})$")
LARGO_MAX = 120
_FUNCIONES = {"medio": (2, 2), "prom": (1, 8), "dist": (2, 2), "max": (1, 8), "min": (1, 8)}


def _arbol(texto: str):
    texto = (texto or "").strip()
    if not texto:
        raise ValueError("la formula esta vacia")
    if len(texto) > LARGO_MAX:
        raise ValueError(f"la formula pasa de {LARGO_MAX} caracteres")
    try:
        return ast.parse(texto, mode="eval").body
    except SyntaxError:
        raise ValueError(f"no se entiende la formula '{texto}'") from None


def usados(texto: str) -> list[int]:
    """Numeros de punto (C<nn>) que nombra la formula (sin repetir, en orden)."""
    return sorted({int(m) for m in re.findall(r"\b[CcKk](\d{1,3})\b", texto or "")})


def _ev(n, K):
    """-> ('p'|'n', array): 'p' (T,2) punto, 'n' (T,1) numero (las constantes (1,1) se difunden)."""
    if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)) and not isinstance(n.value, bool):
        return "n", np.full((1, 1), float(n.value))
    if isinstance(n, ast.Name):
        m = _K.match(n.id)
        if not m:
            raise ValueError(f"'{n.id}' no es un punto: usa C<nn> (ej. C24 = cadera izquierda)")
        if int(m.group(1)) not in K:
            raise ValueError(f"C{int(m.group(1)):02d}: ese punto no esta marcado en los kpoints del ejercicio")
        return "p", K[int(m.group(1))]
    if isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.USub, ast.UAdd)):
        t, v = _ev(n.operand, K)
        return t, -v if isinstance(n.op, ast.USub) else v
    if isinstance(n, ast.BinOp) and isinstance(n.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
        (ta, a), (tb, b) = _ev(n.left, K), _ev(n.right, K)
        op = type(n.op)
        if op in (ast.Add, ast.Sub):
            if ta != tb:
                raise ValueError("solo se suma/resta punto con punto o numero con numero")
            return ta, a + b if op is ast.Add else a - b
        if op is ast.Mult:
            if ta == "p" and tb == "p":
                raise ValueError("no se multiplica punto por punto")
            return ("p" if "p" in (ta, tb) else "n"), a * b
        if tb != "n":
            raise ValueError("solo se divide por un numero (ej. dist(..))")
        with np.errstate(divide="ignore", invalid="ignore"):
            return ta, a / b
    if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in _FUNCIONES and not n.keywords:
        f, (lo, hi) = n.func.id, _FUNCIONES[n.func.id]
        if not lo <= len(n.args) <= hi:
            raise ValueError(f"{f}() lleva {lo if lo == hi else f'{lo} a {hi}'} argumentos")
        vals = [_ev(a, K) for a in n.args]
        if f in ("medio", "prom", "dist"):
            if any(t != "p" for t, _ in vals):
                raise ValueError(f"{f}() trabaja con puntos (C.. o medio/prom)")
            if f == "dist":
                with np.errstate(invalid="ignore"):
                    return "n", np.linalg.norm(vals[0][1] - vals[1][1], axis=-1, keepdims=True)
            return "p", sum(v for _, v in vals) / len(vals)
        if any(t != "n" for t, _ in vals):
            raise ValueError(f"{f}() trabaja con numeros (ej. dist(..))")
        return "n", (np.maximum if f == "max" else np.minimum).reduce([v for _, v in vals])
    raise ValueError("formula no permitida: usa K<numero>, medio, prom, dist, max, min, numeros y + - * /")


def validar(texto: str, tipo: str, numeros) -> None:
    """ValueError con un mensaje para el panel. tipo: 'p' (origen) o 'n' (escala); numeros = kpoints que existen."""
    if re.search(r"\b[Kk]\d", texto or ""):
        raise ValueError("usa C<nn> (igual en todos los ejercicios), no K: ej. C24 = cadera izquierda")
    K = {int(k): np.ones((2, 2)) * (i + 1) for i, k in enumerate(numeros)}
    t, _ = _ev(_arbol(texto), K)
    if t != tipo:
        raise ValueError("el origen debe dar un punto (ej. medio(C24,C25))" if tipo == "p"
                         else "la escala debe dar un numero (ej. dist(C12,C24))")


def evaluar(texto: str, K: dict[int, np.ndarray], tipo: str) -> np.ndarray:
    """K = {numero: (T,2)} -> (T,2) para 'p' o (T,) para 'n'. NaN donde falte un punto."""
    t, v = _ev(_arbol(texto), K)
    if t != tipo:
        raise ValueError("la formula no da " + ("un punto" if tipo == "p" else "un numero"))
    T = len(next(iter(K.values()))) if K else 1
    v = np.broadcast_to(v, (T, 2 if tipo == "p" else 1))
    return v if tipo == "p" else v[:, 0]
