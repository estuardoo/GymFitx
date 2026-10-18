# Cambios

## subir_github: rueda de configuración y ramas de GitHub — 2026-10-18

- Módulo aparte **`subir_github/configuracion.py`** (botón **⚙**): usuarios con su token, repositorios y carpetas. La ventana principal solo elige y sube.
- La **rama** ya no se escribe a mano: se lee de GitHub al elegir usuario y repositorio, como vienen (la predeterminada primero y elegida); se puede escribir otra para crearla.

## subir_github/: ventana para subir el código a GitHub — 2026-10-18

- Carpeta **`subir_github/`** dentro del proyecto (no la importa nada de `src/`): `SUBIR_GITHUB.bat` abre una ventana con **listas elegibles y guardadas** de usuarios (cada uno con su token), repositorios, ramas (🔄 trae las de GitHub) y carpetas, cada una con ➕/🗑; **Probar conexión** se pone verde o rojo; **Subir código actual** y un **cuadro de log** (también en `subir_github.log`). Solo Python + git.
- `config.json` (token) y el log están en su `.gitignore`; además el envío nunca incluye `subir_github/config.json`. Avisa si hay archivos de más de 50 MB. Tests: `tests/test_subir_github.py`.
- La app GYMFITX sigue sin módulo de GitHub (solo el botón «Generar documentación de datos»).

## El gestor de GitHub sale del proyecto — 2026-10-18

- Nuevo programa independiente **`GYMFIT_GITHUB/`** (carpeta hermana de GYMFIT: `GITHUB.bat`, `github_app.py`, `index.html`, README, tests; solo Python + git, sin dependencias). Mismas funciones: paquete por módulo/área, elegir rama, traer cambios, ¿quién soy?, protección, etiqueta, Pull Request. Token y config en su propio `config.json`.
- Se **quitó del proyecto** `src/colaboracion/`, `api/colaboracion.py`, la tarjeta «GitHub» de Sistema y su config en `datos/config.json`. Quedan en Sistema el botón «Generar documentación de datos» (`POST /api/docs/generar`, ahora en `api/sistema.py`) y el respaldo SQL.
- Corregido en el gestor: un archivo versionado y modificado salía con el nombre cortado en la lista de cambios.

## GitHub para varios integrantes — 2026-10-18

- **Módulo a enviar**: el código se agrupa por módulo (`Código · entrenamiento`, `Código · preparacion`, `Código · scripts`…) en «📦 Paquete del envío».
- **Rama**: selector con las ramas locales y las de GitHub (+ «➕ rama nueva…»); continuar la rama de un compañero la sigue en vez de duplicarla. **⬇ Traer cambios** (pull --rebase --autostash). **👤 ¿Quién soy?** valida el token y dice si puede enviar. Aviso claro si la rama está protegida.
- Cada integrante usa su propio token, nombre y correo (`datos/config.json`, no compartido): ver `docs/GUIA_ETAPA3.md` §3.
## Gestor de envíos a GitHub — 2026-10-18

- **Sistema → GitHub → «📦 Paquete del envío»**: los cambios agrupados por área (parámetros y pipeline, decisiones, código, tests, docs, punteros DVC…), con casilla por grupo o archivo; lo marcado es lo que entra al commit (sin marcar = todo). **«🕘 Envíos anteriores»**: últimos commits con su etiqueta de versión. API: `GET /api/github/cambios`, `GET /api/github/historial`. Los `git add` van por tandas de 100 rutas.
## Etapa 3 completa: disco = fuente, SQL = respaldo, 5 etapas con DVC — 2026-10-18

- **Datos en disco**: el entrenamiento lee `datos/clips`, `manifest.json` y `etiquetas.json` (nueva rama `src/preparacion/`); SQL queda como **respaldo** (y para Descomposición/Ranking).
  Sistema → «💾 Datos en disco · respaldo en SQL Server»: interruptores *al cortar* y *al entrenar* (`datos/config.json` → `respaldo_sql`) y «Respaldar ahora». Si SQL cae, solo se avisa.
  `fuente_entrenamiento = "sql"` vuelve al camino antiguo.
