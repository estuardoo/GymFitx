"""Editor visual de la definicion de cada ejercicio (parameters/<n>/, ver src/nucleo/definicion.py):
elegir con clic, sobre un diagrama del cuerpo, que landmarks
arma cada 'feature' (angulo o razon de distancia), en vez de escribir el archivo a mano.
Es el mismo dato que ya lee puntos_de_ejercicio() en src/nucleo/ejercicio.py -- este
modulo es el que ahora tambien puede ESCRIBIRLO.

Solo toca 'name'/'description'/'source'/'features'/'kpoints'; cualquier otra
clave (signal, segmentation...) se deja tal cual estaba. Antes de cada guardado la definicion
anterior queda en sistema/respaldos/<slug>.json."""
from __future__ import annotations

import json
import re
import time
from datetime import datetime

from src.nucleo import definicion as DEF
from src.nucleo.config import KPOINTS_PENDIENTES_PATH
from src.nucleo.ejercicio import construir, resolver_features
from src.nucleo.landmarks import POSE_CONNECTIONS_NOMBRES
from src.procesamiento.puntos import normalizacion as NORM
from src.procesamiento.puntos.kpoints import FUENTES_KPOINT

# --- catalogo de puntos: nombre -> (x, y, grupo), 0..1, y hacia arriba -------
# mismos 33 landmarks de MediaPipe Pose que ya usa dataset (ver poblar_desde_manifest),
# agrupados en las MISMAS 7 regiones del selector-cuerpo del header (ver
# src/nucleo/landmarks.POSE_REGIONES) para que el diagrama, la tabla numerada
# y el muneco del panel en vivo se vean con los mismos colores. POSE_REGIONES
# se define con solapes a proposito (el hombro cuenta para brazos Y torso);
# aqui cada punto necesita UN solo color, asi que se resuelve por prioridad
# (la region mas especifica gana): manos > pies > cadera > brazos > piernas > cabeza.
# 'torso' queda sin puntos propios -- MediaPipe no tiene un landmark de pecho.
# Nota: cabeza, manos y pies estan mas separados de lo que un cuerpo real
# guardaria proporcion -- a proposito, para que los puntos no se peguen entre
# si cuando se dibujan como circulos con brillo (ver _siluetaHumana en
# src/interfaz/web/js/puntos.js). No representan una pose real.
POSE_PUNTOS = {
    "NOSE": (0.50, 0.93, "cabeza"),
    "LEFT_EYE_INNER": (0.485, 0.955, "cabeza"), "LEFT_EYE": (0.465, 0.96, "cabeza"),
    "LEFT_EYE_OUTER": (0.44, 0.955, "cabeza"),
    "RIGHT_EYE_INNER": (0.515, 0.955, "cabeza"), "RIGHT_EYE": (0.535, 0.96, "cabeza"),
    "RIGHT_EYE_OUTER": (0.56, 0.955, "cabeza"),
    "LEFT_EAR": (0.40, 0.90, "cabeza"), "RIGHT_EAR": (0.60, 0.90, "cabeza"),
    "MOUTH_LEFT": (0.475, 0.895, "cabeza"), "MOUTH_RIGHT": (0.525, 0.895, "cabeza"),
    "LEFT_SHOULDER": (0.40, 0.80, "brazos"), "RIGHT_SHOULDER": (0.60, 0.80, "brazos"),
    # brazos largos: el brazo se abre 20 grados del cuerpo y el antebrazo sube "saludando"
    "LEFT_ELBOW": (0.31, 0.56, "brazos"), "RIGHT_ELBOW": (0.69, 0.56, "brazos"),
    "LEFT_WRIST": (0.20, 0.78, "manos"), "RIGHT_WRIST": (0.80, 0.78, "manos"),
    "LEFT_PINKY": (0.124, 0.843, "manos"), "RIGHT_PINKY": (0.876, 0.843, "manos"),
    "LEFT_INDEX": (0.170, 0.888, "manos"), "RIGHT_INDEX": (0.830, 0.888, "manos"),
    "LEFT_THUMB": (0.225, 0.843, "manos"), "RIGHT_THUMB": (0.775, 0.843, "manos"),
    "LEFT_HIP": (0.44, 0.50, "cadera"), "RIGHT_HIP": (0.56, 0.50, "cadera"),
    "LEFT_KNEE": (0.43, 0.28, "piernas"), "RIGHT_KNEE": (0.57, 0.28, "piernas"),
    # tobillo, talon (adentro) y punta del pie (afuera): los pies miran hacia afuera
    "LEFT_ANKLE": (0.42, 0.08, "pies"), "RIGHT_ANKLE": (0.58, 0.08, "pies"),
    "LEFT_HEEL": (0.44, 0.02, "pies"), "RIGHT_HEEL": (0.56, 0.02, "pies"),
    "LEFT_FOOT_INDEX": (0.32, 0.0, "pies"), "RIGHT_FOOT_INDEX": (0.68, 0.0, "pies"),
}
# cabeza mas grande y separada del cuerpo (x1.8 alrededor de su centro, subida) para que sus 11 puntos
# se puedan tocar; tampoco representa una pose real
_CENTRO_CABEZA, _CENTRO_NUEVO, _AUMENTO_CABEZA = (0.5, 0.925), (0.5, 1.02), 1.8
for _n, (_x, _y, _g) in list(POSE_PUNTOS.items()):
    if _g == "cabeza":
        POSE_PUNTOS[_n] = (round(_CENTRO_NUEVO[0] + _AUMENTO_CABEZA * (_x - _CENTRO_CABEZA[0]), 3),
                           round(_CENTRO_NUEVO[1] + _AUMENTO_CABEZA * (_y - _CENTRO_CABEZA[1]), 3), _g)
