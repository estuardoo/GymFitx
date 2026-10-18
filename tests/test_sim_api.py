"""Modulo SIM (interfaz/api/sim.py): 3 vistas de verificacion visual de un clip -- video original,
esqueleto crudo (points_screen del propio .npz del clip) y esqueleto normalizado ya alineado en tiempo
(DTW) contra el clip base, sin recalcular nada nuevo (ver docstring de sim.py)."""

from __future__ import annotations

import numpy as np
from test_swap_sink import _instalar_stub_mediapipe  # noqa: E402

_instalar_stub_mediapipe()

from fastapi.testclient import TestClient  # noqa: E402

from src.interfaz.api import sim  # noqa: E402
from src.interfaz.app import app  # noqa: E402

client = TestClient(app)

FILAS = [
    {"clip": "base/b.mp4", "clase": "base", "type": 1, "exercise": "sentadilla", "npz": "b.npz"},
    {"clip": "bien/c1.mp4", "clase": "bien", "type": 1, "exercise": "sentadilla", "npz": "c1.npz"},
    {"clip": "mal/c2.mp4", "clase": "mal", "type": 1, "exercise": "sentadilla", "npz": None},
]
KPOINTS = [{"nombre": "P1", "origen": {}}, {"nombre": "P2", "origen": {}}]


def test_sim_opciones_agrupa_clips_por_clase(monkeypatch):
    monkeypatch.setattr(sim, "_manifest", lambda: FILAS)
    monkeypatch.setattr(sim.SQL, "tipos_conocidos", lambda: {1: "sentadilla"})
    r = client.get("/api/sim/opciones?tipo=1")
    assert r.status_code == 200
    d = r.json()
    assert d["clips"] == {"base": ["base/b.mp4"], "bien": ["bien/c1.mp4"], "mal": ["mal/c2.mp4"]}


def test_sim_crudo_devuelve_puntos_de_pantalla_y_angulos(monkeypatch, tmp_path):
    npz = tmp_path / "bien" / "c1.npz"
    npz.parent.mkdir(parents=True)
    np.savez(npz, points=np.zeros((3, 2, 3), dtype="float32"), point_names=np.array(["P1", "P2"]),
              points_screen=np.ones((3, 2, 2), dtype="float32") * 0.5,
              points_t_ms=np.array([0, 100, 200]))
    monkeypatch.setattr(sim, "_manifest", lambda: FILAS)
    monkeypatch.setattr(sim, "OUT", tmp_path)
    monkeypatch.setattr(sim, "kpoints_de_ejercicio", lambda ej: KPOINTS)
    monkeypatch.setattr(sim, "features_de_ejercicio", lambda ej: [])
    monkeypatch.setattr(sim.FEAT, "medibles", lambda nombres, features: [{"name": "a1", "points": ["P1", "P2"]}])
    monkeypatch.setattr(sim.FEAT, "medir_clip", lambda points, nombres, features: (np.array([[10.0], [20.0], [30.0]]), ["a1"], ["angle"]))
    monkeypatch.setattr(sim.PUNTOS, "conexiones_kpoints", lambda kpoints: [[0, 1]])

    r = client.get("/api/sim/crudo?clip=bien/c1.mp4")
    assert r.status_code == 200
    d = r.json()
    assert d["t_ms"] == [0, 100, 200]
    assert d["nombres"] == ["P1", "P2"]
    assert d["conexiones"] == [[0, 1]]
    assert d["nombres_angulos"] == ["a1"]
    assert d["angulos"] == [[10.0], [20.0], [30.0]]
    assert d["angulos_puntos"] == [["P1", "P2"]]   # '1-2' -> point_names[0], point_names[1]
    assert len(d["puntos"]) == 3 and d["puntos"][0][0] == [0.5, 0.5]


def test_sim_crudo_sin_npz_da_404(monkeypatch):
    monkeypatch.setattr(sim, "_manifest", lambda: FILAS)
    r = client.get("/api/sim/crudo?clip=mal/c2.mp4")
    assert r.status_code == 404 and "npz" in r.json()["error"]


