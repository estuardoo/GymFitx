# `scripts/busqueda_features_slurm.py`

```text
Busqueda aleatoria de que kpoints/angulos/proporciones mueven el accuracy y el F1 de un ejercicio.

Standalone a proposito -- solo necesita numpy + scikit-learn, nada de GYMFITX -- para poder correrlo en un
cluster/supercomputador copiando UNICAMENTE este archivo y el .npz de scripts/exportar_dataset_slurm.py
(el modulo AHPC del panel arma ambos en un .zip listo para subir).

Flujo completo (repetible para cualquier ejercicio: solo cambia --ejercicio / --dataset):
  1. En la PC con SQL Server (o desde la pestana AHPC del panel):
       python scripts/exportar_dataset_slurm.py --ejercicio <nombre>
     -> datos/slurm/<nombre>.npz
  2. Copia ese .npz (y este script) al cluster.
  3. Ahi:
       python busqueda_features_slurm.py --dataset <nombre>.npz --z 300 --salida resultados.csv
     Para repartir las Z pruebas en un SLURM array (mas rapido, mismas combinaciones divididas entre
     tareas): --tarea-id/--n-tareas -- ver slurm_busqueda_features.sbatch, un ejemplo de sbatch listo.
  4. Mientras corre (o cuando termine): cada tarea deja un <salida>.estado.json (cuantas combinaciones ya
     hizo, cuantas le tocan, % y si termino) -- scripts/estado_busqueda_slurm.py junta los de todas las
     tareas del array en una tabla (no necesita numpy/sklearn, se puede correr en el cluster aunque el
     modulo de python este roto). ponytail: si una tarea revienta a mitad de una combinacion, su
     estado.json se queda pegado en el ultimo % con terminado=false para siempre -- cruzalo con sacct
     (ver LEEME.txt) para distinguir "sigue corriendo" de "fallo".
  5. Para ver la matriz resumen, la tabla de detalle y la grafica de progreso a partir del/los .csv que
     salieron: scripts/resumen_busqueda_slurm.py (se corre en tu PC, no hace falta el cluster para eso).

Que hace: cada 'prueba' es UNA combinacion al azar -- un subconjunto de tamano al azar (1..m) de los m
kpoints del ejercicio (con sus 3 ejes x,y,z), un subconjunto (1..p) de sus p angulos y un subconjunto (1..q)
de sus q proporciones -- y la entrena/mide, con el catalogo COMPLETO de modelos (los mismos ~14 del panel
Entrenamiento), con el mismo k-fold para todos.

El .csv de salida trae una fila por (escenario, modelo), TODO codificado -- nada de nombres/texto (esos ya
estan en tu tabla SQL): llave (= escenario*100 + codigo del modelo, ver MODELOS_CODIGO), type, modelo
(codigo), escenario, K01..KN/A01..AN/P01..PN (1 si ese kpoint/angulo/proporcion se uso en esta fila, 0 si
no -- mismo orden que point_names/metric_types de ese ejercicio en el .npz), accuracy, f1_macro, error.

Combinaciones que NO se repiten entre corridas, y 'escenario' es GLOBAL y persistente: cada combinacion
probada queda anotada en un '<dataset>.historial.json' junto al .npz (o el que le pases con --historial),
con el numero de escenario que le toco -- ese numero es suyo para siempre, nunca se reasigna ni se repite,
asi hayas corrido el script muchas veces. Si vuelves a correr el script sobre el mismo dataset (mismo o
distinto --semilla/--z), las Z combinaciones nuevas EXCLUYEN las que ya estan en ese historial y siguen la
numeracion de escenario donde se quedo -- asi cada corrida agrega escenarios nuevos, nunca repite ni
renumera los de antes. Borra ese .json si alguna vez quieres empezar de cero.

--heuristico: por default el sorteo es puro azar (cada kpoint/angulo/proporcion tiene la misma chance de
entrar). Con --heuristico, antes de sortear se entrena UNA vez un RandomForest de referencia con TODO
activado, se mide que tan importante fue cada kpoint/angulo/proporcion (feature_importances_), y el sorteo
de las Z combinaciones queda sesgado hacia lo que mas importa -- sigue habiendo exploracion (nada llega a
probabilidad 0), pero deja de tratar todo por igual. Con el mismo Z, suele encontrar mejores combinaciones
mas rapido que el azar puro; el costo es una corrida de referencia extra al principio (no cuenta contra Z).

--escalada: ACTIVADO POR DEFECTO (ver PARAMETROS POR DEFECTO mas abajo) -- CADA TAREA hace su propio
hill-climbing local en vez de sortear combinaciones sueltas: prueba un lote inicial al azar de --lote
combinaciones (tambien sesgado por --heuristico si esta activo; por default LOTE_PCT_POR_DEFECTO de --z), se
queda con las --arranques mejores (por default ARRANQUES_PCT_POR_DEFECTO de ese lote) y desde cada una prueba
vecinos -- un solo kpoint/angulo/proporcion agregado o quitado a la vez -- moviendose hacia el vecino apenas
uno mejora el accuracy y descartandolo si no, hasta --intentos-sin-mejora vecinos seguidos sin mejorar o
hasta agotar el presupuesto de esa cadena. Usa --no-escalada para el azar puro de siempre (cada combinacion
un sorteo independiente, --z es el total de la corrida repartido entre tareas en vez del presupuesto POR
TAREA). Cada tarea explora sola, sin coordinarse con las demas (cada una tiene su propio bloque de
escenario_id y su propio '<dataset>.historial.tN.json'), asi que sigue corriendo en paralelo igual de bien
que el modo sin escalada -- lo que cambia es que cada tarea, en vez de recibir una lista pareja de
combinaciones al azar, persigue su propio mejor resultado local. Todo se sigue comparando contra la
linea_base (escenario=-1) de siempre.

--arranques (multi-arranque, solo tiene efecto con --escalada, que es el default): en vez de escalar desde
LA mejor combinacion del lote inicial nomas, cada tarea se queda con las --arranques mejores de ese lote y
escala una cadena de vecinos INDEPENDIENTE desde cada una, repartiendo lo que queda del presupuesto (--z
menos el lote) entre todas a partes iguales -- distinto punto de partida puede llegar a un optimo local
distinto, asi que el mejor de todas las cadenas suele ser mas robusto que una sola escalada que se puede
quedar pegada en el primer optimo que encuentra. Las cadenas comparten el historial de la tarea (ninguna
re-explora lo que otra ya probo). Por default se calcula solo (ver PARAMETROS POR DEFECTO), no hace falta
pasarlo a mano.
```

