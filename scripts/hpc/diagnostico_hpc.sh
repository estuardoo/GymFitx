#!/bin/bash
# Un solo script para correr en el LOGIN NODE del cluster (dentro de la carpeta descomprimida del zip de
# AHPC, junto al .npz y busqueda_features_slurm.py). Junta en un solo .txt todo lo necesario para decidir
# particion/paralelismo sin gastar cupo real: que particion tiene los nodos sin GPU, si estan libres ahora,
# los limites de cada particion, y (si encuentra el .npz) una prueba real de 10 combinaciones para medir
# segundos por combinacion en ESTE cluster.
#
# Uso:
#   bash diagnostico_hpc.sh
#
# Al terminar, pega el .txt que genera (o mandalo) para decidir --partition/--array del .sbatch con datos
# reales de tu cluster, no con supuestos.

OUT="diagnostico_hpc_$(date +%Y%m%d_%H%M%S).txt"

{
echo "=== fecha ==="
date

echo
echo "=== nodos: particion, GPU (gres), cpus, memoria, estado (idle=libre) ==="
sinfo -N -o "%N %P %G %c %m %t" 2>&1

echo
echo "=== resumen por particion (nodos libres/total del formato A/I/O/T, limite de tiempo) ==="
sinfo -s 2>&1

echo
echo "=== tus jobs / uso actual en el cluster ==="
squeue -u "$USER" 2>&1

echo
echo "=== limites de cada particion (tiempo maximo, nodos totales) ==="
for p in $(sinfo -h -o "%P" 2>/dev/null | tr -d '*' | sort -u); do
  echo "--- particion: $p ---"
  scontrol show partition "$p" 2>&1 | grep -E "MaxTime|TotalCPUs|TotalNodes|State|Nodes="
done

DATASET=$(ls input/*.npz 2>/dev/null | head -1)
if [ -f busqueda_features_slurm.py ] && [ -n "$DATASET" ]; then
  echo
  echo "=== prueba real: 10 combinaciones de '$DATASET' EN ESTE NODO (mide seg/combinacion aqui mismo) ==="
  time python3 busqueda_features_slurm.py --dataset "$DATASET" --z 10 --salida /tmp/prueba_diagnostico.csv \
    --historial /tmp/prueba_diagnostico.historial.json
else
  echo
  echo "(no hay un input/*.npz + busqueda_features_slurm.py en esta carpeta -- se salta la prueba de tiempo;"
  echo " corre este script DENTRO de la carpeta que descomprimiste del zip de AHPC para tenerla)"
fi
} | tee "$OUT"

echo
echo "Todo quedo en $OUT -- pegalo o mandalo para decidir particion y cuanto paralelismo pedir."
