# Estructura de datos y configuración

Todo se identifica por **número** (ejercicio, video crudo, clip), nunca por nombre. Un solo lugar por cosa, sin copias paralelas.
La fecha, la persona y los cortes viven en las tablas (`parameters/inputs.json`), no en el nombre del archivo.

```
input/                       datos (no se versionan en git; DVC)
  raw/<n>/<id>.mp4|npz|json    grabación tal cual se grabó (id = número de video crudo)
  bronze/<n>/<id>.mp4|npz      clips cortados (id = número de clip, global y sin reutilizar)
  plate/<n>/<id>.p.npy|.a.npy  puntos y ángulos de cada clip (intermedio, sin normalizar) + meta.json (hash) + registros "fuera" (f000001…)
  gold/<n>/<id>.npy            vector normalizado listo para entrenar (mismo <id> que bronze y plate) + meta.json (hash)
output/
  models/<n>/run_NNN/          modelo.joblib + meta.json + gráficas; meta.origen = tabla, clips usados (id, etiqueta, persona), hash_gold
  reportes/<n>/                informes de selección y limpieza de las etapas
parameters/                  configuración (sí se versiona)
  exercise.json                número → ejercicio (1 = zancada, 2 = cuerpo completo…) y su type en SQL
  <n>/kpoints.json, angles.json, guide.json   definición de cada ejercicio (puntos, ángulos/proporciones, segmentación, señal, reglas): única fuente, la edita el panel
  config.json                  umbrales (seleccion, limpieza, construccion, formato, entrenamiento, base_clip), cortador (cortes), modelos, cámaras, respaldo SQL
  inputs.json                  TABLAS: raw (videos crudos) y clips; contadores
  server.json                  servidor SQL Server (host, base, autenticación)
  plantillas/                  calibración por ejercicio (<slug>.npz)
sistema/                     estado de ejecución (no se versiona): logs, previews, respaldos/ (definición anterior de cada ejercicio), gymfitx.db, sql_tipos.json, sql_config.json, export_estado.json, acceso.json, pendientes
assets/                      modelos de MediaPipe (se descargan solos)
```

`<n>` = número del ejercicio. Variables de entorno para moverlas: `GYMFITX_INPUT`, `GYMFITX_OUTPUT`, `GYMFITX_PARAMETROS`, `GYMFITX_DATOS`.

## Las dos tablas (`parameters/inputs.json`)

| Tabla | Campos | Notas |
|---|---|---|
| `raw` | `id, ej, persona, fecha, archivos, segmentos[], origen_viejo` | `persona` = P1…Pn, se asigna al grabar o en el panel (Cortar videos). `segmentos` = cortes `{ini, fin, clase (bien/mal/descarte), reps}` (ya no hay `etiquetas.json`) |
| `clips` | `id, ej, raw_id, seg, t_ini_ms, t_fin_ms, etiqueta (1 bien / 0 mal), reps, usar, copia, persona, nombre, rev` | `raw_id` vacío = clip importado ya cortado (lleva su propia `persona`). `usar=false` = desmarcado para entrenar. `seg` = posición del corte en `raw.segmentos` |
| `contadores` | `raw, clip` | siguiente número; nunca se reutiliza |

Unión datos ↔ metadata: `clips.raw_id → raw.id` y `clips.ej → exercise.json`. El grupo de validación de un clip es su `raw_id` (ningún video queda a la vez en entrenar y probar).

## Flujo

| Paso | Lee | Escribe |
|---|---|---|
| Grabar | cámara | `raw/<n>/<id>.*` + fila en `raw` (con persona) |
| Cortar videos | `raw` | `raw[].segmentos` |
| Generar cortes | `raw`, `raw/<n>` | `bronze/<n>/<id>.*` + filas en `clips` |
| Importar carpeta (Bien/Mal/P1…) | carpeta externa | `bronze/<n>/<id>.*` + `clips` (+ reconstruye el `raw` si trae `indice.csv`) |
| Construir (plate) | `bronze` + puntos del ejercicio | `plate/<n>/<id>.p.npy, .a.npy` |
| Formatear (gold) | `plate` + normalización | `gold/<n>/<id>.npy` |
| Entrenar | `gold` | `output/models/<n>/run_NNN` |

`plate` y `gold` son cache con hash: si cambian los puntos, la normalización (fórmula de origen/escala o cuadros por ciclo, definida por ejercicio en `parameters/<n>/guide.json → normalizacion`) o la limpieza, se rehacen solos.
