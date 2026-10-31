"""Verifica la integracion GYMFITX + dataset y el rendimiento de captura:

- src/procesamiento/puntos/vectorizar.py da EXACTAMENTE el mismo vector en vivo que el que
  entrenar() lee de SQL (mismo camino que poblar_desde_manifest + features_por_archivo).
- El clasificador entrenado puntua una repeticion en vivo (src/evaluacion/comparadores/).
- El DTW del indicador (dataset) ahora usa src.evaluacion.comparadores.dtw.dtw_band y da lo mismo
  que la copia vieja en Python puro.
- src.procesamiento.puntos.kpoints.resolver: catalogo -> puntos por cuadro (derivados, lado, NaN).
- Pipeline en vivo: captura desacoplada -> el video lleva todos los cuadros
  de la camara aunque la deteccion sea lenta; la camara tolera fallos sueltos.
"""

from __future__ import annotations

import json
import tempfile
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent

from test_swap_sink import _instalar_stub_mediapipe  # noqa: E402

_instalar_stub_mediapipe()

from src.evaluacion import comparadores as scorers
from src.nucleo.ejercicio import load_exercise  # noqa: E402
from src.nucleo.landmarks import POSE_LANDMARKS  # noqa: E402
from src.nucleo.tipos import Frame, Landmarks, Segment  # noqa: E402
from src.procesamiento.puntos import kpoints as KP  # noqa: E402
from src.procesamiento.puntos import normalizacion as NORM  # noqa: E402
from src.procesamiento.puntos import vectorizar  # noqa: E402

_CUERPO = load_exercise("cuerpo_completo")
KPOINTS_DER = _CUERPO.kpoints
FEATS = _CUERPO.features
NOMBRES_DER = [kp["nombre"] for kp in KPOINTS_DER]


def _clip(T=37, seed=0, cerrar=1.0):
    """(T,33,3) pose que se mueve; 'cerrar' escala cuanto se mueve."""
    rng = np.random.default_rng(seed)
    base = rng.normal(scale=0.03, size=(33, 3)).astype(np.float32)
    fase = np.sin(np.linspace(0, np.pi, T))[:, None, None] * cerrar
    return (base[None] + fase * 0.2 * np.arange(33)[None, :, None] / 33).astype(np.float32)


# --- vivo == entrenamiento ---------------------------------------------------

def _vector_camino_sql(points, nombres, kpoints, cfg_guardada, usar):
    """Replica poblar_desde_manifest (strings en SQL) + features_por_archivo."""
    from src.almacenamiento import dataset_sql as SQL
    prep = vectorizar.preparar(points, nombres, nombres, kpoints, FEATS)
    pts, nms, ang, _ = prep
    cfg = vectorizar.cfg_para(nms, cfg_guardada)
    fijo, ang_fijo = vectorizar.fijo(pts, nms, ang, cfg, FEATS)
    filas = [(SQL._ejes_str(p), SQL._angulos_str(a)) for p, a in zip(fijo, ang_fijo)]
    partes = []
    for (ex, ey, ez), angs in filas:          # lo que hace features_por_archivo
        if usar in ("puntos", "ambos"):
            partes.append(SQL._ejes_de(ex, ey, ez).flatten())
        if usar in ("angulos", "ambos"):
            partes.append(np.array([float(v) for v in angs.split("|")], dtype=np.float32))
    return np.nan_to_num(np.concatenate(partes), nan=0.0)


def test_vector_en_vivo_igual_al_que_entrena_sql():
    pts = _clip()
    pts[5] = np.nan                                     # un cuadro sin deteccion
    for usar in ("puntos", "angulos", "ambos"):
        cfg = {"n_frames_fijo": 30}
        sql = _vector_camino_sql(pts, NOMBRES_DER, KPOINTS_DER, cfg, usar)
        vivo = vectorizar.vector_de_clip(pts, NOMBRES_DER, {"point_names": NOMBRES_DER,
                                                           "kpoints": KPOINTS_DER, "cfg": cfg,
                                                           "features": usar, "features_def": FEATS})
        assert vivo.shape == sql.shape, usar
        assert np.allclose(vivo, sql, atol=0.051), (usar, np.abs(vivo - sql).max())


# --- clasificador en vivo ----------------------------------------------------

