#!/bin/bash
# sbatch para scripts/hpc/resumen_busqueda_slurm.py SOLO (sin la busqueda): para cuando la busqueda ya termino, o
# se corto pero los .csv que ya estan en resultados/ alcanzan, y queres armar/actualizar el resumen
# (detalle.csv, matriz_resumen.csv, graficos/, resumen.txt) como un job aparte -- en vez de a mano en el
# login node (algunos clusters no dejan correr nada pesado ahi) o de esperar a que termine todo el array.
# Si en cambio todavia no corriste la busqueda: usa lanzar_manguito_rotador.sh (encadena busqueda + este
# mismo resumen solo, automatico) o corre resumen_busqueda_slurm.py a mano en tu PC (no hace falta el
# cluster para eso). Reusa el MISMO modulo/venv que slurm_manguito_rotador.sbatch -- necesita ADEMAS
# matplotlib instalado (la busqueda no lo usa, el resumen si, para los graficos).
#
#   sbatch slurm_resumen_manguito_rotador.sbatch

#SBATCH --job-name=gymfit_resumen_manguito_rotador
#SBATCH --partition=standard
#SBATCH --time=00:15:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=1
#SBATCH --output=logs/resumen_%j.out

module load python/scikit-learn   # o: source /ruta/a/tu/venv/bin/activate (o conda activate <env>) -- ADEMAS necesita matplotlib

mkdir -p logs resumen_manguito_rotador

python resumen_busqueda_slurm.py --csv "resultados/resultados_*.csv" --salida resumen_manguito_rotador/

echo "Listo: resumen_manguito_rotador/ (detalle.csv, matriz_resumen.csv, graficos/, resumen.txt)"
