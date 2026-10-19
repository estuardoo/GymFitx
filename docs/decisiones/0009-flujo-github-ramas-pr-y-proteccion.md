# 0009 · Flujo de colaboracion en GitHub

- **Estado:** aceptada (la proteccion de rama la activa el administrador del repo) · **Etapa:** criterio 7 · **Issue:** #10
- **Decision:** issue → rama → commits con `Refs #N` → Pull Request con `Closes #N` → revision → merge. La rama principal protegida (PR obligatorio, 1 aprobacion). Una etiqueta `datos-vN` por version del conjunto. Cada integrante usa su propio token, nombre y correo.
- **Herramienta aparte:** el envio se hace con el programa independiente `subir_github/SUBIR_GITHUB.bat` (ventana con usuario, token, repositorio, rama y log), no desde el panel del proyecto: asi el token y el flujo de git no forman parte del codigo ni de sus dependencias.
- **Codigo:** `subir_github/subir_github.py` · en el repo: `.github/pull_request_template.md`, `.github/workflows/reproducir.yml`.
- **Verificacion:** boton «Ver proteccion» (`GET /api/github/proteccion`).
