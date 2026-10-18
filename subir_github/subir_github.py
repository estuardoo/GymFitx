"""Subir el codigo actual de GYMFITX a GitHub: ventana pequena con usuario, token, repositorio y rama, y un cuadro de log.

    SUBIR_GITHUB.bat            (o: python subir_github.py)

Solo libreria estandar + git instalado. No forma parte de la app: nada de src/ lo importa. La configuracion (incluido el
token) queda en config.json junto a este archivo, que esta en .gitignore y nunca se sube."""

from __future__ import annotations

import base64
import json
import os
import queue
import re
import subprocess
import threading
from datetime import datetime
from pathlib import Path

AQUI = Path(__file__).resolve().parent
CONFIG, LOG = AQUI / "config.json", AQUI / "subir_github.log"
URL = re.compile(r"^https://github\.com/([\w.\-]+)/([\w.\-]+?)(?:\.git)?/?$")
RAMA = re.compile(r"^[\w][\w./\-]*$")
GRANDE_MB = 50   # GitHub rechaza archivos de 100 MB
# config.json: listas para elegir y lo elegido ("actual"). El token de cada usuario vive aqui y en ningun otro lado.
VACIA = {"usuarios": [], "repos": [], "carpetas": [str(AQUI.parent)], "actual": {}}   # las ramas se leen de GitHub


class Error(Exception):
    """Mensaje listo para el log."""


def leer() -> dict:
    """Lee config.json (y convierte el formato viejo de un solo usuario/repo)."""
    try:
        d = json.loads(CONFIG.read_text("utf-8"))
    except (OSError, ValueError):
        d = {}
    if "usuario" in d:   # formato anterior: usuario, token, repo, rama, carpeta sueltos
        d = {"usuarios": [{"usuario": d["usuario"], "token": d.get("token", "")}] if d["usuario"] else [], "repos": [d["repo"]] if d.get("repo") else [],
             "carpetas": [d["carpeta"]] if d.get("carpeta") else [], "actual": {"rama": d.get("rama", "")}}
    cfg = {k: list(d.get(k) or v) for k, v in VACIA.items() if k != "actual"} | {"actual": dict(d.get("actual") or {})}
    for clave, lista in (("usuario", [u["usuario"] for u in cfg["usuarios"]]), ("repo", cfg["repos"]), ("carpeta", cfg["carpetas"])):
        if cfg["actual"].get(clave) not in lista:   # lo elegido ya no existe: se usa el primero (el "por defecto")
            cfg["actual"][clave] = lista[0] if lista else ""
    cfg["actual"].setdefault("rama", "")   # la rama viene de GitHub; aqui solo se recuerda la ultima
    return cfg


def guardar(cfg: dict) -> None:
    CONFIG.write_text(json.dumps(cfg, indent=1, ensure_ascii=False), "utf-8")


def plano(cfg: dict) -> dict:
    """Lo elegido, listo para subir()/probar(): usuario, token, repo, rama, carpeta."""
    a = cfg["actual"]
    token = next((u["token"] for u in cfg["usuarios"] if u["usuario"] == a["usuario"]), "")
    return {"usuario": a["usuario"], "token": token, "repo": a["repo"], "rama": a["rama"], "carpeta": a["carpeta"]}


def validar(cfg: dict) -> None:
    if not cfg["usuario"].strip():
        raise Error("Falta el usuario.")
    if not cfg["token"].strip():
        raise Error("Falta el token.")
    if not URL.match(cfg["repo"].strip()):
        raise Error("El repositorio debe ser https://github.com/usuario/repo")
    if not cfg["rama"].strip():
        raise Error("Elige una rama (se cargan de GitHub al elegir usuario y repositorio).")
    if not RAMA.match(cfg["rama"].strip()) or ".." in cfg["rama"]:
        raise Error(f"Rama no valida: '{cfg['rama']}'")
    if not Path(cfg["carpeta"]).is_dir():
        raise Error(f"La carpeta no existe: {cfg['carpeta']}")