- **5 tareas como etapas** (`python -m src.preparacion.etapas <seleccionar|limpiar|construir|integrar|formatear|todo> <ejercicio>`) → `datos/intermedio/`, `datos/final/`, `reportes/`,
  `docs/diccionario/`. Salidas deterministas (mismas entradas = mismos bytes). `limpieza.aplicar` ahora **saca** los clips malos (antes solo informaba).
- **`params.yaml`**: todos los umbrales (selección, limpieza, clase «fuera», formato, semilla, `test_pct`, base de conteo); ninguno vive en el código.
- **`dvc.yaml`** (`foreach` por ejercicio + `documentar_codigo`), `.dvcignore`, `.gitignore` deja pasar los punteros `datos/*.dvc`. Probado: `dvc repro --force` → `dvc.lock` idéntico.
- **Bitácora** `docs/decisiones/` (10 ADR: decisión → parámetro → código → salida) y `tests/test_trazabilidad.py` que la verifica.
- **Documentación del código** `docs/codigo/` generada por `scripts/generar_docs_codigo.py` (índice, matriz de dependencias, rutas API, parámetros, un `.md` por módulo); `--revisar` en el CI.
- **GitHub**: `rutas` (commit por decisión), `etiqueta` (`datos-vN`), «Ver protección» de la rama, PR con `Closes #N`; `.github/workflows/reproducir.yml` y `pull_request_template.md`.
- `docs/GUIA_ETAPA3.md` (qué hacer de tu lado y cómo verificar cada criterio), `environment.yml`, `scripts/iniciar_dvc.bat`, `dvc` en `requirements-dev.txt`.
- `colaboracion/documentar.py` se movió a `preparacion/documentar.py`.

## Fuga de datos corregida: validación por grabación — 2026-10-17

- El k-fold ya no mezcla clips del mismo video entre entrenar y probar: `StratifiedGroupKFold` con el grupo = grabación de origen (`datos.grupo_de`); las copias `_2/_3`
  y las ventanas «fuera» de un video van con él. La CV anidada también. `k` ya no pasa del número de grabaciones de la clase más chica (zancada «bien»: 3 → k = 3).
- `meta.json` guarda `validacion` y `grabaciones`. **Los F1 anteriores (p. ej. run_20 = 1.0) estaban inflados**; vuelve a entrenar para tener la cifra honesta.
- `scripts/busqueda_features_slurm.py` (HPC) usa la misma partición por grabación (`StratifiedGroupKFold`, `k` limitado por las grabaciones de la clase más chica).

## Etapa 3 CRISP-DM: diccionario, limpieza y GitHub — 2026-10-17

- **Criterio 5 · diccionario de datos**: `docs/diccionario/<ejercicio>.csv|.md`, una fila por columna del vector final de la última corrida
  (nombre `fNN_PUNTO_eje` / `fNN_metrica`, tipo, unidad, rango, origen, transformación). Se verifica que el total sea igual al `n_features` del modelo.
- **Criterio 6 · informe de limpieza**: `reportes/limpieza_<ejercicio>.json|.md` (clips por clase, base / desmarcados / sin `.npz`, muy cortos, con muchos
  puntos sin detectar, copias `_N` con riesgo de fuga). Umbrales en el nuevo `params.yaml` (`limpieza.min_frames`, `limpieza.max_nan_pct`). Marca, no borra.
- **Criterio 7 · traza de colaboración**: nueva rama `src/colaboracion/` (`github.py`, `documentar.py`). **Sistema → 🐙 GitHub**: repositorio, rama, nombre, correo y token
  (solo en `datos/config.json`), estado de la carpeta, «Enviar avances» (init + traer historial la primera vez → commit con `Refs #N` → push), rama nueva por decisión
  y Pull Request opcional. Avisa si hay archivos de más de 50 MB. Botón «Generar diccionario + informe de limpieza». API: `/api/github*`, `/api/docs/generar`.

## DroidCam (cámara del celular) — 2026-10-17