# Vista ESPEJO: la figura te mira, su lado DERECHO queda a la IZQUIERDA de la pantalla y el izquierdo a la derecha.
# Los puntos se escribieron con LEFT_ a la izquierda; aqui se espeja todo el dibujo una sola vez.
for _n, (_x, _y, _g) in list(POSE_PUNTOS.items()):
    POSE_PUNTOS[_n] = (round(1 - _x, 3), _y, _g)
# esqueleto del diagrama: la definicion unica de src/nucleo/landmarks.py
POSE_ESQUELETO = [list(par) for par in POSE_CONNECTIONS_NOMBRES]
POSE_GRUPOS = {
    "cabeza": "Cabeza", "manos": "Manos", "brazos": "Brazos", "torso": "Torso",
    "cadera": "Cadera", "piernas": "Piernas", "pies": "Pies",
}

# tipo de feature -> cuantos 'points' y 'reference' exige (ver las definiciones ya
# existentes: angle siempre 3 puntos, distance_ratio 2 + 2 de referencia)
TIPOS_FEATURE = {
    "angle": {"puntos": 3, "referencia": 0, "etiqueta": "Angulo fijo (3 puntos, vertice el del medio)"},
    "distance_ratio": {"puntos": 2, "referencia": 2, "etiqueta": "Razon de distancia (2 puntos / 2 de referencia)"},
    "proporcion": {"puntos": 2, "referencia": 0,
                   "etiqueta": "Proporcion en cadena (tramo / suma de tramos de la fila, base 100)"},
}

# Atajos de angulos "conocidos" (los mas comunes en rehab/ejercicio), sobre
# landmarks crudos de pose o de una mano -- un clic en la interfaz los agrega
# (creando en el catalogo de kpoints los que todavia falten) y arma la
# feature ya lista, sin dejar de poder crear cualquier otro a mano igual que
# antes.
ANGULOS_CONOCIDOS = {
    "pose": [
        {"nombre": "codo_izq", "puntos": ["LEFT_SHOULDER", "LEFT_ELBOW", "LEFT_WRIST"]},
        {"nombre": "codo_der", "puntos": ["RIGHT_SHOULDER", "RIGHT_ELBOW", "RIGHT_WRIST"]},
        {"nombre": "hombro_izq", "puntos": ["LEFT_HIP", "LEFT_SHOULDER", "LEFT_ELBOW"]},
        {"nombre": "hombro_der", "puntos": ["RIGHT_HIP", "RIGHT_SHOULDER", "RIGHT_ELBOW"]},
        {"nombre": "cadera_izq", "puntos": ["LEFT_SHOULDER", "LEFT_HIP", "LEFT_KNEE"]},
        {"nombre": "cadera_der", "puntos": ["RIGHT_SHOULDER", "RIGHT_HIP", "RIGHT_KNEE"]},
        {"nombre": "rodilla_izq", "puntos": ["LEFT_HIP", "LEFT_KNEE", "LEFT_ANKLE"]},
        {"nombre": "rodilla_der", "puntos": ["RIGHT_HIP", "RIGHT_KNEE", "RIGHT_ANKLE"]},
        {"nombre": "tobillo_izq", "puntos": ["LEFT_KNEE", "LEFT_ANKLE", "LEFT_FOOT_INDEX"]},
        {"nombre": "tobillo_der", "puntos": ["RIGHT_KNEE", "RIGHT_ANKLE", "RIGHT_FOOT_INDEX"]},
    ],
}

