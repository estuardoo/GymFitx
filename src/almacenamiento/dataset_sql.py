"""Dataset de keypoints en SQL Server: SOLO guardar y leer (sin logica de negocio).

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
  table_angles      catalogo de la columna 'angles' por type -> idx, descripcion"""

from __future__ import annotations

import json

import numpy as np

from src.almacenamiento import sqlserver as _SQL
from src.almacenamiento.sqlserver import (  # noqa: F401
    SQLSERVER_DB,
    SQLSERVER_HOST,
    SQLServerNoDisponible,
    ejecutar_ddl,
)
from src.almacenamiento.sqlserver import conectar as _conectar
from src.nucleo.config import SQL_CONFIG_PATH, SQL_TIPOS_PATH

CONFIG_PATH = SQL_CONFIG_PATH


TIPOS_PATH = SQL_TIPOS_PATH


def tipo_de_ejercicio(exercise: str) -> int:
    """'type' en las 4 tablas = un ejercicio (el mismo nombre que su
    ejercicios/<exercise>.yaml, guardado en el .json de cada video
    grabado). Se le asigna un numero la primera vez que aparece y se guarda
    en sql_tipos.json, asi el mismo ejercicio siempre cae en el mismo type
    sin tener que numerarlos a mano."""
    tipos = json.loads(TIPOS_PATH.read_text("utf-8")) if TIPOS_PATH.exists() else {}
    if exercise not in tipos:
        tipos[exercise] = max(tipos.values(), default=0) + 1
        TIPOS_PATH.write_text(json.dumps(tipos, indent=1, ensure_ascii=False), "utf-8")
    return tipos[exercise]


def tipos_conocidos() -> dict[int, str]:
    """{type: ejercicio} de todos los ejercicios ya vistos, para el selector
    'elegir el tipo' del panel de entrenamiento."""
    tipos = json.loads(TIPOS_PATH.read_text("utf-8")) if TIPOS_PATH.exists() else {}
    return {v: k for k, v in tipos.items()}


TABLAS = ("table_file", "table_kpoints", "table_frames", "table_frames_fix", "table_frame_base", "table_config",
          "table_indicator", "table_angles", "table_features", "table_ejercicio")


DATOS_A_BLANQUEAR = ("table_indicator", "table_frame_base", "table_frames_fix", "table_frames", "table_file")   # orden por llaves foraneas


def blanquear_datos():
    """Vacia los datos de todos los clips en SQL (frames crudos y normalizados, base, indicadores y archivos).
    Se conservan las definiciones (table_ejercicio, table_features, table_config): los catalogos se reescriben al regenerar."""
    borradas = {}
    with _conectar() as cx:
        for t in DATOS_A_BLANQUEAR:
            borradas[t] = cx.execute(f"DELETE FROM {t}").rowcount
        cx.commit()
    return borradas


