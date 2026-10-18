"""Verifica el log de sesion y las rutas /api/log, /api/libraries,
/api/system/shutdown, /api/system/restart. Mismo truco que test_swap_sink.py:
mediapipe queda sustituido por un doble minimo, no hace falta camara.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parent.parent

from test_swap_sink import _instalar_stub_mediapipe  # noqa: E402

_instalar_stub_mediapipe()

from fastapi.testclient import TestClient  # noqa: E402

from src.interfaz import control as serve  # noqa: E402
from src.interfaz.app import app  # noqa: E402

client = TestClient(app)


def test_log_tail_no_revienta_sin_archivo_previo():
    r = client.get("/api/log")
    assert r.status_code == 200
    assert "lineas" in r.json()


def test_log_registra_eventos_relevantes_y_salta_status():
    serve.log.handlers[0].flush()
    serve._al_bus_archivo({"type": "rep", "exercise": "sentadilla", "score": 90})
    serve._al_bus_archivo({"type": "status", "angulo": 45})  # no debe loguearse
    serve.log.handlers[0].flush()
    from src.nucleo.log import SESSION_LOG_PATH

    texto = SESSION_LOG_PATH.read_text(encoding="utf-8")
    assert "rep" in texto
    assert "'angulo': 45" not in texto


def test_libraries_incluye_python_y_version_o_none():
    r = client.get("/api/libraries")
    assert r.status_code == 200
    libs = r.json()["librerias"]
    nombres = [l["nombre"] for l in libs]
    assert "python" in nombres
    assert all("version" in l for l in libs)


def test_shutdown_apaga_el_proceso_sin_matar_el_test():
    with patch("src.interfaz.api.sistema.os._exit") as salida, patch("threading.Timer") as temporizador:
        r = client.post("/api/system/shutdown")
        assert r.status_code == 200
        assert temporizador.called
        assert not salida.called  # se agenda con Timer, no se llama directo


def test_restart_relanza_el_bat_antes_de_salir():
    with patch("src.interfaz.api.sistema.subprocess.Popen") as popen, patch("threading.Timer") as temporizador:
        r = client.post("/api/system/restart")
        assert r.status_code == 200
        assert popen.called
        assert "GYMFITX.bat" in str(popen.call_args)
        assert temporizador.called


def test_libraries_incluye_version_requerida():
    r = client.get("/api/libraries")
    libs = {l["nombre"]: l for l in r.json()["librerias"]}
    assert libs["python"]["requerida"] is None
    algun_paquete = next(l for l in libs.values() if l["nombre"] != "python")
    assert algun_paquete["requerida"]   # viene de requirements.txt, no vacio


def test_actualizar_libreria_desconocida_da_404():
    r = client.post("/api/system/libraries/update", json={"nombre": "no-existe-esta-lib"})
    assert r.status_code == 404


def test_actualizar_libreria_llama_pip_con_la_restriccion_del_requirements():
    import subprocess as sp
    resultado = sp.CompletedProcess(args=[], returncode=0, stdout="ok", stderr="")
    with patch("src.interfaz.api.sistema.subprocess.run", return_value=resultado) as correr:
        r = client.post("/api/system/libraries/update", json={"nombre": "numpy"})
        assert r.status_code == 200
        args = correr.call_args[0][0]
        assert any(a.startswith("numpy") for a in args)


def test_actualizar_todo_usa_requirements_txt():
    import subprocess as sp
    resultado = sp.CompletedProcess(args=[], returncode=0, stdout="ok", stderr="")
    with patch("src.interfaz.api.sistema.subprocess.run", return_value=resultado) as correr:
        r = client.post("/api/system/libraries/update", json={})
        assert r.status_code == 200
        args = correr.call_args[0][0]
        assert "-r" in args


def test_python_entorno_devuelve_version_actual():
    r = client.get("/api/system/python")
    assert r.status_code == 200
    d = r.json()
    assert d["actual"]
    assert isinstance(d["detectadas"], list)


def test_cambiar_version_python_rechaza_version_no_detectada():
    with patch("src.interfaz.api.sistema._detectar_versiones_python", return_value=["3.11", "3.12"]):
        r = client.post("/api/system/python_version", json={"version": "2.7"})
        assert r.status_code == 400


def test_cambiar_version_python_escribe_marcador_y_reinicia():
    with patch("src.interfaz.api.sistema._detectar_versiones_python", return_value=["3.12"]), \
         patch("src.interfaz.api.sistema.shutil.rmtree") as borrar, \
         patch("src.interfaz.api.sistema.subprocess.Popen") as popen, \
         patch("threading.Timer") as temporizador:
        r = client.post("/api/system/python_version", json={"version": "3.12"})
        assert r.status_code == 200
        assert borrar.called
        assert popen.called
        assert temporizador.called
    from src.interfaz.api import sistema
    marcador = sistema.ROOT / "python_version.txt"
    assert marcador.exists() and marcador.read_text(encoding="utf-8").strip() == "3.12"
    marcador.write_text("", encoding="utf-8")   # no se puede borrar el archivo aqui; lo vaciamos


def test_al_bus_gestos_ignora_eventos_que_no_son_gesto():
    with patch.object(serve.sesion, "grabar_iniciar") as iniciar, \
         patch.object(serve.sesion, "grabar_detener") as detener:
        serve._al_bus_gestos({"type": "rep"})
        assert not iniciar.called and not detener.called


def test_al_bus_gestos_sin_sesion_activa_no_hace_nada():
    assert serve.sesion.pipeline is None
    with patch.object(serve.sesion, "grabar_iniciar") as iniciar:
        serve._al_bus_gestos({"type": "gesto", "gesto": "mano_abrir_cerrar"})
        assert not iniciar.called


def test_al_bus_gestos_inicia_grabacion_si_no_esta_grabando():
    class FalsoPipeline:
        sink = serve.Sink()   # sumidero vacio = previsualizando, no grabando
        grabando = False

    serve.sesion.pipeline = FalsoPipeline()
    try:
        with patch.object(serve.sesion, "grabar_iniciar") as iniciar, \
             patch.object(serve.sesion, "grabar_detener") as detener:
            serve._al_bus_gestos({"type": "gesto", "gesto": "mano_abrir_cerrar"})
            assert iniciar.called and not detener.called
    finally:
        serve.sesion.pipeline = None


def test_al_bus_gestos_detiene_si_ya_esta_grabando():
    # Sumidero REAL de grabacion, no un doble artificial: Recorder hereda de
    # Sink (igual que Evaluator y MultiSink), asi que "isinstance(sink, Sink)"
    # es cierto para CUALQUIER sumidero y nunca distingue grabando de no
    # grabando -- este test con un doble que no heredaba de Sink no lo
    # hubiera detectado. pipeline.grabando usa "type(sink) is Sink" y si
    # distingue.
    class FalsoPipeline:
        sink = serve.Recorder("dummy_no_se_escribe")
        grabando = True

    serve.sesion.pipeline = FalsoPipeline()
    try:
        with patch.object(serve.sesion, "grabar_iniciar") as iniciar, \
             patch.object(serve.sesion, "grabar_detener") as detener:
            serve._al_bus_gestos({"type": "gesto", "gesto": "mano_abrir_cerrar"})
            assert detener.called and not iniciar.called
    finally:
        serve.sesion.pipeline = None


def test_camera_on_con_pipeline_que_falla_cierra_la_camara_y_da_502():
    """Si el modelo de deteccion no se pudo cargar (p.ej. no se descargo:
    ver src/captura/deteccion/tracker.py ensure_model), antes esto tumbaba con un 500 crudo
    y ademas dejaba la camara abierta -- el siguiente intento fallaba con
    "camara en uso" en vez del error real.
    """
    fuente_falsa = MagicMock()
    with patch("src.interfaz.control.CameraSource", return_value=fuente_falsa), \
         patch("src.interfaz.control.Pipeline", side_effect=RuntimeError("modelo no descargado")):
        r = client.post("/api/session/camera_on", json={"exercise": "manguito_rotador"})
        assert r.status_code == 502
        assert "modelo no descargado" in r.json()["detail"]
        assert fuente_falsa.close.called
    assert not serve.sesion.activa


def test_set_exercise_con_deteccion_que_falla_da_502_y_no_pierde_la_sesion():
    class FalsoPipeline:
        sink = serve.Sink()
        grabando = False

        def set_exercise(self, ex, plantilla):
            raise RuntimeError("modelo no descargado")

    serve.sesion.thread = MagicMock(is_alive=lambda: True)
    serve.sesion.pipeline = FalsoPipeline()
    serve.sesion._cfg = {"slug": "cuerpo_completo"}
    serve.sesion.info = {"exercise": "cuerpo_completo", "name": "Cuerpo completo"}
    try:
        r = client.post("/api/session/exercise", json={"exercise": "manguito_rotador"})
        assert r.status_code == 502
        assert "modelo no descargado" in r.json()["detail"]
        assert serve.sesion.info["exercise"] == "cuerpo_completo"   # no cambio de ejercicio
    finally:
        serve.sesion.thread = None
        serve.sesion.pipeline = None
        serve.sesion._cfg = None
        serve.sesion.info = {}

