# 0004 · Reglas de postura en la definición del ejercicio

- **Estado:** aceptada · **Etapa:** 3.3 Construir (angulos/proporciones) · **Issue:** #5
- **Contexto:** los angulos y proporciones que se calculan como features y las reglas de evaluacion dependen del ejercicio y cambian con frecuencia.
- **Decision:** viven en `parameters/<n>/guide.json`, no en el codigo. Agregar o cambiar una regla se hace desde el panel (queda en el diff).
- **Parametro:** `parameters/<n>/guide.json` (fuera de config.json: es definicion del ejercicio, no umbral del pipeline).
- **Codigo:** `src/evaluacion/`, `src/procesamiento/puntos/vectorizar.py` (columnas `a` y `p`).
- **Salida:** `docs/diccionario/<ej>.csv` lista cada columna con su origen.