# --- catalogo de kpoints por ejercicio (vive en la definicion, parameters/<n>/kpoints.json) ------------------------------------------------------------
# Cada kpoint: {"numero": int, "nombre": str, "origen": {...}}. Es la lista de
# QUE landmarks le importan a este ejercicio -- de ahi salen (a) que trackers
# corre src/procesamiento/offline.py y (b) contra que nombres se validan los
# 'features' (angulos), en vez de contra los 33 landmarks crudos.
# origen = {"tipo": "landmark", "fuente": "pose", "landmark": NOMBRE}
#        o {"tipo": "derivado", "de": [numero_a, numero_b]}  (punto medio de otros dos kpoints
#           YA definidos antes en la lista -- ese orden es lo unico que evita ciclos)

def _nombres_landmark_de(fuente):
    """Los 33 nombres crudos de pose."""
    return {p["nombre"] for p in catalogo("pose")["puntos"]}


def _validar_kpoints(kpoints):
    vistos_num, vistos_nom = set(), set()
    for i, kp in enumerate(kpoints):
        numero, nombre = kp.get("numero"), kp.get("nombre")
        if numero is None or not nombre or not str(nombre).strip():
            raise ValueError(f"kpoint #{i + 1}: necesita 'numero' y 'nombre'")
        if numero in vistos_num:
            raise ValueError(f"numero {numero} repetido")
        if nombre in vistos_nom:
            raise ValueError(f"nombre '{nombre}' repetido")
        origen = kp.get("origen") or {}
        tipo = origen.get("tipo")
        if tipo == "landmark":
            fuente = origen.get("fuente")
            if fuente not in FUENTES_KPOINT:
                raise ValueError(f"'{nombre}': fuente '{fuente}' invalida")
            if origen.get("landmark") not in _nombres_landmark_de(fuente):
                raise ValueError(f"'{nombre}': landmark '{origen.get('landmark')}' no existe en '{fuente}'")
        elif tipo == "derivado":
            de = origen.get("de") or []
            if len(de) != 2:
                raise ValueError(f"'{nombre}': un punto derivado necesita exactamente 2 puntos base")
            if not all(n in vistos_num for n in de):
                raise ValueError(f"'{nombre}': solo puede derivarse de kpoints YA definidos antes en la lista")
        else:
            raise ValueError(f"'{nombre}': origen.tipo desconocido '{tipo}'")
        vistos_num.add(numero)
        vistos_nom.add(nombre)


def catalogo(source="pose"):
    """Puntos + esqueleto del diagrama de pose (33, cuerpo)."""
    return {
        "puntos": [{"nombre": n, "x": x, "y": y, "grupo": g} for n, (x, y, g) in POSE_PUNTOS.items()],
        "esqueleto": [list(par) for par in POSE_ESQUELETO],
        "grupos": POSE_GRUPOS,
        "angulos_conocidos": ANGULOS_CONOCIDOS.get(source, []),
    }


def listar_ejercicios():
    """Slugs de los ejercicios activos."""
    return DEF.slugs()


def leer_ejercicio(nombre):
    """Los campos editables de un ejercicio. None si no existe."""
    data = DEF.leer(nombre)
    if data is None:
        return None
    return {
        "name": data.get("name", nombre),
        "description": data.get("description", ""),
        "source": data.get("source", "pose"),
        "features": data.get("features") or [],
        "kpoints": data.get("kpoints") or [],
        "reglas": data.get("reglas") or [],
        "normalizacion": _normalizacion_panel(nombre, data),
    }


