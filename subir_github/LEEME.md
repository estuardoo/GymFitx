# subir_github

Sube el código actual de GYMFITX a GitHub. No es parte de la app.

1. Doble clic en `SUBIR_GITHUB.bat` (necesita Python 3.9+ con tkinter y git).
2. **⚙ (rueda, arriba a la derecha)** abre la configuración (`configuracion.py`): pestañas **Usuarios** (cada uno con su token fine-grained, *Contents: Read and write*), **Repositorios** y **Carpetas**, con ➕ Agregar / 🔑 Cambiar token / 🗑 Quitar. Todo se guarda solo en `config.json`.
3. En la ventana principal eliges **Usuario**, **Repositorio** y **Carpeta** de las listas (el primero de cada lista es el predeterminado).
4. **Rama**: se carga sola desde GitHub al elegir usuario y repositorio, **tal como vienen** (la predeterminada primero y elegida). Puedes escribir otro nombre para crear una rama nueva.
5. **🔌 Probar conexión** se pone **verde** si usuario/token/repositorio sirven, **rojo** si no (el log dice por qué). Se apaga al cambiar cualquier dato.
6. **⬆ Subir código actual**. El cuadro de abajo muestra cada paso con hora (✔ bien, ✘ falló); también queda en `subir_github.log`.

Los tokens se guardan solo en `config.json` (ignorado por git y excluido de todo commit). `datos/`, `modelos/` y `herramientas/` no se suben.
