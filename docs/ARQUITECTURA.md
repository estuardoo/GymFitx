# GYMFITX — Arquitectura

Diseño y decisiones. El paso a paso de uso está en [PIPELINE.md](PIPELINE.md).
Estado al 23-sep-2026 (v2.1: árbol funcional).

## 1. Árbol funcional

Un solo sistema, una rama por función. Cada rama tiene sus propias funciones; ninguna es una
carpeta "adaptada" que mezcle etapas.

```
GYMFIT/
├─ src/                 EL CÓDIGO: una rama por función
│  ├─ nucleo/            TRONCO   config · tipos · log · landmarks · ejercicio · migrar
│  ├─ almacenamiento/    1ª       sqlserver · historial · dataset_sql (solo guardar/leer)
│  ├─ captura/           1ª
│  │  ├─ fuentes/        2ª       base · camara · video
│  │  └─ deteccion/      2ª       tracker (único módulo que importa MediaPipe)
│  ├─ procesamiento/     1ª       offline (kpoints sobre un video grabado)
│  │  ├─ puntos/         2ª       kpoints · normalizacion · vectorizar
│  │  └─ medidas/        2ª       angulos · features · filtros
│  ├─ evaluacion/        1ª       segmentador · plantilla · esquemas · similitud
│  │  └─ comparadores/   2ª       dtw · angulos_directo · clasificador
│  ├─ sesion/            1ª       pipeline · gesto · sumideros · grabacion · overlay
│  ├─ etiquetado/        1ª       manifest · cortes · previews · exportar · tablas · editor_puntos
│  ├─ preparacion/       1ª       tabla · etapas (las 5 tareas) · documentar (diccionario, limpieza)
│  ├─ entrenamiento/     1ª       datos · modelos · validacion · reportes · entrenar · descomposicion
│  └─ interfaz/          1ª       control · tunel · app
│     ├─ api/            2ª       sesion · grabaciones · etiquetado · entrenamiento · sistema · publicar
│     └─ web/            2ª       index.html · estilos.css · js/ (un archivo por pestaña)
├─ datos/               lo que genera el uso: grabaciones, clips, modelos entrenados (fuera de git)
├─ ejercicios/          un .yaml por ejercicio
├─ modelos/             modelos de MediaPipe (se descargan solos)
├─ herramientas/        cloudflared.exe (botón Publicar)
├─ scripts/  tests/  docs/
└─ GYMFITX.bat · UPDATE.bat · requirements*.txt · pyproject.toml · README.md · CHANGELOG.md
```

**Regla del árbol:** cada rama importa solo del tronco o de ramas anteriores, en este orden:
`nucleo → almacenamiento → captura → procesamiento → evaluacion → sesion → etiquetado → preparacion → entrenamiento → interfaz`.
`tests/test_capas.py` falla si alguien la rompe (y si aparece un módulo suelto en la raíz).

