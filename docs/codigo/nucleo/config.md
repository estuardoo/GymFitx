# `src/nucleo/config.py`

```text
Rutas y configuracion del proyecto en un solo lugar. Ningun otro modulo arma rutas a mano.

Estructura en disco (todo se identifica por NUMERO: ejercicio 1, 2...; clip 000123; run_001):

    GYMFIT/
      src/ tests/ scripts/ docs/    codigo y documentacion
      assets/          modelos de MediaPipe (*.task, se descargan solos) + cloudflared.exe (boton Publicar)
      input/           LOS DATOS (fuera de git), cada capa por ejercicio: input/<capa>/<ej>/<id>.<ext>
        raw/             grabacion tal cual se grabo (.mp4 .npz .json)
        bronze/          clips cortados (.mp4 .npz)
        plate/           puntos + angulos por clip, sin normalizar (.p.npy .a.npy)
        gold/            vector normalizado listo para entrenar (.npy)
      output/          LO QUE SE PRODUCE
        models/<ej>/run_001/   modelo.joblib + meta.json (con el origen de cada dato) + graficas
        reportes/              informes de limpieza / seleccion por ejercicio
      parameters/      CONFIGURACION y metadata (se versiona)
        exercise.json  tabla numerada de ejercicios      config.json  umbrales, modelos, camaras, cortador
        server.json    servidor SQL
        inputs.json    tablas raw y clips (persona, etiqueta 1/0, origen)
        <ej>/kpoints.json, angles.json, guide.json   definicion de cada ejercicio (puntos, angulos, guia): lo edita el panel
        plantillas/    toma de referencia calibrada por ejercicio
      sistema/         estado de ejecucion: logs, previews, gymfitx.db, acceso, pendientes de SQL
```

## Constantes

`PAQUETE`, `ROOT`, `WEB_DIR`, `PITCH_DIR`, `DICCIONARIO_DIR`, `MODELS_DIR`, `INPUT_DIR`, `RECORDINGS_DIR`, `CLIPS_DIR`, `PLATE_DIR`, `GOLD_DIR`, `OUTPUT_DIR`, `ENTRENAMIENTOS_DIR`, `REPORTES_DIR`, `PARAMETROS_DIR`, `INPUTS_PATH`, `EXERCISE_PATH`, `CONFIG_PATH`, `SERVER_PATH`, `TEMPLATES_DIR`, `DATOS_DIR`, `SLURM_DIR`, `PREVIEWS_DIR`, `EXPORT_ESTADO_PATH`, `SQL_CONFIG_PATH`, `SQL_TIPOS_PATH`, `ACCESO_PATH`, `LOG_DIR`, `SPOOL_PATH`, `KPOINTS_PENDIENTES_PATH`, `DB_PATH`, `PUERTO_PANEL`, `SERVIDORES_POR_PC`, `_PC`, `_AJUSTE_EN_SERVER`, `_AJUSTES`, `_SERVIDORES`, `SQLSERVER_HOST`, `SQLSERVER_DB`, `SQLSERVER_TIMEOUT_S`, `DROIDCAM_PUERTO`, `_DROIDCAM`, `_NADA`, `MODELOS_MATRIZ`

## `_leer_json`

`def _leer_json(path) -> dict`

_sin docstring_

## `_actualizar_json`

`def _actualizar_json(path, cambios: dict) -> None`

```text
Mezcla 'cambios' en el json (escritura atomica: nunca queda a medias).
```

## `leer_ajustes`

`def leer_ajustes() -> dict`

```text
Los ajustes editables, con los nombres de siempre: parameters/server.json (SQL) + parameters/config.json.
```

## `guardar_servidor_sql`

`def guardar_servidor_sql(host: str, base: str) -> None`

```text
Guarda en parameters/server.json y lo aplica ya (sqlserver.py lee estos valores en cada conexion).
```

## `normalizar_droidcam`

`def normalizar_droidcam(entrada: str) -> str`

```text
'192.168.1.20', IP de Tailscale ('100.x.y.z') o nombre MagicDNS, con o sin ':4747' -> 'host:puerto' (puerto por defecto 4747). ValueError si no sirve.
```

## `url_droidcam`

`def url_droidcam(entrada: str) -> str`

_sin docstring_

## `_entrada_droidcam`

`def _entrada_droidcam(e) -> dict`

```text
Una entrada guardada: 'IP:puerto' (formato viejo) o {"nombre", "ip"} -> {"nombre", "ip"} normalizado.
```

## `droidcams_nombrados`

`def droidcams_nombrados() -> list[dict]`

```text
[{"nombre", "ip"}] de lo guardado (lo invalido se salta).
```

## `droidcams`

`def droidcams() -> list[str]`

_sin docstring_

## `guardar_droidcams`

`def guardar_droidcams(lista: list) -> list[str]`

```text
Guarda la lista (strings 'IP:puerto' o {"nombre","ip"}; sin IPs repetidas, en orden) en parameters/config.json. -> las IP.
```

## `params`

`def params(seccion: str) -> dict`

```text
Una seccion de parameters/config.json (seleccion, limpieza, construccion, formato, entrenamiento, base_clip...). Sin
valores por defecto a proposito: cada umbral vive en ese archivo y en ningun otro lado (criterio de parametrizacion).
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
La matriz efectiva: defaults + lo guardado en parameters/config.json ("modelos"), leido en cada llamada
(cambiarla no pide reiniciar). Las celdas guardadas que no aplican o no son validas se ignoran.
```

## `guardar_matriz_modelos`

`def guardar_matriz_modelos(cambios: dict) -> dict`

```text
Aplica 'cambios' ({modelo: {celda: valor}}) sobre la matriz efectiva, guarda en parameters/config.json
solo lo que difiere de los defaults y devuelve la matriz efectiva.
```