def test_clasificador_puntua_una_repeticion_en_vivo():
    import joblib
    from sklearn.linear_model import LogisticRegression
    spec = {"exercise": "cuerpo_completo", "features": "ambos", "cfg": {"n_frames_fijo": 20},
            "point_names": NOMBRES_DER, "kpoints": KPOINTS_DER, "features_def": FEATS}
    X, y = [], []
    for i in range(12):
        bien = i % 2 == 0
        X.append(vectorizar.vector_de_clip(_clip(seed=i, cerrar=1.0 if bien else 0.1), NOMBRES_DER, spec))
        y.append(1 if bien else 0)
    X = np.array(X)
    spec["n_features"] = X.shape[1]
    modelo = LogisticRegression(max_iter=2000).fit(X, y)
    with tempfile.TemporaryDirectory() as d:
        from src.nucleo import inputs as INP
        run = Path(d) / str(INP.asegurar_ejercicio("cuerpo_completo")) / "run_003"
        run.mkdir(parents=True)
        joblib.dump({"modelo": modelo, "clases": ["bien", "mal"][::-1], "nombre": "logistic", "spec": spec},
                    run / "modelo.joblib")
        (run / "meta.json").write_text(json.dumps({"exercise": "cuerpo_completo", "criterio": "f1_macro"}))
        ruta = scorers.buscar_clasificador("cuerpo_completo", Path(d))
        assert ruta == run / "modelo.joblib"
        clf = scorers.Clasificador(ruta)

    seg = Segment(start_ms=0, end_ms=1000, data=np.zeros((25, 2), np.float32),
                  valid=np.ones((25, 2), bool), kpoints=_clip(T=25, seed=99, cerrar=1.0))
    s = clf.puntuar(seg, None)
    assert 0.0 <= s.total <= 100.0 and s.clase in ("bien", "mal")
    sin_kp = Segment(start_ms=0, end_ms=1000, data=np.zeros((5, 2)), valid=np.ones((5, 2), bool))
    assert np.isnan(clf.puntuar(sin_kp, None).total)   # sin puntos: no inventa puntaje


def test_modelo_viejo_sin_spec_no_se_usa_en_vivo():
    with tempfile.TemporaryDirectory() as d:
        run = Path(d) / "run_1"
        run.mkdir()
        (run / "meta.json").write_text(json.dumps({"exercise": "cuerpo_completo"}))   # sin 'criterio'
        (run / "modelo.joblib").write_bytes(b"x")
        assert scorers.buscar_clasificador("cuerpo_completo", Path(d)) is None


# --- DTW unico ---------------------------------------------------------------

