"""Ventana de configuracion (⚙) de subir_github: usuarios con su token, repositorios y carpetas. Cada cambio se guarda al instante.
Las ramas NO se configuran aqui: se leen de GitHub tal como vienen."""

from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk


def abrir(raiz, datos: dict, guardar, al_cambiar, url_valida) -> None:
    """datos = la config (se modifica); guardar() la escribe; al_cambiar() refresca la ventana principal; url_valida(str) -> bool."""
    v = tk.Toplevel(raiz)
    v.title("Configuracion · subir_github")
    v.transient(raiz)
    v.minsize(520, 300)
    libro = ttk.Notebook(v)
    libro.pack(fill="both", expand=True, padx=8, pady=8)
    listas = {}

    def nombres(clave: str) -> list[str]:
        return [u["usuario"] for u in datos["usuarios"]] if clave == "usuarios" else datos[clave]

    def pintar() -> None:
        for clave, lb in listas.items():
            lb.delete(0, "end")
            for n in nombres(clave):
                lb.insert("end", n + ("   (token guardado)" if clave == "usuarios" else ""))

    def listo() -> None:
        guardar()
        pintar()
        al_cambiar()

    def agregar(clave: str, cambiar_token: bool = False) -> None:
        if clave == "usuarios":
            if cambiar_token:
                sel = listas[clave].curselection()
                if not sel:
                    return
                usuario = nombres(clave)[sel[0]]
            else:
                usuario = (simpledialog.askstring("Usuario", "Usuario de GitHub:", parent=v) or "").strip()
            token = (simpledialog.askstring("Token", f"Token de {usuario}:" if usuario else "", show="•", parent=v) or "").strip() if usuario else ""
            if not (usuario and token):
                return
            datos["usuarios"] = [u for u in datos["usuarios"] if u["usuario"] != usuario] + [{"usuario": usuario, "token": token}]
            datos["actual"]["usuario"] = usuario
        elif clave == "carpetas":
            valor = (filedialog.askdirectory(parent=v, title="Carpeta del codigo") or "").strip()
            if not valor:
                return
            if valor not in datos["carpetas"]:
                datos["carpetas"].append(valor)
            datos["actual"]["carpeta"] = valor
        else:
            valor = (simpledialog.askstring("Repositorio", "URL (https://github.com/usuario/repo):", parent=v) or "").strip()
            if not valor:
                return
            if not url_valida(valor):
                return messagebox.showerror("Repositorio", "Debe ser https://github.com/usuario/repo", parent=v)
            if valor not in datos["repos"]:
                datos["repos"].append(valor)
            datos["actual"]["repo"] = valor
        listo()

    def quitar(clave: str) -> None:
        sel = listas[clave].curselection()
        if not sel:
            return
        valor = nombres(clave)[sel[0]]
        if not messagebox.askyesno("Quitar", f"¿Quitar «{valor}»?", parent=v):
            return
        if clave == "usuarios":
            datos["usuarios"] = [u for u in datos["usuarios"] if u["usuario"] != valor]
        else:
            datos[clave].remove(valor)
        listo()

    for clave, titulo, nota in (("usuarios", "Usuarios", "Cada usuario con su propio token (fine-grained, Contents: Read and write)."),
                                ("repos", "Repositorios", "El primero es el predeterminado."),
                                ("carpetas", "Carpetas", "Carpetas con el codigo a subir.")):
        pagina = ttk.Frame(libro, padding=8)
        libro.add(pagina, text=titulo)
        ttk.Label(pagina, text=nota, foreground="gray").pack(anchor="w")
        cuerpo = ttk.Frame(pagina)
        cuerpo.pack(fill="both", expand=True, pady=6)
        lb = tk.Listbox(cuerpo, height=8, exportselection=False)
        lb.pack(side="left", fill="both", expand=True)
        listas[clave] = lb
        botones = ttk.Frame(cuerpo)
        botones.pack(side="left", padx=6, anchor="n")
        ttk.Button(botones, text="➕ Agregar", command=lambda c=clave: agregar(c)).pack(fill="x", pady=1)
        if clave == "usuarios":
            ttk.Button(botones, text="🔑 Cambiar token", command=lambda c=clave: agregar(c, True)).pack(fill="x", pady=1)
        ttk.Button(botones, text="🗑 Quitar", command=lambda c=clave: quitar(c)).pack(fill="x", pady=1)
    ttk.Button(v, text="Cerrar", command=v.destroy).pack(pady=(0, 8))
    pintar()
