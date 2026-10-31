# `scripts/hpc/resumen_busqueda_slurm.py`

```text
Junta el/los .csv que salieron de busqueda_features_slurm.py (una o varias corridas, uno o varios
--tarea-id de un mismo SLURM array, incluso de corridas separadas en el tiempo -- el historial de ese script
ya evita que se repitan escenarios) y arma esto para decidir que combinacion de kpoints/angulos/proporciones
conviene, con que modelo, al minimo costo:

  detalle.csv          una fila por (escenario, modelo) ya probada -- TODO codificado igual que en el .csv de
                        entrada (llave, type, modelo, escenario, K01..KN/A01..AN/P01..PN en 0/1, accuracy,
                        f1_macro) mas n_kpoints/n_angulos/n_proporciones/n_elementos (sumas simples) e
                        iteracion (orden de eleccion -- se deriva del numero de escenario, que ya es global y
                        nunca se reasigna). Va CRECIENDO: cada vez que corres esto con mas .csv (de corridas
                        nuevas), vuelve a armar el archivo completo con todo lo que le pasaste.
  matriz_resumen.csv   formato LARGO (una fila por type+accuracy_bucket+modelo+escenario -- nunca hay
                        choques aunque el bucket sea de 1%) lista para pivotear en Excel: Tabla dinamica,
                        filas=accuracy_bucket, columnas=modelo, valores=contar 'escenario' (o promediar
                        accuracy). Cada fila trae 'llave' para ir directo al detalle de ese resultado.
  graficos/progreso.png     accuracy (Y) segun el orden en que se fue eligiendo cada escenario (X) -- punto
                        gris = mejor accuracy de ese escenario (cualquier modelo), linea azul = el mejor
                        accuracy visto hasta ese punto.
  graficos/costo.png    accuracy (Y) vs cuantos elementos uso ese escenario -- n_kpoints+n_angulos+
                        n_proporciones (X). Linea azul = mejor accuracy visto hasta ese costo (la "frontera":
                        para cada presupuesto de elementos, lo maximo que se consiguio) -- para elegir al
                        minimo costo como pediste.
  graficos/matriz_calor.png    accuracy_bucket (Y) x modelo (X), color = cuantos escenarios cayeron ahi.
  resumen.txt           analisis en texto (unico lugar con nombres, para que se lea facil): mejor combinacion
                        encontrada (y cuanto mejora sobre la linea base), ranking de los 5 modelos con mejor
                        F1 promedio, correlacion entre n_kpoints/n_angulos/n_proporciones y el accuracy, y si
                        la busqueda ya se estanco o vale la pena seguir corriendo.

No hace falta el cluster para esto -- se corre en tu PC, donde ya tienes numpy/matplotlib (requirements.txt
de GYMFITX). Uso:

    python scripts/hpc/resumen_busqueda_slurm.py --csv resultados_*.csv --salida resumen_manguito_rotador/

Sirve igual para 1 corrida o para varias (por ejemplo si corriste busqueda_features_slurm.py mas de una vez
sobre el mismo ejercicio para agregar mas combinaciones).
```

## Constantes

`NOMBRE_MODELO`

## `_leer`

`def _leer(ruta) -> list[dict]`

_sin docstring_

## `_num`

`def _num(v)`

_sin docstring_

## `_entero`

`def _entero(v, default=0)`

_sin docstring_

## `_contar_prefijo`

`def _contar_prefijo(fila: dict, prefijo: str) -> int`

```text
Suma las columnas K01/K02.../A01.../P01... (1 si se uso ese kpoint/angulo/proporcion) -- el ancho
cambia segun el ejercicio, por eso se cuenta por prefijo de columna en vez de un numero fijo.
```

## `_rango_accuracy`

`def _rango_accuracy(acc)`

```text
Bucket de 1%: 0.873 -> '87-88%'. acc=1.0 cae en el ultimo bucket ('99-100%').
```

## `_iteraciones`

`def _iteraciones(escenarios: set) -> dict`

```text
orden de eleccion = orden de aparicion del numero de escenario (ya es global y creciente -- asignado
UNA vez por busqueda_features_slurm.py y nunca reasignado, asi que no hace falta mirar de que archivo
vino cada fila para saber el orden real en que se eligio).
```

## `armar_detalle`

`def armar_detalle(rutas: list[str]) -> list[dict]`

_sin docstring_

## `armar_matriz`

`def armar_matriz(detalle: list[dict]) -> list[dict]`

```text
Formato LARGO (una fila por resultado, sin agrupar) -- con un bucket de 1% chocarian demasiado
escenarios distintos en la misma celda de una tabla ancha; asi no se pierde ninguno, y en Excel se arma
la vista ancha con una tabla dinamica (filas=accuracy_bucket, columnas=modelo, valores=contar/promediar).
```

## `grafico_progreso`

`def grafico_progreso(detalle: list[dict], destino: Path)`

_sin docstring_

## `grafico_costo`

`def grafico_costo(detalle: list[dict], destino: Path)`

```text
accuracy vs n_elementos (kpoints+angulos+proporciones) -- la linea es la 'frontera': para cada
presupuesto de elementos, el mejor accuracy que se consiguio gastando eso o menos. Para elegir la
combinacion mas chica que ya te da un accuracy aceptable, en vez de la que mas kpoints/angulos usa.
```

## `armar_calor`

`def armar_calor(matriz: list[dict]) -> dict`

```text
{(accuracy_bucket, modelo): conteo} -- a partir de la matriz larga.
```

## `grafico_calor`

`def grafico_calor(matriz: list[dict], destino: Path) -> bool`

```text
accuracy_bucket (Y, solo los buckets con datos) x modelo (X) -- color = cuantos escenarios cayeron ahi.
```

## `analisis_convergencia`

`def analisis_convergencia(detalle: list[dict]) -> dict`

```text
Sin probar TODAS las combinaciones (inviable, ver docstring de busqueda_features_slurm.py): la forma
de saber si el mejor resultado encontrado ya es "suficientemente bueno" es ver si la busqueda se
estanco -- si hace rato que ninguna eleccion nueva supera al mejor visto hasta ahora, agregar mas --z
probablemente no va a cambiar mucho; si la mejora fue en una de las ultimas elecciones, todavia vale la
pena seguir.
```

## `resumen_ejecutivo`

`def resumen_ejecutivo(detalle: list[dict]) -> str`

```text
Texto corto tipo informe -- el UNICO lugar donde se traducen los codigos a nombre de modelo (para que
se lea facil); mejor combinacion (y cuanto mejora sobre la linea base), ranking de modelos, y si usar mas
kpoints/angulos/proporciones realmente ayuda (correlacion simple con el accuracy).
```

## `_escribir_csv`

`def _escribir_csv(filas, ruta)`

_sin docstring_

## `main`

`def main(argv=None)`

_sin docstring_

