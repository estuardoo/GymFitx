"""Tests del archivado de sesiones: video, features y metadatos.

No necesita camara ni mediapipe: se simula el pipeline con cuadros sinteticos.
"""

import json
import tempfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent

from synth import a_framevecs, rep_sintetica  # noqa: E402

from src.nucleo.ejercicio import load_exercise  # noqa: E402
from src.nucleo.tipos import Frame  # noqa: E402
from src.procesamiento.medidas.features import FeatureExtractor  # noqa: E402
from src.sesion.grabacion import (
    FPS_SALIDA,
    VideoLogger,
    features_a_csv,
    listar_grabaciones,
    resolver_json,
    uso_en_disco,
)
from src.sesion.sumideros import EventBus, MultiSink, Sink  # noqa: E402

EJ = load_exercise(ROOT / "ejercicios" / "manguito_rotador.yaml")
EXT = FeatureExtractor(EJ)


class PipeFalso:
    """Lo minimo que VideoLogger necesita de un Pipeline."""

    def __init__(self):
        self.exercise = EJ
        self.extractor = EXT
        self.segmenter = None
        self.frames_vistos = 0
        self.bus = EventBus()
        self.eventos = []
        self.bus.subscribe(self.eventos.append)


def _sesion(dir_base, n=60, fps=20.0, guardar_video=True, fps_deteccion=None):
    """Simula una sesion completa y devuelve (logger, pipe). La camara entrega
    'fps'; la deteccion procesa 1 de cada k cuadros si se pide fps_deteccion
    (como el pipeline en vivo, que descarta los que no alcanza)."""
    pipe = PipeFalso()
    vl = VideoLogger(dir_base, guardar_video=guardar_video)
    vl.on_start(pipe)
    datos = rep_sintetica(n_frames=n)[:, :EXT.size]
    fvs = a_framevecs(datos, fps=fps)
    rng = np.random.default_rng(0)
    cada = max(1, round(fps / fps_deteccion)) if fps_deteccion else 1
    for i, fv in enumerate(fvs):
        img = rng.integers(0, 255, (120, 160, 3), dtype=np.uint8)
        frame = Frame(image=img, t_ms=fv.t_ms, index=i)
        vl.on_raw_frame(pipe, frame)                 # hilo de captura: todos los cuadros
        if i % cada == 0:
            vl.on_frame(pipe, frame, fv)             # hilo de deteccion: los que alcanza
            pipe.frames_vistos += 1
    vl.on_stop(pipe)
    return vl, pipe


def test_archiva_video_features_y_metadatos():
    with tempfile.TemporaryDirectory() as d:
        vl, _ = _sesion(d)
        assert vl.video_path.exists() and vl.video_path.stat().st_size > 0
        assert vl.npz_path.exists()
        assert vl.json_path.exists()

        z = np.load(vl.npz_path, allow_pickle=False)
        assert z["values"].shape == (60, EXT.size)
        assert z["t_ms"].shape == (60,)
        assert list(z["names"]) == EXT.names


def test_se_archiva_en_una_carpeta_por_ejercicio():
    """Cada ejercicio en su propia carpeta: datos/grabaciones/<slug>/<dia>/*.{mp4,npz,json}."""
    with tempfile.TemporaryDirectory() as d:
        vl, _ = _sesion(d)
        assert vl.video_path.parent.parent.name == "manguito_rotador"
        assert vl.video_path.parent.name == vl.json_path.parent.name


def test_metadatos_describen_la_sesion():
    with tempfile.TemporaryDirectory() as d:
        vl, _ = _sesion(d, n=60, fps=20.0)
        m = json.loads(vl.json_path.read_text(encoding="utf-8"))
        assert m["exercise"] == "manguito_rotador"
        assert m["modo"] == "referencia"            # sin segmentador = toma de referencia
        assert m["frames_con_deteccion"] == 60
        assert abs(m["fps_medio"] - 20.0) < 1.5
        assert m["resolucion"] == [160, 120]


def test_el_video_dura_lo_que_duro_la_sesion():
    """Con captura a 20 fps, escribir 1:1 a 30 fps daria un video 1.5x mas rapido."""
    import cv2
    with tempfile.TemporaryDirectory() as d:
        vl, _ = _sesion(d, n=60, fps=20.0)     # 60 cuadros a 20 fps = 3.0 s reales
        cap = cv2.VideoCapture(str(vl.video_path))
        cuadros = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        dur_video = cuadros / FPS_SALIDA
        assert abs(dur_video - 3.0) < 0.35, f"el video dura {dur_video:.2f} s, deberia durar 3.0"


