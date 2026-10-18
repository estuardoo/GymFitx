# Documentacion del codigo

Generada por `scripts/generar_docs_codigo.py` desde los docstrings, firmas e imports (no se edita a mano; `python scripts/generar_docs_codigo.py` la regenera y `dvc repro documentar_codigo` la deja registrada).

Otras vistas: [dependencias entre ramas](dependencias.md) · [rutas de la API](api_rutas.md) · [parametros](parametros.md).

## (raiz)

| Archivo | Que hace | Contenido |
|---|---|---|
| [src/__init__.py](__init__.md) | GYMFITX: coach de movimiento por camara. | 0 clases, 0 funciones |

## almacenamiento

| Archivo | Que hace | Contenido |
|---|---|---|
| [src/almacenamiento/__init__.py](almacenamiento/__init__.md) | Guardar y leer: SQL Server (conexion unica), historial de repeticiones y tablas del dataset. | 0 clases, 0 funciones |
| [src/almacenamiento/dataset_sql.py](almacenamiento/dataset_sql.md) | Dataset de keypoints en SQL Server: SOLO guardar y leer (sin logica de negocio). | 0 clases, 35 funciones |
| [src/almacenamiento/historial.py](almacenamiento/historial.md) | Persistencia en SQL Server (antes SQLite local, `gymfitx.db`) -- `reps`, | 1 clases, 3 funciones |
| [src/almacenamiento/sqlserver.py](almacenamiento/sqlserver.md) | Conexion UNICA a SQL Server para todo el proyecto. | 1 clases, 8 funciones |

## captura

| Archivo | Que hace | Contenido |
|---|---|---|
| [src/captura/__init__.py](captura/__init__.md) | De la camara (o un video) a landmarks crudos. | 0 clases, 0 funciones |
| [src/captura/deteccion/__init__.py](captura/deteccion/__init__.md) | MediaPipe: tracker de pose (33 puntos). | 0 clases, 0 funciones |
| [src/captura/deteccion/tracker.py](captura/deteccion/tracker.md) | Capa 2: cuadro -> landmarks. Unico archivo del proyecto que importa mediapipe. | 2 clases, 3 funciones |
| [src/captura/fuentes/__init__.py](captura/fuentes/__init__.md) | De donde salen los cuadros: camara o archivo de video. | 0 clases, 0 funciones |
| [src/captura/fuentes/base.py](captura/fuentes/base.md) | Interfaz comun de las fuentes de cuadros: el pipeline no distingue camara de video. | 1 clases, 0 funciones |
| [src/captura/fuentes/camara.py](captura/fuentes/camara.md) | Webcam: abrir (DSHOW/MSMF, MJPG), listar camaras y entregar cuadros tolerando fallos sueltos. | 1 clases, 6 funciones |
| [src/captura/fuentes/video.py](captura/fuentes/video.md) | Reproduce un archivo como fuente de cuadros (tests, reprocesar sin camara). | 1 clases, 0 funciones |

## entrenamiento

