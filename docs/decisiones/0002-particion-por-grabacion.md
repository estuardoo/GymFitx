# 0002 · Particion de validacion por grabacion (sin fuga)

- **Estado:** aceptada · **Etapa:** 3.5 Formatear / entrenamiento · **Issue:** #pendiente
- **Contexto:** los ciclos de una misma grabacion son casi identicos; partirlos al azar entre train y test infla el accuracy (fuga). La guia CRISP-DM lo marca como antipatron.
- **Decision:** el grupo es la grabacion (`grupo_de`, quita el sufijo `_copy`/`_N` de la copia). Validacion cruzada con `StratifiedGroupKFold`: ninguna grabacion queda en train y test a la vez. La busqueda de features (`scripts/busqueda_features_slurm.py`) usa lo mismo.
- **Pendiente de confirmar:** si el prefijo numerico del nombre es el ID de la persona, el grupo deberia ser la persona.
- **Parametro:** `entrenamiento.test_pct`, `entrenamiento.semilla`, `entrenamiento.min_muestras`.
- **Codigo:** `src/entrenamiento/validacion.py` (`PorGrabacion`, `cv_anidada`), `src/preparacion/tabla.py::grupo_de`, `src/entrenamiento/modelos.py::SEMILLA`.
- **Metrica:** `meta.validacion` y `meta.grabaciones` del modelo; test `tests/test_fuga.py`.