DDL = """
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'table_file')
CREATE TABLE table_file (
    id        INT IDENTITY(1,1) PRIMARY KEY,
    type      INT           NOT NULL,
    archivo   NVARCHAR(400) NOT NULL,
    frames    INT           NOT NULL,
    guia_fix  NVARCHAR(150) NULL,        -- que parametros de normalizacion se usaron para su table_frames_fix
    creado_en DATETIME2     NOT NULL DEFAULT SYSDATETIME(),
    CONSTRAINT UQ_table_file_type_archivo UNIQUE (type, archivo)
);
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'table_kpoints')
CREATE TABLE table_kpoints (
    type        INT           NOT NULL,
    point       INT           NOT NULL,
    descripcion NVARCHAR(100) NOT NULL,
    CONSTRAINT PK_table_kpoints PRIMARY KEY (type, point)
);
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'table_frames')
CREATE TABLE table_frames (
    type    INT           NOT NULL,
    file_id INT           NOT NULL,
    frame   INT           NOT NULL,
    VectorX   NVARCHAR(MAX) NULL,   -- "x1|x2|...|xN" de todos los puntos, orden de table_kpoints
    VectorY   NVARCHAR(MAX) NULL,
    VectorZ   NVARCHAR(MAX) NULL,
    angles  NVARCHAR(MAX) NULL,
    CONSTRAINT PK_table_frames PRIMARY KEY (type, file_id, frame),
    CONSTRAINT FK_table_frames_file FOREIGN KEY (file_id) REFERENCES table_file(id)
);
-- 'mano' ya no aplica (ejercicios de pose, no solo de mano) y nadie la leia --
-- solo se escribia. Se borra si una tabla vieja todavia la tiene.
IF COL_LENGTH('table_frames', 'mano') IS NOT NULL ALTER TABLE table_frames DROP COLUMN mano;
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'table_frames_fix')
CREATE TABLE table_frames_fix (
    type    INT           NOT NULL,
    file_id INT           NOT NULL,
    frame   INT           NOT NULL,
    VectorX   NVARCHAR(MAX) NOT NULL,
    VectorY   NVARCHAR(MAX) NOT NULL,
    VectorZ   NVARCHAR(MAX) NOT NULL,
    angles  NVARCHAR(MAX) NULL,
    CONSTRAINT PK_table_frames_fix PRIMARY KEY (type, file_id, frame),
    CONSTRAINT FK_table_frames_fix_file FOREIGN KEY (file_id) REFERENCES table_file(id)
);
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'table_frame_base')
CREATE TABLE table_frame_base (
    type    INT           NOT NULL,
    file_id INT           NOT NULL,
    frame   INT           NOT NULL,
    VectorX   NVARCHAR(MAX) NOT NULL,
    VectorY   NVARCHAR(MAX) NOT NULL,
    VectorZ   NVARCHAR(MAX) NOT NULL,
    angles  NVARCHAR(MAX) NULL,
    CONSTRAINT PK_table_frame_base PRIMARY KEY (type, file_id, frame),
    CONSTRAINT FK_table_frame_base_file FOREIGN KEY (file_id) REFERENCES table_file(id)
);
-- migracion: nombres de columna viejos -> VectorX/VectorY/VectorZ.
-- Un IF por statement (no BEGIN/END) porque asegurar_base_y_tablas() parte
-- este DDL por comilla-punto-y-coma-mas-salto-de-linea -- un bloque con varios statements adentro quedaria cortado.
-- Caso 1: la tabla tenia 'eje_x/eje_y/eje_z' (nombre usado brevemente antes
-- de este): se renombra con sp_rename, sin perder los datos ya cargados.
IF COL_LENGTH('table_frames', 'eje_x') IS NOT NULL AND COL_LENGTH('table_frames', 'VectorX') IS NULL EXEC sp_rename 'table_frames.eje_x', 'VectorX', 'COLUMN';
IF COL_LENGTH('table_frames', 'eje_y') IS NOT NULL AND COL_LENGTH('table_frames', 'VectorY') IS NULL EXEC sp_rename 'table_frames.eje_y', 'VectorY', 'COLUMN';
IF COL_LENGTH('table_frames', 'eje_z') IS NOT NULL AND COL_LENGTH('table_frames', 'VectorZ') IS NULL EXEC sp_rename 'table_frames.eje_z', 'VectorZ', 'COLUMN';
IF COL_LENGTH('table_frames_fix', 'eje_x') IS NOT NULL AND COL_LENGTH('table_frames_fix', 'VectorX') IS NULL EXEC sp_rename 'table_frames_fix.eje_x', 'VectorX', 'COLUMN';
IF COL_LENGTH('table_frames_fix', 'eje_y') IS NOT NULL AND COL_LENGTH('table_frames_fix', 'VectorY') IS NULL EXEC sp_rename 'table_frames_fix.eje_y', 'VectorY', 'COLUMN';
IF COL_LENGTH('table_frames_fix', 'eje_z') IS NOT NULL AND COL_LENGTH('table_frames_fix', 'VectorZ') IS NULL EXEC sp_rename 'table_frames_fix.eje_z', 'VectorZ', 'COLUMN';
-- Caso 2: la tabla tenia la 'vectors' original (empacada x,y,z por punto,
-- mas vieja aun) -- esa si se pierde (nunca tuvo separado por eje), se
-- agregan las 3 columnas nuevas vacias y se descarta 'vectors'.
IF COL_LENGTH('table_frames', 'vectors') IS NOT NULL AND COL_LENGTH('table_frames', 'VectorX') IS NULL ALTER TABLE table_frames ADD VectorX NVARCHAR(MAX) NULL;
IF COL_LENGTH('table_frames', 'vectors') IS NOT NULL AND COL_LENGTH('table_frames', 'VectorY') IS NULL ALTER TABLE table_frames ADD VectorY NVARCHAR(MAX) NULL;
IF COL_LENGTH('table_frames', 'vectors') IS NOT NULL AND COL_LENGTH('table_frames', 'VectorZ') IS NULL ALTER TABLE table_frames ADD VectorZ NVARCHAR(MAX) NULL;
IF COL_LENGTH('table_frames', 'vectors') IS NOT NULL ALTER TABLE table_frames DROP COLUMN vectors;
IF COL_LENGTH('table_frames_fix', 'vectors') IS NOT NULL AND COL_LENGTH('table_frames_fix', 'VectorX') IS NULL ALTER TABLE table_frames_fix ADD VectorX NVARCHAR(MAX) NULL;
IF COL_LENGTH('table_frames_fix', 'vectors') IS NOT NULL AND COL_LENGTH('table_frames_fix', 'VectorY') IS NULL ALTER TABLE table_frames_fix ADD VectorY NVARCHAR(MAX) NULL;
IF COL_LENGTH('table_frames_fix', 'vectors') IS NOT NULL AND COL_LENGTH('table_frames_fix', 'VectorZ') IS NULL ALTER TABLE table_frames_fix ADD VectorZ NVARCHAR(MAX) NULL;
IF COL_LENGTH('table_frames_fix', 'vectors') IS NOT NULL ALTER TABLE table_frames_fix DROP COLUMN vectors;
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'table_config')
CREATE TABLE table_config (
    type           INT           NOT NULL PRIMARY KEY,
    parametros     NVARCHAR(500) NOT NULL,   -- json de modo/ancho/alto/n_frames_fijo/puntos activos
    guia_fix       NVARCHAR(150) NOT NULL,   -- mismo descriptor que table_file.guia_fix, para verla sin parsear el json
    actualizado_en DATETIME2     NOT NULL DEFAULT SYSDATETIME()
);
-- 'clase' (bien/mal/base/descarte) de cada clip, para que table_indicator sepa
-- cual es el clip 'base' de cada type sin tener que releer el manifest.
IF COL_LENGTH('table_file', 'clase') IS NULL ALTER TABLE table_file ADD clase NVARCHAR(20) NULL;
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'table_indicator')
CREATE TABLE table_indicator (
    type           INT           NOT NULL,
    file_id        INT           NOT NULL,
    point          INT           NOT NULL,
    base_file_id   INT           NOT NULL,
    indicador      FLOAT         NULL,
    guia           NVARCHAR(200) NOT NULL,   -- archivo_base|guia_fix_base: si no cambio, no se recalcula
    actualizado_en DATETIME2     NOT NULL DEFAULT SYSDATETIME(),
    CONSTRAINT PK_table_indicator PRIMARY KEY (type, file_id, point),
    CONSTRAINT FK_table_indicator_file FOREIGN KEY (file_id) REFERENCES table_file(id),
    CONSTRAINT FK_table_indicator_base FOREIGN KEY (base_file_id) REFERENCES table_file(id)
);
-- catalogo de la columna 'angles' (table_frames/_fix/_base): que angulo va en
-- cada posicion de "a1|a2|...|aN" (ver src/procesamiento/medidas/angulos.py). Grados.
-- definicion completa del ejercicio (source, kpoints, features) tal como la edita la pestana Kpoints:
-- es lo que manda; el .yaml local se rehace desde aqui cuando SQL difiere.
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'table_ejercicio')
CREATE TABLE table_ejercicio (
    type        INT            NOT NULL PRIMARY KEY,
    ejercicio   NVARCHAR(200)  NOT NULL,
    definicion  NVARCHAR(MAX)  NOT NULL,
    actualizado DATETIME2      NOT NULL
);
-- filas de la pestana Kpoints (angulos y proporciones) por type: recorrido "K01>K02>K03" con los
-- numeros de table_kpoints (point + 1); activo = si se usa en entrenamiento/vivo.
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'table_features')
CREATE TABLE table_features (
    type        INT           NOT NULL,
    id          INT           NOT NULL,
    nombre      NVARCHAR(100) NOT NULL,
    tipo        NVARCHAR(20)  NOT NULL,
    recorrido   NVARCHAR(400) NOT NULL,
    activo      BIT           NOT NULL,
    CONSTRAINT PK_table_features PRIMARY KEY (type, id)
);
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'table_angles')
CREATE TABLE table_angles (
    type        INT           NOT NULL,
    idx         INT           NOT NULL,
    descripcion NVARCHAR(100) NOT NULL,
    CONSTRAINT PK_table_angles PRIMARY KEY (type, idx)
);
-- si el clip se usa o no para entrenar (se marca con clic en el panel de
-- Entrenamiento; la fuente de verdad es seleccion_entrenamiento.json, esto es espejo).
IF COL_LENGTH('table_file', 'usar') IS NULL ALTER TABLE table_file ADD usar BIT NOT NULL CONSTRAINT DF_table_file_usar DEFAULT 1;
-- guias mas largas (la firma de puntos/angulos + la lista de puntos de la caja no cabian en 150/200)
IF COL_LENGTH('table_file', 'guia_fix') < 800 ALTER TABLE table_file ALTER COLUMN guia_fix NVARCHAR(400) NULL;
IF COL_LENGTH('table_config', 'guia_fix') < 800 ALTER TABLE table_config ALTER COLUMN guia_fix NVARCHAR(400) NOT NULL;
IF COL_LENGTH('table_indicator', 'guia') < 1600 ALTER TABLE table_indicator ALTER COLUMN guia NVARCHAR(800) NOT NULL;
"""