## Constantes

`MODELOS_CODIGO`, `RESERVA_ESCENARIOS_POR_TAREA`, `ESCALADA_POR_DEFECTO`, `LOTE_PCT_POR_DEFECTO`, `ARRANQUES_PCT_POR_DEFECTO`, `INTENTOS_SIN_MEJORA_POR_DEFECTO`, `GRUPOS`

## `_lote_y_arranques`

`def _lote_y_arranques(z: int, lote: int | None, arranques: int | None) -> tuple[int, int]`

```text
Resuelve --lote/--arranques cuando no se pasaron por linea de comandos (quedan en None): el
LOTE_PCT_POR_DEFECTO de --z para el lote inicial, y el ARRANQUES_PCT_POR_DEFECTO de ESE lote como
semillas para escalar (ver PARAMETROS POR DEFECTO arriba) -- minimo 1 en ambos casos. Un --lote/
--arranques explicito por linea de comandos siempre gana, se usa tal cual.
```

## `cargar`

`def cargar(ruta)`

_sin docstring_

## `grupo_de`

`def grupo_de(clip)`

```text
Grabacion de origen del clip (igual que src/entrenamiento/datos.py): sus ciclos y copias _2/_3 no se separan entre entrenar y probar.
```

## `elegir_k`

`def elegir_k(y, test_pct, grupos=None)`

