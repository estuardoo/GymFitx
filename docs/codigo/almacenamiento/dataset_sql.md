# `src/almacenamiento/dataset_sql.py`

```text
Dataset de keypoints en SQL Server: SOLO guardar y leer (sin logica de negocio).

Conecta por la conexion unica de src/almacenamiento/sqlserver.py (mismo host/base que el
resto del panel). La preparacion de cada clip (procesamiento/puntos) y el orden en que se
escribe (etiquetado/tablas.py) viven fuera de este modulo. Si falta pyodbc
o el servidor no responde, cortar/entrenar avisan con SQLServerNoDisponible
sin tumbar nada.

Tablas (una fila de configuracion en sql_config.json define, por 'type' de
ejercicio, con que se normaliza table_frames_fix):

  table_file        un video/clip exportado -> id, type, archivo, frames
  table_kpoints     catalogo de puntos por type -> point (indice), descripcion
                     (nombre del landmark, tal como aparece en el .yaml del
                     ejercicio)
  table_frames      puntos (x,y,z) crudos por cuadro, uno por fila -- una
                     columna por eje ('VectorX','VectorY','VectorZ'), cada una
                     "v1|v2|...|vN" con un valor por punto, en el orden de
                     table_kpoints (point 0..N-1), correlativo entre las 3.
                     Sin columna de mano/lado: el lado ya viene en el catalogo
                     de kpoints del ejercicio.
                     'angles' = "a1|...|aA", angulos del ejercicio en grados
                     (convencion flexion), orden de table_angles (src/procesamiento/medidas/angulos.py).
  table_frames_fix  igual que table_frames pero centrado+escalado (invariante
                     a posicion/tamano) y remuestreado a un numero fijo de
                     cuadros -- ver procesamiento/puntos/normalizacion.py
  table_frame_base  igual que table_frames_fix (misma estructura), pero solo
                     para los frames normalizados del clip 'base' de cada
                     type -- separado de table_frames_fix para no tener que
                     filtrar por clase/id cada vez que se necesita la base
  table_angles      catalogo de la columna 'angles' por type -> idx, descripcion
```

## Constantes

`CONFIG_PATH`, `TIPOS_PATH`, `TABLAS`, `DATOS_A_BLANQUEAR`, `DDL`

## `tipo_de_ejercicio`

`def tipo_de_ejercicio(exercise: str) -> int`

```text
'type' en las 4 tablas = un ejercicio (el mismo nombre que su
ejercicios/<exercise>.yaml, guardado en el .json de cada video
grabado). Se le asigna un numero la primera vez que aparece y se guarda
en sql_tipos.json, asi el mismo ejercicio siempre cae en el mismo type
sin tener que numerarlos a mano.
```

## `tipos_conocidos`

`def tipos_conocidos() -> dict[int, str]`

```text
{type: ejercicio} de todos los ejercicios ya vistos, para el selector
'elegir el tipo' del panel de entrenamiento.
```

## `blanquear_datos`

`def blanquear_datos()`

```text
Vacia los datos de todos los clips en SQL (frames crudos y normalizados, base, indicadores y archivos).
Se conservan las definiciones (table_ejercicio, table_features, table_config): los catalogos se reescriben al regenerar.
```

## `asegurar_base_y_tablas`

`def asegurar_base_y_tablas()`

```text
Idempotente: crea la base GymFitX (si hace falta) y las tablas del dataset.
```

## `estado`

`def estado()`

```text
Diagnostico para el panel: nunca revienta aunque el servidor no responda.
```

## `config`

`def config()`

_sin docstring_

## `guardar_config`

`def guardar_config(cfg)`

_sin docstring_

## `_ejes_str`

`def _ejes_str(frame_points)`

```text
(N,3) -> (VectorX, VectorY, VectorZ), cada uno 'v1|v2|...|vN' en el orden
de table_kpoints (un valor por punto, no un triple).
```

## `_angulos_str`

`def _angulos_str(fila)`

```text
(A,) -> 'a1|a2|...|aA' en el orden de table_angles; None si no hay angulos.
```

## `_ejes_de`

`def _ejes_de(ex, ey, ez)`

```text
Inverso de _ejes_str: 3 strings 'v1|...|vN' -> (N,3).
```

## `conexion`

`def conexion()`

```text
Conexion a la base del dataset (usar con 'with').
```

## `guardar_catalogo`

`def guardar_catalogo(cx, type_, nombres, nombres_ang)`

```text
Reemplaza table_kpoints y table_angles de este type.
```

## `guardar_definicion`

`def guardar_definicion(cx, type_, ejercicio, definicion)`

```text
Reemplaza la definicion completa del ejercicio (dict con source, kpoints, features).
```

## `leer_definicion`

`def leer_definicion(type_)`

