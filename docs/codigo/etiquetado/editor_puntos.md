# `src/etiquetado/editor_puntos.py`

```text
Editor visual de los .yaml de ejercicio (ejercicios/*.yaml):
elegir con clic, sobre un diagrama del cuerpo, que landmarks
arma cada 'feature' (angulo o razon de distancia), en vez de escribir el YAML
a mano. Mismo archivo que ya lee puntos_de_ejercicio() en src/nucleo/ejercicio.py -- este
modulo es el que ahora tambien puede ESCRIBIRLO.

Solo toca 'name'/'description'/'source'/'features'/'kpoints'; cualquier otra
clave del yaml (signal, segmentation) se deja tal cual estaba. PyYAML no
conserva comentarios al reescribir -- por eso se guarda una copia del
contenido anterior en ejercicios/.respaldos/ antes de cada guardado.
```

## Constantes

`RESPALDOS_DIR`, `POSE_PUNTOS`, `POSE_ESQUELETO`, `POSE_GRUPOS`, `TIPOS_FEATURE`, `ANGULOS_CONOCIDOS`, `PENDIENTES_PATH`, `ESPERA_SQL_CAIDO_S`

## `_nombres_landmark_de`

`def _nombres_landmark_de(fuente)`

```text
Los 33 nombres crudos de pose.
```

## `_validar_kpoints`

`def _validar_kpoints(kpoints)`

_sin docstring_

## `catalogo`

`def catalogo(source='pose')`

```text
Puntos + esqueleto del diagrama de pose (33, cuerpo).
```

## `listar_ejercicios`

`def listar_ejercicios()`

```text
Nombres (sin .yaml) de todos los ejercicios en ejercicios/.
```

## `leer_ejercicio`

`def leer_ejercicio(nombre)`

```text
Los campos editables de un ejercicio, tal cual estan en su .yaml. None
si el archivo no existe.
```

## `_validar_features`

`def _validar_features(source, features, kpoints=None)`

_sin docstring_

## `guardar_ejercicio`

`def guardar_ejercicio(nombre, cambios)`

```text
cambios: {name, description, source, features, kpoints}. Valida
kpoints (numeros/nombres unicos, origenes validos, derivados solo de
kpoints previos) y luego features (mismo tipo conocido y cantidad de
puntos/reference de siempre, pero ahora contra los nombres del catalogo
de kpoints si ya existe uno) -- antes de tocar el archivo. Todo lo demas
del yaml (signal, segmentation, etc) se deja tal cual estaba. Guarda una
copia del contenido anterior en ejercicios/.respaldos/ (PyYAML no conserva
los comentarios del archivo al reescribir).
```

## `guardar_reglas`

`def guardar_reglas(nombre, reglas)`

```text
Reemplaza `reglas:` del .yaml (validadas por evaluacion/reglas.py) sin tocar el resto; respaldo antes.
```

## `crear_ejercicio`

`def crear_ejercicio(nombre)`

```text
Ejercicio nuevo desde cero (guardar_ejercicio solo puede EDITAR uno que ya exista): stub de
.yaml minimo pero valido, sus carpetas en datos/clips/<nombre>/ y datos/grabaciones/<nombre>/, y
lo sube ya a SQL (su 'type' + definicion) para que quede conectado desde el primer guardado en
el editor de Puntos.
```

## `modificar_ejercicio`

`def modificar_ejercicio(nombre, cambios)`

```text
Datos basicos de un ejercicio (el slug NO se renombra: ata 'type' en SQL, carpeta de clips y plantilla).
cambios: {name, description, direction, min_duration_ms, max_duration_ms}; lo que falte se deja igual.
Puntos/angulos se editan con guardar_ejercicio. Valida con load_exercise antes de escribir y respalda el
.yaml anterior. Devuelve base_invalida=True si cambio la segmentacion y ya hay base grabada.
```

## `eliminar_ejercicio`

`def eliminar_ejercicio(nombre)`

```text
Archiva un ejercicio: su .yaml pasa a ejercicios/.respaldos/ (recuperable). Solo mueve el .yaml; sus clips,
grabaciones, manifest y SQL los limpia etiquetado/depurar.py (lo llama el endpoint; el 'type' queda reservado
en sql_tipos.json).
```

## `conexiones_kpoints`

`def conexiones_kpoints(kpoints)`

```text
Pares (i, j) de indices dentro de 'kpoints' que forman un hueso del
esqueleto de pose -- para dibujar el overlay del video solo con los
puntos del catalogo. Dos kpoints se unen si son de la misma fuente y su
par de landmarks esta en POSE_ESQUELETO.
```

## `codigo_kpoint`

`def codigo_kpoint(kp, kpoints)`

```text
Codigo que ve el usuario: C01..C33 = Cuerpo 33 (ID de MediaPipe + 1); D01.. = derivados.
```

## `_definicion`

`def _definicion(nombre)`

```text
Lo que se comparte por SQL: source, kpoints y features (signal/segmentation se quedan en el .yaml).
```

## `_canon`

`def _canon(definicion)`

_sin docstring_

## `_espejo_sql`

`def _espejo_sql(nombre)`

```text
(type, kpoints, nombres, filas de features) tal como deben quedar en las tablas de consulta de SQL.
```

## `_nombres_metricas`

`def _nombres_metricas(nombres, kps, nombre)`

```text
Columnas de 'angles' del type: los angulos y proporciones activados (o el catalogo fijo si el ejercicio no tiene).
```

## `sincronizar_sql`

`def sincronizar_sql(nombre)`

```text
Sube a SQL Server la definicion de este ejercicio (su 'type') y sus tablas de consulta (kpoints, angulos,
filas). Lanza SQLServerNoDisponible si el servidor no responde.
```

## `_pendientes`

`def _pendientes()`

_sin docstring_

## `_marcar_pendiente`

`def _marcar_pendiente(nombre, pendiente)`

_sin docstring_

## `subir`

`def subir(nombre)`

```text
Tras guardar el .yaml: lo sube a SQL. Sin conexion queda pendiente (y se sube solo despues).
```

## `sincronizar`

`def sincronizar(nombre)`

```text
Deja el .yaml y SQL iguales, con SQL mandando:
- con pendiente local (se guardo sin conexion): se sube lo local;
- SQL no tiene el ejercicio: se sube el .yaml;
- SQL tiene otra cosa: se aplica al .yaml (queda copia en .respaldos);
- sin conexion: no se toca nada.
```

## `reintentar`

`def reintentar(todos=False)`

```text
Para el hilo de fondo del panel: sube los pendientes (todos=True: ademas trae de SQL lo que difiera).
```

