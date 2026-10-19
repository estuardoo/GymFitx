# 0004 · Reglas de postura en YAML por ejercicio

- **Estado:** aceptada · **Etapa:** 3.3 Construir (angulos/proporciones) · **Issue:** #5
- **Contexto:** los angulos y proporciones que se calculan como features y las reglas de evaluacion dependen del ejercicio y cambian con frecuencia.
- **Decision:** viven en `ejercicios/*.yaml`, no en el codigo. Agregar o cambiar una regla es editar un YAML (queda en el diff).
- **Parametro:** `ejercicios/<ej>.yaml` (fuera de params.yaml: es definicion del ejercicio, no umbral del pipeline).
- **Codigo:** `src/evaluacion/`, `src/procesamiento/puntos/vectorizar.py` (columnas `a` y `p`).
- **Salida:** `docs/diccionario/<ej>.csv` lista cada columna con su origen.