def asegurar_base_y_tablas():
    """Idempotente: crea la base GymFitX (si hace falta) y las tablas del dataset."""
    ejecutar_ddl(DDL)


def estado():
    """Diagnostico para el panel: nunca revienta aunque el servidor no responda."""
    return _SQL.estado(TABLAS)


# --- configuracion de normalizacion (una entrada por type, en sql_config.json) ---

def config():
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text("utf-8"))
    return {}


def guardar_config(cfg):
    CONFIG_PATH.write_text(json.dumps(cfg, indent=1, ensure_ascii=False), "utf-8")


def _ejes_str(frame_points):
    """(N,3) -> (VectorX, VectorY, VectorZ), cada uno 'v1|v2|...|vN' en el orden
    de table_kpoints (un valor por punto, no un triple)."""
    return tuple("|".join(f"{v:.2f}" for v in frame_points[:, eje]) for eje in range(3))


def _angulos_str(fila):
    """(A,) -> 'a1|a2|...|aA' en el orden de table_angles; None si no hay angulos."""
    return "|".join(f"{v:.4f}" for v in fila) if len(fila) else None


def _ejes_de(ex, ey, ez):
    """Inverso de _ejes_str: 3 strings 'v1|...|vN' -> (N,3)."""
    return np.array([[float(v) for v in ex.split("|")],
                      [float(v) for v in ey.split("|")],
                      [float(v) for v in ez.split("|")]], dtype=np.float32).T