| Rama | Módulo | Qué hace |
|---|---|---|
| **nucleo** | `config.py` | Todas las rutas (`datos/`, `ejercicios/`, `modelos/`) y SQL Server en un solo lugar |
| | `tipos.py` | `Frame`, `Landmarks`, `FeatureVec`, `Segment`, `Score`: lo único que viaja entre etapas |
| | `landmarks.py` | Nombres y conexiones de los 33 puntos de pose (vocabulario común) |
| | `ejercicio.py` | Carga y valida `ejercicios/*.yaml`; catálogo de kpoints del ejercicio |
| | `log.py`, `migrar.py` | Log único rotativo y traída de datos del proyecto viejo |
| **almacenamiento** | `sqlserver.py` | Conexión única (driver y host automáticos) |
| | `historial.py` | reps/sesiones/rutina con cola y reintento: el panel no depende de SQL |
| | `dataset_sql.py` | Tablas del dataset: DDL y primitivas de lectura/escritura, sin lógica |
| **captura** | `fuentes/camara.py`, `video.py` | `CameraSource` (MJPG, tolera lecturas fallidas) y `VideoSource`, misma interfaz (`base.py`) |
| | `deteccion/tracker.py` | `PoseTracker` (33 pts) |
| **procesamiento** | `puntos/kpoints.py` | Catálogo del ejercicio → puntos por cuadro. La misma función en vivo y offline |
| | `puntos/normalizacion.py` | Caja 100×100 o punto de referencia + remuestreo a N cuadros |
| | `puntos/vectorizar.py` | Clip → vector fijo. Idéntico para entrenar y para puntuar en vivo |
| | `medidas/angulos.py`, `features.py`, `filtros.py` | Ángulos (flexión: 0° = recto), features del YAML y One Euro |
| | `offline.py` | kpoints en cada cuadro de un video grabado (pose) |
| **evaluacion** | `segmentador.py`, `plantilla.py` | Repeticiones por histéresis y referencia (μ, σ, umbrales, τ) |
| | `comparadores/` | `dtw` (banda), `angulos_directo` y `clasificador` (modelo entrenado) |
| | `similitud.py` | Parecido R² (con DTW) de un clip contra el base, punto por punto |
| | `esquemas.py` | Comparar variantes de un mismo ejercicio |
| **sesion** | `pipeline.py` | Hilo de captura + hilo de detección, pausa |
| | `gesto.py` | Muñeca sostenida 1 s en la esquina = grabar/detener, con espera entre disparos (sale de la misma pose, sin modelo extra) |
| | `sumideros.py`, `grabacion.py`, `overlay.py` | Recorder/Evaluator + bus, archivo de la toma y dibujo |
| **etiquetado** | `manifest.py` | Rutas del dataset e índice de clips exportados |
| | `cortes.py`, `previews.py` | Etiquetas por segmento y copia H.264 para el navegador |
| | `exportar.py` | Segmentos → clips `.mp4` + `.npz` y subida a SQL |
| | `tablas.py` | Lógica de las tablas: crudo, normalizado e indicador contra el base |
| | `editor_puntos.py` | Editor visual de los `.yaml` (kpoints y features) |
| **preparacion** | `tabla.py`, `etapas.py`, `documentar.py` | Las 5 tareas de la etapa 3 sobre el **disco**; umbrales en `params.yaml`; diccionario (`docs/diccionario/`) e informe de limpieza (`reportes/`) |
| **entrenamiento** | `datos.py` | Arma X / y desde la tabla del disco (SQL = respaldo) |
| | `modelos.py`, `validacion.py` | Catálogo de modelos; k-fold, F1 macro, CV anidada |
| | `reportes.py`, `entrenar.py` | Gráficas y `meta.json` de cada `run_N`; orquesta todo |
| | `descomposicion.py` | Cada clip contra el clip base, punto por punto |
| **interfaz** | `control.py` | La sesión de cámara (una sola), historial y log de eventos |
| | `api/*.py` | Rutas REST por área + MJPEG y WebSocket (`api/sesion.py`) |
| | `tunel.py` | Túnel Cloudflare bajo demanda + login para lo que entra por él |
| | `app.py` | Solo arma la app: middleware, ciclo de vida, routers, carpetas estáticas |
| | `web/js/` | `panel`, `sistema`, `vivo`, `cortes`, `sql`, `entrenamiento`, `ranking`, `descomposicion`, `puntos`, `pipeline`, `pitch`, `navegacion` |

## 2. Flujo de datos

```
cámara ─┬─ hilo captura ── video (todos los cuadros) ── datos/grabaciones/<ej>/<día>/HHMMSS_<modo>.mp4
        │                  vista previa (MJPEG)
        └─ hilo detección (cuadro más reciente)
             ├─ pose (33 pts) → gesto de la esquina
             ├─ features → filtro → segmentador → rep → comparadores → puntaje
             └─ kpoints (si hay clasificador) ─────────────────────────┘
datos/grabaciones/*.mp4 ─ Cortar (etiquetas.json) ─ Generar cortes ─ procesamiento/offline.py (kpoints en cada cuadro)
     ─ datos/clips/<clase>/*.npz ─ SQL: table_frames → table_frames_fix (etiquetado/tablas.py) ─ entrenar ─ run_N/modelo.joblib
                                                                                  └─ vuelve al vivo (paso 7)
```

**Etiquetas:** la única fuente es `datos/etiquetas.json` (clase por segmento). La pestaña
"Etiquetado" de antes (bien/mal por video entero, en la tabla SQL `videos`) se quitó porque no
alimentaba el entrenamiento. La tabla `videos` quedó en la base y se puede borrar a mano.

**Modos de grabación:** `referencia` (sin plantilla: la toma calibra el ejercicio; antes se
llamaba `base`) y `serie`. La clase `base` del cortador es otra cosa: el clip de referencia
contra el que compara la Descomposición. Esa clase no se usa como clase del clasificador.

## 3. Rendimiento de la cámara

Antes todo corría en un solo hilo y en serie: leer la cámara, correr la detección
(pose y gesto) y escribir el video. En la PC del proyecto eso daba unos 7 fps de
detección. El video relleno repetía cada cuadro hasta unas 4 veces: 70 % de cuadros congelados.

| Cambio | Efecto |
|---|---|
| Hilo de captura separado del de detección | El video lleva **todos** los cuadros de la cámara; la detección toma siempre el más reciente |
| Un solo modelo (Pose, 33 puntos); el gesto sale de esa misma pose | Sin modelo de manos: ~2× más rápido por cuadro |
| Conversión BGR→RGB una vez por cuadro | Antes se repetía una vez por detector |
| Panel del overlay en un recorte (ROI) | Antes copiaba y mezclaba el cuadro entero |
| JPEG del stream en un hilo, a 960 px y solo con cuadros nuevos | Ya no bloquea el servidor |
| Cámara en MJPG | Muchas webcams USB en YUY2 solo dan 5-10 fps a 1280×720 |
| SQL de cada repetición en cola aparte | El hilo de detección ya no espera a la red |

Medido en el entorno de prueba (2 núcleos, `cuerpo_completo` con pose y manos, 150 cuadros a 30 fps):

