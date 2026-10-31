"""recorta_npz (src/etiquetado/exportar.py): recorta el .npz hermano de un video al segmento [ini,fin] --
incluye points_screen/points_t_ms (relativos al INICIO DEL CLIP) para que la pestana SIM pueda sincronizar
el overlay de puntos con la reproduccion del clip ya cortado."""

import numpy as np


def test_recorta_npz_incluye_points_screen_y_t_ms_relativos_al_clip(tmp_path):
    from src.etiquetado import exportar as X

    src = tmp_path / "video.mp4"
    npz = src.with_suffix(".npz")
    # 10 cuadros de "puntos" a 100 cuadros/seg (10ms entre cuadros), 1 punto
    t_ms = np.arange(10) * 100
    np.savez(npz, values=np.zeros((3, 1), dtype=np.float32), t_ms=np.array([0, 500, 999]),
             names=np.array(["m1"]), units=np.array(["u"]),
             points=np.arange(10, dtype=np.float32).reshape(10, 1, 1) * np.ones((1, 1, 3)),
             points_t_ms=t_ms, point_names=np.array(["P1"]),
             points_screen=np.arange(10, dtype=np.float32).reshape(10, 1, 1) * np.ones((1, 1, 2)) / 10)

    dst = tmp_path / "clip.npz"
    # recorta el segmento [0.3s, 0.7s] -> cuadros con t_ms en [300,700]: indices 3..7 (5 cuadros)
    nombre = X.recorta_npz(src, 0.3, 0.7, dst)

    assert nombre == "clip.npz"
    d = dict(np.load(dst, allow_pickle=True))
    assert list(d["points_t_ms"]) == [0, 100, 200, 300, 400]   # relativo al INICIO del clip (300), no del video
    assert d["points"].shape[0] == 5 and d["points_screen"].shape[0] == 5
    assert d["points"][0, 0, 0] == 3.0   # el cuadro que caia en t_ms=300 del video fuente


def test_recorta_npz_sin_points_screen_en_la_fuente_no_revienta(tmp_path):
    """Grabaciones viejas / en vivo de GYMFITX no traen points_screen -- el clip se recorta igual, solo
    sin ese campo (SIM lo reporta como 'sin puntos de pantalla' en vez de fallar)."""
    from src.etiquetado import exportar as X

    src = tmp_path / "video.mp4"
    npz = src.with_suffix(".npz")
    np.savez(npz, values=np.zeros((3, 1), dtype=np.float32), t_ms=np.array([0, 500, 999]),
             names=np.array(["m1"]), units=np.array(["u"]),
             points=np.zeros((3, 1, 3), dtype=np.float32), point_names=np.array(["P1"]))

    dst = tmp_path / "clip.npz"
    X.recorta_npz(src, 0.0, 1.0, dst)
    d = dict(np.load(dst, allow_pickle=True))
    assert "points_screen" not in d and "points_t_ms" not in d
    assert d["points"].shape[0] == 3


def test_exportar_conserva_clips_sin_raw(tmp_path, monkeypatch):
    """Clips sin video de origen (importados ya cortados) siguen en la tabla tras un 'Generar cortes'."""
    from src.almacenamiento import dataset_sql as SQL
    from src.etiquetado import exportar as X
    from src.nucleo import inputs as INP

    with INP.editar() as t:
        c = INP.registrar_clip(t, "sentadilla", etiqueta=1, t_ini_ms=0, t_fin_ms=1000, persona="P1")
    monkeypatch.setattr(X, "ESTADO", tmp_path / "export_estado.json")
    monkeypatch.setattr(SQL, "asegurar_base_y_tablas", lambda: (_ for _ in ()).throw(SQL.SQLServerNoDisponible("x")))

    X.exportar({})   # sin cortes: nada que cortar, el clip sin raw debe sobrevivir

    assert [x["id"] for x in INP.tabla()["clips"]] == [c["id"]]