def _run(args: list[str], cfg: dict, red: bool = False, timeout: int = 300) -> tuple[int, str]:
    auth = base64.b64encode(f"x-access-token:{cfg['token']}".encode()).decode()
    cmd = ["git", *(["-c", f"http.extraheader=Authorization: Basic {auth}"] if red else []), *args]
    try:
        r = subprocess.run(cmd, cwd=cfg["carpeta"], capture_output=True, text=True, timeout=timeout, encoding="utf-8", errors="replace",
                           env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "LC_ALL": "C"},
                           creationflags=0x08000000 if os.name == "nt" else 0)   # sin ventana de consola
    except FileNotFoundError:
        raise Error("git no esta instalado (https://git-scm.com/downloads).") from None
    except subprocess.TimeoutExpired:
        raise Error(f"git {args[0]} tardo mas de {timeout} s (¿sin internet?).") from None
    salida = (r.stdout + r.stderr).strip()
    for secreto in (cfg["token"], auth):
        salida = salida.replace(secreto, "***")
    return r.returncode, salida


def _git(args: list[str], cfg: dict, red: bool = False) -> str:
    rc, out = _run(args, cfg, red)
    if rc:
        raise Error(f"git {args[0]}: {out[-500:]}")
    return out


def ramas_github(cfg: dict) -> tuple[list[str], str]:
    """Ramas del repositorio tal como las devuelve GitHub y cual es la predeterminada -> (ramas, predeterminada). Lee, no cambia nada."""
    validar({**cfg, "rama": cfg["rama"] or "main"})
    rc, out = _run(["ls-remote", "--symref", cfg["repo"].strip(), "HEAD", "refs/heads/*"], cfg, red=True, timeout=60)
    if rc:
        raise Error(f"No se pudo leer el repositorio (¿token, URL o permisos?): {out[-300:]}")
    ramas, defecto = [], ""
    for linea in out.splitlines():
        if linea.startswith("ref: refs/heads/"):
            defecto = linea.split("\t")[0].removeprefix("ref: refs/heads/")
        elif "\trefs/heads/" in linea:
            ramas.append(linea.split("\trefs/heads/", 1)[1])
    if defecto in ramas:   # la predeterminada primero; el resto en el orden de GitHub
        ramas.remove(defecto)
        ramas.insert(0, defecto)
    return ramas, defecto


def probar(cfg: dict, log) -> list[str]:
    """¿El token y la ruta del repositorio sirven? Devuelve las ramas de GitHub."""
    ramas, defecto = ramas_github(cfg)
    log(f"✔ Conexion correcta ({cfg['usuario']} → {cfg['repo']}). Ramas: {', '.join(ramas) or '(repositorio vacio)'}"
        + (f" · predeterminada: {defecto}" if defecto else ""))
    return ramas


def subir(cfg: dict, mensaje: str, log) -> None:
    """init (si hace falta) -> rama -> add -A -> commit -> push. Si no hay cambios, solo empuja lo pendiente."""
    validar(cfg)
    rama, repo, usuario = cfg["rama"].strip(), cfg["repo"].strip(), cfg["usuario"].strip()
    mensaje = mensaje.strip() or f"Actualizacion {datetime.now():%Y-%m-%d %H:%M}"
    if not (Path(cfg["carpeta"]) / ".git").exists():
        _git(["init"], cfg)
        _git(["symbolic-ref", "HEAD", f"refs/heads/{rama}"], cfg)
        log("• Repositorio git iniciado en la carpeta")
    remotos = _git(["remote"], cfg).split()
    _git(["remote", "set-url" if "origin" in remotos else "add", "origin", repo], cfg)
    _git(["config", "user.name", usuario], cfg)
    _git(["config", "user.email", f"{usuario}@users.noreply.github.com"], cfg)

    rc, out = _run(["fetch", "origin"], cfg, red=True)   # para conocer las ramas de GitHub
    if rc:
        raise Error(f"No se pudo leer GitHub (¿token o URL?): {out[-400:]}")
    if _run(["rev-parse", "--verify", "-q", "HEAD"], cfg)[0]:   # aun sin commits: se parte de lo que ya hay en GitHub
        for origen in (f"origin/{rama}", "origin/HEAD", "origin/main", "origin/master"):
            if _run(["rev-parse", "--verify", "-q", origen], cfg)[0] == 0:
                _git(["reset", "--mixed", origen], cfg)   # el historial remoto queda de base; tus archivos no se tocan
                log(f"• Historial traido de {origen}")
                break
    actual = _run(["symbolic-ref", "--short", "HEAD"], cfg)[1]
    if actual != rama:
        local = _run(["show-ref", "--verify", "--quiet", f"refs/heads/{rama}"], cfg)[0] == 0
        remota = _run(["show-ref", "--verify", "--quiet", f"refs/remotes/origin/{rama}"], cfg)[0] == 0
        _git(["checkout", rama] if local else ["checkout", "-b", rama, "--track", f"origin/{rama}"] if remota else ["checkout", "-b", rama], cfg)
        log(f"• Rama {rama}")

    _git(["add", "-A"], cfg)
    _run(["reset", "-q", "--", "subir_github/config.json"], cfg)   # el token nunca entra a un commit
    nombres = _git(["diff", "--cached", "--name-only", "-z"], cfg).split("\0")
    grandes = [n for n in nombres if n and (Path(cfg["carpeta"]) / n).is_file() and (Path(cfg["carpeta"]) / n).stat().st_size > GRANDE_MB * 2**20]
    if grandes:
        _git(["reset", "-q"], cfg)
        raise Error(f"Archivos de mas de {GRANDE_MB} MB (GitHub no los acepta): {', '.join(grandes[:5])}. Agregalos a .gitignore.")
    if _run(["diff", "--cached", "--quiet"], cfg)[0]:
        _git(["commit", "-m", mensaje], cfg)
        log(f"• Commit {_git(['rev-parse', '--short', 'HEAD'], cfg)} · {len([n for n in nombres if n])} archivo(s)")
    else:
        log("• Sin cambios nuevos")
    rc, out = _run(["push", "-u", "origin", f"HEAD:refs/heads/{rama}"], cfg, red=True)
    if rc:
        hint = " La rama tiene commits que no tienes aqui: usa otra rama." if "rejected" in out else (
            " Sin permiso para esa rama (¿protegida?): usa otra rama." if "protected" in out.lower() or "denied" in out.lower() else "")
        raise Error(f"git push: {out[-400:]}{hint}")
    log(f"✔ Enviado a {rama}: {repo.removesuffix('.git').rstrip('/')}/tree/{rama}")


