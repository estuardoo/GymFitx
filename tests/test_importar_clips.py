"""importar_clips (src/etiquetado/importar.py): clips ya cortados -> dataset + manifest + SQL."""
import json
import subprocess

import numpy as np
import pytest

from src.etiquetado import importar as IMP
from src.etiquetado.previews import ffmpeg_exe


@pytest.fixture
def entorno(tmp_path, monkeypatch):
    clips, manifest = tmp_path / "clips", tmp_path / "manifest.json"
    registrados, borrados = [], []
    m = monkeypatch
    m.setattr(IMP, "OUT", clips)
    m.setattr(IMP, "MANIFEST", manifest)
    m.setattr(IMP.EP, "leer_ejercicio", lambda s: {} if s == "sentadilla" else None)
    m.setattr(IMP.SQL, "asegurar_base_y_tablas", lambda: None)
    m.setattr(IMP.SQL, "tipo_de_ejercicio", lambda e: 7)
    m.setattr(IMP, "poblar_desde_manifest", lambda rows, d, type_: registrados.extend(rows) or {"archivos_nuevos": len(rows), "omitidos_sin_puntos": 0})
    m.setattr(IMP, "_borrar_en_sql", lambda t, a: borrados.append(a))

    def falsa_deteccion(mp4, ej):
        npz = mp4.with_suffix(".npz")
        d = dict(np.load(npz))
        d.update(points=np.zeros((5, 3, 3), np.float32), point_names=np.array(["a", "b", "c"]))
        np.savez(npz, **d)
        return True
    m.setattr(IMP.deteccion, "detectar_puntos_si_faltan", falsa_deteccion)
    return clips, manifest, registrados, borrados


@pytest.fixture
def video(tmp_path):
    p = tmp_path / "Mi Video 1.mp4"
    subprocess.run([ffmpeg_exe(), "-y", "-loglevel", "error", "-f", "lavfi", "-i", "testsrc=size=64x64:rate=10:duration=1",
                    "-pix_fmt", "yuv420p", str(p)], check=True)
    return p


def test_sube_clip_y_lo_registra(entorno, video):
    clips, manifest, registrados, _ = entorno
    r = IMP.importar_clips("sentadilla", "bien", [(video.name, video)])
    assert r["errores"] == [] and r["ok"] == ["sentadilla/bien/mi_video_1.mp4"]
    assert (clips / "sentadilla/bien/mi_video_1.mp4").exists() and (clips / "sentadilla/bien/mi_video_1.npz").exists()
    fila = json.loads(manifest.read_text())[0]
    assert fila["clase"] == "bien" and fila["exercise"] == "sentadilla" and fila["origen"].startswith("importados/")
    assert 0.8 < fila["dur"] < 1.2
    assert registrados == [fila] and r["sql"]["archivos_nuevos"] == 1


def test_mismo_nombre_no_pisa(entorno, video):
    IMP.importar_clips("sentadilla", "mal", [(video.name, video)])
    r = IMP.importar_clips("sentadilla", "mal", [(video.name, video)])
    assert r["ok"] == ["sentadilla/mal/mi_video_1_2.mp4"]


def test_base_pide_reemplazo(entorno, video):
    clips, manifest, _, borrados = entorno
    IMP.importar_clips("sentadilla", "base", [(video.name, video)])
    r = IMP.importar_clips("sentadilla", "base", [("otra.mp4", video)])
    assert r["base_existente"] and r["ok"] == [] and not (clips / "sentadilla/base/otra.mp4").exists()
    r = IMP.importar_clips("sentadilla", "base", [("otra.mp4", video)], reemplazar=True)
    assert r["base_reemplazada"] and borrados == ["sentadilla/base/mi_video_1.mp4"]
    assert [x["clip"] for x in json.loads(manifest.read_text())] == ["sentadilla/base/otra.mp4"]
    assert not (clips / "sentadilla/base/mi_video_1.mp4").exists()


def test_invalidos(entorno, video, tmp_path):
    clips, *_ = entorno
    with pytest.raises(ValueError):
        IMP.importar_clips("no_existe", "bien", [(video.name, video)])
    with pytest.raises(ValueError):
        IMP.importar_clips("sentadilla", "descarte", [(video.name, video)])
    basura = tmp_path / "x.mp4"
    basura.write_bytes(b"no es video")
    r = IMP.importar_clips("sentadilla", "bien", [("x.mp4", basura), ("nota.txt", basura)])
    assert r["ok"] == [] and len(r["errores"]) == 2
    assert not list(clips.rglob("*.mp4")) and not list(clips.rglob("*.npz"))   # nada a medias


def test_sql_caido_deja_el_clip_local(entorno, video, monkeypatch):
    def cae():
        raise IMP.SQL.SQLServerNoDisponible("sin conexion")
    monkeypatch.setattr(IMP.SQL, "asegurar_base_y_tablas", cae)
    r = IMP.importar_clips("sentadilla", "bien", [(video.name, video)])
    assert r["ok"] and r["sql_error"] == "sin conexion" and r["sql"] is None


def test_endpoint_multipart(entorno, video, monkeypatch):
    from fastapi.testclient import TestClient

    from src.interfaz.app import app
    c = TestClient(app)
    with open(video, "rb") as f:
        r = c.post("/api/ejercicio/clips", data={"slug": "sentadilla", "clase": "bien"}, files=[("archivos", ("a.mp4", f, "video/mp4"))])
    assert r.status_code == 200 and r.json()["ok"] == ["sentadilla/bien/a.mp4"]
    r = c.post("/api/ejercicio/clips", data={"slug": "nada", "clase": "bien"}, files=[("archivos", ("a.mp4", b"x", "video/mp4"))])
    assert r.status_code == 400


