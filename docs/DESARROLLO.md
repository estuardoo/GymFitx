# Guía de desarrollo

> Detalle técnico (estructura, regla del árbol, variables de entorno). La presentación del proyecto está en [../README.md](../README.md).

Coach de movimiento por cámara (MediaPipe + Python). En vivo detecta el cuerpo (33 puntos de MediaPipe Pose), cuenta
repeticiones y puntúa cada una. Con las grabaciones se arma un dataset (clips *bien / mal*
en SQL Server) y se entrena un clasificador que después **puntúa en vivo**.

Un solo sistema con una rama por función: cada etapa tiene sus propios módulos y
solo usa las anteriores.

## Arrancar

```
UPDATE.bat      (una vez, y cuando cambie requirements.txt)
GYMFITX.bat     (a diario: no instala nada)
```

`UPDATE.bat` crea `.venv`, instala `requirements.txt` y, al terminar bien, abre `GYMFITX.bat`. `GYMFITX.bat` solo ejecuta: copia tus datos
desde `..\GYMFITX` la primera vez (sin tocar el proyecto viejo) y abre http://127.0.0.1:8000.

Si algo tarda: `GET /api/tiempos` o `sistema/logs/tiempos_*.log` muestran la matriz de tiempos por
proceso (imports, SQL, `/api/state`, cada ruta); `python scripts/perfil_arranque.py` mide el arranque.

Requisitos: Windows, Python 3.11 o 3.12 y una webcam. SQL Server es opcional para la cámara,
pero el historial y el dataset lo necesitan (`pyodbc` + *ODBC Driver 17/18*). Si no responde,
el panel arranca igual y las repeticiones esperan en `sistema/pendientes_sql.jsonl`.

## El pipeline

```
 cámara ─► captura ─► procesamiento ─► evaluacion ─► sesion ──► puntaje por repetición
                                                          │
                                                          └─► input/raw ─► etiquetado ─► almacenamiento (SQL) ─► entrenamiento
                                                                                                                           │
                                          evaluacion/comparadores/clasificador ◄── output/models/<n>/run_NNN ◄───────────┘
```

| # | Etapa | Dónde (panel) | Código | Resultado |
|---|---|---|---|---|
| 1 | Grabar la referencia (5 reps) | Panel → Grabar | `sesion/`, `evaluacion/plantilla.py` | `parameters/plantillas/` |
| 2 | Grabar series | Panel → Grabar | `sesion/`, `evaluacion/` | puntaje por rep + `input/raw/` |
| 3 | Cortar y etiquetar | ✂️ Cortar videos | `etiquetado/cortes.py` | `parameters/inputs.json (raw[].segmentos)` |
| 4 | Exportar clips | ⬇ Generar cortes | `etiquetado/exportar.py`, `procesamiento/offline.py` | `input/bronze/<n>/` |
| 5 | Subir a SQL | ⚙️ Sistema → Tablas del dataset | `etiquetado/tablas.py` → `almacenamiento/dataset_sql.py` | `table_frames_fix` |
| 6 | Entrenar | 🧠 Entrenamiento | `entrenamiento/entrenar.py` | `output/models/<n>/run_NNN/` |
| 7 | Puntuar en vivo | Panel → modelo "Clasificador entrenado" | `evaluacion/comparadores/clasificador.py` | P(bien) por rep |

El detalle de cada etapa está en [docs/PIPELINE.md](PIPELINE.md) y el diseño en
[docs/ARQUITECTURA.md](ARQUITECTURA.md).

## Estructura

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
├─ input/               raw → bronze → plate → gold, por número de ejercicio (fuera de git; ver docs/ESTRUCTURA_DATOS.md)
├─ output/              models/<n>/run_NNN y reportes/
├─ parameters/          exercise.json · inputs.json (tablas raw y clips) · config.json · server.json · <n>/kpoints.json
├─ sistema/             estado de ejecución: logs, SQL, previews (fuera de git)
├─ assets/              modelos de MediaPipe + cloudflared.exe (se descargan solos)
├─ scripts/ (hpc/ = cluster)  tests/  docs/ (incl. CHANGELOG.md)
└─ GYMFITX.bat · UPDATE.bat · requirements*.txt · pyproject.toml · README.md
```

**Regla del árbol:** cada rama importa solo del tronco o de ramas anteriores, en este orden:
`nucleo → almacenamiento → captura → procesamiento → evaluacion → sesion → etiquetado → preparacion → entrenamiento → interfaz`.
`tests/test_capas.py` falla si alguien la rompe (y si aparece un módulo suelto en la raíz).

```
scripts/           grabar, evaluar, reprocesar, comparar_esquemas, camara (sin panel); scripts/hpc/ = busqueda de features en el cluster
tests/             pytest (sin cámara, sin SQL Server, MediaPipe simulado) + test_capas
docs/              ARQUITECTURA.md, PIPELINE.md, pitch/
input/  output/  sistema/  assets/      generados por el uso (fuera de git)
```

## Documentación

`docs/codigo/` (generada del código: `python scripts/generar_docs_codigo.py`) · `docs/decisiones/` (por qué) · `docs/diccionario/` (columnas) · `docs/GUIA_ETAPA3.md` (DVC, GitHub y verificación CRISP-DM).

## Publicar en internet

Se activa en **Sistema → Publicar en internet** y viene apagado. Abre un enlace de
Cloudflare que pide usuario y clave. Desde internet no se puede apagar el panel ni tocar
la configuración.

## Desarrollo

```
pip install -r requirements.txt
pip install -e . --no-deps
ruff check .        # estilo
pytest              # incluye la regla del árbol y la trazabilidad de decisiones
```

GitHub Actions corre los controles en cada push y Pull Request (`.github/workflows/reproducir.yml`).

El servidor y la base de SQL Server se cambian en **⚙️ Sistema → Base de datos** y quedan en
`parameters/server.json`, que manda al arrancar. Si ese archivo no existe se usan las variables. Para una PC nueva, sin tocar codigo, agrega en `parameters/server.json` la clave `servidores_por_pc` (ej. `{"NOMBRE_PC": "SERVIDOR\\INSTANCIA"}`). Orden de precedencia del servidor: `parameters/server.json` (Sistema) → variable `GYMFITX_SQLSERVER_HOST` → `servidores_por_pc` (incluido el de fabrica) → `PROGRAM\HYPER`:

| Variable de entorno | Por defecto |
|---|---|
| `GYMFITX_SQLSERVER_HOST` | según la PC: `HYPERCUBE\SERVER`, `PROGRAM\HYPER` |
| `GYMFITX_SQLSERVER_DB` | `GymFitX` |
| `GYMFITX_PORT` | `8000` |
| `GYMFITX_DATOS` | `sistema/` |