def test_sim_crudo_clip_viejo_sin_points_screen_da_error_claro(monkeypatch, tmp_path):
    npz = tmp_path / "bien" / "c1.npz"
    npz.parent.mkdir(parents=True)
    np.savez(npz, points=np.zeros((2, 2, 3), dtype="float32"), point_names=np.array(["P1", "P2"]))
    monkeypatch.setattr(sim, "_manifest", lambda: FILAS)
    monkeypatch.setattr(sim, "OUT", tmp_path)
    r = client.get("/api/sim/crudo?clip=bien/c1.mp4")
    assert r.status_code == 404 and "Generar Cortes" in r.json()["error"]


def test_sim_crudo_clip_desconocido_da_404(monkeypatch):
    monkeypatch.setattr(sim, "_manifest", lambda: FILAS)
    r = client.get("/api/sim/crudo?clip=no/existe.mp4")
    assert r.status_code == 404


def test_sim_crudo_reindexa_conexiones_al_orden_del_npz_y_descarta_huesos_incompletos(monkeypatch, tmp_path):
    # catalogo del ejercicio: P1-P2 y P2-P3 son huesos. El npz trae P2 y P1 (en ESE orden, sin P3) --
    # las conexiones deben salir en indices de ESTE arreglo (no del catalogo) y sin el hueso P2-P3 (P3 no
    # esta), no todas vacias como antes.
    npz = tmp_path / "bien" / "c1.npz"
    npz.parent.mkdir(parents=True)
    np.savez(npz, points=np.zeros((1, 2, 3), dtype="float32"), point_names=np.array(["P2", "P1"]),
              points_screen=np.zeros((1, 2, 2), dtype="float32"), points_t_ms=np.array([0]))
    catalogo = [{"nombre": "P1"}, {"nombre": "P2"}, {"nombre": "P3"}]
    monkeypatch.setattr(sim, "_manifest", lambda: FILAS)
    monkeypatch.setattr(sim, "OUT", tmp_path)
    monkeypatch.setattr(sim, "kpoints_de_ejercicio", lambda ej: catalogo)
    monkeypatch.setattr(sim, "features_de_ejercicio", lambda ej: [])
    monkeypatch.setattr(sim.FEAT, "medibles", lambda nombres, features: [])
    monkeypatch.setattr(sim.PUNTOS, "conexiones_kpoints", lambda kpoints: [[0, 1], [1, 2]])
    monkeypatch.setattr(sim.FEAT, "medir_clip", lambda points, nombres, features: (np.array([[0.0]]), ["a1"], ["angle"]))

    r = client.get("/api/sim/crudo?clip=bien/c1.mp4")
    assert r.status_code == 200
    d = r.json()
    assert d["nombres"] == ["P2", "P1"]
    assert d["conexiones"] == [[1, 0]]   # P1(idx1)-P2(idx0), el hueso P2-P3 se descarta (P3 no esta)


def _frames(x, y):
    return {"x": list(x), "y": list(y), "z": [0.0] * len(x)}


def test_sim_normalizado_alinea_y_calcula_indicador_por_kpoint(monkeypatch):
    # base: P1 se mueve en linea recta; P2 no se mueve (SStot~0 -> sin indicador)
    frames_base = {"P1": _frames([0, 1, 2, 3], [0, 1, 2, 3]), "P2": _frames([5, 5, 5, 5], [5, 5, 5, 5])}
    frames_otro = {"P1": _frames([0, 1, 2, 3], [0, 1, 2, 3]), "P2": _frames([5, 5, 5, 5], [5, 5, 5, 5])}

    def falso_frames_de(tipo, archivo):
        return frames_base if archivo == "base/b.mp4" else frames_otro

    monkeypatch.setattr(sim, "_manifest", lambda: FILAS)
    monkeypatch.setattr(sim.SQL, "frames_de", falso_frames_de)
    monkeypatch.setattr(sim, "kpoints_de_ejercicio", lambda ej: KPOINTS)
    monkeypatch.setattr(sim.PUNTOS, "conexiones_kpoints", lambda kpoints: [[0, 1]])

    r = client.get("/api/sim/normalizado?tipo=1&base=base/b.mp4&clip=bien/c1.mp4")
    assert r.status_code == 200
    d = r.json()
    assert d["nombres"] == ["P1", "P2"]
    assert d["conexiones"] == [[0, 1]]
    assert d["indicadores"][0] == 100.0   # P1 identico tras alinear -> R2 perfecto
    assert d["indicadores"][1] is None    # P2 sin variacion en el base -> sin indicador
    assert len(d["base"]) == 2 and len(d["base"][0]) == 4   # 4 frames