def conexion():
    """Conexion a la base del dataset (usar con 'with')."""
    return _conectar()


# --- escritura: reciben una conexion abierta; quien orquesta decide cuando hacer commit ---

def guardar_catalogo(cx, type_, nombres, nombres_ang):
    """Reemplaza table_kpoints y table_angles de este type."""
    cx.execute("DELETE FROM table_kpoints WHERE type=?", (type_,))
    for i, nombre in enumerate(nombres):
        cx.execute("INSERT INTO table_kpoints (type, point, descripcion) VALUES (?,?,?)", (type_, i, nombre))
    cx.execute("DELETE FROM table_angles WHERE type=?", (type_,))
    for i, nombre in enumerate(nombres_ang):
        cx.execute("INSERT INTO table_angles (type, idx, descripcion) VALUES (?,?,?)", (type_, i, nombre))


def guardar_definicion(cx, type_, ejercicio, definicion):
    """Reemplaza la definicion completa del ejercicio (dict con source, kpoints, features)."""
    cx.execute("DELETE FROM table_ejercicio WHERE type=?", (type_,))
    cx.execute("INSERT INTO table_ejercicio (type, ejercicio, definicion, actualizado) VALUES (?,?,?,SYSDATETIME())",
               (type_, ejercicio, json.dumps(definicion, ensure_ascii=False, sort_keys=True)))


