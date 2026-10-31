"""Rutas y configuracion del proyecto en un solo lugar. Ningun otro modulo arma rutas a mano.

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
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

PAQUETE = Path(__file__).resolve().parent.parent   # src/
ROOT = PAQUETE.parent

WEB_DIR = PAQUETE / "interfaz" / "web"
PITCH_DIR = ROOT / "docs" / "pitch"
DICCIONARIO_DIR = ROOT / "docs" / "diccionario"   # criterio 5 CRISP-DM: una fila por columna del vector final (se versiona)
MODELS_DIR = ROOT / "assets"
INPUT_DIR = Path(os.environ.get("GYMFITX_INPUT") or ROOT / "input")
RECORDINGS_DIR = INPUT_DIR / "raw"
CLIPS_DIR = INPUT_DIR / "bronze"
PLATE_DIR = INPUT_DIR / "plate"
GOLD_DIR = INPUT_DIR / "gold"
OUTPUT_DIR = Path(os.environ.get("GYMFITX_OUTPUT") or ROOT / "output")
ENTRENAMIENTOS_DIR = OUTPUT_DIR / "models"             # <ej>/run_001/
REPORTES_DIR = OUTPUT_DIR / "reportes"                 # informes de limpieza / seleccion por ejercicio
PARAMETROS_DIR = Path(os.environ.get("GYMFITX_PARAMETROS") or ROOT / "parameters")
INPUTS_PATH = PARAMETROS_DIR / "inputs.json"           # tablas raw y clips
EXERCISE_PATH = PARAMETROS_DIR / "exercise.json"       # id -> ejercicio
CONFIG_PATH = PARAMETROS_DIR / "config.json"           # umbrales (params), modelos, camaras, respaldo
SERVER_PATH = PARAMETROS_DIR / "server.json"           # servidor SQL
TEMPLATES_DIR = PARAMETROS_DIR / "plantillas"

DATOS_DIR = Path(os.environ.get("GYMFITX_DATOS") or ROOT / "sistema")   # estado de ejecucion
SLURM_DIR = DATOS_DIR / "slurm"       # .npz autocontenidos para scripts/hpc/busqueda_features_slurm.py (modulo AHPC)
PREVIEWS_DIR = DATOS_DIR / "previews"
EXPORT_ESTADO_PATH = DATOS_DIR / "export_estado.json"
SQL_CONFIG_PATH = DATOS_DIR / "sql_config.json"      # normalizacion por type
SQL_TIPOS_PATH = DATOS_DIR / "sql_tipos.json"        # ejercicio -> type
ACCESO_PATH = DATOS_DIR / "acceso.json"              # usuario/clave del tunel (solo hash)
LOG_DIR = DATOS_DIR / "logs"                  # un archivo por sesion (arranque del panel o del .bat)
SPOOL_PATH = DATOS_DIR / "pendientes_sql.jsonl"      # escrituras que esperan a SQL Server
KPOINTS_PENDIENTES_PATH = DATOS_DIR / "pendientes_kpoints.json"   # ejercicios guardados en local que aun no se subieron a SQL
DB_PATH = DATOS_DIR / "gymfitx.db"                   # SQLite viejo: solo se lee para migrar

PUERTO_PANEL = int(os.environ.get("GYMFITX_PORT", "8000"))

for _d in (DATOS_DIR, RECORDINGS_DIR, TEMPLATES_DIR, CLIPS_DIR, PLATE_DIR, GOLD_DIR, ENTRENAMIENTOS_DIR, PARAMETROS_DIR, SLURM_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# -- SQL Server (una sola configuracion para todo el proyecto) ---------------
# Orden: 1) parameters/config.json (lo que se guarda desde Sistema), 2) variable de entorno,
# 3) el servidor de esta PC, 4) PROGRAM\HYPER.
# Autenticacion de Windows (Trusted_Connection): sin usuario/clave que guardar.
SERVIDORES_POR_PC = {
    "HYPERCUBE": r"HYPERCUBE\SERVER",
    "PROGRAM": r"PROGRAM\HYPER",
}
_PC = (os.environ.get("COMPUTERNAME") or os.environ.get("HOSTNAME") or "").upper()


def _leer_json(path) -> dict:
    try:
        d = json.loads(Path(path).read_text("utf-8"))
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError):
        return {}


def _actualizar_json(path, cambios: dict) -> None:
    """Mezcla 'cambios' en el json (escritura atomica: nunca queda a medias)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps({**_leer_json(path), **cambios}, indent=1, ensure_ascii=False) + "\n", "utf-8")
    tmp.replace(path)


# nombre interno de cada ajuste -> (archivo, clave). server.json = SQL; config.json = el resto.
_AJUSTE_EN_SERVER = {"sqlserver_host": "host", "sqlserver_db": "base", "sqlserver_timeout_s": "timeout_s",
                     "servidores_por_pc": "servidores_por_pc"}


