# 0007 · Formato del vector de entrada

- **Estado:** aceptada · **Etapa:** 3.5 Formatear · **Issue:** #pendiente
- **Contexto:** los modelos clasicos necesitan un vector plano de largo fijo.
- **Decision:** normalizacion espacial «rectangulo» (caja 100×100), 30 cuadros por ciclo (remuestreo), componentes `xyzap`. Por cuadro: ejes de cada kpoint (punto a punto) y luego las metricas enmascaradas; zancada = 30 × 44 = 1320 columnas. Misma funcion en entrenamiento y en vivo (`vector_de_prep`) para que no diverjan.
- **Parametro:** `formato.{modo, n_frames_fijo, componentes}` (con override por ejercicio en `formato.por_ejercicio`).
- **Codigo:** `src/procesamiento/puntos/vectorizar.py`, `src/nucleo/config.py::formato_de`, `src/preparacion/etapas.py::formatear`.
- **Salida:** `datos/final/<ej>/X.npy`, `meta.json`, diccionario `docs/diccionario/<ej>.md|csv` (falla si no coincide el numero de columnas).