def _dtw_viejo(base_pts, otro_pts):
    """Copia de la implementacion anterior de src/almacenamiento/dataset_sql.py (Python puro)."""
    n, m = len(base_pts), len(otro_pts)
    ventana = max(2, round(max(n, m) * 0.15))
    INF = float("inf")
    dist = lambda p, q: (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2  # noqa: E731
    costo = [[INF] * m for _ in range(n)]
    costo[0][0] = dist(base_pts[0], otro_pts[0])
    for i in range(1, n):
        if abs(i) <= ventana:
            costo[i][0] = costo[i - 1][0] + dist(base_pts[i], otro_pts[0])
    for j in range(1, m):
        if abs(j) <= ventana:
            costo[0][j] = costo[0][j - 1] + dist(base_pts[0], otro_pts[j])
    for i in range(1, n):
        for j in range(1, m):
            if abs(i - j) <= ventana:
                costo[i][j] = dist(base_pts[i], otro_pts[j]) + min(costo[i - 1][j], costo[i][j - 1], costo[i - 1][j - 1])
    i, j = n - 1, m - 1
    grupos = {i: [otro_pts[j]]}
    while i > 0 or j > 0:
        if i == 0:
            j -= 1
        elif j == 0:
            i -= 1
        else:
            _, (i, j) = min([(costo[i - 1][j], (i - 1, j)), (costo[i][j - 1], (i, j - 1)),
                             (costo[i - 1][j - 1], (i - 1, j - 1))], key=lambda o: o[0])
        grupos.setdefault(i, []).append(otro_pts[j])
    return [(sum(p[0] for p in grupos[i]) / len(grupos[i]), sum(p[1] for p in grupos[i]) / len(grupos[i]))
            for i in range(n)]


def test_indicador_con_dtw_unico_da_lo_mismo_que_antes():
    from src.evaluacion import similitud as SIM
    rng = np.random.default_rng(3)
    t = np.linspace(0, 1, 30)
    base = {"x": list(np.sin(3 * t) * 40 + 50), "y": list(t * 60 + 10)}
    assert SIM.indicador(base, base) == 100.0
    diferencias = []
    for _ in range(8):
        otro = {"x": list(np.sin(3 * t + rng.normal(0, .3)) * 40 + 50 + rng.normal(0, 3, 30)),
                "y": list(t * 60 + 10 + rng.normal(0, 3, 30))}
        nuevo = SIM.indicador(base, otro)
        viejo_fn = SIM._dtw_alinear
        SIM._dtw_alinear = _dtw_viejo
        try:
            viejo = SIM.indicador(base, otro)
        finally:
            SIM._dtw_alinear = viejo_fn
        diferencias.append(abs(nuevo - viejo))
    assert max(diferencias) < 3.0, diferencias      # mismo criterio, puede variar el desempate


# --- kpoints por cuadro ------------------------------------------------------

def _pose(desplazamiento=0.0):
    P = np.arange(99, dtype=np.float32).reshape(33, 3) / 100 + desplazamiento
    return Landmarks(source="pose", world=P, screen=P, label="", score=0.9)


def test_resolver_kpoints_y_derivados():
    kps = [{"numero": 1, "nombre": "muneca", "origen": {"tipo": "landmark", "fuente": "pose", "landmark": "RIGHT_WRIST"}},
           {"numero": 2, "nombre": "codo", "origen": {"tipo": "landmark", "fuente": "pose", "landmark": "RIGHT_ELBOW"}},
           {"numero": 3, "nombre": "medio", "origen": {"tipo": "derivado", "de": [1, 2]}}]
    p = _pose()
    world, screen = KP.resolver(kps, [p])
    i = POSE_LANDMARKS.index("RIGHT_ELBOW")
    assert np.allclose(world[1], p.world[i])
    assert np.allclose(world[2], (world[0] + world[1]) / 2)
    assert screen.shape == (3, 2)
    assert KP.resolver(kps, []) is None     # sin deteccion


# --- rendimiento: captura desacoplada ---------------------------------------

class _CamaraFalsa:
    """Fuente 'en vivo' a ~fps reales (como CameraSource), sin hardware."""
    en_vivo = True
    motivo_fin = None

    def __init__(self, n=60, fps=30.0):
        self.n, self.fps = n, fps

    def frames(self):
        t0 = time.perf_counter()
        for i in range(self.n):
            espera = t0 + i / self.fps - time.perf_counter()
            if espera > 0:
                time.sleep(espera)
            yield Frame(image=np.full((72, 96, 3), i % 255, np.uint8), t_ms=int(i * 1000 / self.fps), index=i)

    def close(self):
        pass


def test_video_con_todos_los_cuadros_aunque_la_deteccion_sea_lenta():
    from src.sesion.grabacion import VideoLogger
    from src.sesion.pipeline import MultiSink, Pipeline, Sink
    ej = load_exercise("manguito_rotador")
    with tempfile.TemporaryDirectory() as d:
        vl = VideoLogger(d)
        pipe = Pipeline(ej, _CamaraFalsa(n=60, fps=30.0), MultiSink(Sink(), vl), annotate=True)
        detectar_original = pipe.tracker.detect

        def lento(frame):                     # deteccion a ~10 fps
            time.sleep(0.1)
            return detectar_original(frame)
        pipe.tracker.detect = lento
        eventos = []
        pipe.bus.subscribe(eventos.append)
        pipe.run()
        meta = json.loads(vl.json_path.read_text("utf-8"))
        assert meta["frames_camara"] == 60
        assert meta["fps_video_real"] > 25, meta          # video fluido
        assert pipe.frames_vistos < 40                     # deteccion lenta: descarto cuadros
        assert pipe.frames_descartados > 0
        parado = [e for e in eventos if e["type"] == "stopped"][0]
        assert parado["motivo"] == "la fuente termino"
        assert pipe.latest_frame is not None and pipe.latest_version >= 50   # vista previa a fps de camara


def test_camara_tolera_lecturas_fallidas_sueltas():
    from src.captura.fuentes import camara as source
    cam = source.CameraSource.__new__(source.CameraSource)
    lecturas = iter([(False, None), (False, None)] + [(True, np.zeros((4, 4, 3), np.uint8))] * 3)

    class Cap:
        def read(self):
            return next(lecturas, (False, None))
    cam._cap, cam.mirror, cam.index = Cap(), False, 0
    viejo = source.FALLOS_TOLERADOS_S
    source.FALLOS_TOLERADOS_S = 0.3
    try:
        cuadros = list(cam.frames())
    finally:
        source.FALLOS_TOLERADOS_S = viejo
    assert len(cuadros) == 3                     # los 2 fallos del inicio no cortaron la sesion
    assert cam.motivo_fin and "dejo de entregar" in cam.motivo_fin


def test_publicar_bloquea_sistema_por_el_tunel_y_pide_clave():
    from src.interfaz import tunel as publicar
    assert publicar.viene_del_tunel({"cf-connecting-ip": "8.8.8.8"}, "127.0.0.1")
    assert not publicar.viene_del_tunel({}, "127.0.0.1")
    assert publicar.viene_del_tunel({}, "192.168.1.20")
    assert not publicar.credencial_valida("Basic eDp5")


def test_entrenar_elige_por_f1_guarda_spec_y_el_vivo_lo_usa():
    """Ciclo completo sin SQL Server: entrenar() (con la lectura de SQL simulada
    con los MISMOS vectores de src.procesamiento.puntos.vectorizar) -> run_N con spec -> el
    clasificador en vivo lo carga y puntua una rep."""
    from unittest.mock import patch

    from src.almacenamiento import dataset_sql as SQL
    from src.entrenamiento import datos as DATOS
    from src.entrenamiento import entrenar as ENTRENAR
    from src.entrenamiento import reportes as REPORTES
    from src.nucleo import ejercicio as EJ
    spec_cfg = NORM.cfg_normalizacion("cuerpo_completo")   # la normalizacion sale de la definicion del ejercicio: entrenar y vivo deben usar la misma
    filas, vectores = [], {}
    for i in range(24):
        clase = "bien" if i % 3 == 0 else "mal"          # desbalanceado a proposito
        clip = f"{clase}/c{i}.mp4"
        filas.append({"clip": clip, "clase": clase, "origen": f"cuerpo_completo/x/{i}.mp4",
                      "exercise": "cuerpo_completo", "type": 1})
        vectores[clip] = vectorizar.vector_de_clip(
            _clip(seed=i, cerrar=1.0 if clase == "bien" else 0.2), NOMBRES_DER,
            {"point_names": NOMBRES_DER, "kpoints": KPOINTS_DER, "cfg": spec_cfg, "features": "ambos",
                 "features_def": FEATS})
    filas.append({"clip": "base/b.mp4", "clase": "base", "origen": "x", "exercise": "cuerpo_completo", "type": 1})
    with tempfile.TemporaryDirectory() as d, \
         patch.object(DATOS, "_manifest", return_value=filas), \
         patch.object(REPORTES, "ENTR", Path(d)), \
         patch.object(DATOS, "seleccion", return_value={}), \
         patch.object(ENTRENAR, "leer_ajustes", return_value={"fuente_entrenamiento": "sql"}), \
         patch.object(ENTRENAR, "respaldo_sql", return_value={"al_entrenar": False}), \
         patch.object(SQL, "features_por_archivo", return_value=vectores), \
         patch.object(SQL, "tipos_conocidos", return_value={1: "cuerpo_completo"}), \
         patch.object(SQL, "config", return_value={"1": spec_cfg}), \
         patch.object(EJ, "kpoints_de_ejercicio", return_value=KPOINTS_DER), \
         patch.object(EJ, "features_de_ejercicio", return_value=FEATS), \
             patch.object(EJ, "puntos_de_ejercicio", return_value=NOMBRES_DER):
        meta = ENTRENAR.entrenar(test_pct=25, modelos=["logistic", "knn", "random_forest"], tipo=1)
        assert meta["criterio"] == "f1_macro" and "base" not in meta["clases"]
        assert meta["linea_base"]["nombre"] == "linea_base"
        assert meta["f1_macro"] >= max(m["f1_macro"] for m in meta["modelos"] if "f1_macro" in m)
        assert meta["f1_macro"] > meta["linea_base"]["f1_macro"]
        assert meta["anidado"] is not None and 0 <= meta["anidado"]["f1_macro"] <= 1
        # lo que define la corrida y la comparacion con la anterior (pedido del tutor)
        assert meta["conteo_clases"] == {"bien": 8, "mal": 16} and meta["kpoints_usados"] == NOMBRES_DER
        assert len(meta["angulos"]) > 0 and all(len(a) == 3 for a in meta["angulos"])
        assert meta["vs_anterior"] is None                      # es la primera
        # matriz de epocas / max_iter y cuantas iteraciones uso cada modelo antes de frenar
        assert set(meta["matriz_modelos"]) == {"logistic", "random_forest", "knn"}
        por = {m["nombre"]: m for m in meta["modelos"]}
        assert por["random_forest"]["iteraciones"]["max"] == 200
        assert por["logistic"]["iteraciones"]["tope"] == 2000 and por["logistic"]["iteraciones"]["freno"]
        assert "iteraciones" not in por["knn"]
        assert len(meta["f1_folds"]) == meta["k"] and meta["f1_std"] >= 0 and meta["n_features"] > 0
        ruta = scorers.buscar_clasificador("cuerpo_completo", Path(d))
        clf = scorers.Clasificador(ruta)
        meta2 = ENTRENAR.entrenar(test_pct=25, modelos=["logistic"], tipo=1, features="puntos")
        v = meta2["vs_anterior"]
        assert v["contra"] == meta["numero"] and v["veredicto"] in ("mejoro", "empeoro", "igual")
        assert "features ambos→puntos" in v["cambios"] and meta2["angulos"] == []
    # una rep 'bien' del set de entrenamiento, como si llegara en vivo
    seg = Segment(start_ms=0, end_ms=900, data=np.zeros((37, 2), np.float32),
                  valid=np.ones((37, 2), bool), kpoints=_clip(seed=0, cerrar=1.0))
    s = clf.puntuar(seg, None)
    assert s.clase == "bien" and s.total > 50, (s.clase, s.total)

