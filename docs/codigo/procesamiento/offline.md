# `src/procesamiento/offline.py`

```text
Detecta los kpoints del ejercicio sobre un video YA GRABADO: es la fuente
del dataset de entrenamiento.

Por que offline y no solo en vivo: desde que la grabacion guarda TODOS los
cuadros de la camara (captura desacoplada, ver src/sesion/pipeline.py), el video
tiene ~30 fps reales, mientras que la deteccion en vivo corre a lo que de la
CPU. Re-detectar sobre el video da puntos en cada cuadro. La resolucion
kpoint-por-cuadro es la misma funcion que el vivo (src.procesamiento.puntos.kpoints.resolver) y
los trackers son los de src/captura/deteccion/tracker.py: no hay logica duplicada.

Se llama desde exportar() en src/etiquetado/cortes.py, una vez por video (si el .npz
hermano ya tiene los puntos que le hacen falta a este ejercicio no hace nada
-- por eso es seguro llamarlo en cada corte). Aislado a proposito: si falta
GYMFITX, mediapipe u opencv-python, se lanza DeteccionNoDisponible y quien
llama decide seguir sin puntos para ese video en vez de tumbar el corte
entero.

Los puntos quedan con su PROPIO eje de tiempo (points_t_ms), independiente
del t_ms de las features ya guardadas: salen de re-decodificar el .mp4 ahora,
no de la sesion de captura original, asi que no coincide frame a frame con
el t_ms de 'values'. recorta_npz() en src/etiquetado/cortes.py los recorta cada uno con
su propia mascara de tiempo.

Dos modos, segun si el ejercicio ya tiene un catalogo de 'kpoints' (ver
src/etiquetado/editor_puntos.py) en su definicion:

- CON catalogo: se guardan los kpoints del ejercicio en UN array de puntos nombrados como el
  usuario los llamo, calculando tambien los derivados (punto medio de otros dos). Si el catalogo
  cambia (se agrega un kpoint nuevo) el set de nombres guardado ya no coincide con el pedido
  y se vuelve a detectar solo, en el siguiente export -- automatico.
- SIN catalogo todavia: se guardan los 33 landmarks crudos con sus nombres de MediaPipe.
```

## class `DeteccionNoDisponible`

```text
Falta GYMFITX, mediapipe/opencv-python, o el modelo -- nunca tumba el corte de videos.
```

## `_cargar_motor`

`def _cargar_motor()`

_sin docstring_

## `_kpoints_de`

`def _kpoints_de(exercise)`

```text
(kpoints, source) de la definicion de ese ejercicio. kpoints es [] si el
ejercicio no existe, no tiene definicion, o no tiene catalogo definido todavia
-- en cualquiera de esos casos quien llama cae al modo viejo.
```

## `_abrir_video`

`def _abrir_video(mp4_path)`

_sin docstring_

## `_detectar_legacy`

`def _detectar_legacy(mp4_path, source)`

```text
Guarda los 33 landmarks crudos con sus nombres de MediaPipe -- para ejercicios sin catalogo de kpoints.
```

## `_detectar_combinado`

`def _detectar_combinado(mp4_path, kpoints)`

```text
Resuelve cada kpoint por cuadro con src.procesamiento.puntos.kpoints.resolver -- la MISMA funcion que
usa el pipeline en vivo, asi offline y vivo producen exactamente los mismos puntos.
```

## `_version`

`def _version(npz_dict)`

_sin docstring_

## `detectar_puntos_si_faltan`

`def detectar_puntos_si_faltan(mp4_path: Path, exercise: str | None=None) -> bool`

```text
True si acabo de detectar y guardar puntos nuevos en el .npz hermano;
False si ya tenia los que le hacen falta a este ejercicio, o si no hay
.npz que actualizar. 'exercise' se lee del .json hermano si no se pasa.
```