def leer_definicion(type_):
    """La definicion guardada para este type, o None si SQL todavia no la tiene."""
    with _conectar() as cx:
        fila = cx.execute("SELECT definicion FROM table_ejercicio WHERE type=?", (type_,)).fetchone()
    return json.loads(fila[0]) if fila else None


def guardar_features(cx, type_, filas):
    """Reemplaza table_features de este type. filas: [(id, nombre, tipo, recorrido, activo)]."""
    cx.execute("DELETE FROM table_features WHERE type=?", (type_,))
    for id_, nombre, tipo, recorrido, activo in filas:
        cx.execute("INSERT INTO table_features (type, id, nombre, tipo, recorrido, activo) VALUES (?,?,?,?,?,?)",
                   (type_, id_, nombre, tipo, recorrido, 1 if activo else 0))


def guardar_config_activa(cx, type_, cfg, guia):
    """table_config: la ultima normalizacion usada para este type, visible desde SQL."""
    parametros = json.dumps(cfg, ensure_ascii=False)
    cx.execute(
        "MERGE table_config AS t USING (SELECT ? AS type) AS s ON t.type = s.type "
        "WHEN MATCHED THEN UPDATE SET parametros=?, guia_fix=?, actualizado_en=SYSDATETIME() "
        "WHEN NOT MATCHED THEN INSERT (type, parametros, guia_fix) VALUES (?,?,?);",
        (type_, parametros, guia, type_, parametros, guia),
    )


def archivo_registrado(cx, type_, archivo):
    """(id, guia_fix) del clip, o None si todavia no esta en table_file."""
    return cx.execute("SELECT id, guia_fix FROM table_file WHERE type=? AND archivo=?",
                      (type_, archivo)).fetchone()


def crear_archivo(cx, type_, archivo, frames, guia, clase):
    cx.execute("INSERT INTO table_file (type, archivo, frames, guia_fix, clase) VALUES (?,?,?,?,?)",
               (type_, archivo, frames, guia, clase))
    return cx.execute("SELECT id FROM table_file WHERE type=? AND archivo=?", (type_, archivo)).fetchone()[0]


def actualizar_archivo(cx, file_id, frames, guia, clase):
    cx.execute("UPDATE table_file SET frames=?, guia_fix=?, clase=? WHERE id=?", (frames, guia, clase, file_id))


def frames_crudos_guardados(cx, type_, file_id):
    """Filas utiles de table_frames. 'IS NOT NULL': una migracion vieja pudo dejar
    filas con VectorX vacio, que existen pero no sirven."""
    return cx.execute(
        "SELECT COUNT(*) FROM table_frames WHERE type=? AND file_id=? AND VectorX IS NOT NULL",
        (type_, file_id),
    ).fetchone()[0]


def borrar_frames(cx, type_, file_id):
    cx.execute("DELETE FROM table_frames WHERE type=? AND file_id=?", (type_, file_id))
    cx.execute("DELETE FROM table_frames_fix WHERE type=? AND file_id=?", (type_, file_id))


def insertar_frames(cx, tabla, type_, file_id, points, angulos):
    """Una fila por cuadro en table_frames (crudo) o table_frames_fix (normalizado)."""
    if tabla not in ("table_frames", "table_frames_fix"):
        raise ValueError(tabla)
    for i, (pts, ang) in enumerate(zip(points, angulos), 1):
        ex, ey, ez = _ejes_str(pts)
        cx.execute(
            f"INSERT INTO {tabla} (type, file_id, frame, VectorX, VectorY, VectorZ, angles) VALUES (?,?,?,?,?,?,?)",
            (type_, file_id, i, ex, ey, ez, _angulos_str(ang)),
        )


def base_del_tipo(cx, type_):
    """(id, archivo, guia_fix) del clip clase='base' de este type, o None."""
    return cx.execute(
        "SELECT id, archivo, guia_fix FROM table_file WHERE type=? AND clase='base'", (type_,)
    ).fetchone()


