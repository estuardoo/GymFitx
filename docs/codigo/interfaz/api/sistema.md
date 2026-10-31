# `src/interfaz/api/sistema.py`

```text
API de la pestana Sistema: log, librerias, version de Python, apagar/reiniciar y laminas del pitch.
```

## `_cerrar_todo`

`def _cerrar_todo() -> None`

```text
Antes de salir: guarda la toma en curso, vacia la cola de SQL y baja el tunel.
```

## class `ServidorSql`

_sin docstring_

## `sql_servidor`

`async def sql_servidor() -> dict`

Ruta: **GET /api/system/sql**

```text
Servidor y base en uso (de parameters/server.json si existe) + estado de la conexion.
```

## `sql_servidor_guardar`

`async def sql_servidor_guardar(cfg: ServidorSql) -> dict`

Ruta: **POST /api/system/sql**

```text
Guarda servidor/base en parameters/server.json, lo aplica sin reiniciar y reconecta.
```

## class `RespaldoSql`

_sin docstring_

## `respaldo_sql_estado`

`def respaldo_sql_estado() -> dict`

Ruta: **GET /api/system/respaldo-sql**

```text
El disco es la fuente de los datos; SQL Server es una copia. Cuando se actualiza la copia: al cortar y/o al entrenar.
```

## `respaldo_sql_guardar`

`def respaldo_sql_guardar(cfg: RespaldoSql) -> dict`

Ruta: **POST /api/system/respaldo-sql**

_sin docstring_

## `respaldo_sql_ahora`

`def respaldo_sql_ahora() -> dict`

Ruta: **POST /api/system/respaldo-sql/ahora**

```text
Copia a SQL todos los clips del disco ya mismo (ignora las dos opciones de arriba).
```

## class `ListaDroidcam`

_sin docstring_

## `droidcam_lista`

`def droidcam_lista() -> dict`

Ruta: **GET /api/system/droidcam**

_sin docstring_

## `droidcam_guardar`

`def droidcam_guardar(cfg: ListaDroidcam) -> dict`

Ruta: **POST /api/system/droidcam**

```text
Guarda la lista de DroidCam (nombre + IP:puerto) en parameters/config.json; aparecen en amarillo en el selector de camaras.
```

## class `CambiarVersionPython`

_sin docstring_

## class `ActualizarLibreria`

_sin docstring_

## `log_tail`

`async def log_tail(lines: int=200) -> dict`

Ruta: **GET /api/log**

_sin docstring_

## `_requisitos`

`def _requisitos() -> dict[str, str]`

```text
{nombre: linea de requirements.txt tal cual, sin el nombre} -- ej.
"mediapipe" -> ">=0.10.18,<0.11". Se usa para mostrar la version pedida
y para saber con que restriccion actualizar cada paquete.
```

## `libraries`

`async def libraries() -> dict`

Ruta: **GET /api/libraries**

```text
Lee requirements.txt y busca la version realmente instalada de cada
paquete (puede diferir de lo que pide el archivo).
```

## `actualizar_libreria`

`async def actualizar_libreria(cfg: ActualizarLibreria) -> dict`

Ruta: **POST /api/system/libraries/update**

```text
Actualiza una libreria (o todas, si no se pasa nombre) respetando lo
que pide requirements.txt. Corre pip en un hilo aparte para no trabar el
resto del panel mientras baja el paquete.
```

## `_detectar_versiones_python`

`def _detectar_versiones_python() -> list[str]`

```text
Versiones de Python que el lanzador 'py' de Windows encuentra
instaladas (ej. ["3.12", "3.11"]). Vacio si 'py' no esta disponible
(Linux/Mac, o Windows sin el lanzador) -- no es un error, el panel
simplemente no ofrece cambiar de version en ese caso.
```

## `python_entorno`

`async def python_entorno() -> dict`

Ruta: **GET /api/system/python**

_sin docstring_

## `cambiar_version_python`

`async def cambiar_version_python(cfg: CambiarVersionPython) -> dict`

Ruta: **POST /api/system/python_version**

```text
Recrea el entorno virtual con otra version de Python y reinicia.

No cambia el interprete de este proceso en caliente (no se puede); en
su lugar deja la version pedida en un archivo que UPDATE.bat lee al
crear el .venv, borra el .venv actual para forzar que se rearme, y
corre UPDATE.bat (rehace el entorno y, al terminar, abre la app). Tarda mas:
reinstala todo.
```

## `system_shutdown`

`async def system_shutdown() -> dict`

Ruta: **POST /api/system/shutdown**

```text
Guarda lo que haya en curso y cierra el proceso del servidor. El
.bat, al ver que python termino, cierra la ventana de cmd sola.
```

## `system_restart`

`async def system_restart() -> dict`

Ruta: **POST /api/system/restart**

```text
Como apagar, pero antes relanza GYMFITX.bat en una ventana nueva.
```

## `_pitch`

`def _pitch()`

```text
Laminas del pitch (docs/pitch/*.png, en orden) + el .pptx original.
```

## `dataset_pitch`

`def dataset_pitch()`

Ruta: **GET /api/pitch**

_sin docstring_

## class `Generar`

_sin docstring_

## `docs_generar`

`def docs_generar(g: Generar) -> dict`

Ruta: **POST /api/docs/generar**

```text
Corre las 5 etapas (seleccionar → formatear): deja los reportes en reportes/, el diccionario en docs/diccionario/ y
la tabla final en input/gold/. Sin ejercicio, los de parameters/config.json (ejercicios).
```