| | Antes | Después |
|---|---|---|
| Detección | 13,2 fps | 25,2 fps (×1,9) |
| Cuadros de la cámara en el video | se repetía cada cuadro detectado | 100 % (los 150 cuadros de la fuente) |

El overlay muestra por separado los fps de la cámara y los de la detección, y el `.json` de cada
grabación guarda `fps_camara`, `fps_video_real` y `fps_medio` (detección).

## 4. Base de datos (SQL Server, base `GymFitX`)

Una sola conexión (`almacenamiento/sqlserver.py`). El driver ODBC se detecta solo (18 → 17 → …) y el
host sale de la PC.

| Tabla | Contenido |
|---|---|
| `reps`, `sessions`, `routine` | Historial del panel (`almacenamiento/historial.py`) |
| `table_file` | Un renglón por clip: type, archivo, clase, frames, guía de normalización, `usar` |
| `table_kpoints` / `table_angles` | Catálogo de puntos / ángulos por type |
| `table_frames` | Puntos crudos por cuadro: `VectorX/Y/Z` y `angles` ("v1\|v2\|…") |
| `table_frames_fix` | Normalizado (rectángulo 100×100 o punto de referencia) y remuestreado a N cuadros. **Esto entra al modelo** |
| `table_frame_base`, `table_indicator` | Clip base del type y parecido (R² con DTW, banda ±15 %) de cada clip contra él |
| `table_config` | Normalización vigente por type |

Cada clip guarda su "guía" (puntos, ángulos y normalización). Si algo cambia, el clip se
regenera solo.

## 5. Puntos y ángulos

- Catálogo de kpoints en `ejercicios/<ejercicio>.yaml`. Se edita en la pestaña Kpoints (tablero del cuerpo de 33 puntos);
  desde ahí también se **crean** y **eliminan** ejercicios (el `.yaml` eliminado queda en `ejercicios/.respaldos/`).
- **Ángulos y proporciones**: los que armas en el tablero (3 o más kpoints por fila). Convención: flexión = 180° − ángulo interior
  (0° = recto). Se calculan sobre las coordenadas *world*, así que no dependen del encuadre.
- Normalización (`procesamiento/puntos/normalizacion.py`): caja envolvente del clip completo encajada en un lienzo de
  100×100 con un solo factor de escala, y remuestreo a `n_frames_fijo` cuadros.

## 6. Entrenamiento

- Una muestra = un clip. El vector se arma por cuadro (x, y, z de cada punto, ángulos o ambos).
- `StratifiedKFold` (k ≈ 100 / % de test) con el mismo reparto para todos los modelos.
- **Criterio: F1 macro**, no accuracy. Con 51 clips "mal" y 24 "bien", responder siempre "mal" ya
  da cerca de 68 % de accuracy.
- **Línea base** (`DummyClassifier`) en cada corrida: un modelo que no la supera no aprendió nada.
- **CV anidada**: la elección del mejor modelo se repite dentro de cada fold. Es el número honesto
  para reportar; la accuracy del ganador sin anidar es optimista.
- La clase `base` no entra al clasificador.
- `datos/entrenamientos/run_N/modelo.joblib` guarda su `spec` (puntos, normalización, features) para que el vivo arme
  exactamente el mismo vector. Las corridas anteriores a esta versión no tienen `spec`: hay que
  volver a entrenar una vez para usar el modelo en vivo.

Última corrida real antes de estos cambios (run 10): knn, 74,6 % de accuracy pero F1 macro 0,50,
con 59 clips (base 2 / bien 24 / mal 51 en el manifest).

## 7. Limitaciones y próximos pasos

| Limitación | Qué la resuelve |
|---|---|
| Dataset chico y desbalanceado, 1 ejercicio, 1 día, 1 persona | Más sesiones y personas; terminar de clasificar los segmentos pendientes |
| Criterio de "correcto" definido por una sola persona | Validarlo con el tutor o un fisioterapeuta |
| Segmentos muy cortos | Cortar segmentos más largos |
| GPU delegate de MediaPipe no disponible en Windows/Python | Si hace falta más velocidad: multiproceso o bajar la resolución de detección |

## 8. Incidentes resueltos (resumen)

- **Cortes que no cargaban (16-sep):** una pestaña vieja sobrescribió `labels.json` con su copia
  incompleta. Ahora `/api/labels` combina en vez de reemplazar, y `exportar()` vuelve a cortar
  si falta un clip en disco.
- **La cámara se cortaba a los 2-7 cuadros (22/23-sep):** una sola lectura fallida terminaba la
  sesión. Ahora se toleran 2 s de fallos, y el motivo del corte se muestra en el panel y queda en el log.
- **El panel no arrancaba sin SQL Server:** `Storage()` lanzaba una excepción al importar. Ahora
  arranca igual y las repeticiones esperan en `pendientes_sql.jsonl`.
- **Gesto doble:** si la muñeca se perdía un cuadro, el gesto volvía a disparar. Ahora hay
  memoria de 600 ms y 1,5 s de espera entre disparos.