_sin docstring_

## `_elige_subconjunto`

`def _elige_subconjunto(rng, n, pesos)`

```text
Subconjunto de tamano al azar (1..n). Sin pesos: azar uniforme. Con pesos: sesgado hacia los indices
de mayor peso via muestreo ponderado sin reemplazo (Efraimidis-Spirakis: clave = u**(1/peso), top-k).
```

## `combinacion_azar`

`def combinacion_azar(rng, m, p, q, pesos_m=None, pesos_p=None, pesos_q=None)`

```text
Un subconjunto de tamano al azar (1..n) por categoria -- [] si esa categoria no tiene nada que elegir.
Sin pesos_*: azar uniforme (default). Con pesos_*: sesgado hacia los indices de mayor peso -- ver
importancias() / --heuristico.
```

## `_normalizar_con_piso`

`def _normalizar_con_piso(valores, piso)`

```text
Normaliza a pesos > 0 con un 'piso' -- ningun indice llega a probabilidad ~0 (se conserva exploracion).
```

## `importancias`

`def importancias(ds, idx_metric_ang, idx_metric_pro, piso=0.1)`

```text
Para --heuristico: entrena UNA vez un RandomForest de referencia con TODO activado (no cuenta contra
--z) y devuelve (pesos_m, pesos_p, pesos_q) -- que tan importante fue cada kpoint/angulo/proporcion
(feature_importances_, sumada sobre frames y ejes x,y,z), listos para combinacion_azar.
```

## `_firma`

`def _firma(combo)`

_sin docstring_

## `historial_de`

`def historial_de(args) -> Path`

_sin docstring_

## `cargar_historial`

`def cargar_historial(ruta: Path) -> dict`

```text
{firma: escenario_id}. escenario_id es GLOBAL y nunca se reasigna -- una vez que una combinacion entra
aca, ese numero es suyo para siempre (para esta exercise/--historial), aunque corras el script mil veces.
```

## `guardar_historial`

`def guardar_historial(ruta: Path, vistas: dict) -> None`

_sin docstring_

## `guardar_estado`

`def guardar_estado(ruta: Path, **campos) -> None`

```text
Archivo chico (<salida>.estado.json) que esta tarea se va sobreescribiendo sola cada vez que termina
una combinacion -- para saber cuanto avanzo, si termino o si sigue corriendo SIN depender de sacct/squeue
ni de contar filas del .csv. Lo lee scripts/estado_busqueda_slurm.py (arma una tabla con todas las tareas
del array); no necesita numpy/sklearn, se puede mirar aunque el job siga corriendo.
```

## `guardar_avance_txt`

`def guardar_avance_txt(ruta: Path, **campos) -> None`

```text
<salida>.avance.txt -- lo mismo que guardar_estado() pero en texto plano (un 'cat' en el cluster
alcanza, sin json.loads) y actualizado cada 5 min nomas (no en cada combinacion): pensado para un
vistazo rapido de 'n/total' por tarea sin generar IO de mas en corridas con combinaciones muy rapidas.
Al terminar la tarea se le agrega 'fin' y 'duracion_seg' (ver main).
```

## `vecino`

`def vecino(rng, combo, m, p, q)`

```text
Un vecino de 'combo' para hill-climbing (--escalada): voltea (agrega o quita) UN solo elemento al
azar en K, A o P -- el cambio minimo posible, para explorar alrededor del mejor punto encontrado hasta
ahora en vez de saltar a un punto completamente distinto. Nunca deja una categoria en 0 si ya tenia 1
(evita el vecino vacio).
```

## `combinaciones_nuevas`

`def combinaciones_nuevas(rng, m, p, q, z, vistas: dict, intentos_por_combo=200, pesos_m=None, pesos_p=None, pesos_q=None, base_id=None)`

