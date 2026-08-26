"""Tests del archivado de sesiones: video, features y metadatos.

No necesita camara ni mediapipe: se simula el pipeline con cuadros sinteticos.

    python tests/test_grabacion.py
"""

import json
import sys
import tempfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

from core.exercise import load_exercise            # noqa: E402
from core.features import FeatureExtractor         # noqa: E402
from core.sinks import EventBus, MultiSink, Sink    # noqa: E402
from core.types import Frame                       # noqa: E402
from core.videolog import (FPS_SALIDA, VideoLogger, features_a_csv,  # noqa: E402
                           listar_grabaciones, resolver_json, uso_en_disco)
from synth import a_framevecs, rep_sintetica       # noqa: E402

EJ = load_exercise(ROOT / "exercises" / "mano_apertura.yaml")
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


def _sesion(dir_base, n=60, fps=20.0, guardar_video=True):
    """Simula una sesion completa y devuelve (logger, pipe)."""
    pipe = PipeFalso()
    vl = VideoLogger(dir_base, guardar_video=guardar_video)
    vl.on_start(pipe)
    datos = rep_sintetica(n_frames=n)
    fvs = a_framevecs(datos, fps=fps)
    rng = np.random.default_rng(0)
    for i, fv in enumerate(fvs):
        img = rng.integers(0, 255, (120, 160, 3), dtype=np.uint8)
        vl.on_frame(pipe, Frame(image=img, t_ms=fv.t_ms, index=i), fv)
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
        assert z["values"].shape == (60, 6)
        assert z["t_ms"].shape == (60,)
        assert list(z["names"]) == EXT.names


def test_se_archiva_en_una_carpeta_por_ejercicio():
    """Cada ejercicio en su propia carpeta: recordings/<slug>/<dia>/*.{mp4,npz,json}."""
    with tempfile.TemporaryDirectory() as d:
        vl, _ = _sesion(d)
        assert vl.video_path.parent.parent.name == "mano_apertura"
        assert vl.video_path.parent.name == vl.json_path.parent.name


def test_metadatos_describen_la_sesion():
    with tempfile.TemporaryDirectory() as d:
        vl, _ = _sesion(d, n=60, fps=20.0)
        m = json.loads(vl.json_path.read_text(encoding="utf-8"))
        assert m["exercise"] == "mano_apertura"
        assert m["modo"] == "base"                  # sin segmentador = grabacion de base
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
        _sesion(d); _sesion(d)
        lista = listar_grabaciones(d)
        assert len(lista) == 2
        assert all("ruta_relativa" in g and g["existe_video"] for g in lista)
        assert all(g["ruta_relativa"].startswith("mano_apertura/") for g in lista)
        uso = uso_en_disco(d)
        assert uso["sesiones"] == 2 and uso["videos"] == 2 and uso["bytes"] > 0


def test_listado_filtra_por_ejercicio():
    with tempfile.TemporaryDirectory() as d:
        _sesion(d)
        assert len(listar_grabaciones(d, exercise="mano_apertura")) == 1
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
            raise AssertionError("deberia rechazar rutas fuera de recordings/")


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


if __name__ == "__main__":
    fallos = 0
    for nombre, fn in sorted(globals().items()):
        if nombre.startswith("test_") and callable(fn):
            try:
                fn(); print(f"  OK    {nombre}")
            except Exception as e:
                fallos += 1; print(f"  FALLA {nombre}: {e}")
    print("\nTodo bien." if not fallos else f"\n{fallos} test(s) fallaron.")
    raise SystemExit(1 if fallos else 0)
