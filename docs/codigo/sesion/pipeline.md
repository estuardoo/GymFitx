# `src/sesion/pipeline.py`

```text
Orquestacion. El corazon del diseño: UN pipeline, sumideros intercambiables.

Grabar la plantilla y evaluar una serie recorren exactamente las mismas capas
1 a 5. Lo unico que cambia es el sumidero del final. Es lo que garantiza que la
plantilla grabada y la repeticion evaluada se midan con la misma vara: no hay
dos rutas que puedan desincronizarse porque no hay dos rutas.

En modo grabacion no hay segmentador: todavia no existen umbrales. La toma se
segmenta despues, offline, con los umbrales que la propia toma produce.

Pausa: la camara sigue entregando cuadros mientras el usuario tiene la sesion
en pausa (no se puede pausar el sensor), pero esos cuadros no llegan a ningun
lado: no se trackean, no se archivan y no cuentan repeticiones. El tiempo que
dura la pausa se resta de la linea de tiempo que ven el filtro, el segmentador
y el archivador (`_pause_offset_ms`), asi que al reanudar todo continua como
si la pausa nunca hubiera existido -- sin saltos en el video archivado ni
sobresaltos en el filtro por un dt gigante.

Rendimiento (camara en vivo). Dos hilos, cada uno a su ritmo:
  captura    lee la camara a sus fps reales, escribe el video (on_raw_frame)
             y pinta la vista previa con la ultima deteccion disponible.
  deteccion  toma SIEMPRE el cuadro mas reciente (descarta los que no alcanza)
             y corre la pose (33 puntos); el gesto de control sale de esa misma pose.
Antes todo era un solo hilo en serie: la grabacion quedaba a ~7 fps con 70 %
de cuadros congelados. Con un video (VideoSource, tests) se sigue procesando
cuadro por cuadro en orden, para que el resultado sea repetible.
```

## class `Pipeline`

```text
Capas 1-6 encadenadas. No decide nada: obedece al Exercise y al Sink.
```

### `Pipeline.__init__`

`def __init__(self, exercise, source, sink: Sink, template: Template | None=None, bus: EventBus | None=None, annotate: bool=True) -> None`

_sin docstring_

### `Pipeline.sink_of`

`def sink_of(self, tipo)`

```text
El sumidero de este tipo, este solo o dentro de un MultiSink.
```

### `Pipeline.grabando`

`def grabando(self) -> bool`

```text
True si el sumidero actual ya no es el placeholder de
previsualizacion. OJO: tiene que ser 'type(...) is Sink', NO
'isinstance(..., Sink)' -- Recorder/Evaluator/MultiSink heredan de
Sink, asi que isinstance() da True para TODOS los sumideros
(grabando o no) y nunca distingue nada.
```

### `Pipeline.set_template`

`def set_template(self, template: Template) -> None`

```text
Instala o reemplaza la plantilla de esta sesion sin reabrir la
camara: reconstruye el segmentador con los nuevos umbrales.

Es lo que permite, dentro de la MISMA sesion de camara, grabar la
base de un ejercicio que todavia no tenia y evaluar contra ella acto
seguido -- sin apagar y volver a prender.
```

### `Pipeline.set_exercise`

`def set_exercise(self, exercise, template: Template | None=None) -> None`

```text
Cambia de ejercicio SIN reabrir la camara: reconstruye tracker,
extractor y filtro para el ejercicio nuevo . Es lo que permite elegir otro de la lista de rutina
con la camara ya prendida, sin el corte de apagar/prender.

El tracker nuevo se arma ANTES de tomar el lock (puede tardar
milisegundos en crear el landmarker) para no bloquear el hilo de
captura mientras tanto; el swap de referencias es rapido y atomico
bajo el lock, y el tracker viejo se cierra DESPUES de soltarlo.
```

### `Pipeline.set_fps`

`def set_fps(self, fps: int) -> bool`

```text
Delega en la fuente si sabe hacerlo en caliente (solo CameraSource;
VideoSource no tiene FPS que pedir). Ver CameraSource.set_fps.
```

