# `src/nucleo/config.py`

```text
Rutas y configuracion del proyecto en un solo lugar. Ningun otro modulo arma rutas a mano.

Estructura en disco:

    GYMFIT/
      src/             codigo (una rama por funcion)
      ejercicios/      un .yaml por ejercicio (datos, no codigo)
      modelos/         modelos de MediaPipe (*.task, se descargan solos)
      datos/           TODO lo que genera el uso (fuera de git):
        grabaciones/     <ejercicio>/<AAAA-MM-DD>/HHMMSS_<modo>.{mp4,npz,json}
        plantillas/      toma de referencia calibrada por ejercicio
        clips/           <ejercicio>/<clase>/<clip>.{mp4,npz}  (dataset)
        entrenamientos/  run_N/ (modelo.joblib, meta.json, graficas)
        previews/        copia H.264 de cada grabacion para el navegador
        etiquetas.json, manifest.json, ...
      herramientas/    cloudflared.exe (boton Publicar)
```

## Constantes

`PAQUETE`, `ROOT`, `EXERCISES_DIR`, `MODELS_DIR`, `HERRAMIENTAS_DIR`, `WEB_DIR`, `PITCH_DIR`, `DICCIONARIO_DIR`, `REPORTES_DIR`, `PARAMS_PATH`, `DATOS_DIR`, `RECORDINGS_DIR`, `TEMPLATES_DIR`, `CLIPS_DIR`, `SLURM_DIR`, `ENTRENAMIENTOS_DIR`, `PREVIEWS_DIR`, `ETIQUETAS_PATH`, `MANIFEST_PATH`, `EXPORT_ESTADO_PATH`, `SELECCION_PATH`, `SQL_CONFIG_PATH`, `SQL_TIPOS_PATH`, `AJUSTES_PATH`, `ACCESO_PATH`, `CONFIG_PATH`, `LOG_DIR`, `SPOOL_PATH`, `KPOINTS_PENDIENTES_PATH`, `DB_PATH`, `PUERTO_PANEL`, `SERVIDORES_POR_PC`, `_PC`, `_AJUSTES`, `SQLSERVER_HOST`, `SQLSERVER_DB`, `SQLSERVER_TIMEOUT_S`, `DROIDCAM_PUERTO`, `_DROIDCAM`, `_NADA`, `MODELOS_MATRIZ`

## `leer_ajustes`

`def leer_ajustes() -> dict`

```text
datos/config.json ({} si no existe o esta roto).
```

## `guardar_servidor_sql`

`def guardar_servidor_sql(host: str, base: str) -> None`

```text
Guarda en datos/config.json y lo aplica ya (sqlserver.py lee estos valores en cada conexion).
```

## `normalizar_droidcam`

`def normalizar_droidcam(entrada: str) -> str`

```text
'192.168.1.20' o '192.168.1.20:4747' -> 'IP:puerto' (puerto por defecto 4747). ValueError si no sirve.
```

## `url_droidcam`

`def url_droidcam(entrada: str) -> str`

_sin docstring_

## `droidcams`

`def droidcams() -> list[str]`

_sin docstring_

## `guardar_droidcams`

`def guardar_droidcams(lista: list[str]) -> list[str]`

```text
Guarda la lista (sin repetidos, en orden) en datos/config.json y la devuelve normalizada.
```

## `params`

`def params(seccion: str) -> dict`

```text
Una seccion de params.yaml (seleccion, limpieza, construccion, formato, entrenamiento, base_clip...). Sin valores por
defecto a proposito: cada umbral vive en ese archivo y en ningun otro lado (criterio de parametrizacion).
```

## `formato_de`

`def formato_de(ejercicio: str | None) -> dict`

```text
Lo que params.yaml fija de la normalizacion (modo, n_frames_fijo...) y sus ajustes por ejercicio. Se completa con los
defaults de procesamiento/puntos/normalizacion.py (cfg_para).
```

## `respaldo_sql`

`def respaldo_sql() -> dict`

_sin docstring_

## `guardar_respaldo_sql`

`def guardar_respaldo_sql(al_cortar: bool, al_entrenar: bool) -> dict`

_sin docstring_

## `_celda_valida`

`def _celda_valida(k: str, v) -> bool`

_sin docstring_

## `matriz_modelos`

`def matriz_modelos() -> dict`

```text
La matriz efectiva: defaults + lo guardado en datos/config.json ("modelos"), leido en cada llamada
(cambiarla no pide reiniciar). Las celdas guardadas que no aplican o no son validas se ignoran.
```

## `guardar_matriz_modelos`

`def guardar_matriz_modelos(cambios: dict) -> dict`

```text
Aplica 'cambios' ({modelo: {celda: valor}}) sobre la matriz efectiva, guarda en datos/config.json
solo lo que difiere de los defaults y devuelve la matriz efectiva.
```

