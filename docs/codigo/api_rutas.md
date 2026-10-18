# Rutas de la API

88 rutas. Detalle y docstring en el modulo de cada una.

| Metodo | Ruta | Funcion | Que hace | Archivo |
|---|---|---|---|---|
| GET | `/` | `index` |  | src/interfaz/app.py |
| GET | `/api/ahpc/ejercicios` | `ahpc_ejercicios` | Un ejercicio por fila: cuantos clips tiene en el manifest (bien/mal, sin 'base') y si ya tiene | src/interfaz/api/ahpc.py |
| POST | `/api/ahpc/exportar` | `ahpc_exportar` | body: {ejercicios: [nombre, ...]}. Arma un .zip con el .npz de cada ejercicio (rehecho con lo que hay | src/interfaz/api/ahpc.py |
| POST | `/api/archivados/depurar` | `archivados_depurar` |  | src/interfaz/api/etiquetado.py |
| GET | `/api/archivados/plan` | `archivados_plan` | Ejercicios archivados que aun dejan clips o datos en SQL (lo que quitaria el boton de Sistema). | src/interfaz/api/etiquetado.py |
| GET | `/api/cameras` | `cameras` |  | src/interfaz/api/sesion.py |
| GET | `/api/config` | `dataset_config` |  | src/interfaz/api/etiquetado.py |
| POST | `/api/descomp/analizar` | `dataset_descomp_analizar` |  | src/interfaz/api/entrenamiento.py |
| POST | `/api/descomp/opciones` | `dataset_descomp_opciones` |  | src/interfaz/api/entrenamiento.py |
| POST | `/api/descomp/ranking` | `dataset_descomp_ranking` |  | src/interfaz/api/entrenamiento.py |
| POST | `/api/docs/generar` | `docs_generar` | Corre las 5 etapas (seleccionar → formatear): deja los reportes en reportes/, el diccionario en docs/diccionario/ y | src/interfaz/api/sistema.py |
| POST | `/api/ejercicio/base-clip` | `ejercicio_base_clip` | Rehace la base del ejercicio desde un clip (por defecto el primero de 'bien'). Reinicia la camara para tomarla. | src/interfaz/api/etiquetado.py |
| GET | `/api/ejercicio/clips` | `ejercicio_clips` | Cuantos clips bien/mal/base tiene el ejercicio (para el dialogo de subida). | src/interfaz/api/etiquetado.py |
| POST | `/api/ejercicio/clips/carpeta` | `ejercicio_importar_carpeta` | Importa una carpeta Base/Bien/Mal/P1..Pn del disco del servidor (segundo plano; avance en .../progreso). | src/interfaz/api/etiquetado.py |
| GET | `/api/ejercicio/clips/carpeta/progreso` | `ejercicio_importar_progreso` |  | src/interfaz/api/etiquetado.py |
| GET | `/api/entrenamientos` | `dataset_entrenamientos` |  | src/interfaz/api/entrenamiento.py |
| POST | `/api/entrenar` | `dataset_entrenar` |  | src/interfaz/api/entrenamiento.py |
| GET | `/api/entrenar/clips` | `dataset_entrenar_clips` |  | src/interfaz/api/entrenamiento.py |
| POST | `/api/entrenar/seleccion` | `dataset_entrenar_seleccion` |  | src/interfaz/api/entrenamiento.py |
| POST | `/api/export` | `dataset_export` |  | src/interfaz/api/etiquetado.py |
| GET | `/api/export_estado` | `dataset_export_estado` |  | src/interfaz/api/etiquetado.py |
| GET | `/api/export_progreso` | `dataset_export_progreso` |  | src/interfaz/api/etiquetado.py |
| GET | `/api/history` | `history` |  | src/interfaz/api/sesion.py |
| GET | `/api/labels` | `dataset_labels_get` |  | src/interfaz/api/etiquetado.py |
| POST | `/api/labels` | `dataset_labels_post` |  | src/interfaz/api/etiquetado.py |
| GET | `/api/libraries` | `libraries` | Lee requirements.txt y busca la version realmente instalada de cada | src/interfaz/api/sistema.py |
| GET | `/api/log` | `log_tail` |  | src/interfaz/api/sistema.py |
| GET | `/api/modelos` | `dataset_modelos` |  | src/interfaz/api/entrenamiento.py |
| GET | `/api/modelos/matriz` | `modelos_matriz` | epocas / max_iter / parar de cada modelo que itera (la matriz de src/nucleo/config.py + lo guardado). | src/interfaz/api/entrenamiento.py |
| POST | `/api/modelos/matriz` | `modelos_matriz_guardar` |  | src/interfaz/api/entrenamiento.py |
| GET | `/api/overlay` | `dataset_overlay` |  | src/interfaz/api/etiquetado.py |
| GET | `/api/pitch` | `dataset_pitch` |  | src/interfaz/api/sistema.py |
| POST | `/api/publicar/detener` | `publicar_detener` |  | src/interfaz/api/publicar.py |
| GET | `/api/publicar/estado` | `publicar_estado` |  | src/interfaz/api/publicar.py |
| POST | `/api/publicar/iniciar` | `publicar_iniciar` |  | src/interfaz/api/publicar.py |
| POST | `/api/publicar/nueva_clave` | `publicar_nueva_clave` | Genera otra clave (la anterior deja de servir) y la muestra UNA vez. | src/interfaz/api/publicar.py |
| GET | `/api/puntos/catalogo` | `dataset_puntos_catalogo` |  | src/interfaz/api/etiquetado.py |
| POST | `/api/puntos/crear` | `dataset_puntos_crear` |  | src/interfaz/api/etiquetado.py |
| GET | `/api/puntos/ejercicios` | `dataset_puntos_ejercicios` |  | src/interfaz/api/etiquetado.py |
| POST | `/api/puntos/eliminar` | `dataset_puntos_eliminar` |  | src/interfaz/api/etiquetado.py |
| GET | `/api/puntos/figura.png` | `dataset_puntos_figura` |  | src/interfaz/api/etiquetado.py |
| POST | `/api/puntos/modificar` | `dataset_puntos_modificar` |  | src/interfaz/api/etiquetado.py |
| POST | `/api/puntos/reglas` | `dataset_puntos_reglas` |  | src/interfaz/api/etiquetado.py |
| GET | `/api/puntos/sincronizar` | `dataset_puntos_sincronizar` |  | src/interfaz/api/etiquetado.py |
| GET | `/api/puntos/tipos` | `dataset_puntos_tipos` |  | src/interfaz/api/etiquetado.py |
| GET | `/api/puntos/yaml` | `dataset_puntos_yaml_get` |  | src/interfaz/api/etiquetado.py |
| POST | `/api/puntos/yaml` | `dataset_puntos_yaml_post` |  | src/interfaz/api/etiquetado.py |
| GET | `/api/recordings` | `recordings` |  | src/interfaz/api/grabaciones.py |
| GET | `/api/recordings/csv` | `recording_csv` | Descarga en CSV las features (movimientos) ya guardadas en el .npz de | src/interfaz/api/grabaciones.py |
| POST | `/api/recordings/use_as_base` | `use_as_base` | Recalibra la plantilla de un ejercicio a partir de una grabacion archivada. | src/interfaz/api/grabaciones.py |
| POST | `/api/routine` | `set_routine` |  | src/interfaz/api/sesion.py |
| POST | `/api/session/camera_on` | `session_camera_on` |  | src/interfaz/api/sesion.py |
| POST | `/api/session/clasificador` | `session_clasificador` |  | src/interfaz/api/sesion.py |
| POST | `/api/session/exercise` | `session_exercise` |  | src/interfaz/api/sesion.py |
| POST | `/api/session/fps` | `session_fps` |  | src/interfaz/api/sesion.py |
| POST | `/api/session/grabar` | `session_grabar` |  | src/interfaz/api/sesion.py |
| POST | `/api/session/grabar_detener` | `session_grabar_detener` |  | src/interfaz/api/sesion.py |
| POST | `/api/session/modelo` | `session_modelo` |  | src/interfaz/api/sesion.py |
| POST | `/api/session/overlay` | `session_overlay` |  | src/interfaz/api/sesion.py |
| POST | `/api/session/pause` | `session_pause` |  | src/interfaz/api/sesion.py |
| POST | `/api/session/resume` | `session_resume` |  | src/interfaz/api/sesion.py |
| POST | `/api/session/stop` | `session_stop` |  | src/interfaz/api/sesion.py |
| GET | `/api/sim/crudo` | `sim_crudo` | Puntos SIN normalizar (coordenadas de pantalla 0-1, ver points_screen) + angulos/proporciones, | src/interfaz/api/sim.py |
| GET | `/api/sim/cuerpo3d` | `sim_cuerpo3d` | Puntos 3D en metros (world, origen en la cadera) del clip, cuadro a cuadro, para el avatar 3D de SIM. | src/interfaz/api/sim.py |
| GET | `/api/sim/normalizado` | `sim_normalizado` | Puntos normalizados+remuestreados (table_frames_fix de SQL) del clip 'base' y del 'clip' elegido, con | src/interfaz/api/sim.py |
| GET | `/api/sim/opciones` | `sim_opciones` | Ejercicio(s) y sus clips por clase (igual que Descomposicion) -- para los selectores del panel. | src/interfaz/api/sim.py |
| POST | `/api/sql/blanquear` | `dataset_sql_blanquear` |  | src/interfaz/api/etiquetado.py |
| POST | `/api/sql/config` | `dataset_sql_config` |  | src/interfaz/api/etiquetado.py |
| GET | `/api/sql/estado` | `dataset_sql_estado` |  | src/interfaz/api/etiquetado.py |
| POST | `/api/sql/generar` | `dataset_sql_generar` |  | src/interfaz/api/etiquetado.py |
| GET | `/api/state` | `state` |  | src/interfaz/api/sesion.py |
| GET | `/api/system/droidcam` | `droidcam_lista` |  | src/interfaz/api/sistema.py |
| POST | `/api/system/droidcam` | `droidcam_guardar` | Guarda la lista de DroidCam (IP:puerto) en datos/config.json; aparecen en amarillo en el selector de camaras. | src/interfaz/api/sistema.py |
| POST | `/api/system/libraries/update` | `actualizar_libreria` | Actualiza una libreria (o todas, si no se pasa nombre) respetando lo | src/interfaz/api/sistema.py |
| GET | `/api/system/python` | `python_entorno` |  | src/interfaz/api/sistema.py |
| POST | `/api/system/python_version` | `cambiar_version_python` | Recrea el entorno virtual con otra version de Python y reinicia. | src/interfaz/api/sistema.py |
| GET | `/api/system/respaldo-sql` | `respaldo_sql_estado` | El disco es la fuente de los datos; SQL Server es una copia. Cuando se actualiza la copia: al cortar y/o al entrenar. | src/interfaz/api/sistema.py |
| POST | `/api/system/respaldo-sql` | `respaldo_sql_guardar` |  | src/interfaz/api/sistema.py |
| POST | `/api/system/respaldo-sql/ahora` | `respaldo_sql_ahora` | Copia a SQL todos los clips del disco ya mismo (ignora las dos opciones de arriba). | src/interfaz/api/sistema.py |
| POST | `/api/system/restart` | `system_restart` | Como apagar, pero antes relanza GYMFITX.bat en una ventana nueva. | src/interfaz/api/sistema.py |
| POST | `/api/system/shutdown` | `system_shutdown` | Guarda lo que haya en curso y cierra el proceso del servidor. El | src/interfaz/api/sistema.py |
| GET | `/api/system/sql` | `sql_servidor` | Servidor y base en uso (de datos/config.json si existe) + estado de la conexion. | src/interfaz/api/sistema.py |
| POST | `/api/system/sql` | `sql_servidor_guardar` | Guarda servidor/base en datos/config.json, lo aplica sin reiniciar y reconecta. | src/interfaz/api/sistema.py |
| GET | `/api/tiempos` | `tiempos_api` | Matriz de tiempos por proceso de esta sesion (tambien en datos/logs/tiempos_*.log). | src/interfaz/app.py |
| GET | `/api/tipos` | `dataset_tipos` |  | src/interfaz/api/etiquetado.py |
| GET | `/data/{name:path}` | `dataset_data` |  | src/interfaz/api/etiquetado.py |
| GET | `/video` | `video` | MJPEG. El JPEG se codifica en un hilo (antes bloqueaba el event loop | src/interfaz/api/sesion.py |
| WEBSOCKET | `/ws` | `ws_endpoint` |  | src/interfaz/api/sesion.py |