def copiar_a_frame_base(cx, type_, base_file_id):
    """table_frame_base = espejo de table_frames_fix del clip 'base' (se refresca siempre: son
    ~n_frames_fijo filas)."""
    cx.execute("DELETE FROM table_frame_base WHERE type=?", (type_,))
    cx.execute(
        "INSERT INTO table_frame_base (type, file_id, frame, VectorX, VectorY, VectorZ, angles) "
        "SELECT type, file_id, frame, VectorX, VectorY, VectorZ, angles FROM table_frames_fix "
        "WHERE type=? AND file_id=?",
        (type_, base_file_id),
    )
    cx.commit()


def nombres_kpoints(cx, type_):
    return [r[0] for r in cx.execute(
        "SELECT descripcion FROM table_kpoints WHERE type=? ORDER BY point", (type_,)
    ).fetchall()]


def otros_archivos(cx, type_, base_file_id):
    return cx.execute("SELECT id, archivo FROM table_file WHERE type=? AND id<>?",
                      (type_, base_file_id)).fetchall()


def indicadores_con_guia(cx, type_, file_id, guia):
    return cx.execute(
        "SELECT COUNT(*) FROM table_indicator WHERE type=? AND file_id=? AND guia=?",
        (type_, file_id, guia),
    ).fetchone()[0]


def reemplazar_indicadores(cx, type_, file_id, base_file_id, guia, valores):
    """valores: [(point, indicador), ...] de un clip contra el base."""
    cx.execute("DELETE FROM table_indicator WHERE type=? AND file_id=?", (type_, file_id))
    for point, val in valores:
        cx.execute(
            "INSERT INTO table_indicator (type, file_id, point, base_file_id, indicador, guia) "
            "VALUES (?,?,?,?,?,?)",
            (type_, file_id, point, base_file_id, val, guia),
        )


def features_por_archivo(type_, usar="ambos", tipos=None):
    """{archivo: vector 1D} de todos los clips de este 'type' que ya tengan
    table_frames_fix -- una sola consulta para todos, no una por clip.
    usar: letras x, y, z (ejes de cada kpoint), a (angulos) y p (proporciones), o los
    nombres de siempre: 'puntos', 'angulos', 'ambos'. NaN -> 0 para que sklearn no reviente."""
    with _conectar() as cx:
        filas = cx.execute(
            "SELECT f.archivo, ff.frame, ff.VectorX, ff.VectorY, ff.VectorZ, ff.angles FROM table_frames_fix ff "
            "JOIN table_file f ON f.id = ff.file_id AND f.type = ff.type "
            "WHERE ff.type = ? ORDER BY ff.file_id, ff.frame",
            (type_,),
        ).fetchall()
    from src.nucleo.componentes import componentes, mascara_metricas
    ejes, con_ang, con_pro = componentes(usar)
    con_metricas = con_ang or con_pro
    por_archivo = {}
    for archivo, _frame, ex, ey, ez, ang in filas:
        partes = []
        if ejes:
            partes.append(_ejes_de(ex, ey, ez)[:, ejes].flatten())
        if con_metricas:
            met = np.array([float(v) for v in ang.split("|")], dtype=np.float32) if ang else np.zeros(0, dtype=np.float32)
            partes.append(met[np.array(mascara_metricas(tipos, usar, len(met)), dtype=bool)] if len(met) else met)
        por_archivo.setdefault(archivo, []).append(np.concatenate(partes))
    salida = {}
    for archivo, frames in por_archivo.items():
        vec = np.concatenate(frames)
        if vec.size:
            salida[archivo] = np.nan_to_num(vec, nan=0.0)
    return salida


def frames_fix_por_archivo(type_):
    """{archivo: (points (T,N,3) float32, metrics (T,A) float32)} de table_frames_fix, SIN aplanar ni filtrar --
    para exportar el dataset completo (ver entrenamiento/exportar_slurm.py). T = el n_frames_fijo de este type."""
    with _conectar() as cx:
        filas = cx.execute(
            "SELECT f.archivo, ff.frame, ff.VectorX, ff.VectorY, ff.VectorZ, ff.angles FROM table_frames_fix ff "
            "JOIN table_file f ON f.id = ff.file_id AND f.type = ff.type "
            "WHERE ff.type = ? ORDER BY ff.file_id, ff.frame",
            (type_,),
        ).fetchall()
    por_archivo = {}
    for archivo, _frame, ex, ey, ez, ang in filas:
        met = np.array([float(v) for v in ang.split("|")], dtype=np.float32) if ang else np.zeros(0, dtype=np.float32)
        d = por_archivo.setdefault(archivo, {"p": [], "m": []})
        d["p"].append(_ejes_de(ex, ey, ez))
        d["m"].append(met)
    return {a: (np.stack(d["p"]), np.stack(d["m"])) for a, d in por_archivo.items()}