- **Sistema → 📱 DroidCam**: un solo listbox con las cámaras como `IP:puerto` (si escribes solo la IP usa 4747); Agregar / Quitar. Se guarda en `datos/config.json` → `droidcam`.
- **Panel → selector de cámara**: cada DroidCam aparece como «📱 DroidCam · IP:puerto» en **amarillo pastel** (y el selector se tiñe cuando está elegida). Se abre por `http://IP:puerto/video` (MJPEG, tiempo de espera de 5 s). `CameraSource(url=...)`.

## Contador único, zancada y cabeza por defecto — 2026-10-15

- El número de repeticiones sale de **una sola cifra** (`Pipeline.n_conteo()`, la del sumidero que cuenta): la usan el video («rep N»), el evento de estado y el contador grande del panel,
  que además ya no depende solo del evento «rep» (sube con cada estado).
- Por defecto: ejercicio **zancada** (panel, Kpoints, Entrenamiento) y su entrenamiento más reciente; la región **cabeza** siempre activa en el selector de cuerpo.

## Zancada: la rep se cuenta al volver al inicio y brazos rectos al bajar — 2026-10-15

- La repetición se cuenta cuando vuelves a la **posición inicial** (`fin` = 70 % del recorrido de la señal, ~150° de rodilla), no a mitad de la subida. `Template.fin` (opcional, `None` = comportamiento anterior); un intento que sube sin llegar abajo se descarta y se rearma.
  La base automática de antes (sin `fin`) se rehace sola al prender la cámara.
- Reglas **Brazo izq / Brazo der** (hombro-codo-muñeca ≥ 160°, fase nueva `bajando` = descenso y abajo): rojo + «Mantén los brazos rectos al bajar.» si se doblan.

## Zancada: cuenta sin entrenar, base desde el primer clip y regla de postura verde/rojo — 2026-10-15

- **Base desde un clip** (`evaluacion/base_clip.py`; solo ejercicios con `base_clip: bien` en el .yaml, hoy zancada): si no tiene base grabada, al prender la cámara se crea
  `datos/plantillas/<ej>.npz` con el primer clip «bien» (umbrales: P10/P90 de la señal, `low` = 30 %, `high` = 50 %). `POST /api/ejercicio/base-clip`
  `{ejercicio, clip?, clase?}` la rehace con otro clip.
- Los clips con 12 o 23 puntos (solo sus kpoints) se miden por nombre; un fallo al crear la base ya no impide prender la cámara.
- **Cuenta sin modelo entrenado**: con base, la vista previa cuenta con el segmentador (el modelo, si hay, solo clasifica).
- `zancada.yaml`: la señal de conteo ahora son las rodillas (`signal: rodilla_izq/rodilla_der`); antes promediaba los 8 ángulos y casi no variaba.
  Con los clips de zancada: 10/10 «bien» cuentan una sola vez.
- **Ángulos de la caracterización de zancada (PDF FitVision)**: las reglas ahora admiten 3 puntos (ángulo en el vértice), `D##`/`T##` (pierna
  delantera/trasera, la de la rodilla más alta va delante), `lado` (±, ≥, ≤), `fase: abajo` (solo en la parte baja de la repetición) y `mensaje`
  (feedback en rojo). En `zancada.yaml`: **Tronco** ≤ 16° de la vertical (hombro medio–cadera media), **Cadera delantera** ≥ 82° (hombro medio–cadera–rodilla
  delanteras, abajo); **Rodilla delantera** (~90°) y **Tibia delantera** quedan como control, apagadas (en el piloto no separaron: AUC 0,57–0,60).
  Pensadas para vista lateral. No incluido: profundidad de rodilla trasera (≤ 0,18 L, es una razón, no un ángulo) ni valgo (vista frontal).
- **Reglas de postura** (`nucleo/reglas.py`, `reglas:` del .yaml): recta B→A contra la horizontal (90° = recta). Dentro de la tolerancia
  (% del ángulo o grados) se pinta en **verde**, fuera en **rojo**, en el video y en la lista de valores. Por defecto: C01 (nariz) vs promedio
  C24/C25 (caderas), 90° ± 8 %. Se edita en la pestaña Kpoints → «Reglas de postura» (`POST /api/puntos/reglas`).

## Importar carpeta: reconstruye los videos originales con el indice.csv — 2026-10-15