def test_sim_normalizado_conserva_conexiones_aunque_falte_un_kpoint_del_catalogo(monkeypatch):
    # P3 esta en frames_base/frames_otro pero NO en el catalogo del ejercicio (caso raro) -- antes esto
    # tiraba TODAS las conexiones (incluida P1-P2, que si son validas); ahora solo se pierde lo que toca P3.
    frames_base = {"P1": _frames([0, 1], [0, 1]), "P2": _frames([5, 5], [5, 5]), "P3": _frames([1, 1], [1, 1])}
    frames_otro = {"P1": _frames([0, 1], [0, 1]), "P2": _frames([5, 5], [5, 5]), "P3": _frames([1, 1], [1, 1])}
    catalogo = [{"nombre": "P1"}, {"nombre": "P2"}]   # P3 no esta

    def falso_frames_de(tipo, archivo):
        return frames_base if archivo == "base/b.mp4" else frames_otro

    monkeypatch.setattr(sim, "_manifest", lambda: FILAS)
    monkeypatch.setattr(sim.SQL, "frames_de", falso_frames_de)
    monkeypatch.setattr(sim, "kpoints_de_ejercicio", lambda ej: catalogo)
    monkeypatch.setattr(sim.PUNTOS, "conexiones_kpoints", lambda kpoints: [[0, 1]])   # P1-P2 en el catalogo

    r = client.get("/api/sim/normalizado?tipo=1&base=base/b.mp4&clip=bien/c1.mp4")
    assert r.status_code == 200
    d = r.json()
    assert set(d["nombres"]) == {"P1", "P2", "P3"}
    i1, i2 = d["nombres"].index("P1"), d["nombres"].index("P2")
    assert d["conexiones"] == [[i1, i2]]   # el hueso P1-P2 sigue ahi aunque P3 no este en el catalogo


def test_sim_normalizado_sql_no_disponible(monkeypatch):
    from src.almacenamiento import dataset_sql as SQL

    def revienta(tipo, archivo):
        raise SQL.SQLServerNoDisponible("sin servidor")
    monkeypatch.setattr(sim.SQL, "frames_de", revienta)
    r = client.get("/api/sim/normalizado?tipo=1&base=base/b.mp4&clip=bien/c1.mp4")
    assert r.status_code == 400 and "SQL Server" in r.json()["error"]


def test_sim_normalizado_sin_table_frames_fix_da_404(monkeypatch):
    monkeypatch.setattr(sim, "_manifest", lambda: FILAS)
    monkeypatch.setattr(sim.SQL, "frames_de", lambda tipo, archivo: {})
    r = client.get("/api/sim/normalizado?tipo=1&base=base/b.mp4&clip=bien/c1.mp4")
    assert r.status_code == 404


def test_sim_cuerpo3d_devuelve_puntos_world_y_nan_como_null(monkeypatch, tmp_path):
    npz = tmp_path / "bien" / "c1.npz"
    npz.parent.mkdir(parents=True)
    pts = np.zeros((2, 2, 3), dtype="float32")
    pts[1, 0, 0] = np.nan
    np.savez(npz, points=pts, point_names=np.array(["P1", "P2"]), t_ms=np.array([0, 50]))
    monkeypatch.setattr(sim, "_manifest", lambda: FILAS)
    monkeypatch.setattr(sim, "OUT", tmp_path)
    d = client.get("/api/sim/cuerpo3d?clip=bien/c1.mp4").json()
    assert d["nombres"] == ["P1", "P2"] and d["t_ms"] == [0, 50]
    assert d["puntos"][0][0] == [0.0, 0.0, 0.0] and d["puntos"][1][0][0] is None


def test_sim_cuerpo3d_sin_npz_da_404(monkeypatch):
    monkeypatch.setattr(sim, "_manifest", lambda: FILAS)
    assert client.get("/api/sim/cuerpo3d?clip=mal/c2.mp4").status_code == 404