def test_video_fluido_aunque_la_deteccion_sea_lenta():
    """Camara a 30 fps, deteccion a ~7 fps: el video lleva los 30 cuadros
    reales por segundo (antes repetia cada cuadro detectado ~4 veces)."""
    with tempfile.TemporaryDirectory() as d:
        vl, _ = _sesion(d, n=90, fps=30.0, fps_deteccion=7.5)
        m = json.loads(vl.json_path.read_text(encoding="utf-8"))
        assert m["fps_video_real"] > 28, m
        assert m["fps_medio"] < 9                     # la deteccion si fue lenta
        assert m["frames_camara"] == 90


def test_puede_archivar_sin_video():
    with tempfile.TemporaryDirectory() as d:
        vl, _ = _sesion(d, guardar_video=False)
        assert vl.video_path is None or not vl.video_path.exists()
        assert vl.npz_path.exists() and vl.json_path.exists()


def test_dos_sesiones_en_el_mismo_segundo_no_se_pisan():
    """Un archivo sobrescrito es material perdido: los nombres deben ser unicos."""
    with tempfile.TemporaryDirectory() as d:
        a, _ = _sesion(d)
        b, _ = _sesion(d)
        assert a.json_path != b.json_path
        assert a.video_path != b.video_path
        assert a.json_path.exists() and b.json_path.exists()


def test_listado_y_uso_de_disco():
    with tempfile.TemporaryDirectory() as d:
        _sesion(d)
        _sesion(d)
        lista = listar_grabaciones(d)
        assert len(lista) == 2
        assert all("ruta_relativa" in g and g["existe_video"] for g in lista)
        assert all(g["ruta_relativa"].startswith("manguito_rotador/") for g in lista)
        uso = uso_en_disco(d)
        assert uso["sesiones"] == 2 and uso["videos"] == 2 and uso["bytes"] > 0


def test_listado_filtra_por_ejercicio():
    with tempfile.TemporaryDirectory() as d:
        _sesion(d)
        assert len(listar_grabaciones(d, exercise="manguito_rotador")) == 1
        assert len(listar_grabaciones(d, exercise="otro_ejercicio")) == 0


def test_resolver_json_desde_ruta_relativa():
    with tempfile.TemporaryDirectory() as d:
        vl, _ = _sesion(d)
        ruta_rel = f"{vl.video_path.parent.parent.name}/{vl.video_path.parent.name}/{vl.video_path.name}"
        assert resolver_json(d, ruta_rel) == vl.json_path


def test_resolver_json_rechaza_escapes():
    with tempfile.TemporaryDirectory() as d:
        try:
            resolver_json(d, "../../etc/passwd")
        except ValueError:
            pass
        else:
            raise AssertionError("deberia rechazar rutas fuera de datos/grabaciones/")


def test_features_a_csv_incluye_cabecera_y_una_fila_por_cuadro():
    with tempfile.TemporaryDirectory() as d:
        vl, _ = _sesion(d, n=60)
        texto = features_a_csv(vl.npz_path)
        filas = texto.strip().splitlines()
        assert filas[0].split(",") == ["t_ms", *EXT.names]
        assert len(filas) == 1 + 60


def test_multisink_reparte_a_todos():
    class Espia(Sink):
        def __init__(self): self.n = {"start":0, "frame":0, "rep":0, "stop":0}
        def on_start(self, p): self.n["start"] += 1
        def on_frame(self, p, f, v): self.n["frame"] += 1
        def on_rep(self, p, s): self.n["rep"] += 1
        def on_stop(self, p): self.n["stop"] += 1

    a, b = Espia(), Espia()
    ms = MultiSink(a, b)
    pipe = PipeFalso()
    ms.on_start(pipe)
    ms.on_frame(pipe, None, None)
    ms.on_frame(pipe, None, None)
    ms.on_rep(pipe, None)
    ms.on_stop(pipe)
    for e in (a, b):
        assert e.n == {"start":1, "frame":2, "rep":1, "stop":1}
    assert ms.find(Espia) is a


def test_emite_evento_de_grabacion():
    with tempfile.TemporaryDirectory() as d:
        _, pipe = _sesion(d)
        tipos = [e["type"] for e in pipe.eventos]
        assert "grabacion" in tipos

