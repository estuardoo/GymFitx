"""DroidCam: lista IP:puerto en datos/config.json y su fuente por URL."""
import pytest

from src.nucleo import config as CFG


def test_normalizar_droidcam():
    assert CFG.normalizar_droidcam("192.168.1.20") == "192.168.1.20:4747"
    assert CFG.normalizar_droidcam(" 10.0.0.5:8080 ") == "10.0.0.5:8080"
    assert CFG.normalizar_droidcam("100.101.102.103") == "100.101.102.103:4747"                    # IP de Tailscale
    assert CFG.url_droidcam("celular.tail1a2b.ts.net:4747") == "http://celular.tail1a2b.ts.net:4747/video"   # MagicDNS
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


def test_nombre_y_formato_viejo(tmp_path, monkeypatch):
    monkeypatch.setattr(CFG, "CONFIG_PATH", tmp_path / "config.json")
    monkeypatch.setattr(CFG, "leer_ajustes", lambda: {"droidcam": CFG._leer_json(CFG.CONFIG_PATH).get("camaras_droidcam", [])})
    CFG.guardar_droidcams(["9.9.9.9", {"nombre": "  Celular   Juan ", "ip": "100.1.2.3"}, {"nombre": "dup", "ip": "9.9.9.9:4747"}])
    assert CFG.droidcams_nombrados() == [{"nombre": "dup", "ip": "9.9.9.9:4747"}, {"nombre": "Celular Juan", "ip": "100.1.2.3:4747"}]
    CFG._actualizar_json(CFG.CONFIG_PATH, {"camaras_droidcam": ["1.1.1.1:4747"]})            # archivo viejo: solo textos
    assert CFG.droidcams_nombrados() == [{"nombre": "", "ip": "1.1.1.1:4747"}] and CFG.droidcams() == ["1.1.1.1:4747"]
    with pytest.raises(ValueError):
        CFG.guardar_droidcams([{"nombre": "x", "ip": "no valido!"}])