- Al importar una carpeta con `indice.csv` (columnas `video_origen`, `inicio_s`, `fin_s`, `persona`, `fecha`), cada video original se
  **recrea uniendo sus clips en orden de `inicio_s`** (el original no está: los tramos entre cortes no existen). Queda en
  `datos/grabaciones/<ejercicio>/<fecha>/<persona>_<origen>.mp4` con su `.npz` (puntos de los clips, sin volver a detectar) y `.json`.
- Sus cortes quedan en `etiquetas.json` (pestaña Cut/Edit), con `persona` y los tiempos originales (`ini_orig`/`fin_orig`); los clips
  del manifest apuntan a ese video (`origen`, `seg`, `ini`, `fin`) y «Generar cortes» no los vuelve a cortar (hash igual).
- `indice.csv` recibe 3 columnas: `video_reconstruido`, `ini_rec_s`, `fin_rec_s`. Repetible: lo ya reconstruido se salta.
- Los videos reconstruidos no aportan ejemplos «fuera» al entrenamiento (no hay tramos reales entre cortes).

## Importar una carpeta entera por persona (P1, P2, …) — 2026-10-15

- 🎞 en Rutina → «…o una carpeta entera»: escribes la ruta de una carpeta `Base/ Bien/ Mal/` con subcarpetas `P1, P2, …`
  (como `01Zancada`) y se importa en segundo plano con avance. Es **incremental**: lo que ya está en
  `datos/clips/<ejercicio>/<clase>/` se salta, así que puedes repetirlo cuando agregues personas o clips.
- Cada fila del manifest guarda `persona` (P1…), y si hay `indice.csv`, también `vista`, `fecha` y `video_origen`. Los nombres
  conservan el prefijo `p1_`, `p2_`… y se listan P2 antes que P10.
- Endpoints: `POST /api/ejercicio/clips/carpeta`, `GET /api/ejercicio/clips/carpeta/progreso`.

## Contador grande a un costado del video — 2026-10-15

- Panel: número grande a la derecha del video con las repeticiones contadas (y «N bien · N mal»); salta y se pone verde cada vez que
  suma una. Cuenta tanto por modelo como por base. Se pone en 0 al prender/apagar la cámara, cambiar de ejercicio o de
  entrenamiento, y al empezar/terminar una grabación.

## El modelo cuenta los ciclos solo (clase «fuera» + ventana deslizante) — 2026-10-15

- **Entrenamiento:** además de bien/mal, agrega la clase `fuera` con ventanas del largo de un ciclo tomadas de los tramos de tus
  grabaciones que NO están cortados como bien/mal/base (IoU < 0.3 con cualquier corte; no más «fuera» que ciclos). Se guarda
  `spec.ventana_ms` (mediana de la duración de tus cortes) y `meta.fuera`. Se apaga con `fuera:false` en `POST /api/entrenar`.
  Sin grabaciones con cortes y puntos, entrena como antes.
- **En vivo:** si el entrenamiento en uso tiene `fuera`, la cámara usa `ContadorModelo`: ventana deslizante sobre los kpoints cada
  150 ms; un ciclo se cuenta cuando P(ciclo) = 1 − P(fuera) sube de 0.6 y vuelve a bajar de 0.4 (`DetectorCiclos.ALTO/BAJO`). No
  necesita base ni umbrales. Sin `fuera` sigue contando por segmentación de la base.
- Lista de entrenamientos: «cuenta sola» marca los que traen `fuera`; arriba dice si cuenta «solo el modelo» o «por base».
- **Hay que reentrenar** para que el modelo tenga la clase `fuera`.

## Panel: la cámara cuenta y clasifica las repeticiones con el modelo entrenado — 2026-10-15

- Antes el modelo solo puntuaba al pulsar **Grabar**; con la cámara en vista previa las repeticiones se segmentaban y se descartaban.
  Ahora, con base + un entrenamiento válido, la vista previa usa `Contador` (un `Evaluator` sin guardar nada): cada repetición se
  segmenta como siempre (yaml `segmentation`) y el modelo la clasifica (bien / mal). No cuenta como "grabando".