def _normalizacion_panel(nombre, data):
    n = NORM.normalizacion_de(nombre)
    n["error"] = None
    if n["origen"] or n["escala"]:
        try:
            NORM.validar_normalizacion(n, data.get("kpoints"))
        except ValueError as e:   # p.ej. la formula nombra un kpoint que se quito del catalogo
            n["error"] = str(e)
    return n


def _validar_features(source, features, kpoints=None):
    # Si el ejercicio ya tiene su catalogo de kpoints, los angulos solo pueden
    # referenciar ESOS nombres (lo que el usuario selecciono para ahorrar
    # deteccion). Sin catalogo todavia (ejercicios viejos): se valida contra
    # los 33/21 landmarks crudos, como antes.
    # Mejora: los 'features' de la definicion los mide GYMFITX en vivo con los nombres
    # CRUDOS de su 'source' (src/procesamiento/medidas/features.py -> resolve), asi que una definicion como
    # cuerpo_completo no se podia volver a
    # guardar desde aqui. Se aceptan ambos: nombres del catalogo o crudos.
    valido = {p["nombre"] for p in catalogo(source)["puntos"]}
    if kpoints:
        valido |= {kp["nombre"] for kp in kpoints}
    for feat in features:
        nombre, tipo = feat.get("name"), feat.get("type")
        if not nombre:
            raise ValueError("Cada feature necesita un nombre")
        if tipo not in TIPOS_FEATURE:
            raise ValueError(f"'{nombre}': tipo desconocido '{tipo}'")
        spec = TIPOS_FEATURE[tipo]
        puntos, referencia = feat.get("points") or [], feat.get("reference") or []
        if len(puntos) != spec["puntos"]:
            raise ValueError(f"'{nombre}' ({tipo}) necesita {spec['puntos']} puntos, llegaron {len(puntos)}")
        if len(referencia) != spec["referencia"]:
            raise ValueError(f"'{nombre}' ({tipo}) necesita {spec['referencia']} de referencia, llegaron {len(referencia)}")
        cadena = feat.get("cadena") or []
        if tipo == "proporcion":
            if len(cadena) < 3:
                raise ValueError(f"'{nombre}': necesita 'cadena' con 3 o mas puntos")
            if puntos not in [[a, b] for a, b in zip(cadena, cadena[1:])]:
                raise ValueError(f"'{nombre}': 'points' debe ser un tramo consecutivo de 'cadena'")
        for n in [*puntos, *referencia, *cadena]:
            if n not in valido:
                origen = "el catalogo de kpoints de este ejercicio" if kpoints else f"el catalogo de '{source}'"
                raise ValueError(f"'{nombre}': el punto '{n}' no existe en {origen}")


def _guardar_valido(nombre, data):
    """El ejercicio tiene que poder cargarse (si no, se cae /api/state para TODOS): se valida antes de escribir."""
    try:
        construir(nombre, data)
    except (ValueError, KeyError) as e:
        raise ValueError(f"El ejercicio no quedaria valido, no se guardo nada: {e}") from None
    DEF.guardar(nombre, data)


def _definicion_de(nombre):
    data = DEF.leer(nombre)
    if data is None:
        raise ValueError(f"No existe el ejercicio '{nombre}'")
    return data


def guardar_ejercicio(nombre, cambios):
    """cambios: {name, description, source, features, kpoints}. Valida
    kpoints (numeros/nombres unicos, origenes validos, derivados solo de
    kpoints previos) y luego features (mismo tipo conocido y cantidad de
    puntos/reference de siempre, pero ahora contra los nombres del catalogo
    de kpoints si ya existe uno) -- antes de tocar nada. Todo lo demas
    (signal, segmentation, etc) se deja tal cual estaba; la definicion anterior queda en
    sistema/respaldos/."""
    data = _definicion_de(nombre)

    source = cambios.get("source") or data.get("source", "pose")
    kpoints = cambios.get("kpoints") if "kpoints" in cambios else data.get("kpoints") or []
    _validar_kpoints(kpoints)
    features = cambios.get("features") or []
    _validar_features(source, features, kpoints)

    data["name"] = cambios.get("name") or data.get("name", nombre)
    data["description"] = cambios.get("description", data.get("description", ""))
    data["source"] = source
    data.pop("hand", None)   # clave vieja
    data["kpoints"] = [
        {k: v for k, v in kp.items() if k in ("numero", "nombre", "origen")}
        for kp in kpoints
    ]
    data["features"] = [
        {k: v for k, v in feat.items() if k in ("name", "type", "points", "reference", "cadena")
         and v} | ({"activo": False} if feat.get("activo") is False else {})
        for feat in features
    ]

    # signal.features viejas (del ejercicio base) que ya no existen: se descartan; si no queda ninguna, se usan todas
    sig = data.get("signal")
    if isinstance(sig, dict) and sig.get("features"):
        vivas = {f["name"] for f in data["features"] if f.get("activo") is not False}
        sig["features"] = [n for n in sig["features"] if n in vivas]
        if not sig["features"]:
            del sig["features"]

    _guardar_valido(nombre, data)


