"""Publicar el panel en internet con un tunel de Cloudflare (boton del panel).

NO se activa solo: el panel arranca siempre local (127.0.0.1). Desde la
pestana Sistema -> "Publicar en internet" se prende/apaga el tunel.

- Tunel: Cloudflare "quick tunnel" (gratis, sin cuenta). Da un enlace
  https://<algo>.trycloudflare.com que cambia cada vez que se prende.
  cloudflared se busca en el PATH o en herramientas/; si no esta se descarga
  solo a herramientas/ (Windows).
- Login (HTTP Basic): se exige SOLO a lo que llega por el tunel (Cloudflare
  agrega la cabecera cf-connecting-ip). Desde esta PC se entra sin clave.
  Credenciales en datos/acceso.json (solo el hash, nunca la clave en texto).
- Por el tunel NUNCA se permiten /api/system/* ni /api/publicar/* (apagar,
  reinstalar librerias, cambiar Python, apagar el tunel): solo desde la PC.

"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import re
import secrets
import shutil
import subprocess
import threading
import urllib.request
from pathlib import Path

from src.nucleo.config import ACCESO_PATH, HERRAMIENTAS_DIR

ACCESO = ACCESO_PATH
CLOUDFLARED_URL = ("https://github.com/cloudflare/cloudflared/releases/latest/download/"
                   "cloudflared-windows-amd64.exe")
REALM = "GYMFITX"
RUTAS_SOLO_LOCAL = ("/api/system/", "/api/publicar/")

_lock = threading.Lock()
_proc: subprocess.Popen | None = None
ESTADO: dict = {"activo": False, "url": None, "error": None, "con_clave": True, "iniciando": False}


# --- credenciales -----------------------------------------------------------

def _archivo() -> Path:
    return ACCESO


def _hash(clave: str, sal: str) -> str:
    return hashlib.pbkdf2_hmac("sha256", clave.encode(), bytes.fromhex(sal), 200_000).hex()


def fijar_clave(clave: str, usuario: str = "gymfitx") -> None:
    sal = secrets.token_hex(16)
    ACCESO.write_text(json.dumps({"usuario": usuario, "sal": sal, "hash": _hash(clave, sal)},
                                 indent=1), "utf-8")
    _validos.clear()


def nueva_clave(usuario: str | None = None) -> dict:
    """Genera una clave aleatoria, la guarda (hash) y la devuelve UNA vez."""
    usuario = usuario or (credenciales() or {}).get("usuario") or "gymfitx"
    clave = secrets.token_urlsafe(9)
    fijar_clave(clave, usuario)
    return {"usuario": usuario, "clave": clave}


def credenciales() -> dict | None:
    p = _archivo()
    try:
        return json.loads(p.read_text("utf-8")) if p.exists() else None
    except Exception:
        return None


_validos: set[str] = set()   # Authorization ya verificadas (pbkdf2 es lento a proposito)


def credencial_valida(cabecera: str) -> bool:
    datos = credenciales()
    if not datos:
        return False
    llave = hashlib.sha256((cabecera + datos["hash"]).encode()).hexdigest()
    if llave in _validos:
        return True
    m = re.match(r"Basic\s+(.+)", cabecera or "")
    if not m:
        return False
    try:
        usuario, _, clave = base64.b64decode(m.group(1)).decode("utf-8").partition(":")
    except Exception:
        return False
    ok = (hmac.compare_digest(usuario, datos["usuario"])
          and hmac.compare_digest(_hash(clave, datos["sal"]), datos["hash"]))
    if ok:
        _validos.add(llave)
    return ok


def viene_del_tunel(headers: dict[str, str], cliente: str | None) -> bool:
    if cliente not in (None, "127.0.0.1", "::1", "testclient"):
        return True
    return bool(headers.get("cf-connecting-ip") or headers.get("cf-ray")
                or headers.get("x-forwarded-for"))


# --- middleware ASGI (http + websocket) -------------------------------------

class ProteccionTunel:
    """Pide usuario/clave a lo que llega por el tunel y bloquea las rutas de
    sistema desde afuera. Lo local pasa sin tocar."""

    def __init__(self, app) -> None:
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] not in ("http", "websocket"):
            return await self.app(scope, receive, send)
        headers = {k.decode("latin-1").lower(): v.decode("latin-1") for k, v in scope.get("headers", [])}
        cliente = (scope.get("client") or (None,))[0]
        if not viene_del_tunel(headers, cliente):
            return await self.app(scope, receive, send)

        ruta = scope.get("path", "")
        if any(ruta.startswith(r) for r in RUTAS_SOLO_LOCAL):
            return await _responder(scope, send, 403, "Solo disponible desde la PC del panel")
        if ESTADO["con_clave"] and not credencial_valida(headers.get("authorization", "")):
            return await _responder(scope, send, 401, "Se requiere usuario y clave",
                                    [(b"www-authenticate", f'Basic realm="{REALM}", charset="UTF-8"'.encode())])
        return await self.app(scope, receive, send)


async def _responder(scope, send, codigo: int, texto: str, extra=()):
    if scope["type"] == "websocket":
        await send({"type": "websocket.close", "code": 1008})
        return
    cuerpo = texto.encode()
    await send({"type": "http.response.start", "status": codigo,
                "headers": [(b"content-type", b"text/plain; charset=utf-8"),
                            (b"content-length", str(len(cuerpo)).encode()), *extra]})
    await send({"type": "http.response.body", "body": cuerpo})


# --- tunel ------------------------------------------------------------------

def cloudflared() -> str:
    exe = shutil.which("cloudflared")
    if exe:
        return exe
    nombre = "cloudflared.exe" if os.name == "nt" else "cloudflared"
    local = HERRAMIENTAS_DIR / nombre
    if local.exists() and local.stat().st_size > 0:
        return str(local)
    if os.name != "nt":
        raise RuntimeError("Instala cloudflared (https://developers.cloudflare.com/cloudflare-one/"
                           "connections/connect-networks/downloads/)")
    HERRAMIENTAS_DIR.mkdir(exist_ok=True)
    tmp = local.with_suffix(".part")
    urllib.request.urlretrieve(CLOUDFLARED_URL, tmp)
    tmp.replace(local)
    return str(local)


def estado() -> dict:
    datos = credenciales() or {}
    publico = {k: v for k, v in ESTADO.items() if not k.startswith("_")}
    return {**publico, "usuario": datos.get("usuario"), "tiene_clave": bool(datos)}


def iniciar(puerto: int, con_clave: bool = True, log=None) -> dict:
    """Prende el tunel en segundo plano. La URL aparece en estado() apenas
    Cloudflare la asigna (unos segundos). Si se pide clave y todavia no hay
    credenciales, se crean y se devuelven UNA vez en 'nueva_clave'."""
    global _proc
    with _lock:
        if (_proc is not None and _proc.poll() is None) or ESTADO["iniciando"]:
            ESTADO["con_clave"] = con_clave     # ya corre (o arrancando): solo cambia la clave
            return estado()
        ESTADO.update(activo=False, url=None, error=None, con_clave=con_clave, iniciando=True)
    extra = {}
    if con_clave and not credenciales():
        extra["nueva_clave"] = nueva_clave()

    def correr():
        global _proc
        try:
            exe = cloudflared()
        except Exception as e:
            ESTADO.update(error=f"No se pudo obtener cloudflared: {e}", iniciando=False)
            if log:
                log.error(ESTADO["error"])
            return
        flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        proc = subprocess.Popen(
            [exe, "tunnel", "--no-autoupdate", "--url", f"http://127.0.0.1:{puerto}"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8",
            errors="replace", creationflags=flags)
        with _lock:
            _proc = proc
        ESTADO.update(activo=True)
        import atexit
        atexit.register(proc.terminate)   # si el panel se cierra, el tunel no queda huerfano
        for linea in proc.stdout:
            m = re.search(r"https://(?!api\.)[a-z0-9-]+\.trycloudflare\.com", linea)
            if m and not ESTADO["url"]:
                ESTADO.update(url=m.group(0), iniciando=False)
                if log:
                    log.info("enlace publico: %s (%s)", ESTADO["url"],
                             "con usuario/clave" if ESTADO["con_clave"] else "SIN clave")
        codigo = proc.wait()
        with _lock:
            if _proc is proc:
                _proc = None
        detenido = ESTADO.get("_detenido")
        ESTADO.update(activo=False, url=None, iniciando=False, _detenido=False,
                      error=None if detenido else f"cloudflared termino (codigo {codigo})")

    threading.Thread(target=correr, daemon=True, name="cloudflared").start()
    return {**estado(), **extra}


def detener() -> dict:
    global _proc
    with _lock:
        proc = _proc
    if proc is not None and proc.poll() is None:
        ESTADO["_detenido"] = True
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
    ESTADO.update(activo=False, url=None, iniciando=False)
    return estado()
