#!/bin/bash
# Lanza TODO de un tiro: el array de busqueda (slurm_manguito_rotador.sbatch) y, recien cuando ESE array
# termine -- afterany, no afterok: asi arma igual el resumen con lo que se pudo aunque alguna tarea haya
# fallado -- el resumen (detalle.csv, matriz_resumen.csv, graficos/, resumen.txt), sin que tengas que volver
# a entrar al cluster y correr nada a mano. Reusa la MISMA linea de modulo/venv y particion que ya editaste
# en slurm_manguito_rotador.sbatch (las lee de ahi con grep -- si cambias una, no hace falta tocar la otra),
# asi que ajusta ese .sbatch primero como siempre. Eso si, para que el resumen (las graficas) funcione, ese
# modulo/venv necesita TAMBIEN matplotlib instalado, ademas de numpy/scikit-learn.
#
#   bash lanzar_manguito_rotador.sh
#
# Si preferis lanzar solo la busqueda (sin el resumen automatico), segui pudiendo: sbatch slurm_manguito_rotador.sbatch
set -e
cd "$(dirname "$0")"
mkdir -p logs resultados resumen_manguito_rotador

JID=$(sbatch --parsable slurm_manguito_rotador.sbatch)
echo "Busqueda (array): job $JID"

PART=$(grep '^#SBATCH --partition=' slurm_manguito_rotador.sbatch | head -1 | cut -d= -f2)
MODLINE=$(grep -E '^(module load|source |conda activate)' slurm_manguito_rotador.sbatch | head -1)
ARGS=(--parsable --dependency="afterany:${JID}" --job-name="gymfit_resumen_manguito_rotador"
      --time=00:15:00 --mem=4G --output="logs/resumen_%j.out")
[ -n "$PART" ] && ARGS+=(--partition="$PART")

RID=$(sbatch "${ARGS[@]}" --wrap="${MODLINE}; python resumen_busqueda_slurm.py --csv 'resultados/resultados_*.csv' --salida resumen_manguito_rotador/")
echo "Resumen (arranca solo, automatico, cuando el array de arriba termine): job $RID"
echo
echo "Avance de ambos:  squeue -u \$USER   o  python estado_busqueda_slurm.py --resultados resultados/"
echo "Cuando el job $RID termine, la matriz/graficos/resumen.txt quedan en resumen_manguito_rotador/"