def guardar_reglas(nombre, reglas):
    """Reemplaza `reglas` de la definicion (validadas por nucleo/reglas.py) sin tocar el resto."""
    from src.nucleo import reglas as REGLAS
    data = _definicion_de(nombre)
    ok = REGLAS.validar(reglas)
    data["reglas"] = ok
    if not ok:
        del data["reglas"]
    DEF.guardar(nombre, data)
    return ok


def guardar_normalizacion(nombre, norm):
    """Guarda {origen, escala, n_frames} en la definicion (guide.json -> normalizacion) sin tocar el resto.
    -> {normalizacion, cambio}: cambio=True si difiere de lo vigente (gold se rehace solo; modelos ya entrenados: reentrenar)."""
    data = _definicion_de(nombre)
    limpio = NORM.validar_normalizacion(norm, data.get("kpoints"))
    antes = NORM.normalizacion_de(nombre)
    data["normalizacion"] = limpio
    DEF.guardar(nombre, data)
    return {"normalizacion": limpio, "cambio": any(antes[k] != limpio[k] for k in limpio)}


def crear_ejercicio(nombre):
    """Ejercicio nuevo desde cero (guardar_ejercicio solo puede EDITAR uno que ya exista): definicion
    minima pero valida, su numero y carpetas en input/<capa>/<numero>/, y
    lo sube ya a SQL (su 'type' + definicion) para que quede conectado desde el primer guardado en
    el editor de Puntos."""
    nombre = (nombre or "").strip()
    if not re.fullmatch(r"[a-z0-9_]+", nombre):
        raise ValueError("Nombre invalido: solo minusculas, numeros y '_' (sin espacios ni acentos)")
    if DEF.existe(nombre):
        raise ValueError(f"Ya existe un ejercicio '{nombre}'")
    ej = DEF.guardar(nombre, {"name": nombre, "description": "", "source": "pose", "features": [], "kpoints": []})

    from src.nucleo import config as CONF
    for capa in (CONF.RECORDINGS_DIR, CONF.CLIPS_DIR, CONF.PLATE_DIR, CONF.GOLD_DIR):   # los datos se nombran con el numero
        (capa / str(ej)).mkdir(parents=True, exist_ok=True)

    return {"ok": True, "numero": ej, "sql": subir(nombre)}


def modificar_ejercicio(nombre, cambios):
    """Datos basicos de un ejercicio (el slug NO se renombra: ata 'type' en SQL, carpeta de clips y plantilla).
    cambios: {name, description, direction, min_duration_ms, max_duration_ms}; lo que falte se deja igual.
    Puntos/angulos se editan con guardar_ejercicio. Valida antes de escribir y respalda la definicion
    anterior. Devuelve base_invalida=True si cambio la segmentacion y ya hay base grabada."""
    data = _definicion_de(nombre)
    nom = (cambios.get("name") or "").strip()
    if "name" in cambios and not nom:
        raise ValueError("El nombre no puede quedar vacio")
    if nom:
        data["name"] = nom
    if "description" in cambios:
        data["description"] = (cambios.get("description") or "").strip()
    seg = dict(data.get("segmentation") or {})
    seg0 = dict(seg)
    for k in ("direction", "min_duration_ms", "max_duration_ms"):
        if cambios.get(k) not in (None, ""):
            seg[k] = cambios[k] if k == "direction" else int(cambios[k])
    mn, mx = seg.get("min_duration_ms"), seg.get("max_duration_ms")
    if mn is not None and mx is not None and not 0 < mn < mx:
        raise ValueError("La duracion minima debe ser mayor que 0 y menor que la maxima")
    if seg:
        data["segmentation"] = seg

    _guardar_valido(nombre, data)

    from src.evaluacion.plantilla import template_path
    from src.nucleo.config import TEMPLATES_DIR
    return {"ok": True, "base_invalida": seg != seg0 and template_path(TEMPLATES_DIR, nombre).exists()}