def ventana() -> None:
    import tkinter as tk
    from tkinter import ttk

    import configuracion

    raiz = tk.Tk()
    raiz.title("Subir a GitHub · GYMFITX")
    raiz.minsize(640, 500)
    datos, cola, combos = leer(), queue.Queue(), {}
    marco = ttk.Frame(raiz, padding=10)
    marco.pack(fill="both", expand=True)
    marco.columnconfigure(1, weight=1)

    def log(txt: str) -> None:
        linea = f"{datetime.now():%H:%M:%S}  {txt}"
        cola.put(linea)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(linea + "\n")

    def vaciar() -> None:   # solo el hilo principal toca la ventana; el trabajo le deja funciones en la cola
        while not cola.empty():
            x = cola.get()
            if callable(x):
                x()
                continue
            cuadro.configure(state="normal")
            cuadro.insert("end", x + "\n")
            cuadro.see("end")
            cuadro.configure(state="disabled")
        raiz.after(150, vaciar)

    def sin_color() -> None:   # al cambiar cualquier dato, la prueba anterior ya no vale
        probar_btn.configure(bg=NEUTRO, fg="black", text="🔌 Probar conexion")

    def guardar_eleccion() -> None:
        for clave, combo in combos.items():
            if combo.get().strip() != "cargando…":
                datos["actual"][clave] = combo.get().strip()
        guardar(datos)

    def pintar() -> None:
        listas = {"usuario": [u["usuario"] for u in datos["usuarios"]], "repo": datos["repos"], "carpeta": datos["carpetas"]}
        for clave, valores in listas.items():
            combos[clave]["values"] = valores
            combos[clave].set(datos["actual"].get(clave, ""))
        cargar_ramas()

    def cargar_ramas() -> None:
        """Las ramas salen de GitHub (la predeterminada primero y elegida); se puede escribir otra para crearla."""
        combos["rama"]["values"] = []
        cfg_ = plano(datos)
        if not (cfg_["usuario"] and cfg_["token"] and cfg_["repo"]):
            return combos["rama"].set("")
        combos["rama"].set("cargando…")

        def tarea() -> None:
            try:
                ramas, defecto = ramas_github({**cfg_, "rama": "main"})
            except Error as e:
                log(f"✘ {e}")
                return en_ventana(lambda: combos["rama"].set(""))
            def aplicar() -> None:
                if plano(datos)["usuario"] != cfg_["usuario"] or plano(datos)["repo"] != cfg_["repo"]:
                    return   # mientras cargaba, cambiaron de usuario o repositorio
                combos["rama"]["values"] = ramas
                recordada = datos["actual"].get("rama")
                combos["rama"].set(recordada if recordada in ramas else (defecto or (ramas[0] if ramas else "")))
                guardar_eleccion()
            en_ventana(aplicar)
        threading.Thread(target=tarea, daemon=True).start()

    def en_ventana(f) -> None:
        cola.put(f)

    def cambio(clave: str) -> None:
        guardar_eleccion()
        sin_color()
        if clave in ("usuario", "repo"):
            datos["actual"]["rama"] = ""
            cargar_ramas()

    # --- filas: etiqueta | lista | (rueda de configuracion arriba a la derecha)
    for fila, (clave, etiqueta, editable) in enumerate((("usuario", "Usuario", False), ("repo", "Repositorio", False),
                                                         ("rama", "Rama (linea de envio)", True), ("carpeta", "Carpeta del codigo", False))):
        ttk.Label(marco, text=etiqueta).grid(row=fila, column=0, sticky="w", pady=3)
        combo = ttk.Combobox(marco, state="normal" if editable else "readonly", width=52)
        combo.grid(row=fila, column=1, sticky="we", padx=6)
        combo.bind("<<ComboboxSelected>>", lambda _e, c=clave: cambio(c))
        combos[clave] = combo
    combos["rama"].bind("<FocusOut>", lambda _e: (guardar_eleccion(), sin_color()))
    ttk.Button(marco, text="⚙", width=3, command=lambda: configuracion.abrir(raiz, datos, lambda: guardar(datos), pintar, lambda u: bool(URL.match(u)))
               ).grid(row=0, column=2, sticky="e")
    ttk.Label(marco, text="Mensaje").grid(row=4, column=0, sticky="w", pady=3)
    mensaje = tk.StringVar()
    ttk.Entry(marco, textvariable=mensaje).grid(row=4, column=1, columnspan=2, sticky="we", padx=6)

    def al_probar() -> None:
        guardar_eleccion()
        cfg_ = plano(datos)
        probar_btn.configure(bg="#e0b400", fg="black", text="🔌 Probando…")

        def tarea() -> None:
            try:
                probar(cfg_, log)
                en_ventana(lambda: probar_btn.configure(bg="#2e9e4f", fg="white", text="✔ Conexion valida"))
            except Error as e:
                log(f"✘ {e}")
                en_ventana(lambda: probar_btn.configure(bg="#c93c3c", fg="white", text="✘ Conexion invalida"))
            except Exception as e:   # noqa: BLE001 - el log debe mostrar cualquier fallo
                log(f"✘ {type(e).__name__}: {e}")
                en_ventana(lambda: probar_btn.configure(bg="#c93c3c", fg="white", text="✘ Conexion invalida"))
        threading.Thread(target=tarea, daemon=True).start()

    def al_subir() -> None:
        guardar_eleccion()
        cfg_, msg = plano(datos), mensaje.get()
        log("Subiendo…")
        subir_btn.configure(state="disabled")

        def tarea() -> None:
            try:
                subir(cfg_, msg, log)
            except Error as e:
                log(f"✘ {e}")
            except Exception as e:   # noqa: BLE001
                log(f"✘ {type(e).__name__}: {e}")
            finally:
                en_ventana(lambda: subir_btn.configure(state="normal"))
        threading.Thread(target=tarea, daemon=True).start()

    barra = ttk.Frame(marco)
    barra.grid(row=5, column=0, columnspan=3, sticky="w", pady=8)
    probar_btn = tk.Button(barra, text="🔌 Probar conexion", command=al_probar, padx=8)
    probar_btn.pack(side="left", padx=(0, 6))
    NEUTRO = probar_btn.cget("bg")
    subir_btn = tk.Button(barra, text="⬆ Subir codigo actual", command=al_subir, padx=8)
    subir_btn.pack(side="left")

    cuadro = tk.Text(marco, height=12, state="disabled", wrap="word", font=("Consolas", 9))
    cuadro.grid(row=6, column=0, columnspan=3, sticky="nsew")
    marco.rowconfigure(6, weight=1)
    pintar()
    if not datos["usuarios"] or not datos["repos"]:
        log("Primera vez: pulsa ⚙ y agrega tu usuario (con su token) y el repositorio.")
    vaciar()
    raiz.mainloop()


if __name__ == "__main__":
    ventana()