def leer_ajustes() -> dict:
    """Los ajustes editables, con los nombres de siempre: parameters/server.json (SQL) + parameters/config.json."""
    c, s = _leer_json(CONFIG_PATH), _leer_json(SERVER_PATH)
    out = {**c, "droidcam": c.get("camaras_droidcam", [])}
    out.update({viejo: s[nuevo] for viejo, nuevo in _AJUSTE_EN_SERVER.items() if nuevo in s})
    return out


_AJUSTES = leer_ajustes()
_SERVIDORES = {**SERVIDORES_POR_PC, **(_AJUSTES.get("servidores_por_pc") or {})}   # parameters/config.json puede agregar PCs
SQLSERVER_HOST = (_AJUSTES.get("sqlserver_host") or os.environ.get("GYMFITX_SQLSERVER_HOST")
                  or _SERVIDORES.get(_PC, r"PROGRAM\HYPER"))
SQLSERVER_DB = _AJUSTES.get("sqlserver_db") or os.environ.get("GYMFITX_SQLSERVER_DB") or "GymFitX"
# segundos que se espera a SQL Server al conectar (parameters/config.json: "sqlserver_timeout_s"); mas alto = arranque lento si esta caido
SQLSERVER_TIMEOUT_S = int(_AJUSTES.get("sqlserver_timeout_s") or 3)


def guardar_servidor_sql(host: str, base: str) -> None:
    """Guarda en parameters/server.json y lo aplica ya (sqlserver.py lee estos valores en cada conexion)."""
    global SQLSERVER_HOST, SQLSERVER_DB
    host, base = host.strip(), base.strip()
    if not host or not base:
        raise ValueError("Servidor y base no pueden quedar vacios")
    _actualizar_json(SERVER_PATH, {"host": host, "base": base})
    SQLSERVER_HOST, SQLSERVER_DB = host, base


# -- DroidCam (camara del celular por WiFi) -----------------------------------
# parameters/config.json -> "camaras_droidcam": [{"nombre": "Celular Juan", "ip": "100.101.102.103:4747"}, ...]
# (el formato viejo, un texto "IP:puerto" por entrada, tambien se lee). El nombre es lo que se muestra en el selector.
DROIDCAM_PUERTO = 4747
_DROIDCAM = re.compile(r"^([A-Za-z0-9][A-Za-z0-9.\-]*)(?::(\d{1,5}))?$")


def normalizar_droidcam(entrada: str) -> str:
    """'192.168.1.20', IP de Tailscale ('100.x.y.z') o nombre MagicDNS, con o sin ':4747' -> 'host:puerto' (puerto por defecto 4747). ValueError si no sirve."""
    m = _DROIDCAM.match(str(entrada).strip())
    puerto = int(m.group(2) or DROIDCAM_PUERTO) if m else 0
    if not m or not 1 <= puerto <= 65535:
        raise ValueError(f"'{entrada}' no es valido: escribe IP:puerto, por ejemplo 192.168.1.20:4747 o la IP de Tailscale 100.101.102.103:4747")
    return f"{m.group(1)}:{puerto}"


def url_droidcam(entrada: str) -> str:
    return f"http://{normalizar_droidcam(entrada)}/video"


def _entrada_droidcam(e) -> dict:
    """Una entrada guardada: 'IP:puerto' (formato viejo) o {"nombre", "ip"} -> {"nombre", "ip"} normalizado."""
    nombre, ip = (e.get("nombre"), e.get("ip")) if isinstance(e, dict) else ("", e)
    nombre = " ".join(str(nombre or "").split())[:40]
    return {"nombre": nombre, "ip": normalizar_droidcam(ip)}


def droidcams_nombrados() -> list[dict]:
    """[{"nombre", "ip"}] de lo guardado (lo invalido se salta)."""
    out = []
    for e in leer_ajustes().get("droidcam", []):
        try:
            out.append(_entrada_droidcam(e))
        except ValueError:
            continue
    return out


def droidcams() -> list[str]:
    return [d["ip"] for d in droidcams_nombrados()]


def guardar_droidcams(lista: list) -> list[str]:
    """Guarda la lista (strings 'IP:puerto' o {"nombre","ip"}; sin IPs repetidas, en orden) en parameters/config.json. -> las IP."""
    ok = list({d["ip"]: d for d in map(_entrada_droidcam, lista)}.values())
    _actualizar_json(CONFIG_PATH, {"camaras_droidcam": ok})
    return [d["ip"] for d in ok]


# -- Parametros de la preparacion de datos (parameters/config.json, se versiona) -
def params(seccion: str) -> dict:
    """Una seccion de parameters/config.json (seleccion, limpieza, construccion, formato, entrenamiento, base_clip...). Sin
    valores por defecto a proposito: cada umbral vive en ese archivo y en ningun otro lado (criterio de parametrizacion)."""
    try:
        return dict(json.loads(CONFIG_PATH.read_text("utf-8"))[seccion])
    except (OSError, KeyError, TypeError, ValueError) as e:
        raise ValueError(f"falta la seccion '{seccion}' en {CONFIG_PATH}") from e


