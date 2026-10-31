#!/bin/bash
# sbatch para scripts/hpc/busqueda_features_slurm.py. --partition/--time/--array ya vienen puestos para un
# cluster con particion "standard" = nodos SIN GPU (sklearn no la usa, no hace falta pedirla) -- son los
# valores que salieron de correr diagnostico_hpc.sh en ESE cluster. Si tu cluster es otro: corre
# diagnostico_hpc.sh ahi primero y ajusta --partition/modulos/venv con lo que te diga (nombres de
# particion varian de cluster a cluster).
# N_TAREAS abajo debe ser (--array = 0..N_TAREAS-1) y --n-tareas coincidir; cada tarea reparte las
# mismas --z combinaciones (semilla fija => siempre las mismas) y escribe su propio CSV.
# Cada tarea deja <su .csv>.estado.json (avance en detalle, ver estado_busqueda_slurm.py) y
# <su .csv>.avance.txt (lo mismo en texto plano, actualizado cada 5 min, con inicio/fin/duracion_seg de esa
# tarea al terminar) -- un 'cat resultados/*.avance.txt' en el cluster alcanza para ver el avance de todas.
# --array=0-71 * --cpus-per-task=4 = 288 cores = TODO lo que tiene la particion "standard" en este cluster
# (4 nodos, ver diagnostico_hpc.sh) -- si la comparten otros usuarios, algunas tareas quedaran en cola hasta
# que haya cupo. Para no acaparar toda la particion, baja --array (y N_TAREAS abajo, deben coincidir).
#
#   sbatch slurm_busqueda_features.sbatch

#SBATCH --job-name=gymfit_busqueda
#SBATCH --partition=standard
#SBATCH --array=0-71
#SBATCH --time=04:00:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=4
#SBATCH --output=logs/busqueda_%A_%a.out

module load python/scikit-learn   # o: source /ruta/a/tu/venv/bin/activate (o conda activate <env>)

mkdir -p logs resultados   # cada tarea del array escribe su .csv en resultados/ -- no ensucia la carpeta

N_TAREAS=72

# --heuristico (opcional): en vez de sortear parejo, sesga las combinaciones hacia los kpoints/angulos/
# proporciones que mas importan (una referencia rapida al principio, no cuenta contra --z) -- suele llegar
# a mejores combinaciones mas rapido que el azar puro. Descomenta la linea de abajo para activarlo.
# --escalada (opcional): cada tarea hace su propio hill-climbing local en vez de solo evaluar al azar --
# CON --escalada, --z pasa a ser el presupuesto POR TAREA (no el total repartido entre las 72 como sin ella).
# Se puede combinar con --heuristico (el lote inicial de cada tarea sale sesgado tambien). Descomenta las
# 2 lineas de abajo para activarlo -- de paso baja --z a algo mas chico (es por tarea ahora).
# --arranques (opcional, requiere --escalada): en vez de escalar desde LA mejor del lote nomas, escala desde
# las N mejores (una cadena independiente cada una) -- mas robusto contra un optimo local, mismo --z.
python busqueda_features_slurm.py \
  --dataset input/manguito_rotador.npz \
  --z 500 \
  --semilla 0 \
  --tarea-id "${SLURM_ARRAY_TASK_ID}" \
  --n-tareas "${N_TAREAS}" \
  --salida "resultados/resultados_${SLURM_ARRAY_TASK_ID}.csv"
  # --heuristico
  # --escalada --lote 10 --intentos-sin-mejora 10
  # --escalada --lote 100 --arranques 10 --intentos-sin-mejora 10   # multi-arranque: mas robusto, mismo --z

# --modelo (opcional, paralelismo alternativo): en vez de --array=0-71 (72 tareas geneicas, cada una
# probando LOS ~18 MODELOS por combinacion), repartir por MODELO -- una tarea por modelo, cada una entrena
# SOLO el suyo (mucho mas liviano por tarea; si el cluster corta corridas de 72 tareas con los 18 modelos
# cada una, este reparto es mas chico y liviano). Cambia el array y el comando de arriba por esto (borra o
# comenta el bloque de arriba si usas este):
#
#   MODELOS=(linea_base random_forest extra_trees gradient_boosting hist_gradient_boosting adaboost \
#            logistic sgd_logistico ridge lda svm knn decision_tree mlp naive_bayes lightgbm catboost xgboost)
#   #SBATCH --array=0-17
#   python busqueda_features_slurm.py \
#     --dataset input/manguito_rotador.npz \
#     --z 500 --semilla 0 \
#     --modelo "${MODELOS[$SLURM_ARRAY_TASK_ID]}" \
#     --salida "resultados/resultados_${MODELOS[$SLURM_ARRAY_TASK_ID]}.csv"
#     # --escalada --lote 100 --arranques 10 --intentos-sin-mejora 10   # tambien combinable con --modelo
#
# (si compilaste sin lightgbm/catboost/xgboost, saca esos 3 de MODELOS[] y ajusta el --array)

# Al terminar todas las tareas del array, juntar los CSV en uno solo:
#   head -1 resultados/resultados_0.csv > resultados/resultados_todo.csv
#   tail -n +2 -q resultados/resultados_*.csv >> resultados/resultados_todo.csv
# Si usaste --escalada no hace falta juntar nada a mano: cada tarea guarda SU PROPIO
# <dataset>.historial.tN.json, y en la proxima corrida cada tarea vuelve a leer TODOS esos .tN.json (no solo
# el suyo) para no repetir lo que encontro cualquier otra.
#
# Despues, en tu PC (no hace falta el cluster), con lo que bajes de resultados/:
#   python resumen_busqueda_slurm.py --csv resultados_*.csv --salida resumen/
# deja detalle.csv, matriz_resumen.csv, progreso.png, matriz_calor.png y resumen.txt -- ver LEEME.txt