- Por defecto manda el entrenamiento **más reciente** del ejercicio (`clasificador` del yaml o su slug); sin modelo vuelve al DTW.
- Bajo **Rutina** hay una lista de los entrenamientos del ejercicio seleccionado (run, modelo, F1, fecha). Click = usar ese run en
  caliente (`POST /api/session/clasificador`). Arriba de la lista: `Contando: N reps · X bien · Y mal (run_N)`; avisa si falta la
  base o si el entrenamiento es viejo (sin `spec`: reentrenar).
- Límite: el modelo clasifica repeticiones ya segmentadas; no detecta el inicio/fin por sí solo.

## Archivar un ejercicio lo quita también de SQL y del dataset — 2026-10-15

- Antes, archivar (🗑 en Rutina) solo movía el `.yaml`: sus clips seguían en `manifest.json`, en el entrenamiento y en SQL, y las
  cantidades de videos no bajaban. Ahora `etiquetado/depurar.py` lo deja fuera de todo: manifest, cortes (`etiquetas.json`,
  `export_estado.json`), selección de entrenamiento y **todas** las tablas de SQL de su `type` (archivos, frames, indicadores,
  catálogo, config, definición). El número del type queda reservado en `sql_tipos.json`.
- Nada se borra del disco: clips, grabaciones y plantilla pasan a `datos/archivados/<ejercicio>_<fecha>/`.
- **Ya archivados antes:** Sistema → Tablas del dataset → **🧹 Quitar de SQL lo archivado** lista lo que se quitaría (clips y
  archivos en SQL por ejercicio), pide confirmar y lo limpia. Si SQL no responde, lo local queda limpio y el ejercicio queda
  pendiente (`datos/pendientes_purga.json`) hasta que repitas el botón.
- Endpoints `GET /api/archivados/plan` y `POST /api/archivados/depurar`.

## Épocas / max_iter por modelo y épocas usadas — 2026-10-14

- **Matriz de modelos** (`MODELOS_MATRIZ` en `src/nucleo/config.py`): los 17 modelos, con `epocas` (árboles/rondas), `max_iter`
  (tope del optimizador), `parar` (early stopping), `paciencia` (`n_iter_no_change`) y `tol`. Se edita en **Sistema → Modelos de
  entrenamiento** y se guarda en `datos/config.json` → `modelos` (solo lo que cambia). Sin reiniciar: aplica al siguiente entrenamiento.
- **Resumen de la corrida:** columna «Épocas usadas (tope)» por modelo (mín–máx de los folds; ⏹ = frenó antes del tope) y chip
  «Épocas usadas» del ganador reentrenado. `meta.json` guarda `iteraciones` por modelo, `iteraciones_mejor` y `matriz_modelos`.
- **Log en matriz** (`gymfitx.log`): tabla por modelo con F1, tope, mín/media/máx usadas y si frenó. La comparación contra la
  corrida anterior ahora lista cambios de la matriz (`mlp.max_iter 2000→500`).
- Defaults iguales a los de antes y a los de scikit-learn (200/150 árboles, max_iter 2000 en logistic y mlp, paciencia/tol de sklearn): los resultados no cambian hasta que edites la matriz.
- Random forest / extra trees / AdaBoost siempre usan todas sus rondas; solo logistic, SGD, MLP, hist-GB y GB (con `parar`) frenan antes.
  SVM, KNN, árbol, LDA, Ridge y Naive Bayes no iteran, así que no tienen fila.

## UPDATE.bat abre GYMFITX al terminar — 2026-10-12

- Todo lo que instala o actualiza está solo en `UPDATE.bat`; `GYMFITX.bat` solo ejecuta (revisado: no instala nada).
- `UPDATE.bat` ahora siempre abre `GYMFITX.bat` cuando termina bien (si falla, se queda con el error). Ya no existe `--lanzar`.
- El botón «Librerías» del panel sigue pudiendo actualizar paquetes a pedido (no corre solo al arrancar).

## Subir videos bien / mal / base por ejercicio — 2026-10-08

