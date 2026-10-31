# Parametros (`parameters/config.json`)

Cada seccion de `parameters/config.json` y los modulos que la leen con `params("seccion")`. La decision que la origina esta en `docs/decisiones/`.

| Seccion | Usada en |
|---|---|
| `base_clip` | `src/evaluacion/base_clip.py` |
| `construccion` | `src/preparacion/etapas.py`, `src/preparacion/tabla.py` |
| `cortes` | `src/etiquetado/cortes.py` |
| `ejercicios` | `src/interfaz/api/sistema.py` |
| `entrenamiento` | `src/entrenamiento/datos.py`, `src/entrenamiento/entrenar.py`, `src/entrenamiento/modelos.py` |
| `formato` | `src/preparacion/tabla.py`, `src/procesamiento/medidas/features.py`, `src/procesamiento/puntos/normalizacion.py` |
| `limpieza` | `src/preparacion/etapas.py`, `src/preparacion/tabla.py` |
| `seleccion` | `src/entrenamiento/datos.py`, `src/preparacion/etapas.py`, `src/preparacion/tabla.py` |