def eliminar_ejercicio(nombre):
    """Archiva un ejercicio: queda inactivo con su numero reservado (recuperable: crearlo de nuevo con el mismo nombre
    lo reactiva). Sus clips, grabaciones, tablas y SQL los limpia etiquetado/depurar.py (lo llama el endpoint; el 'type'
    queda reservado en sql_tipos.json)."""
    _definicion_de(nombre)
    DEF.archivar(nombre)
    return {"ok": True}


def conexiones_kpoints(kpoints):
    """Pares (i, j) de indices dentro de 'kpoints' que forman un hueso del
    esqueleto de pose -- para dibujar el overlay del video solo con los
    puntos del catalogo. Dos kpoints se unen si son de la misma fuente y su
    par de landmarks esta en POSE_ESQUELETO."""
    pos = {}
    for i, kp in enumerate(kpoints):
        o = kp.get("origen") or {}
        if o.get("tipo") == "landmark":
            pos[(o["fuente"], o["landmark"])] = i
    pares = []
    for a, b in POSE_ESQUELETO:
        if ("pose", a) in pos and ("pose", b) in pos:
            pares.append([pos[("pose", a)], pos[("pose", b)]])
    return pares


def codigo_kpoint(kp, kpoints):
    """Codigo que ve el usuario: C01..C33 = Cuerpo 33 (ID de MediaPipe + 1); D01.. = derivados."""
    o = kp.get("origen") or {}
    if o.get("tipo") != "landmark":
        derivados = [k for k in kpoints if (k.get("origen") or {}).get("tipo") != "landmark"]
        return f"D{derivados.index(kp) + 1:02d}"
    return f"C{list(POSE_PUNTOS).index(o['landmark']) + 1:02d}"


def _definicion(nombre):
    """Lo que se comparte por SQL: source, kpoints y features (signal/segmentation se quedan en la definicion local)."""
    datos = leer_ejercicio(nombre)
    return {k: datos.get(k) for k in ("source", "kpoints", "features")}


def _canon(definicion):
    return json.dumps(definicion, sort_keys=True, ensure_ascii=False, default=str)


def _espejo_sql(nombre):
    """(type, kpoints, nombres, filas de features) tal como deben quedar en las tablas de consulta de SQL."""
    from src.almacenamiento import dataset_sql as SQL
    datos = leer_ejercicio(nombre)
    kps = datos["kpoints"]
    codigo = {k["nombre"]: codigo_kpoint(k, kps) for k in kps}
    filas = []
    for i, f in enumerate(resolver_features(datos["features"], kps), 1):
        recorrido = f.get("cadena") or [*(f.get("points") or []), *(f.get("reference") or [])]
        filas.append((i, f["name"], f["type"], ">".join(codigo.get(p, p) for p in recorrido), f.get("activo", True)))
    return SQL.tipo_de_ejercicio(nombre), kps, [k["nombre"] for k in kps], filas


def _nombres_metricas(nombres, kps, nombre):
    """Columnas de 'angles' del type: los angulos y proporciones activados (o el catalogo fijo si el ejercicio no tiene)."""
    from src.procesamiento.medidas import features as FEAT
    datos = leer_ejercicio(nombre)
    feats = FEAT.medibles(nombres, resolver_features(datos["features"], kps))
    return [f["name"] for f in feats]


def sincronizar_sql(nombre):
    """Sube a SQL Server la definicion de este ejercicio (su 'type') y sus tablas de consulta (kpoints, angulos,
    filas). Lanza SQLServerNoDisponible si el servidor no responde."""
    from src.almacenamiento import dataset_sql as SQL
    tipo, kps, nombres, filas = _espejo_sql(nombre)
    SQL.asegurar_base_y_tablas()
    with SQL.conexion() as cx:
        SQL.guardar_definicion(cx, tipo, nombre, _definicion(nombre))
        SQL.guardar_catalogo(cx, tipo, nombres, _nombres_metricas(nombres, kps, nombre))
        SQL.guardar_features(cx, tipo, filas)
        cx.commit()
    return tipo