- Botón **🎞** en cada fila de Rutina: elige videos ya cortados de **Bien**, **Mal** y **Base** (uno solo). Cada uno se recodifica
  a mp4, se le detectan los puntos del catálogo del ejercicio, entra a `manifest.json` (origen `importados/...`) y se registra en SQL.
- Si SQL no responde el clip queda local; «Sistema → Generar tablas» lo sube después. Un base nuevo pide confirmar el reemplazo.
- El base del dataset (SQL) no es la plantilla en vivo («Usar como base» en Grabaciones): son cosas separadas.
- Endpoints `GET/POST /api/ejercicio/clips`. Nueva dependencia `python-multipart` (la instala `UPDATE.bat`).

## SIM: avatar 3D — 2026-10-08

- Vista nueva **4. Avatar 3D** en SIM: los 33 puntos 3D (`points`, metros) del `.npz` del clip son los huesos y encima va el
  volumen (músculos) hecho con cilindros y elipsoides. Girar con el mouse, rueda para acercar, Play/slider, casillas
  Huesos / Músculos / Espejo / Suavizar y «Seguir el video» (sigue al video de la vista 1-2 cuando se reproduce).
- Endpoint `GET /api/sim/cuerpo3d?clip=`. `js/avatar3d.js` (módulo) + three.js local en `js/vendor/` (sin internet).
- El volumen es visual, no anatomía medida; la profundidad 3D de una sola cámara tiembla (por eso «Suavizar»).

## Kpoints con la misma figura del Panel — 2026-10-08

- El diagrama de Kpoints ya no usa su silueta propia: el fondo es el esqueleto del video (`sesion/overlay.py`) dibujado por el
  servidor en `GET /api/puntos/figura.png`. Cualquier ajuste a la figura (cuello, cabeza) se ve igual en los dos sitios.
  Los puntos clicables, la banda del recorrido y las etiquetas no cambian. `draw_landmarks(..., cabeza_escala)` agranda la
  cabeza en ese diagrama (la cara está ampliada para poder tocar sus puntos).

## Cuello más corto — 2026-10-08

- En el video, el cuello del esqueleto mide la mitad y la cabeza baja hacia los hombros esa misma distancia (`CUELLO_ACORTA` en `sesion/overlay.py`; 0 = como antes). La cabeza es 15 % más grande, creciendo hacia arriba sin cambiar el cuello (`CABEZA_ESCALA`).

## Arranque más rápido + matriz de tiempos — 2026-10-07

- **SQL en hilo aparte**: la conexión inicial ya no frena la apertura del servidor; timeout de conexión 5 → **3 s**
  (`sqlserver_timeout_s` en `datos/config.json`).
- **`UPDATE.bat` / `GYMFITX.bat` separados**: instalar dependencias ya no ocurre en cada arranque. El cambio de versión
  de Python desde el panel ahora corre `UPDATE.bat --lanzar`.
- `/api/state`, `/api/cameras`, `/api/history`, `/api/routine`, `/api/session/*` y `/api/recordings*` pasan a hilo
  (antes bloqueaban el servidor mientras esperaban SQL, la cámara o el disco). YAML con `CSafeLoader` (libyaml).
- **Matriz de tiempos** (`src/nucleo/tiempos.py`): por proceso n, última, media, p95, máx, inicio y hilo; en
  `GET /api/tiempos` y `datos/logs/tiempos_<sesión>.log`; lo ≥ 1 s marca `LENTO` también en el log de sesión.
  `scripts/perfil_arranque.py` mide imports, SQL y `/api/state`.

## Panel: crear, editar y archivar ejercicios — 2026-10-07

- Tarjeta **Rutina**: botón ➕ Nuevo, ✎ editar y 🗑 archivar por fila (diálogo con nombre, descripción, dirección y duración mín./máx.).
- **Crear** = `.yaml` + carpetas de clips/grabaciones + alta en SQL (`type`). **Editar** cambia solo datos básicos (el
  identificador no se renombra); puntos y ángulos siguen en Kpoints. Endpoint nuevo `POST /api/puntos/modificar`.
- Cambiar dirección/duración con base ya grabada avisa que hay que **regrabar la base**. Los cambios básicos no tocan SQL
  (ahí solo se guardan source/kpoints/features).
