"""subir_github/ (herramienta aparte para subir el codigo a GitHub): validacion, envio contra un repo local, el token no se sube."""
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "subir_github"))
import subir_github as S  # noqa: E402

hay_git = pytest.mark.skipif(shutil.which("git") is None, reason="git no instalado")


def _git(cwd, *a):
    return subprocess.run(["git", *a], cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()


@pytest.fixture
def remoto(tmp_path, monkeypatch):
    bare = tmp_path / "remoto.git"
    subprocess.run(["git", "init", "--bare", "-q", str(bare)], check=True)
    monkeypatch.setattr(S, "URL", re.compile(r"(.*)()"))   # el "repo" es una carpeta local
    return bare


def _cfg(tmp_path, remoto, nombre="a", **extra):
    d = tmp_path / nombre
    d.mkdir(exist_ok=True)
    return {"usuario": "ana", "token": "SECRETO", "repo": str(remoto), "rama": "main", "carpeta": str(d), **extra}


def test_validar_pide_cada_dato(tmp_path):
    ok = {"usuario": "ana", "token": "T", "repo": "https://github.com/a/b", "rama": "main", "carpeta": str(tmp_path)}
    S.validar(ok)
    for campo, valor, texto in (("usuario", " ", "usuario"), ("token", "", "token"), ("repo", "http://x/y", "repositorio"),
                                ("rama", "a..b", "Rama"), ("carpeta", str(tmp_path / "no"), "carpeta")):
        with pytest.raises(S.Error, match=texto):
            S.validar({**ok, campo: valor})


@hay_git
def test_subir_primera_vez_segunda_y_log(tmp_path, remoto):
    cfg, lineas = _cfg(tmp_path, remoto), []
    d = Path(cfg["carpeta"])
    (d / "uno.txt").write_text("1")
    S.subir(cfg, "primero", lineas.append)
    assert _git(remoto, "log", "-1", "--format=%s", "main") == "primero"
    assert any("Enviado a main" in x for x in lineas) and any("Commit" in x for x in lineas)
    assert _git(d, "config", "user.email") == "ana@users.noreply.github.com"
    lineas.clear()
    S.subir(cfg, "", lineas.append)   # sin cambios: no falla y lo dice
    assert "• Sin cambios nuevos" in lineas
    (d / "dos.txt").write_text("2")
    S.subir(cfg, "", lineas.append)   # mensaje vacio: pone uno con fecha
    assert _git(remoto, "log", "-1", "--format=%s", "main").startswith("Actualizacion ")


@hay_git
def test_otra_rama_parte_de_lo_que_hay_en_github(tmp_path, remoto):
    a = _cfg(tmp_path, remoto, "a")
    (Path(a["carpeta"]) / "uno.txt").write_text("1")
    S.subir(a, "base", lambda _: None)
    b = _cfg(tmp_path, remoto, "b", rama="ana/prueba")   # otra copia sin .git, a una rama nueva
    (Path(b["carpeta"]) / "uno.txt").write_text("1")
    (Path(b["carpeta"]) / "dos.txt").write_text("2")
    S.subir(b, "en rama", lambda _: None)
    assert _git(remoto, "log", "--format=%s", "ana/prueba").splitlines() == ["en rama", "base"]   # sin historia duplicada
    assert _git(remoto, "rev-list", "--count", "main") == "1"


@hay_git
def test_el_token_no_se_sube_ni_sale_en_errores(tmp_path, remoto):
    cfg = _cfg(tmp_path, remoto)
    d = Path(cfg["carpeta"])
    (d / "subir_github").mkdir()
    (d / "subir_github" / "config.json").write_text('{"token": "SECRETO"}')
    (d / "uno.txt").write_text("1")
    S.subir(cfg, "x", lambda _: None)
    assert _git(remoto, "ls-tree", "-r", "--name-only", "main").split() == ["uno.txt"]
    with pytest.raises(S.Error) as e:
        S.subir({**cfg, "repo": str(tmp_path / "no_existe.git")}, "x", lambda _: None)
    assert "SECRETO" not in str(e.value)


@hay_git
def test_archivos_grandes_y_probar(tmp_path, monkeypatch, remoto):
    cfg, lineas = _cfg(tmp_path, remoto), []
    S.probar(cfg, lineas.append)
    assert "repositorio vacio" in lineas[0]
    monkeypatch.setattr(S, "GRANDE_MB", 0)
    (Path(cfg["carpeta"]) / "tres.txt").write_text("3")
    with pytest.raises(S.Error, match="MB"):
        S.subir(cfg, "grande", lineas.append)
    assert _git(cfg["carpeta"], "diff", "--cached", "--name-only") == ""   # no deja nada preparado


def test_config_migra_formato_viejo_elige_por_defecto_y_arma_lo_elegido(tmp_path, monkeypatch):
    monkeypatch.setattr(S, "CONFIG", tmp_path / "config.json")
    assert S.leer()["actual"] == {"usuario": "", "repo": "", "carpeta": str(S.AQUI.parent), "rama": ""}   # sin archivo: todo por defecto
    S.CONFIG.write_text('{"usuario": "ana", "token": "T", "repo": "https://github.com/a/b", "rama": "dev", "carpeta": "/x"}')
    c = S.leer()   # formato anterior (un solo usuario)
    assert c["usuarios"] == [{"usuario": "ana", "token": "T"}] and c["repos"] == ["https://github.com/a/b"] and c["actual"]["rama"] == "dev"
    c["usuarios"].append({"usuario": "beto", "token": "T2"})
    c["actual"]["usuario"] = "beto"
    S.guardar(c)
    assert S.plano(S.leer()) == {"usuario": "beto", "token": "T2", "repo": "https://github.com/a/b", "rama": "dev", "carpeta": "/x"}
    c["usuarios"] = c["usuarios"][:1]   # se quito el elegido: pasa al primero de la lista
    S.guardar(c)
    assert S.leer()["actual"]["usuario"] == "ana"


@hay_git
def test_ramas_vienen_de_github_con_la_predeterminada_primero(tmp_path, remoto):
    cfg = _cfg(tmp_path, remoto)
    assert S.ramas_github({**cfg, "rama": ""}) == ([], "")   # repositorio vacio
    d = Path(cfg["carpeta"])
    (d / "a.txt").write_text("1")
    for rama in ("zeta", "main", "dev"):
        S.subir({**cfg, "rama": rama}, "x", lambda _: None)
    subprocess.run(["git", "symbolic-ref", "HEAD", "refs/heads/main"], cwd=remoto, check=True)
    assert S.ramas_github({**cfg, "rama": ""}) == (["main", "dev", "zeta"], "main")   # predeterminada primero, resto como GitHub
    with pytest.raises(S.Error, match="Elige una rama"):
        S.subir({**cfg, "rama": ""}, "x", lambda _: None)
