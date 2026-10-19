# Parametros (`params.yaml`)

Cada seccion de `params.yaml` y los modulos que la leen con `params("seccion")`. La decision que la origina esta en `docs/decisiones/`.

| Seccion | Usada en |
|---|---|
| `base_clip` | `src/evaluacion/base_clip.py` |
| `construccion` | `src/preparacion/etapas.py`, `src/preparacion/tabla.py` |
| `ejercicios` | `src/interfaz/api/sistema.py` |
| `entrenamiento` | `src/entrenamiento/datos.py`, `src/entrenamiento/entrenar.py`, `src/entrenamiento/modelos.py` |
| `formato` | `scripts/generar_docs_codigo.py`, `src/etiquetado/tablas.py`, `src/nucleo/config.py`, `src/preparacion/tabla.py`, `src/procesamiento/medidas/features.py`, `src/procesamiento/puntos/normalizacion.py` |
| `limpieza` | `src/preparacion/etapas.py`, `src/preparacion/tabla.py` |
| `seleccion` | `src/entrenamiento/datos.py`, `src/preparacion/etapas.py`, `src/preparacion/tabla.py` |
