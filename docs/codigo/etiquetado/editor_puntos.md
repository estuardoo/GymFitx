# `src/etiquetado/editor_puntos.py`

```text
Editor visual de la definicion de cada ejercicio (parameters/<n>/, ver src/nucleo/definicion.py):
elegir con clic, sobre un diagrama del cuerpo, que landmarks
arma cada 'feature' (angulo o razon de distancia), en vez de escribir el archivo a mano.
Es el mismo dato que ya lee puntos_de_ejercicio() en src/nucleo/ejercicio.py -- este
modulo es el que ahora tambien puede ESCRIBIRLO.

Solo toca 'name'/'description'/'source'/'features'/'kpoints'; cualquier otra
clave (signal, segmentation...) se deja tal cual estaba. Antes de cada guardado la definicion
anterior queda en sistema/respaldos/<slug>.json.
```

## Constantes

`POSE_PUNTOS`, `POSE_ESQUELETO`, `POSE_GRUPOS`, `TIPOS_FEATURE`, `ANGULOS_CONOCIDOS`, `PENDIENTES_PATH`, `ESPERA_SQL_CAIDO_S`

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
Slugs de los ejercicios activos.
```

## `leer_ejercicio`

`def leer_ejercicio(nombre)`

```text
Los campos editables de un ejercicio. None si no existe.
```

## `_normalizacion_panel`

`def _normalizacion_panel(nombre, data)`

_sin docstring_

## `_validar_features`

`def _validar_features(source, features, kpoints=None)`

_sin docstring_

## `_guardar_valido`

`def _guardar_valido(nombre, data)`

```text
El ejercicio tiene que poder cargarse (si no, se cae /api/state para TODOS): se valida antes de escribir.
```

## `_definicion_de`

`def _definicion_de(nombre)`

_sin docstring_

## `guardar_ejercicio`

`def guardar_ejercicio(nombre, cambios)`

```text
cambios: {name, description, source, features, kpoints}. Valida
kpoints (numeros/nombres unicos, origenes validos, derivados solo de
kpoints previos) y luego features (mismo tipo conocido y cantidad de
puntos/reference de siempre, pero ahora contra los nombres del catalogo
de kpoints si ya existe uno) -- antes de tocar nada. Todo lo demas
(signal, segmentation, etc) se deja tal cual estaba; la definicion anterior queda en
sistema/respaldos/.
```

## `guardar_reglas`

`def guardar_reglas(nombre, reglas)`

```text
Reemplaza `reglas` de la definicion (validadas por nucleo/reglas.py) sin tocar el resto.
```

## `guardar_normalizacion`

`def guardar_normalizacion(nombre, norm)`

```text
Guarda {origen, escala, n_frames} en la definicion (guide.json -> normalizacion) sin tocar el resto.
-> {normalizacion, cambio}: cambio=True si difiere de lo vigente (gold se rehace solo; modelos ya entrenados: reentrenar).
```

## `crear_ejercicio`

`def crear_ejercicio(nombre)`

```text
Ejercicio nuevo desde cero (guardar_ejercicio solo puede EDITAR uno que ya exista): definicion
minima pero valida, su numero y carpetas en input/<capa>/<numero>/, y
lo sube ya a SQL (su 'type' + definicion) para que quede conectado desde el primer guardado en
el editor de Puntos.
```

## `modificar_ejercicio`

`def modificar_ejercicio(nombre, cambios)`

```text
Datos basicos de un ejercicio (el slug NO se renombra: ata 'type' en SQL, carpeta de clips y plantilla).
cambios: {name, description, direction, min_duration_ms, max_duration_ms}; lo que falte se deja igual.
Puntos/angulos se editan con guardar_ejercicio. Valida antes de escribir y respalda la definicion
anterior. Devuelve base_invalida=True si cambio la segmentacion y ya hay base grabada.
```

## `eliminar_ejercicio`

`def eliminar_ejercicio(nombre)`

```text
Archiva un ejercicio: queda inactivo con su numero reservado (recuperable: crearlo de nuevo con el mismo nombre
lo reactiva). Sus clips, grabaciones, tablas y SQL los limpia etiquetado/depurar.py (lo llama el endpoint; el 'type'
queda reservado en sql_tipos.json).
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
Lo que se comparte por SQL: source, kpoints y features (signal/segmentation se quedan en la definicion local).
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
Tras guardar la definicion: lo sube a SQL. Sin conexion queda pendiente (y se sube solo despues).
```

## `sincronizar`

`def sincronizar(nombre)`

```text
Deja la definicion local y SQL iguales, con SQL mandando:
- con pendiente local (se guardo sin conexion): se sube lo local;
- SQL no tiene el ejercicio: se sube la definicion local;
- SQL tiene otra cosa: se aplica a la local (queda copia en sistema/respaldos);
- sin conexion: no se toca nada.
```

## `reintentar`

`def reintentar(todos=False)`

```text
Para el hilo de fondo del panel: sube los pendientes (todos=True: ademas trae de SQL lo que difiera).
```