def marcar_uso(type_, seleccion):
    """Espejo en table_file.usar de seleccion_entrenamiento.json ({archivo: bool})."""
    with _conectar() as cx:
        for archivo, usar in seleccion.items():
            cx.execute("UPDATE table_file SET usar=? WHERE type=? AND archivo=?", (1 if usar else 0, type_, archivo))
        cx.commit()


def kpoints_de(type_):
    """[(point, descripcion), ...] de table_kpoints para este type, en orden --
    la fuente de verdad de que numero (point) le toca a cada nombre, el mismo
    orden en que estan empacados VectorX/Y/Z (ver poblar_desde_manifest)."""
    with _conectar() as cx:
        return cx.execute(
            "SELECT point, descripcion FROM table_kpoints WHERE type=? ORDER BY point", (type_,)
        ).fetchall()


def _frames_de_con(cx, type_, archivo, nombres=None):
    """Igual que frames_de(), pero reusando una conexion ya abierta -- para no
    abrir una conexion nueva por clip dentro de etiquetado/tablas.py."""
    if nombres is None:
        nombres = [r[0] for r in cx.execute(
            "SELECT descripcion FROM table_kpoints WHERE type=? ORDER BY point", (type_,)
        ).fetchall()]
    filas = cx.execute(
        "SELECT ff.VectorX, ff.VectorY, ff.VectorZ FROM table_frames_fix ff "
        "JOIN table_file f ON f.id = ff.file_id AND f.type = ff.type "
        "WHERE ff.type = ? AND f.archivo = ? ORDER BY ff.frame",
        (type_, archivo),
    ).fetchall()
    out = {n: {"x": [], "y": [], "z": []} for n in nombres}
    for ex, ey, ez in filas:
        xs, ys, zs = ex.split("|"), ey.split("|"), ez.split("|")
        if len(xs) < len(nombres) or len(ys) < len(nombres) or len(zs) < len(nombres):
            continue  # fila con menos puntos que el catalogo actual (dato viejo desincronizado): se ignora, no revienta
        for i, n in enumerate(nombres):
            out[n]["x"].append(float(xs[i]))
            out[n]["y"].append(float(ys[i]))
            out[n]["z"].append(float(zs[i]))
    return out


def frames_de(type_, archivo):
    """{kpoint: {'x':[...], 'y':[...], 'z':[...]}} de un clip ya en
    table_frames_fix, un valor por frame (mismo orden 1..n_frames_fijo para
    cualquier clip del mismo 'type', por eso son comparables frame a frame
    sin alinear nada mas)."""
    with _conectar() as cx:
        return _frames_de_con(cx, type_, archivo)


def ranking_indicadores(type_):
    """[{'archivo':..., 'clase':..., 'kg':..., 'n':...}, ...] -- un renglon por
    clip (todos menos el 'base'), el promedio de table_indicator.indicador
    entre sus kpoints (KG), de mayor a menor parecido. 'n' es cuantos kpoints
    tienen valor calculado -- si sale menor que el total de kpoints, a ese
    clip le falto algo por calcular (util para diagnosticar sin ver la SQL
    directamente). Vacio si nunca se corrio poblar_desde_manifest con un
    'base' definido para este type."""
    with _conectar() as cx:
        filas = cx.execute(
            "SELECT f.archivo, f.clase, AVG(ti.indicador), COUNT(ti.indicador) "
            "FROM table_indicator ti JOIN table_file f ON f.id = ti.file_id AND f.type = ti.type "
            "WHERE ti.type = ? GROUP BY f.archivo, f.clase ORDER BY AVG(ti.indicador) DESC",
            (type_,),
        ).fetchall()
    return [
        {"archivo": a, "clase": c, "kg": round(kg, 2) if kg is not None else None, "n": n}
        for a, c, kg, n in filas
    ]
