# 0008 · Documentacion del codigo generada desde el codigo

- **Estado:** aceptada · **Etapa:** transversal · **Issue:** #pendiente
- **Contexto:** documentacion escrita a mano se desactualiza.
- **Decision:** `docs/codigo/` se **genera** (`python scripts/generar_docs_codigo.py`) leyendo docstrings, firmas, imports y rutas; sin fechas, asi que los mismos fuentes dan los mismos bytes. El CI corre `--revisar` y falla si esta vieja. En DVC es la etapa `documentar_codigo`. Lo que explica el *por que* se escribe a mano en `docs/decisiones/`.
- **Codigo:** `scripts/generar_docs_codigo.py`, `tests/test_trazabilidad.py`.