- **Archivar** (no borra): el `.yaml` pasa a `ejercicios/.respaldos/`, sale de la rutina y se conservan clips, grabaciones,
  plantilla y SQL (el `type` queda reservado). Se rechaza (409) si hay sesión activa con ese ejercicio.

## Manos eliminadas — 2026-10-07

- Se quitó **todo** el código de manos (modelo Hands, kpoints `hand_*`, ángulos de dedos, botones Izq/Der/Cruzar,
  «dedos detallados», `manos_detalle`, `invertir_manos`). El proyecto usa solo MediaPipe Pose (33 puntos).
- Medido antes de quitarlo: Pose + Manos 29,8 ms/cuadro (33,6 FPS, p95 58,2 ms) vs solo Pose 13,6 ms
  (73,3 FPS, p95 15,2 ms): −54 % por cuadro. Se borró `scripts/benchmark_manos.py`.
- **Gesto de control nuevo:** el modelo de pose no ve los dedos, así que ya no es un puño. Ahora se sostiene
  una **muñeca 1 s** en la esquina superior izquierda para grabar/detener (`sesion/gesto.py`; sale de la misma pose,
  sin modelo extra; hay que salir de la zona para repetir, con 1,5 s de espera). Tiempos y zona en las constantes
  `GESTO_*` del mismo archivo.
- `cuerpo_completo` queda con los 33 puntos de cuerpo y 10 ángulos de pose. Los ejercicios de mano
  (`mano_apertura`, `mano_der_apertura`) se archivaron en `ejercicios/.respaldos/`.
- Pestaña Kpoints: se pueden **crear** y **eliminar** ejercicios (🗑 Eliminar mueve el `.yaml` a
  `ejercicios/.respaldos/`; no toca clips, grabaciones ni SQL).
- Cortar videos: sin columna «Manos» ni botones de mano. Los clips y tablas SQL de `cuerpo_completo` hechos con puntos de
  mano deben regenerarse (Generar cortes, blanquear y generar tablas) y el clasificador reentrenarse.

## 2.4.0 — 2026-09-24 · Un solo proyecto

- La carpeta del código pasa de `gymfitx/` a `src/`: dentro de GYMFIT ya no hay una carpeta con el nombre
  del proyecto. Los imports son `from src.<rama>...`.
- Ya no se instala como paquete (`pip install -e .`): corre directo desde la carpeta del proyecto, así que
  desaparece `gymfitx.egg-info`. `pyproject.toml` queda solo con metadatos y configuración de pytest y ruff.
- README y docs muestran el árbol completo del proyecto.

## 2.3.0 — 2026-09-24 · Comparar entrenamientos

- El historial de Entrenamiento es ahora una matriz: frames, kpoints usados (numerados, p. ej. `1-5|8`),
  ángulos usados (`a-b-c`, vértice al medio), clips por clase, accuracy, F1 macro y modelo ganador.
- Cada corrida se compara con la anterior del mismo ejercicio: **▲ mejoró / ▼ empeoró / ≈ igual**
  (F1 macro; menos de 1 punto se considera ruido) y lista qué parámetros cambiaron. El aviso sale al
  terminar de entrenar y queda en `gymfitx.log`. También funciona con corridas viejas (no muestra kpoints
  ni ángulos de las que no los guardaron).
- La matriz suma F1 anidada, línea base (con la ganancia sobre ella), ± entre folds, recall de «mal» y precisión de «bien».
  «igual» ahora depende del ruido entre folds (mínimo 1 punto), no de un umbral fijo.
- `meta.json` guarda `kpoints_usados`, `angulos` y `conteo_clases`, `f1_folds`, `f1_std` y `n_features`; nuevo `angulos.catalogo()`.

## 2.2.0 — 2026-09-23 · Estandarización visual y Sistema

