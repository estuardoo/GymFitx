# `src/evaluacion/comparadores/__init__.py`

```text
Comparadores intercambiables: cada uno puntua una repeticion contra la
plantilla con una estrategia distinta, para poder elegir y comparar.

Todos parten de las MISMAS features (angulos + razones de distancia, ya
invariantes a camara -- ver src/procesamiento/medidas/features.py) y de la MISMA plantilla
calibrada (src/evaluacion/plantilla.py). Lo unico que cambia es como se comparan en
el tiempo:

- dtw_biomec (default, el original del proyecto): alinea con DTW, tolera
  ritmos distintos entre la base y la repeticion.
- angulos_directo: remuestrea la repeticion a la duracion de la plantilla y
  compara cuadro a cuadro, sin alinear -- mas simple y mas rapido, pero
  castiga diferencias de ritmo. Sirve de control para medir cuanto aporta
  el DTW.

- clasificador: el modelo entrenado en la pestana Entrenamiento
  (datos/entrenamientos/run_N/modelo.joblib). Convierte los kpoints de la
  repeticion en el MISMO vector que vio al entrenar (src/procesamiento/puntos/vectorizar.py) y
  el puntaje es la probabilidad de "bien" (0-100). Es lo que cierra el
  ciclo captura -> etiqueta -> entrena -> puntua en vivo. Solo aparece si
  hay un modelo entrenado para el ejercicio (ver buscar_clasificador).

Registro: cada comparador vive en su propio modulo (dtw, angulos_directo, clasificador).
```

## Constantes

`DEFAULT_MODEL`, `CLAVE_CLASIFICADOR`

## `comparar_todos`

`def comparar_todos(segment: Segment, template, clasificador: Clasificador | None=None) -> dict[str, dict]`

```text
Corre TODOS los modelos registrados (y el clasificador dataset, si hay)
sobre la MISMA repeticion y mide cuanto tarda cada uno.
```

