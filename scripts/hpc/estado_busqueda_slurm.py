#!/usr/bin/env python3
"""Tabla de avance de una corrida de busqueda_features_slurm.py -- lee los <salida>.estado.json que cada
tarea del array va sobreescribiendo sola (uno por tarea, actualizado cada vez que termina una combinacion) y
arma una tabla: cuanto avanzo cada tarea, si ya termino o si fallo. Standalone a proposito, solo libreria
estandar (nada de numpy/sklearn) -- se puede correr en el login node del cluster en cualquier momento,
incluso con el job todavia corriendo, aunque el modulo de python/scikit-learn este roto.

    python estado_busqueda_slurm.py --resultados resultados/

'terminado' en false para una tarea que ya no aparece en squeue/sacct = fallo (revisa su .err); en false y
sigue en squeue = normal, todavia corriendo."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def leer_estados(carpeta: Path) -> list[dict]:
    filas = []
    for a in sorted(carpeta.glob("*.estado.json")):
        try:
            filas.append(json.loads(a.read_text(encoding="utf-8")))
        except Exception as e:
            filas.append({"tarea": a.stem, "objetivo": None, "combos": None, "error": f"no se pudo leer: {e}"})
    filas.sort(key=lambda f: f.get("tarea", 0) if isinstance(f.get("tarea"), int) else 0)
    return filas


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--resultados", default=".", help="carpeta con los <salida>.estado.json (default: aqui)")
    ap.add_argument("--csv", default="", help="tambien guarda la tabla en este .csv (opcional)")
    args = ap.parse_args(argv)

    carpeta = Path(args.resultados)
    filas = leer_estados(carpeta)
    if not filas:
        raise SystemExit(f"Sin *.estado.json en {carpeta} -- ninguna tarea arranco todavia, o --salida no coincide con --resultados")

    anc = max(len(str(f.get("tarea", ""))) for f in filas)
    print(f"{'tarea':>{anc}}  {'avance':>13}  {'%':>6}  {'filas':>7}  estado")
    for f in filas:
        avance = f"{f.get('combos', '?')}/{f.get('objetivo', '?')}"
        pct = f.get("pct")
        pct_s = f"{pct:.1f}" if isinstance(pct, int | float) else "?"
        estado = f"ERROR: {f['error']}" if f.get("error") else ("terminado" if f.get("terminado") else "corriendo")
        print(f"{str(f.get('tarea', '')):>{anc}}  {avance:>13}  {pct_s:>6}  {str(f.get('filas', '?')):>7}  {estado}")

    n = len(filas)
    hechas = sum(1 for f in filas if f.get("terminado"))
    fallidas = sum(1 for f in filas if f.get("error"))
    print(f"\n{hechas}/{n} tareas terminadas" + (f", {fallidas} con error" if fallidas else ""))

    if args.csv:
        import csv as _csv
        campos = ["tarea", "n_tareas", "combos", "objetivo", "pct", "filas", "terminado", "error", "actualizado"]
        with open(args.csv, "w", newline="", encoding="utf-8") as fh:
            w = _csv.DictWriter(fh, fieldnames=campos)
            w.writeheader()
            for f in filas:
                w.writerow({k: f.get(k, "") for k in campos})
        print(f"tabla guardada en {args.csv}")


if __name__ == "__main__":
    main()