# --- SQL manda; sin conexion se guarda en local y se sube cuando vuelva --------------------------------------
# datos/pendientes_kpoints.json = {ejercicio: fecha}: guardado en local y aun no subido. Mientras este ahi, lo LOCAL
# es lo mas nuevo (se sube en cuanto SQL responda); si no esta, lo que diga SQL pisa a la definicion local.
PENDIENTES_PATH = KPOINTS_PENDIENTES_PATH
ESPERA_SQL_CAIDO_S = 30.0
_sql_caido_hasta = 0.0


def _pendientes():
    try:
        return json.loads(PENDIENTES_PATH.read_text("utf-8"))
    except (OSError, ValueError):
        return {}


def _marcar_pendiente(nombre, pendiente):
    p = _pendientes()
    if pendiente:
        p[nombre] = datetime.now().isoformat(timespec="seconds")
    else:
        p.pop(nombre, None)
    PENDIENTES_PATH.write_text(json.dumps(p, indent=1), "utf-8")


def subir(nombre):
    """Tras guardar la definicion: lo sube a SQL. Sin conexion queda pendiente (y se sube solo despues)."""
    global _sql_caido_hasta
    try:
        tipo = sincronizar_sql(nombre)
    except Exception as e:   # SQLServerNoDisponible, pyodbc.Error...
        _sql_caido_hasta = time.monotonic() + ESPERA_SQL_CAIDO_S
        _marcar_pendiente(nombre, True)
        return {"ok": False, "pendiente": True, "error": str(e)[:300]}
    _marcar_pendiente(nombre, False)
    return {"ok": True, "type": tipo, "pendiente": False}


def sincronizar(nombre):
    """Deja la definicion local y SQL iguales, con SQL mandando:
    - con pendiente local (se guardo sin conexion): se sube lo local;
    - SQL no tiene el ejercicio: se sube la definicion local;
    - SQL tiene otra cosa: se aplica a la local (queda copia en sistema/respaldos);
    - sin conexion: no se toca nada."""
    global _sql_caido_hasta
    from src.almacenamiento import dataset_sql as SQL
    pendiente = nombre in _pendientes()
    if time.monotonic() < _sql_caido_hasta:
        return {"estado": "sin_conexion", "pendiente": pendiente, "detalle": "SQL no responde (se reintenta solo)"}
    try:
        tipo = SQL.tipo_de_ejercicio(nombre)
        SQL.asegurar_base_y_tablas()
        if pendiente:
            sincronizar_sql(nombre)
            _marcar_pendiente(nombre, False)
            return {"estado": "enviado", "pendiente": False, "detalle": "Lo guardado sin conexion ya se subio a SQL"}
        remoto = SQL.leer_definicion(tipo)
        if remoto is None:
            sincronizar_sql(nombre)
            return {"estado": "enviado", "pendiente": False, "detalle": "SQL no tenia este ejercicio: se subio la definicion local"}
    except Exception as e:   # sin pyodbc, sin servidor, sin permisos...
        _sql_caido_hasta = time.monotonic() + ESPERA_SQL_CAIDO_S
        return {"estado": "sin_conexion", "pendiente": pendiente, "detalle": str(e)[:200]}
    if _canon(remoto) == _canon(_definicion(nombre)):
        return {"estado": "sincronizado", "pendiente": False}
    try:
        guardar_ejercicio(nombre, remoto)      # SQL manda
    except ValueError as e:                    # p.ej. a lo de SQL le falta una feature que la definicion usa como señal
        return {"estado": "conflicto", "pendiente": False, "detalle": str(e)[:300]}
    return {"estado": "traido", "pendiente": False, "detalle": "SQL tenia otra version: se aplico a la definicion local"}


def reintentar(todos=False):
    """Para el hilo de fondo del panel: sube los pendientes (todos=True: ademas trae de SQL lo que difiera)."""
    for nombre in (listar_ejercicios() if todos else list(_pendientes())):
        try:
            sincronizar(nombre)
        except Exception:
            pass   # un ejercicio con problemas no frena a los demas; se vuelve a intentar en la proxima vuelta