# -- Respaldo en SQL Server (el disco es la fuente; SQL es copia) ----------------
# parameters/config.json -> "respaldo_sql": {"al_cortar": true, "al_entrenar": true}
def respaldo_sql() -> dict:
    return {"al_cortar": True, "al_entrenar": True, **(leer_ajustes().get("respaldo_sql") or {})}


def guardar_respaldo_sql(al_cortar: bool, al_entrenar: bool) -> dict:
    cfg = {"al_cortar": bool(al_cortar), "al_entrenar": bool(al_entrenar)}
    _actualizar_json(CONFIG_PATH, {"respaldo_sql": cfg})
    return cfg


# -- Entrenamiento: matriz de modelos ---------------------------------------
# Una fila por modelo (se edita en Sistema -> Modelos de entrenamiento; se guarda en parameters/config.json -> "modelos").
#   epocas    arboles/rondas del ensamble (n_estimators, iterations)
#   max_iter  tope de iteraciones del optimizador (logistic, sgd, mlp, hist_gb)
#   parar     early stopping: frenar antes si deja de mejorar con datos de validacion (gb, hist_gb, sgd, mlp)
#   paciencia iteraciones seguidas sin mejorar antes de frenar (n_iter_no_change)
#   tol       cuanto tiene que mejorar para contar como mejora
# None = no aplica a ese modelo. Los defaults son los de scikit-learn: no cambian los resultados hasta que los edites.
_NADA = {"epocas": None, "max_iter": None, "parar": None, "paciencia": None, "tol": None}
MODELOS_MATRIZ = {
    "random_forest":          {**_NADA, "epocas": 200},
    "extra_trees":            {**_NADA, "epocas": 200},
    "gradient_boosting":      {**_NADA, "epocas": 150, "parar": False, "paciencia": 10, "tol": 1e-4},
    "hist_gradient_boosting": {**_NADA, "max_iter": 100, "parar": False, "paciencia": 10, "tol": 1e-7},
    "adaboost":               {**_NADA, "epocas": 150},
    "logistic":               {**_NADA, "max_iter": 2000, "tol": 1e-4},
    "sgd_logistico":          {**_NADA, "max_iter": 1000, "parar": False, "paciencia": 5, "tol": 1e-3},
    "ridge":                  dict(_NADA),
    "lda":                    dict(_NADA),
    "svm":                    dict(_NADA),
    "knn":                    dict(_NADA),
    "decision_tree":          dict(_NADA),
    "mlp":                    {**_NADA, "max_iter": 2000, "parar": False, "paciencia": 10, "tol": 1e-4},
    "naive_bayes":            dict(_NADA),
    "lightgbm":               {**_NADA, "epocas": 200},
    "catboost":               {**_NADA, "epocas": 200},
    "xgboost":                {**_NADA, "epocas": 200},
}


def _celda_valida(k: str, v) -> bool:
    if k == "parar":
        return isinstance(v, bool)
    if k == "tol":
        return isinstance(v, (int, float)) and not isinstance(v, bool) and 0 < v < 1
    return isinstance(v, int) and not isinstance(v, bool) and v >= 1


def matriz_modelos() -> dict:
    """La matriz efectiva: defaults + lo guardado en parameters/config.json ("modelos"), leido en cada llamada
    (cambiarla no pide reiniciar). Las celdas guardadas que no aplican o no son validas se ignoran."""
    guardado = leer_ajustes().get("modelos") or {}
    out = {}
    for nombre, base in MODELOS_MATRIZ.items():
        fila = dict(base)
        for k, v in (guardado.get(nombre) or {}).items():
            if k in base and base[k] is not None and _celda_valida(k, v):
                fila[k] = v
        out[nombre] = fila
    return out


def guardar_matriz_modelos(cambios: dict) -> dict:
    """Aplica 'cambios' ({modelo: {celda: valor}}) sobre la matriz efectiva, guarda en parameters/config.json
    solo lo que difiere de los defaults y devuelve la matriz efectiva."""
    nueva = matriz_modelos()
    for nombre, fila in (cambios or {}).items():
        if nombre not in MODELOS_MATRIZ:
            raise ValueError(f"modelo desconocido: {nombre}")
        for k, v in fila.items():
            if k not in MODELOS_MATRIZ[nombre] or MODELOS_MATRIZ[nombre][k] is None:
                raise ValueError(f"{nombre}.{k} no aplica a este modelo")
            if not _celda_valida(k, v):
                raise ValueError(f"{nombre}.{k}: valor invalido ({v!r})")
            nueva[nombre][k] = v
    difiere = {n: {k: v for k, v in f.items() if v != MODELOS_MATRIZ[n][k]} for n, f in nueva.items()}
    _actualizar_json(CONFIG_PATH, {"modelos": {n: f for n, f in difiere.items() if f}})
    return matriz_modelos()