| Archivo | Que hace | Contenido |
|---|---|---|
| [src/entrenamiento/__init__.py](entrenamiento/__init__.md) | Entrenar clasificadores: datos, modelos, validacion, reportes y descomposicion. | 0 clases, 0 funciones |
| [src/entrenamiento/datos.py](entrenamiento/datos.md) | Etapa 6a: que clips entran al entrenamiento (seleccion manual) y armar X / y desde SQL. | 0 clases, 3 funciones |
| [src/entrenamiento/descomposicion.py](entrenamiento/descomposicion.md) | Descomposicion: cada clip contra el clip 'base' de su ejercicio, punto por | 0 clases, 4 funciones |
| [src/entrenamiento/entrenar.py](entrenamiento/entrenar.md) | Etapa 6: orquesta un entrenamiento: datos -> modelos + validacion -> reportes -> modelo.joblib con su spec. | 0 clases, 1 funciones |
| [src/entrenamiento/exportar_slurm.py](entrenamiento/exportar_slurm.md) | Exporta, para UN ejercicio, los datos crudos por video y por cuadro (puntos x,y,z de cada kpoint y las | 0 clases, 1 funciones |
| [src/entrenamiento/modelos.py](entrenamiento/modelos.md) | Catalogo de clasificadores a comparar (sklearn siempre; lightgbm/xgboost si estan instalados). | 0 clases, 4 funciones |
| [src/entrenamiento/reportes.py](entrenamiento/reportes.md) | Etapa 6c: lo que queda de cada corrida en datos/entrenamientos/run_N/ (graficas, meta.json) y su listado. | 0 clases, 12 funciones |
| [src/entrenamiento/validacion.py](entrenamiento/validacion.md) | Etapa 6b: como se mide un modelo (k-fold estratificado, F1 macro, CV anidada). | 1 clases, 5 funciones |

## etiquetado

| Archivo | Que hace | Contenido |
|---|---|---|
| [src/etiquetado/__init__.py](etiquetado/__init__.md) | Dataset: cortar y etiquetar, exportar clips, previews y tablas SQL. | 0 clases, 0 funciones |
| [src/etiquetado/cortes.py](etiquetado/cortes.md) | Etapa 3: cortar y etiquetar grabaciones (bien / mal / base / descarte por segmento). | 0 clases, 5 funciones |
| [src/etiquetado/depurar.py](etiquetado/depurar.md) | Quitar por completo un ejercicio archivado: manifest, cortes, seleccion de entrenamiento y SQL. | 0 clases, 10 funciones |
| [src/etiquetado/editor_puntos.py](etiquetado/editor_puntos.md) | Editor visual de los .yaml de ejercicio (ejercicios/*.yaml): | 0 clases, 23 funciones |
| [src/etiquetado/exportar.py](etiquetado/exportar.md) | Etapa 4: exportar cada segmento etiquetado como clip (.mp4 + .npz con sus kpoints) al disco y, si Sistema lo pide | 0 clases, 10 funciones |
| [src/etiquetado/importar.py](etiquetado/importar.md) | Subir clips ya cortados (bien / mal / base) a un ejercicio, sin pasar por grabacion + etiquetado. | 0 clases, 15 funciones |
| [src/etiquetado/manifest.py](etiquetado/manifest.md) | Rutas e indice del dataset: que video es cual, que clips se exportaron (manifest.json) y de que ejercicio. | 0 clases, 6 funciones |
| [src/etiquetado/previews.py](etiquetado/previews.md) | Copia H.264 liviana de cada grabacion para el <video> del navegador (datos/previews/). | 0 clases, 3 funciones |
| [src/etiquetado/tablas.py](etiquetado/tablas.md) | Etapa 5: llevar los clips exportados a las tablas SQL (crudo, normalizado e indicador vs base). | 0 clases, 8 funciones |

## evaluacion

| Archivo | Que hace | Contenido |
|---|---|---|
| [src/evaluacion/__init__.py](evaluacion/__init__.md) | Repeticiones y puntaje: segmentador, plantilla, comparadores y similitud. | 0 clases, 0 funciones |
| [src/evaluacion/base_clip.py](evaluacion/base_clip.md) | Base (plantilla) a partir de UN clip ya cortado: el primer clip "bien" del ejercicio (o el que se indique). | 0 clases, 6 funciones |
| [src/evaluacion/comparadores/__init__.py](evaluacion/comparadores/__init__.md) | Comparadores intercambiables: cada uno puntua una repeticion contra la | 0 clases, 1 funciones |
| [src/evaluacion/comparadores/angulos_directo.py](evaluacion/comparadores/angulos_directo.md) | Comparador sin DTW: remuestrea la repeticion al largo de la plantilla y compara cuadro a cuadro. | 0 clases, 2 funciones |
| [src/evaluacion/comparadores/clasificador.py](evaluacion/comparadores/clasificador.md) | Comparador con el modelo entrenado (datos/entrenamientos/run_N/modelo.joblib). | 2 clases, 2 funciones |
| [src/evaluacion/comparadores/dtw.py](evaluacion/comparadores/dtw.md) | Capa 6: comparacion de una repeticion contra la plantilla. | 0 clases, 5 funciones |
| [src/evaluacion/esquemas.py](evaluacion/esquemas.md) | Comparar 'esquemas' (que features/regiones del cuerpo se miden) y modelos | 0 clases, 3 funciones |
| [src/evaluacion/plantilla.py](evaluacion/plantilla.md) | La plantilla: el movimiento base y TODO lo que se deriva de el. | 1 clases, 2 funciones |
| [src/evaluacion/segmentador.py](evaluacion/segmentador.md) | Capa 5: recorta repeticiones del flujo continuo de features. | 1 clases, 0 funciones |
| [src/evaluacion/similitud.py](evaluacion/similitud.md) | Parecido de un clip contra el clip base, punto por punto: R2 (%) tras alinear posicion/escala y tiempo (DTW). | 0 clases, 3 funciones |

## interfaz

| Archivo | Que hace | Contenido |
|---|---|---|
| [src/interfaz/__init__.py](interfaz/__init__.md) | Panel web: control de la sesion, API por area, tunel de publicacion y la pagina. | 0 clases, 0 funciones |
| [src/interfaz/__main__.py](interfaz/__main__.md) | python -m src.interfaz  ->  http://127.0.0.1:8000 | 0 clases, 0 funciones |
| [src/interfaz/api/__init__.py](interfaz/api/__init__.md) | Rutas HTTP del panel, una por area funcional. | 0 clases, 0 funciones |
| [src/interfaz/api/ahpc.py](interfaz/api/ahpc.md) | AHPC: modulo independiente para armar, con los datos ya generados (table_frames_fix en SQL), el paquete | 0 clases, 6 funciones |
| [src/interfaz/api/entrenamiento.py](interfaz/api/entrenamiento.md) | API de entrenamiento: clips a usar, entrenar, corridas, modelos y descomposicion. | 0 clases, 10 funciones |
| [src/interfaz/api/etiquetado.py](interfaz/api/etiquetado.md) | API de etiquetado: videos para cortar, etiquetas, overlay de puntos, exportar clips, tablas SQL y editor de puntos. | 0 clases, 32 funciones |
| [src/interfaz/api/grabaciones.py](interfaz/api/grabaciones.md) | API de grabaciones: listar, descargar features en CSV y usar una toma como nueva base. | 1 clases, 3 funciones |
| [src/interfaz/api/publicar.py](interfaz/api/publicar.md) | API del boton "Publicar en internet" (tunel Cloudflare, apagado por defecto). La logica vive en interfaz/tunel.py. | 1 clases, 4 funciones |
| [src/interfaz/api/sesion.py](interfaz/api/sesion.md) | API de la sesion en vivo: camaras, estado, rutina, historial, encender/grabar/detener, video MJPEG y WebSocket. | 7 clases, 22 funciones |
| [src/interfaz/api/sim.py](interfaz/api/sim.md) | SIM: verificacion visual de deteccion + normalizacion, sin recalcular nada nuevo. | 0 clases, 8 funciones |
| [src/interfaz/api/sistema.py](interfaz/api/sistema.md) | API de la pestana Sistema: log, librerias, version de Python, apagar/reiniciar y laminas del pitch. | 6 clases, 20 funciones |
| [src/interfaz/app.py](interfaz/app.md) | Servidor local del panel de control. | 0 clases, 8 funciones |
| [src/interfaz/control.py](interfaz/control.md) | Estado del panel: la sesion de camara (una sola, hay una sola camara), el historial y el log de eventos. | 1 clases, 3 funciones |
| [src/interfaz/tunel.py](interfaz/tunel.md) | Publicar el panel en internet con un tunel de Cloudflare (boton del panel). | 1 clases, 12 funciones |

## nucleo

| Archivo | Que hace | Contenido |
|---|---|---|
| [src/nucleo/__init__.py](nucleo/__init__.md) | Tronco: rutas, tipos, log, nombres de landmarks y ejercicios. No depende de ninguna otra rama. | 0 clases, 0 funciones |
| [src/nucleo/componentes.py](nucleo/componentes.md) | Que entra al vector del modelo: letras x, y, z (ejes de cada kpoint), a (angulos), p (proporciones y razones). | 0 clases, 2 funciones |
| [src/nucleo/config.py](nucleo/config.md) | Rutas y configuracion del proyecto en un solo lugar. Ningun otro modulo arma rutas a mano. | 0 clases, 13 funciones |
| [src/nucleo/ejercicio.py](nucleo/ejercicio.md) | Carga y validacion del ejercicio declarado en YAML. | 1 clases, 8 funciones |
| [src/nucleo/landmarks.py](nucleo/landmarks.md) | Nombres, indices y conexiones de los landmarks de MediaPipe. | 0 clases, 4 funciones |
| [src/nucleo/log.py](nucleo/log.md) | Log del proyecto: un archivo por sesion en datos/logs/ (antes habia uno solo, | 1 clases, 3 funciones |
| [src/nucleo/migrar.py](nucleo/migrar.md) | Trae los datos del proyecto viejo (GYMFITX, con core/ + fgml/) a este. | 0 clases, 4 funciones |
| [src/nucleo/reglas.py](nucleo/reglas.md) | Reglas de postura: un angulo medido en el cuadro contra un valor y una tolerancia. Dentro = verde, fuera = rojo. | 0 clases, 7 funciones |
| [src/nucleo/tiempos.py](nucleo/tiempos.md) | Tiempos por proceso, en matriz. Complementa el log de sesion (datos/logs/gymfitx_*.log): | 0 clases, 5 funciones |
| [src/nucleo/tipos.py](nucleo/tipos.md) | Contratos de datos del pipeline. Cero logica, solo estructura. | 5 clases, 0 funciones |

## preparacion

| Archivo | Que hace | Contenido |
|---|---|---|
| [src/preparacion/__init__.py](preparacion/__init__.md) | Preparacion de datos (etapa 3 de CRISP-DM): seleccionar, limpiar, construir, integrar y dar formato, desde el disco. | 0 clases, 0 funciones |
| [src/preparacion/documentar.py](preparacion/documentar.md) | Documentos que genera el pipeline (nunca a mano, para que no se desincronicen): | 0 clases, 4 funciones |
| [src/preparacion/etapas.py](preparacion/etapas.md) | Las 5 tareas de la etapa 3 de CRISP-DM como etapas ejecutables (las llama dvc.yaml, una por ejercicio): | 0 clases, 10 funciones |
| [src/preparacion/tabla.py](preparacion/tabla.md) | Nucleo de la preparacion: lo comparten el entrenamiento y las 5 etapas ejecutables (etapas.py). | 0 clases, 12 funciones |

## procesamiento

| Archivo | Que hace | Contenido |
|---|---|---|
| [src/procesamiento/__init__.py](procesamiento/__init__.md) | De landmarks a medidas: kpoints, normalizacion, angulos, features y filtros. | 0 clases, 0 funciones |
| [src/procesamiento/medidas/__init__.py](procesamiento/medidas/__init__.md) | Angulos, features por cuadro y filtro One Euro. | 0 clases, 0 funciones |
| [src/procesamiento/medidas/angulos.py](procesamiento/medidas/angulos.md) | Geometria de angulos entre vectores/puntos (grados). | 0 clases, 2 funciones |
| [src/procesamiento/medidas/features.py](procesamiento/medidas/features.md) | Capa 3: landmarks -> vector de features invariantes. | 2 clases, 8 funciones |
| [src/procesamiento/medidas/filtros.py](procesamiento/medidas/filtros.md) | One Euro Filter vectorizado y consciente de las unidades. | 1 clases, 1 funciones |
| [src/procesamiento/offline.py](procesamiento/offline.md) | Detecta los kpoints del ejercicio sobre un video YA GRABADO: es la fuente | 1 clases, 7 funciones |
| [src/procesamiento/puntos/__init__.py](procesamiento/puntos/__init__.md) | Kpoints del ejercicio, normalizacion y vector fijo por clip (mismo camino vivo y dataset). | 0 clases, 0 funciones |
| [src/procesamiento/puntos/kpoints.py](procesamiento/puntos/kpoints.md) | Catalogo de 'kpoints' de un ejercicio -> puntos por cuadro. | 0 clases, 2 funciones |
| [src/procesamiento/puntos/normalizacion.py](procesamiento/puntos/normalizacion.md) | Normalizacion de un clip de puntos: caja 100x100 (o punto de referencia) y remuestreo a N cuadros. | 0 clases, 8 funciones |
| [src/procesamiento/puntos/vectorizar.py](procesamiento/puntos/vectorizar.md) | Clip de puntos -> vector de largo fijo para el clasificador. | 0 clases, 5 funciones |

## scripts

| Archivo | Que hace | Contenido |
|---|---|---|
| [scripts/__init__.py](scripts/__init__.md) | Herramientas de linea de comandos (sin panel). | 0 clases, 0 funciones |
| [scripts/_comun.py](scripts/_comun.md) | Utilidades compartidas por los scripts de linea de comandos. | 0 clases, 7 funciones |
| [scripts/busqueda_features_slurm.py](scripts/busqueda_features_slurm.md) | Busqueda aleatoria de que kpoints/angulos/proporciones mueven el accuracy y el F1 de un ejercicio. | 0 clases, 23 funciones |
| [scripts/camara.py](scripts/camara.md) | Utilidad: descubre que indices de camara responden en esta maquina. | 0 clases, 0 funciones |
| [scripts/comparar_esquemas.py](scripts/comparar_esquemas.md) | Compara esquemas (YAML) y modelos (src/evaluacion/comparadores/) sobre las MISMAS | 0 clases, 3 funciones |
| [scripts/estado_busqueda_slurm.py](scripts/estado_busqueda_slurm.md) | Tabla de avance de una corrida de busqueda_features_slurm.py -- lee los <salida>.estado.json que cada | 0 clases, 2 funciones |
| [scripts/evaluar.py](scripts/evaluar.md) | Evalua repeticiones en vivo contra el movimiento base. | 0 clases, 1 funciones |
| [scripts/exportar_dataset_slurm.py](scripts/exportar_dataset_slurm.md) | CLI de src/entrenamiento/exportar_slurm.py -- ver ese archivo para el flujo completo (exportar aqui, | 0 clases, 0 funciones |
| [scripts/generar_docs_codigo.py](scripts/generar_docs_codigo.md) | Genera docs/codigo/: la documentacion de TODO el codigo, leida del propio codigo (docstrings, firmas, rutas, imports, | 0 clases, 15 funciones |
| [scripts/grabar.py](scripts/grabar.md) | Graba el movimiento base de un ejercicio y calibra su plantilla. | 0 clases, 1 funciones |
| [scripts/perfil_arranque.py](scripts/perfil_arranque.md) | Mide donde se va el tiempo al arrancar.   python scripts/perfil_arranque.py | 0 clases, 1 funciones |
| [scripts/reprocesar.py](scripts/reprocesar.md) | Reprocesa una grabacion por el mismo pipeline, sin camara. | 0 clases, 2 funciones |
| [scripts/resumen_busqueda_slurm.py](scripts/resumen_busqueda_slurm.md) | Junta el/los .csv que salieron de busqueda_features_slurm.py (una o varias corridas, uno o varios | 0 clases, 16 funciones |

## sesion

| Archivo | Que hace | Contenido |
|---|---|---|
| [src/sesion/__init__.py](sesion/__init__.md) | Una sesion en vivo: pipeline con hilos, gesto de control, sumideros, grabacion y overlay. | 0 clases, 0 funciones |
| [src/sesion/gesto.py](sesion/gesto.md) | Gesto de control: mantener una muneca en la esquina superior izquierda inicia/detiene la grabacion. | 1 clases, 0 funciones |
| [src/sesion/grabacion.py](sesion/grabacion.md) | Registro en disco de cada sesion: video crudo + features + metadatos. | 1 clases, 4 funciones |
| [src/sesion/overlay.py](sesion/overlay.md) | Dibujo sobre el cuadro. Lo usan por igual la app de escritorio y el panel web. | 0 clases, 12 funciones |
| [src/sesion/pipeline.py](sesion/pipeline.md) | Orquestacion. El corazon del diseño: UN pipeline, sumideros intercambiables. | 1 clases, 0 funciones |
| [src/sesion/sumideros.py](sesion/sumideros.md) | Bus de eventos y sumideros: el extremo final del pipeline. | 7 clases, 0 funciones |

## web

| Archivo | Que hace | Contenido |
|---|---|---|
| [src/interfaz/web/js/ahpc.js](web/js/ahpc.md) | Pestana AHPC: arma el paquete listo para el cluster (datos .npz + script busqueda_features_slurm.py + .sbatch por ejercicio) | 3 funciones |
| [src/interfaz/web/js/avatar3d.js](web/js/avatar3d.md) | SIM 4: avatar 3D | 18 funciones |
| [src/interfaz/web/js/cortes.js](web/js/cortes.md) | Pestana Cortar videos: linea de tiempo, cortes, clases, overlay del esqueleto y exportar | 24 funciones |
| [src/interfaz/web/js/descomposicion.js](web/js/descomposicion.md) | Pestana Descomposicion: series por punto e indicador contra el base | 14 funciones |
| [src/interfaz/web/js/entrenamiento.js](web/js/entrenamiento.md) | Pestana Entrenamiento: clips a usar, modelos y corridas | 15 funciones |
| [src/interfaz/web/js/navegacion.js](web/js/navegacion.md) | Cambio de pestanas del dataset y entrada directa por #hash | 9 funciones |
| [src/interfaz/web/js/panel.js](web/js/panel.md) | Pestana Panel: estado, rutina, camara, selector de cuerpo y sesion | 38 funciones |
| [src/interfaz/web/js/pipeline.js](web/js/pipeline.md) | Pestana Pipeline: mapa de las etapas con su detalle. | 1 funciones |
| [src/interfaz/web/js/pitch.js](web/js/pitch.md) | Pestana Pitch: laminas del .pptx | 3 funciones |
| [src/interfaz/web/js/puntos.js](web/js/puntos.md) | Pestana Kpoints: tablero de kpoints, angulos y proporciones del .yaml | 52 funciones |
| [src/interfaz/web/js/ranking.js](web/js/ranking.md) | Pestana Ranking: corridas ordenadas por F1 macro | 3 funciones |
| [src/interfaz/web/js/sim.js](web/js/sim.md) | Pestana SIM: verificacion visual de deteccion + normalizacion de un clip | 14 funciones |
| [src/interfaz/web/js/sistema.js](web/js/sistema.md) | Pestana Sistema: servidor SQL, tablas del dataset, librerias, Python, apagar, log y Publicar | 15 funciones |
| [src/interfaz/web/js/sql.js](web/js/sql.md) | Sistema → Tablas del dataset: normalizacion por ejercicio y generar tablas | 6 funciones |
| [src/interfaz/web/js/vivo.js](web/js/vivo.md) | En vivo: WebSocket de eventos, grafico e historial, y el arranque del panel | 5 funciones |

