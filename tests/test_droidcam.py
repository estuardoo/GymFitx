"""DroidCam: lista IP:puerto en datos/config.json y su fuente por URL."""
import pytest

from src.nucleo import config as CFG


def test_normalizar_droidcam():
    assert CFG.normalizar_droidcam("192.168.1.20") == "192.168.1.20:4747"
    assert CFG.normalizar_droidcam(" 10.0.0.5:8080 ") == "10.0.0.5:8080"
    assert CFG.url_droidcam("10.0.0.5:8080") == "http://10.0.0.5:8080/video"
    for malo in ("", "http://x", "1.2.3.4:0", "1.2.3.4:70000", "a b"):
        with pytest.raises(ValueError):
            CFG.normalizar_droidcam(malo)


def test_guardar_lista_sin_repetidos(tmp_path, monkeypatch):
    monkeypatch.setattr(CFG, "CONFIG_PATH", tmp_path / "config.json")
    assert CFG.guardar_droidcams(["1.1.1.1", "1.1.1.1:4747", "2.2.2.2:5000"]) == ["1.1.1.1:4747", "2.2.2.2:5000"]
    assert CFG.droidcams() == ["1.1.1.1:4747", "2.2.2.2:5000"]
    with pytest.raises(ValueError):
        CFG.guardar_droidcams(["no valido!"])
    assert CFG.droidcams() == ["1.1.1.1:4747", "2.2.2.2:5000"]   # lo invalido no pisa lo guardado


def test_camera_source_url_sin_respuesta(monkeypatch):
    from src.captura.fuentes import camara
    monkeypatch.setattr(camara, "_abrir_url", lambda url: None)
    with pytest.raises(RuntimeError, match="DroidCam"):
        camara.CameraSource(url="http://1.2.3.4:4747/video")
