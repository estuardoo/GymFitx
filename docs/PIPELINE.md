# Pipeline paso a paso

Cada etapa tiene una entrada, una salida, un lugar en el panel y un módulo responsable.
Si algo falla, el mensaje queda en `sistema/logs/` y en el panel.

## 1. Grabar la toma de referencia

- **Panel:** elegir ejercicio → **Grabar** (o sostener una muñeca 1 s en la esquina superior izquierda, `sesion/gesto.py`).
  Sin plantilla, la toma es de *referencia*: hacer 5 repeticiones lentas.
- **Código:** `sesion/pipeline.py` → `sesion/sumideros.Recorder` → `evaluacion/plantilla.build_template`
- **Sale:** `parameters/plantillas/<ejercicio>.npz` (umbrales, μ, σ, τ) y el video en `input/raw/`.
- **Ojo:** si una grabación vieja es mejor referencia, en la lista de grabaciones está **Usar como base**.

## 2. Grabar series (puntaje en vivo)

- **Panel:** **Grabar** otra vez. Cada repetición que corta `evaluacion/segmentador.py` se puntúa
  con todos los comparadores (`evaluacion/comparadores/`). El que está elegido en el selector es
  el puntaje oficial.
- **Sale:** una fila por repetición en SQL (`reps`) y `input/raw/<n>/<id>.{mp4,npz,json}`.
- **Rendimiento:** la cámara se lee en su propio hilo. El video guarda todos los cuadros y la
  detección toma siempre el más reciente. El overlay muestra *fps cámara* y *fps detección*.

## 3. Cortar y etiquetar

- **Panel:** ✂️ **Cortar videos**. Se marcan puntos de corte con la tecla `P` y a cada segmento
  se le asigna clase con `1-9`: *bien*, *mal*, *base* o *descarte*.
- **Puntos:** el catálogo de puntos del ejercicio (`parameters/<n>/kpoints.json`) se arma en la pestaña Kpoints,
  donde también se crean y eliminan ejercicios.
- **Código:** `etiquetado/cortes.py`
- **Sale:** `parameters/inputs.json (raw[].segmentos)`. Es la única fuente de etiquetas y se guarda por mezcla, así
  que una pestaña vieja no puede borrar el trabajo de otra.

## 4. Exportar clips

- **Panel:** **⬇ Generar cortes**.
- **Código:** `etiquetado/exportar.py` → `procesamiento/offline.py` detecta los kpoints en cada
  cuadro del video (pose), con la misma función que el vivo
  (`procesamiento/puntos/kpoints.resolver`).
- **Sale:** `input/bronze/<n>/<id>.{mp4,npz}` + `parameters/inputs.json (tabla clips)`. Los videos cuyos
  cortes no cambiaron se saltan.

## 5. Subir a SQL Server

- **Panel:** ⚙️ **Sistema → Tablas del dataset** (el servidor se elige arriba, en Base de datos). Se elige el ejercicio, la normalización (rectángulo 100×100 o punto de
  referencia) y los cuadros fijos. Después **Generar / actualizar tablas** (también corre solo al exportar).
- **Código:** `etiquetado/tablas.poblar_desde_manifest` (lógica) → `almacenamiento/dataset_sql.py`
  (solo guarda), con la preparación de `procesamiento/puntos/`.
- **Sale:** `table_file`, `table_frames` (crudo), `table_frames_fix` (normalizado, lo que se
  entrena) e `table_indicator` (parecido contra el clip *base*).

## 6. Entrenar

- **Panel:** 🧠 **Entrenamiento**. Se elige el ejercicio, las features (puntos, ángulos o
  ambos), el % de test y los modelos. Se pueden desmarcar clips mal etiquetados.
- **Código:** `entrenamiento/entrenar.py` (datos → modelos + validación → reportes)
- **Criterio:** gana el de mayor **F1 macro**. Hay que compararlo con la **línea base** (predecir
  siempre la clase más común). El número honesto para reportar es el de **CV anidada**.
- **Sale:** `output/models/<n>/run_NNN/` con `modelo.joblib` (incluye su *spec*), `meta.json`,
  la comparación de modelos, la matriz de confusión y la curva ROC.
- **Comparar corridas:** el historial muestra frames, kpoints, ángulos, clips por clase, accuracy, F1 y ganador de cada
  corrida, y si **mejoró / empeoró** frente a la anterior del mismo ejercicio (`entrenamiento/reportes.comparar`).

## 7. Puntuar en vivo con el modelo

- **Panel:** en el selector de modelo, **Clasificador entrenado**.
- **Código:** `evaluacion/comparadores/clasificador.buscar_clasificador` toma el último `run_N` del ejercicio
  (o del indicado en `clasificador` de la definición). `sesion/pipeline.set_kpoints_vivo` arma los
  mismos puntos en vivo y `procesamiento/puntos/vectorizar.vector_de_clip` construye el mismo vector.
- **Puntaje:** probabilidad de *bien* (0-100) y clase predicha. Si en una repetición no se vio el
  cuerpo, cae al DTW en vez de inventar un número.

## Análisis adicional

- **🔬 Descomposición** (`entrenamiento/descomposicion.py`): series x/y por punto e indicador R² con
  DTW de cada clip contra el *base*.
- **🏆 Ranking**: corridas ordenadas por F1 macro.
- **Sin panel:** `python scripts/reprocesar.py --video ...` vuelve a pasar un video por el
  pipeline con otra definición o umbral.
