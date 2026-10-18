"""CLI de src/entrenamiento/exportar_slurm.py -- ver ese archivo para el flujo completo (exportar aqui,
correr scripts/busqueda_features_slurm.py en el cluster).

    python scripts/exportar_dataset_slurm.py --ejercicio manguito_rotador
    python scripts/exportar_dataset_slurm.py --ejercicio manguito_rotador --out otra_ruta.npz
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # para 'from src...' sin instalar el paquete

from src.entrenamiento.exportar_slurm import exportar
from src.nucleo.config import SLURM_DIR

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ejercicio", required=True, help="nombre del .yaml en ejercicios/ (sin extension)")
    ap.add_argument("--out", default=None, help="default: datos/slurm/<ejercicio>.npz")
    args = ap.parse_args()
    out = args.out or SLURM_DIR / f"{args.ejercicio}.npz"
    resumen = exportar(args.ejercicio, out)
    print(f"{resumen['clips']} clips ({resumen['clases']}), {resumen['frames_por_clip']} cuadros/clip, "
          f"{resumen['kpoints']} kpoints, {resumen['metricas']} metricas -> {resumen['archivo']}")