```text
La definicion guardada para este type, o None si SQL todavia no la tiene.
```

## `guardar_features`

`def guardar_features(cx, type_, filas)`

```text
Reemplaza table_features de este type. filas: [(id, nombre, tipo, recorrido, activo)].
```

## `guardar_config_activa`

`def guardar_config_activa(cx, type_, cfg, guia)`

```text
table_config: la ultima normalizacion usada para este type, visible desde SQL.
```

## `archivo_registrado`

`def archivo_registrado(cx, type_, archivo)`

```text
(id, guia_fix) del clip, o None si todavia no esta en table_file.
```

## `crear_archivo`

`def crear_archivo(cx, type_, archivo, frames, guia, clase)`

_sin docstring_

## `actualizar_archivo`

`def actualizar_archivo(cx, file_id, frames, guia, clase)`

_sin docstring_

## `frames_crudos_guardados`

`def frames_crudos_guardados(cx, type_, file_id)`

```text
Filas utiles de table_frames. 'IS NOT NULL': una migracion vieja pudo dejar
filas con VectorX vacio, que existen pero no sirven.
```

## `borrar_frames`

`def borrar_frames(cx, type_, file_id)`

_sin docstring_

## `insertar_frames`

`def insertar_frames(cx, tabla, type_, file_id, points, angulos)`

```text
Una fila por cuadro en table_frames (crudo) o table_frames_fix (normalizado).
```

## `base_del_tipo`

`def base_del_tipo(cx, type_)`

```text
(id, archivo, guia_fix) del clip clase='base' de este type, o None.
```

## `copiar_a_frame_base`

`def copiar_a_frame_base(cx, type_, base_file_id)`

```text
table_frame_base = espejo de table_frames_fix del clip 'base' (se refresca siempre: son
~n_frames_fijo filas).
```

## `nombres_kpoints`

`def nombres_kpoints(cx, type_)`

_sin docstring_

## `otros_archivos`

`def otros_archivos(cx, type_, base_file_id)`

_sin docstring_

## `indicadores_con_guia`

`def indicadores_con_guia(cx, type_, file_id, guia)`

_sin docstring_

## `reemplazar_indicadores`

`def reemplazar_indicadores(cx, type_, file_id, base_file_id, guia, valores)`

```text
valores: [(point, indicador), ...] de un clip contra el base.
```

## `features_por_archivo`

`def features_por_archivo(type_, usar='ambos', tipos=None)`

```text
{archivo: vector 1D} de todos los clips de este 'type' que ya tengan
table_frames_fix -- una sola consulta para todos, no una por clip.
usar: letras x, y, z (ejes de cada kpoint), a (angulos) y p (proporciones), o los
nombres de siempre: 'puntos', 'angulos', 'ambos'. NaN -> 0 para que sklearn no reviente.
```

## `frames_fix_por_archivo`

`def frames_fix_por_archivo(type_)`

```text
{archivo: (points (T,N,3) float32, metrics (T,A) float32)} de table_frames_fix, SIN aplanar ni filtrar --
para exportar el dataset completo (ver entrenamiento/exportar_slurm.py). T = el n_frames_fijo de este type.
```

## `marcar_uso`

`def marcar_uso(type_, seleccion)`

```text
Espejo en table_file.usar de seleccion_entrenamiento.json ({archivo: bool}).
```

## `kpoints_de`

`def kpoints_de(type_)`

```text
[(point, descripcion), ...] de table_kpoints para este type, en orden --
la fuente de verdad de que numero (point) le toca a cada nombre, el mismo
orden en que estan empacados VectorX/Y/Z (ver poblar_desde_manifest).
```

## `_frames_de_con`

`def _frames_de_con(cx, type_, archivo, nombres=None)`

```text
Igual que frames_de(), pero reusando una conexion ya abierta -- para no
abrir una conexion nueva por clip dentro de etiquetado/tablas.py.
```

## `frames_de`

`def frames_de(type_, archivo)`

```text
{kpoint: {'x':[...], 'y':[...], 'z':[...]}} de un clip ya en
table_frames_fix, un valor por frame (mismo orden 1..n_frames_fijo para
cualquier clip del mismo 'type', por eso son comparables frame a frame
sin alinear nada mas).
```

## `ranking_indicadores`

`def ranking_indicadores(type_)`

```text
[{'archivo':..., 'clase':..., 'kg':..., 'n':...}, ...] -- un renglon por
clip (todos menos el 'base'), el promedio de table_indicator.indicador
entre sus kpoints (KG), de mayor a menor parecido. 'n' es cuantos kpoints
tienen valor calculado -- si sale menor que el total de kpoints, a ese
clip le falto algo por calcular (util para diagnosticar sin ver la SQL
directamente). Vacio si nunca se corrio poblar_desde_manifest con un
'base' definido para este type.
```

