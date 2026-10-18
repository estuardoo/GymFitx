# 0005 · Umbrales de limpieza

- **Estado:** aceptada · **Etapa:** 3.2 Limpiar · **Issue:** #pendiente
- **Contexto:** MediaPipe falla a veces (cuerpo fuera de cuadro, oclusion) y deja cuadros con NaN. Un clip casi vacio no ensena nada.
- **Decision:** se saca el clip si tiene menos de `min_frames` cuadros o mas de `max_nan_pct` % de puntos sin deteccion. Nada se borra del disco: la exclusion queda en `limpio.json`. `aplicar: false` solo informa.
- **Justificacion de los numeros:** 10 cuadros = ~0.3 s a 30 fps, menos que cualquier repeticion; 20 % de NaN es el punto donde el remuestreo a 30 cuadros empieza a inventar mas de lo que mide. **Revisar con el reporte de etapa 2** y ajustar en params.yaml.
- **Parametro:** `limpieza.*` · **Codigo:** `src/preparacion/tabla.py::motivos_limpieza`, `src/preparacion/etapas.py::limpiar`.
- **Salida / metrica:** `reportes/limpieza_<ej>.json` (metrica DVC) y `reportes/limpieza_<ej>.md` (clip, motivo).
