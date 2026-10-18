"""Rutas y configuracion del proyecto en un solo lugar. Ningun otro modulo arma rutas a mano.

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
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

PAQUETE = Path(__file__).resolve().parent.parent   # src/
ROOT = PAQUETE.parent

EXERCISES_DIR = ROOT / "ejercicios"
MODELS_DIR = ROOT / "modelos"
HERRAMIENTAS_DIR = ROOT / "herramientas"
WEB_DIR = PAQUETE / "interfaz" / "web"
PITCH_DIR = ROOT / "docs" / "pitch"
DICCIONARIO_DIR = ROOT / "docs" / "diccionario"   # criterio 5 CRISP-DM: una fila por columna del vector final (se versiona)
REPORTES_DIR = ROOT / "reportes"                  # criterio 6: informe de limpieza por ejercicio (se versiona)
PARAMS_PATH = ROOT / "params.yaml"                # umbrales de limpieza y documentacion (se versiona)

DATOS_DIR = Path(os.environ.get("GYMFITX_DATOS") or ROOT / "datos")
RECORDINGS_DIR = DATOS_DIR / "grabaciones"
TEMPLATES_DIR = DATOS_DIR / "plantillas"
CLIPS_DIR = DATOS_DIR / "clips"
SLURM_DIR = DATOS_DIR / "slurm"       # .npz autocontenidos para scripts/busqueda_features_slurm.py (modulo AHPC)
ENTRENAMIENTOS_DIR = DATOS_DIR / "entrenamientos"
PREVIEWS_DIR = DATOS_DIR / "previews"

ETIQUETAS_PATH = DATOS_DIR / "etiquetas.json"        # cortes y clase por segmento (unica fuente)
MANIFEST_PATH = DATOS_DIR / "manifest.json"          # clips exportados
EXPORT_ESTADO_PATH = DATOS_DIR / "export_estado.json"
SELECCION_PATH = DATOS_DIR / "seleccion_entrenamiento.json"
SQL_CONFIG_PATH = DATOS_DIR / "sql_config.json"      # normalizacion por type
SQL_TIPOS_PATH = DATOS_DIR / "sql_tipos.json"        # ejercicio -> type
AJUSTES_PATH = DATOS_DIR / "ajustes.yaml"            # clases del cortador
ACCESO_PATH = DATOS_DIR / "acceso.json"              # usuario/clave del tunel (solo hash)
CONFIG_PATH = DATOS_DIR / "config.json"             # ajustes editables desde Sistema (servidor SQL, base)
LOG_DIR = DATOS_DIR / "logs"                  # un archivo por sesion (arranque del panel o del .bat)
SPOOL_PATH = DATOS_DIR / "pendientes_sql.jsonl"      # escrituras que esperan a SQL Server
KPOINTS_PENDIENTES_PATH = DATOS_DIR / "pendientes_kpoints.json"   # ejercicios guardados en local que aun no se subieron a SQL
DB_PATH = DATOS_DIR / "gymfitx.db"                   # SQLite viejo: solo se lee para migrar

PUERTO_PANEL = int(os.environ.get("GYMFITX_PORT", "8000"))

for _d in (DATOS_DIR, RECORDINGS_DIR, TEMPLATES_DIR, CLIPS_DIR, ENTRENAMIENTOS_DIR, MODELS_DIR, SLURM_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# -- SQL Server (una sola configuracion para todo el proyecto) ---------------
# Orden: 1) datos/config.json (lo que se guarda desde Sistema), 2) variable de entorno,
# 3) el servidor de esta PC, 4) PROGRAM\HYPER.
# Autenticacion de Windows (Trusted_Connection): sin usuario/clave que guardar.
SERVIDORES_POR_PC = {
    "HYPERCUBE": r"HYPERCUBE\SERVER",
    "PROGRAM": r"PROGRAM\HYPER",
}
_PC = (os.environ.get("COMPUTERNAME") or os.environ.get("HOSTNAME") or "").upper()


def leer_ajustes() -> dict:
    """datos/config.json ({} si no existe o esta roto)."""
    try:
        return json.loads(CONFIG_PATH.read_text("utf-8"))
    except (OSError, ValueError):
        return {}


_AJUSTES = leer_ajustes()
SQLSERVER_HOST = (_AJUSTES.get("sqlserver_host") or os.environ.get("GYMFITX_SQLSERVER_HOST")
                  or SERVIDORES_POR_PC.get(_PC, r"PROGRAM\HYPER"))
SQLSERVER_DB = _AJUSTES.get("sqlserver_db") or os.environ.get("GYMFITX_SQLSERVER_DB") or "GymFitX"
# segundos que se espera a SQL Server al conectar (datos/config.json: "sqlserver_timeout_s"); mas alto = arranque lento si esta caido
SQLSERVER_TIMEOUT_S = int(_AJUSTES.get("sqlserver_timeout_s") or 3)


def guardar_servidor_sql(host: str, base: str) -> None:
    """Guarda en datos/config.json y lo aplica ya (sqlserver.py lee estos valores en cada conexion)."""
    global SQLSERVER_HOST, SQLSERVER_DB
    host, base = host.strip(), base.strip()
    if not host or not base:
        raise ValueError("Servidor y base no pueden quedar vacios")
    ajustes = {**leer_ajustes(), "sqlserver_host": host, "sqlserver_db": base}
    CONFIG_PATH.write_text(json.dumps(ajustes, indent=1, ensure_ascii=False), "utf-8")
    SQLSERVER_HOST, SQLSERVER_DB = host, base


# -- DroidCam (camara del celular por WiFi) -----------------------------------
# datos/config.json -> "droidcam": ["192.168.1.20:4747", ...]; cada entrada es IP:puerto en un solo texto.
DROIDCAM_PUERTO = 4747
_DROIDCAM = re.compile(r"^([A-Za-z0-9][A-Za-z0-9.\-]*)(?::(\d{1,5}))?$")


def normalizar_droidcam(entrada: str) -> str:
    """'192.168.1.20' o '192.168.1.20:4747' -> 'IP:puerto' (puerto por defecto 4747). ValueError si no sirve."""
    m = _DROIDCAM.match(str(entrada).strip())
    puerto = int(m.group(2) or DROIDCAM_PUERTO) if m else 0
    if not m or not 1 <= puerto <= 65535:
        raise ValueError(f"'{entrada}' no es valido: escribe IP:puerto, por ejemplo 192.168.1.20:4747")
    return f"{m.group(1)}:{puerto}"


def url_droidcam(entrada: str) -> str:
    return f"http://{normalizar_droidcam(entrada)}/video"


def droidcams() -> list[str]:
    return [e for e in leer_ajustes().get("droidcam", []) if isinstance(e, str)]


def guardar_droidcams(lista: list[str]) -> list[str]:
    """Guarda la lista (sin repetidos, en orden) en datos/config.json y la devuelve normalizada."""
    ok = list(dict.fromkeys(normalizar_droidcam(e) for e in lista))
    CONFIG_PATH.write_text(json.dumps({**leer_ajustes(), "droidcam": ok}, indent=1, ensure_ascii=False), "utf-8")
    return ok


# -- Parametros de la preparacion de datos (params.yaml, se versiona) -----------
def params(seccion: str) -> dict:
    """Una seccion de params.yaml (seleccion, limpieza, construccion, formato, entrenamiento, base_clip...). Sin valores por
    defecto a proposito: cada umbral vive en ese archivo y en ningun otro lado (criterio de parametrizacion)."""
    try:
        import yaml
        return dict((yaml.safe_load(PARAMS_PATH.read_text("utf-8")) or {})[seccion])
    except (OSError, KeyError, TypeError) as e:
        raise ValueError(f"falta la seccion '{seccion}' en {PARAMS_PATH}") from e


def formato_de(ejercicio: str | None) -> dict:
    """Lo que params.yaml fija de la normalizacion (modo, n_frames_fijo...) y sus ajustes por ejercicio. Se completa con los
    defaults de procesamiento/puntos/normalizacion.py (cfg_para)."""
    f = params("formato")
    base = {k: v for k, v in f.items() if k not in ("componentes", "por_ejercicio")}
    return {**base, **((f.get("por_ejercicio") or {}).get(ejercicio) or {})}


# -- Respaldo en SQL Server (el disco es la fuente; SQL es copia) ----------------
# datos/config.json -> "respaldo_sql": {"al_cortar": true, "al_entrenar": true}
def respaldo_sql() -> dict:
    return {"al_cortar": True, "al_entrenar": True, **(leer_ajustes().get("respaldo_sql") or {})}


def guardar_respaldo_sql(al_cortar: bool, al_entrenar: bool) -> dict:
    cfg = {"al_cortar": bool(al_cortar), "al_entrenar": bool(al_entrenar)}
    CONFIG_PATH.write_text(json.dumps({**leer_ajustes(), "respaldo_sql": cfg}, indent=1, ensure_ascii=False), "utf-8")
    return cfg


# -- Entrenamiento: matriz de modelos ---------------------------------------
# Una fila por modelo (se edita en Sistema -> Modelos de entrenamiento; se guarda en datos/config.json -> "modelos").
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
    """La matriz efectiva: defaults + lo guardado en datos/config.json ("modelos"), leido en cada llamada
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
    """Aplica 'cambios' ({modelo: {celda: valor}}) sobre la matriz efectiva, guarda en datos/config.json
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
    ajustes = {**leer_ajustes(), "modelos": {n: f for n, f in difiere.items() if f}}
    CONFIG_PATH.write_text(json.dumps(ajustes, indent=1, ensure_ascii=False), "utf-8")
    return matriz_modelos()