- Una sola paleta (la oscura de los módulos) para todo el panel, Panel y Sistema incluidos.
- Pestañas iguales: 🎥 Panel y ⚙️ Sistema con icono, mismo recuadro y tamaño que el resto.
- **Sistema concentra la configuración de datos:**
  - Base de datos: servidor y base editables; se guardan en `datos/config.json`, se aplican sin
    reiniciar y se leen al arrancar (mandan sobre las variables de entorno).
  - Tablas del dataset: lo que antes era la pestaña 🗄️ SQL.
  - Librerías de Python: una sola tabla (solicitada, instalada ✓/✗, actualizar). Se quitó la copia
    que había en Entrenamiento.

## 2.1.0 — 2026-09-23 · Árbol funcional

**Estructura**
- `gymfitx/` pasa de carpetas por "zona" (`analisis/`, `bd/`, `dataset/`, `panel/`) a un árbol por
  función: tronco `nucleo/` y ramas `almacenamiento`, `captura`, `procesamiento`, `evaluacion`,
  `sesion`, `etiquetado`, `entrenamiento`, `interfaz`, con sub-ramas donde hay más de una
  responsabilidad (`captura/fuentes`, `captura/deteccion`, `procesamiento/puntos`, `procesamiento/medidas`,
  `evaluacion/comparadores`, `interfaz/api`, `interfaz/web`).
- Módulos que hacían varias cosas se separan por función:
  `dataset_sql` (660 líneas) → almacenamiento (solo guardar/leer) + `etiquetado/tablas.py` (lógica)
  + `evaluacion/similitud.py`; `cortes` → `manifest`, `cortes`, `previews`, `exportar`;
  `entrenamiento` → `datos`, `modelos`, `validacion`, `reportes`, `entrenar`;
  `comparadores` → un módulo por comparador; `vectorizar` → `normalizacion` + `vectorizar`;
  `fuente` → `camara` + `video`; el gesto sale del pipeline (`sesion/gesto.py`);
  `panel/app.py` (763 líneas) → `control.py` + `api/` por área + `app.py` que solo arma.
- El panel web: un `.js` por pestaña en `interfaz/web/js/` (mismo orden de carga).
- Arranque: `python -m src.interfaz` (lo hace `GYMFITX.bat`).

**Calidad**
- `tests/test_capas.py`: ninguna rama importa de una posterior y no hay módulos sueltos en la raíz.
- Verificado: mismas 68 rutas del API, mismas sentencias SQL al poblar las tablas (897 de 897),
  128 tests, `ruff` limpio, panel sin errores de JS y mismo rendimiento de la cámara.

**Comportamiento:** sin cambios (pantallas, API y datos iguales).

## 2.0.0 — 2026-09-23 · Proyecto único

**Estructura**
- `core/` + `fgml/` + `apps/` pasan a ser un solo paquete, `gymfitx/`, con una carpeta por etapa:
  `captura/`, `analisis/`, `sesion/`, `bd/`, `dataset/` y `panel/`.
- `cortador.py` (800 líneas) se divide en `dataset/cortes.py`, `tablas.py`, `entrenamiento.py` y `descomposicion.py`.
- El panel (2 757 líneas en un HTML) se divide en `static/index.html`, `panel.js`, `dataset.js` y `estilos.css`.
- Todo lo que genera el uso vive en `datos/` (grabaciones, clips, entrenamientos, etiquetas, log).
  Antes estaba repartido entre la raíz y `fgml/`.
- Se instala como paquete (`pip install -e .`), así que desaparecen los `_bootstrap.py` y los `sys.path.insert`.
- `gymfitx/migrar.py` copia los datos del proyecto viejo la primera vez, sin tocarlo.

**Calidad**
- `pyproject.toml` con ruff (E, F, I, B, UP) y pytest; el código pasa `ruff check` sin avisos.
- CI en GitHub Actions: ruff + 126 tests en cada push.
- `requirements-dev.txt` para desarrollo.

**Comportamiento** (sin cambios respecto de 1.x)
- Mismas rutas del API y mismas pantallas. El modelo en vivo pasa a llamarse `clasificador`.

## 1.x — hasta 2026-09-23

Mejoras M1–M15 y D1–D14 de la revisión: SQL único, captura desacoplada (×1,9 fps), gesto con
espera, clasificador en vivo, F1 + línea base + CV anidada, botón Publicar, etc. El detalle está en
`docs/ARQUITECTURA.md`.
