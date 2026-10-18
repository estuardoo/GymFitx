"""Descomposicion: cada clip contra el clip 'base' de su ejercicio, punto por
punto (indicador tipo R2 con DTW, calculado en src/almacenamiento/dataset_sql.py)."""
from src.almacenamiento import dataset_sql as SQL
from src.etiquetado.manifest import OUT, _manifest, _tipo_o_primero
from src.etiquetado.tablas import catalogo_puntos_disponible
from src.evaluacion.similitud import indicador


def _rows_de_tipo(tipo):
    return [r for r in _manifest() if r["type"] == _tipo_o_primero(tipo)]


def descomp_opciones(tipo):
    """Para el panel: que clips hay por clase (base/bien/mal) y los kpoints de
    este ejercicio -- en el mismo orden que su numero (point) real en
    table_kpoints, para que 'K1, K2...' en la interfaz sea el mismo punto que
    calcula el indicador. Si SQL no responde, cae al catalogo derivado del
    .npz+yaml (mismo orden en la practica, pero no es la fuente de verdad)."""
    rows_tipo = _rows_de_tipo(tipo)
    clips = {"base": [], "bien": [], "mal": []}
    for row in rows_tipo:
        if row["clase"] in clips:
            clips[row["clase"]].append(row["clip"])
    try:
        kpoints = [nombre for _punto, nombre in SQL.kpoints_de(tipo)]
    except SQL.SQLServerNoDisponible:
        kpoints = catalogo_puntos_disponible(rows_tipo, OUT)
    return {"clips": clips, "kpoints": kpoints}


def descomp_analizar(tipo, base, bien, mal, activos=None):
    """Series x(frame)/y(frame) por kpoint (solo los 'activos', para las
    graficas) + el indicador de cada kpoint contra el 'base' (todos, para la
    tabla-matriz) -- ver indicador() para la formula."""
    if not base:
        raise ValueError("Elige un clip 'base' para comparar")
    try:
        frames_base = SQL.frames_de(tipo, base)
        frames_bien = SQL.frames_de(tipo, bien) if bien else {}
        frames_mal = SQL.frames_de(tipo, mal) if mal else {}
    except SQL.SQLServerNoDisponible as e:
        raise ValueError(str(e)) from None
    if not frames_base:
        raise ValueError(f"'{base}' no tiene table_frames_fix todavia -- genera/actualiza las tablas SQL")

    kpoints = list(frames_base.keys())
    activos = [k for k in (activos or kpoints) if k in kpoints]

    def serie(frames, kps):
        return {k: {"x": frames[k]["x"], "y": frames[k]["y"]} for k in kps if k in frames}

    indicadores = {"bien": {}, "mal": {}}
    for kp in kpoints:
        if frames_bien:
            indicadores["bien"][kp] = indicador(frames_base[kp], frames_bien[kp])
        if frames_mal:
            indicadores["mal"][kp] = indicador(frames_base[kp], frames_mal[kp])

    def promedio(ind):
        vals = [v for v in ind.values() if v is not None]
        return round(sum(vals) / len(vals), 2) if vals else None

    return {
        "kpoints": kpoints,
        "series": {"base": serie(frames_base, activos), "bien": serie(frames_bien, activos), "mal": serie(frames_mal, activos)},
        "indicadores": indicadores,
        "resumen": {"bien": promedio(indicadores["bien"]), "mal": promedio(indicadores["mal"])},
    }


def descomp_ranking(tipo):
    """Ranking de TODOS los clips de este ejercicio contra su 'base', ya
    autocalculado en table_indicator al generar/actualizar tablas SQL --
    de mayor a menor KG (promedio de indicador entre kpoints). Ver
    SQL.ranking_indicadores()."""
    try:
        return {"ranking": SQL.ranking_indicadores(tipo)}
    except SQL.SQLServerNoDisponible as e:
        raise ValueError(str(e)) from None