def test_panel_arranca_sin_python_multipart():
    """Sin python-multipart el import de api.etiquetado no debe tumbar el panel (solo la subida avisa)."""
    import subprocess
    import sys
    code = ("import sys; sys.modules['multipart']=None; sys.modules['python_multipart']=None; "
            "import src.interfaz.app; print('ok')")
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert "ok" in r.stdout, r.stderr[-400:]


def test_importa_carpeta_por_persona_e_incremental(entorno, video, tmp_path):
    clips, manifest, _, _ = entorno
    raiz = tmp_path / "01Zancada"
    for ruta in ("Base/P1/P1_a_base.mp4", "Bien/P2/P2_x_bien.mp4", "Bien/P10/P10_y_bien.mp4", "Mal/P2/P2_z_mal.mp4"):
        (raiz / ruta).parent.mkdir(parents=True, exist_ok=True)
        (raiz / ruta).write_bytes(video.read_bytes())
    (raiz / "indice.csv").write_text("archivo,clase,persona,fecha,descripcion,vista\n"
                                     "Bien/P2/P2_x_bien.mp4,Bien,P2,2026-09-30,x,frontal\n", "utf-8")
    assert [(c, n) for c, n, *_ in IMP.listar_carpeta(raiz)] == [
        ("bien", "P2_x_bien.mp4"), ("bien", "P10_y_bien.mp4"), ("mal", "P2_z_mal.mp4"), ("base", "P1_a_base.mp4")]   # P2 antes que P10
    r = IMP.importar_carpeta("sentadilla", raiz)
    assert r["ok"] == 4 and r["saltados"] == 0 and r["errores"] == [] and r["por_clase"] == {"base": 1, "bien": 2, "mal": 1}
    filas = {f["clip"]: f for f in json.loads(manifest.read_text())}
    assert filas["sentadilla/bien/p2_x_bien.mp4"]["persona"] == "P2" and filas["sentadilla/bien/p2_x_bien.mp4"]["vista"] == "frontal"
    assert filas["sentadilla/bien/p10_y_bien.mp4"]["persona"] == "P10"
    r2 = IMP.importar_carpeta("sentadilla", raiz)   # incremental: nada nuevo
    assert r2["ok"] == 0 and r2["saltados"] == 4 and len(json.loads(manifest.read_text())) == 4


def test_reconstruye_el_original_con_el_indice(entorno, video, tmp_path, monkeypatch):
    from src.etiquetado import exportar as EXP
    clips, manifest, _, _ = entorno
    monkeypatch.setattr(IMP, "DATA", tmp_path / "grab")
    monkeypatch.setattr(IMP, "LABELS", tmp_path / "etiquetas.json")
    monkeypatch.setattr(EXP, "ESTADO", tmp_path / "estado.json")
    raiz = tmp_path / "01Zancada"
    filas = ["archivo,clase,persona,fecha,descripcion,vista,video_origen,inicio_s,fin_s,duracion_s"]
    for ruta, ini in (("Bien/P2/P2_v_zancada_s03_bien.mp4", 5.0), ("Bien/P2/P2_v_zancada_s01_bien.mp4", 1.0), ("Mal/P2/P2_v_zancada_s05_mal.mp4", 9.0)):
        (raiz / ruta).parent.mkdir(parents=True, exist_ok=True)
        (raiz / ruta).write_bytes(video.read_bytes())
        filas.append(f"{ruta},{ruta.split('/')[0]},P2,2026-09-30,x,frontal,v_zancada.mp4,{ini},{ini + 1},1.0")
    (raiz / "indice.csv").write_text("\n".join(filas) + "\n", "utf-8")
    r = IMP.importar_carpeta("sentadilla", raiz)
    assert r["errores"] == [] and r["originales"] == {"videos": 1, "nuevos": 1}
    vid = "sentadilla/2026-09-30/P2_v_zancada.mp4"
    assert (tmp_path / "grab" / vid).exists() and (tmp_path / "grab" / vid).with_suffix(".npz").exists()
    lab = json.loads((tmp_path / "etiquetas.json").read_text())[vid]
    assert lab["reconstruido"] and [s["clase"] for s in lab["segmentos"]] == ["bien", "bien", "mal"]   # en orden de inicio_s
    assert [s["ini_orig"] for s in lab["segmentos"]] == [1.0, 5.0, 9.0] and lab["segmentos"][1]["ini"] > 0.8
    assert all(f["origen"] == vid and f["persona"] == "P2" for f in json.loads(manifest.read_text()))
    d = np.load((tmp_path / "grab" / vid).with_suffix(".npz"), allow_pickle=True)
    assert len(d["points"]) == 15 and np.all(np.diff(d["points_t_ms"]) >= 0) and len(d["t_ms"]) == 15
    ind = (raiz / "indice.csv").read_text()
    assert "video_reconstruido,ini_rec_s,fin_rec_s" in ind and vid in ind
    # repetir no rehace nada y "Generar cortes" no los volveria a cortar (hash igual al que guardo)
    assert IMP.reconstruir_originales("sentadilla", raiz)["nuevos"] == 0
    est = json.loads((tmp_path / "estado.json").read_text())
    assert est[vid] == EXP._hash(lab["segmentos"], EXP._npz_tiene_puntos(tmp_path / "grab" / vid))
