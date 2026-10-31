"""Los tests usan sus propios ejercicios y carpetas temporales: nunca tocan input/, output/ ni parameters/ del usuario."""
import os
import shutil
import tempfile
from pathlib import Path

AQUI = Path(__file__).parent
_T = Path(tempfile.mkdtemp(prefix="gymfitx_test_"))
_P = _T / "parameters"
_P.mkdir()
import json  # noqa: E402

for n in ("server.json",):   # ajustes del repo; inputs.json nace vacio
    if (AQUI.parent / "parameters" / n).exists():
        shutil.copy(AQUI.parent / "parameters" / n, _P / n)
_cfg = json.loads((AQUI.parent / "parameters" / "config.json").read_text("utf-8"))
for k in ("modelos", "camaras_droidcam", "respaldo_sql", "ejercicios"):   # lo que el usuario cambia a su gusto no entra a los tests
    _cfg.pop(k, None)
(_P / "config.json").write_text(json.dumps(_cfg), "utf-8")

os.environ["GYMFITX_INPUT"] = str(_T / "input")
os.environ["GYMFITX_OUTPUT"] = str(_T / "output")
os.environ["GYMFITX_PARAMETROS"] = str(_P)
os.environ["GYMFITX_DATOS"] = str(_T / "sistema")


# ejercicios de prueba (tests/data/ejercicios/*.json) -> parameters/<n>/ de la carpeta temporal, numerados 1, 2, 3...
import sys  # noqa: E402

sys.path.insert(0, str(AQUI.parent))
os.environ["GYMFITX_DATOS"] = str(_T / "sistema")
from src.nucleo import definicion as _DEF  # noqa: E402

for _f in sorted((AQUI / "data" / "ejercicios").glob("*.json")):
    _DEF.guardar(_f.stem, json.loads(_f.read_text("utf-8")))
_SEMILLA = _T / "semilla"
shutil.copytree(_P, _SEMILLA)


def pytest_sessionfinish(session, exitstatus):
    shutil.rmtree(_T, ignore_errors=True)


import pytest  # noqa: E402


@pytest.fixture(autouse=True)
def _estado_limpio():
    """Cada test arranca sin ejercicios, videos ni clips registrados."""
    for d in ("input", "output"):
        shutil.rmtree(_T / d, ignore_errors=True)
    for f in (_T / "sistema").glob("*") if (_T / "sistema").exists() else []:   # el log de la sesion sigue abierto
        if f.name != "logs":
            shutil.rmtree(f, ignore_errors=True) if f.is_dir() else f.unlink(missing_ok=True)
    (_P / "inputs.json").unlink(missing_ok=True)
    for d in _P.iterdir():                       # los ejercicios que un test haya creado o cambiado vuelven a los de prueba
        if d.is_dir() and d.name.isdigit():
            shutil.rmtree(d)
    shutil.copytree(_SEMILLA, _P, dirs_exist_ok=True)
    yield


@pytest.fixture(autouse=True)
def _sin_sql(monkeypatch):
    """Ningun test sube a SQL Server (en el PC del usuario hay un servidor real): formatear() no lo intenta."""
    from src.preparacion import etapas
    monkeypatch.setattr(etapas, "_subir_sql", lambda ejercicio: {"estado": "pendiente", "error": "tests", "resumen": None})