```text
Hasta 'z' combinaciones que NO esten en 'vistas' (mismo objeto -- se va llenando, y a cada nueva le
asigna el siguiente escenario_id GLOBAL, nunca antes usado en este historial). Si el espacio de
combinaciones ya se agoto (todas probadas en corridas anteriores), devuelve las que alcanzo a encontrar.
pesos_*: ver combinacion_azar / --heuristico. base_id: si se pasa, arranca la numeracion ahi en vez de
max(vistas)+1 -- lo usa --escalada para reservar un bloque de ids propio por tarea. Devuelve
[(escenario_id, combo), ...].
```

## `escalada`

`def escalada(rng, m, p, q, z, vistas: dict, evaluar_combo, lote=10, intentos_sin_mejora=10, arranques=1, pesos_m=None, pesos_p=None, pesos_q=None, base_id=None)`

```text
Hill-climbing local para UNA tarea (--escalada), en vez de puro azar: un lote inicial de hasta 'lote'
combinaciones nuevas (sesgadas si hay pesos_*, via combinaciones_nuevas) y, desde ahi, prueba vecinos
(vecino(): un solo elemento agregado/quitado) -- si uno mejora se mueve ahi y sigue escalando, si no lo
descarta y prueba otro, hasta 'intentos_sin_mejora' vecinos seguidos sin mejorar o hasta agotar el
presupuesto de ese arranque. vistas: se muta in-place igual que combinaciones_nuevas. evaluar_combo(
escenario, combo) -> accuracy: la inyecta main() (aca no se sabe nada de sklearn).

arranques (multi-arranque, >1 --arranques): en vez de escalar solo desde LA mejor del lote, se queda con
las 'arranques' mejores y escala UNA cadena de vecinos independiente desde CADA UNA, repartiendo lo que
queda del presupuesto ('z' menos el lote) entre ellas a partes iguales -- distinto punto de partida =
distinto optimo local al que puede llegar cada una, asi que el mejor de todas suele ser mas robusto que
escalar desde un solo punto (que puede quedar pegado en el primer optimo que encuentra). Las cadenas
comparten 'vistas': ninguna re-explora un vecino que otra ya probo. arranques=1 (default) = comportamiento
de siempre, una sola cadena con todo el presupuesto.

Devuelve (mejor_combo, mejor_score) de TODAS las cadenas -- None, -1.0 si el lote no encontro ninguna
combinacion nueva (espacio agotado desde el primer intento).
```

## `vector`

`def vector(ds, idx_pts, idx_metric)`

```text
(n_clips, F): por cuadro, los ejes x,y,z de los kpoints elegidos + las metricas elegidas, concatenados.
```

## `modelos`

`def modelos()`

```text
El catalogo COMPLETO -- los mismos ~14 modelos que compara el panel Entrenamiento (src/entrenamiento/
modelos.py), copiado aqui a mano porque este script es standalone (no puede hacer 'from src...' en el
cluster). lightgbm/catboost/xgboost se suman solo si estan instalados, igual que alla.
```

## `evaluar`

`def evaluar(nombre, est, X, y, skf)`

_sin docstring_

## `campos`

`def campos(m, p, q)`

```text
Nombres de columna del .csv -- todo codificado (nada de texto: los nombres de kpoints/angulos/
proporciones ya estan en el .npz/tabla SQL de origen, aca solo van sus POSICIONES). K/A/P van en el
mismo orden que point_names/metric_types de ese ejercicio -- por eso el ancho cambia segun el ejercicio.
```

## `_fila`

`def _fila(escenario, idx_pts, idx_ang, idx_pro, ds, m, p, q, r)`

```text
llave = escenario*100 + codigo_modelo: identifica esta fila SIN coordinar entre las tareas paralelas
del array (cada una calcula su propia llave sola, y nunca choca con la de otra) -- alcanza con que
escenario ya sea unico (lo garantiza cargar_historial/combinaciones_nuevas). -1/-1 para la linea base.
```

## `main`

`def main(argv=None)`

_sin docstring_

