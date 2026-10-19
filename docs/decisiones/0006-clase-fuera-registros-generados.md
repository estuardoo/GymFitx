# 0006 · Clase «fuera»: registros generados (no medidos)

- **Estado:** aceptada · **Etapa:** 3.3 Construir · **Issue:** #7
- **Contexto:** en vivo el sistema ve ventanas donde no hay ciclo (quieto, caminando). Sin ejemplos de «fuera» el modelo siempre responde bien o mal.
- **Decision:** se generan ventanas deslizantes de las grabaciones crudas que no se solapen (IoU ≤ `iou_max`) con ningun corte bien/mal/base. Son datos sinteticos por construccion y por eso estan marcadas (`meta.json` de `construido/`) y reportadas aparte.
- **Parametro:** `construccion.fuera.{incluir, paso, iou_max, min_cuadros}`.
- **Codigo:** `src/preparacion/tabla.py::ventanas_crudas`, `ventanas_fuera`; `src/preparacion/etapas.py::construir`.
- **Salida:** `datos/intermedio/<ej>/construido/`.