### `Pipeline.set_regiones`

`def set_regiones(self, nombres: list[str] | None) -> None`

```text
Cambia en caliente que partes del cuerpo se dibujan en el video,
sin reabrir la camara ni tocar la deteccion (el modelo pose sigue
midiendo el cuerpo entero; esto solo filtra el dibujo). None = todas.
```

### `Pipeline.set_kpoints_vivo`

`def set_kpoints_vivo(self, catalogo: list[dict] | None) -> None`

```text
Arma en cada cuadro los kpoints de 'catalogo' (el del modelo
entrenado, asi el orden de los puntos es el mismo que vio al
entrenar). None/[] = apagado.
```

### `Pipeline.swap_sink`

`def swap_sink(self, nuevo: Sink) -> Sink`

```text
Cambia el sumidero sin detener la camara ni el hilo del pipeline.

Cierra el sumidero anterior (on_stop) antes de instalar el nuevo, asi
que quien llama puede leer sus resultados (plantilla, rutas de video)
en el valor devuelto. Esto es lo que separa "prender la camara" de
"grabar": los dos corren el mismo pipeline, solo cambia que hace cada
sumidero con los cuadros. El lock evita que on_stop() se cruce con un
on_frame() todavia en marcha en el hilo de captura (p.ej. el
VideoWriter cerrandose a mitad de una escritura).

Si el sumidero anterior revienta al cerrar (p.ej. VideoLogger si el
disco falla a mitad de escritura), el swap AL SUMIDERO NUEVO tiene
que pasar igual: si no, "detener grabacion" queda trabado en el
sumidero viejo -- se ve el aviso de "grabando" pero cerrar/guardar
nunca ocurre, porque la excepcion nunca llega a nadie (el gesto la
dispara desde el bus, que traga cualquier excepcion del que escucha).
El error se avisa por el bus en vez de perderse en silencio.
```

### `Pipeline.latest_frame`

`def latest_frame(self)`

_sin docstring_

### `Pipeline.is_paused`

`def is_paused(self) -> bool`

_sin docstring_

### `Pipeline.pause`

`def pause(self) -> None`

_sin docstring_

### `Pipeline.resume`

`def resume(self) -> None`

_sin docstring_

### `Pipeline.run`

`def run(self, should_stop: Callable[[], bool] | None=None) -> None`

_sin docstring_

### `Pipeline._run_en_vivo`

`def _run_en_vivo(self, should_stop: Callable[[], bool]) -> None`

```text
Hilo de captura (camara -> video + vista previa) separado del de
deteccion (este), que siempre toma el cuadro mas reciente.
```

### `Pipeline._entrada`

`def _entrada(self, frame: Frame) -> Frame | None`

```text
Pausa + linea de tiempo + video (on_raw_frame). Devuelve el cuadro
con el tiempo ya ajustado, o None si la sesion esta en pausa.
```

### `Pipeline._procesar`

`def _procesar(self, frame: Frame) -> None`

```text
Un paso completo en serie (videos y tests): entrada + deteccion.
```

### `Pipeline._detectar`

`def _detectar(self, frame: Frame) -> None`

_sin docstring_

### `Pipeline.n_conteo`

`def n_conteo(self) -> int`

```text
Repeticiones contadas: UNA sola cifra para el video, el contador del panel y el evento de estado.
```

### `Pipeline._evaluar_reglas`

`def _evaluar_reglas(self, detecciones, frame: Frame) -> list[dict]`

_sin docstring_

### `Pipeline._anotar_pausado`

`def _anotar_pausado(self, frame: Frame) -> None`

```text
Mientras esta en pausa: se sigue viendo la camara, pero marcada.
```

### `Pipeline._anotar`

`def _anotar(self, frame: Frame, detecciones, fv: FeatureVec | None) -> None`

_sin docstring_

### `Pipeline._emitir_estado`

`def _emitir_estado(self, fv: FeatureVec | None, n_det: int) -> None`

_sin docstring_

