# 0001 · Datos en disco como fuente de verdad; SQL Server como respaldo

- **Estado:** aceptada · **Etapa CRISP-DM:** 3.1 Seleccionar · **Issue:** #pendiente
- **Contexto:** la tabla de entrenamiento se leia de SQL Server (`table_frames_fix`), fuera del control de versiones. Un dato que cambia en SQL no deja rastro y nadie puede reproducir un modelo.
- **Decision:** los clips (`datos/clips/*.npz`), `manifest.json` y `etiquetas.json` en disco son la fuente. El entrenamiento y las 5 etapas leen del disco. SQL se llena como **respaldo** (y para Descomposicion/Ranking, que aun lo consultan).
- **Respaldo:** dos interruptores en Sistema → «Datos en disco · respaldo en SQL Server»: `al_cortar` (tras cortar clips) y `al_entrenar` (tras cada entrenamiento), mas el boton «Respaldar ahora». Viven en `datos/config.json` → `respaldo_sql`. Un fallo de SQL **no** interrumpe el entrenamiento: queda en `meta.respaldo_sql.error`.
- **Excepcion consciente:** `fuente_entrenamiento = "sql"` en ajustes vuelve al camino antiguo (comparar ambos).
- **Parametro:** `seleccion.excluir_clases` (params.yaml) · **Codigo:** `src/preparacion/tabla.py`, `src/entrenamiento/entrenar.py`, `src/etiquetado/tablas.py::respaldar_sql`, `src/etiquetado/exportar.py`.
- **Salida / metrica:** `datos/intermedio/<ej>/seleccion.json`, `reportes/seleccion_<ej>.json`.
