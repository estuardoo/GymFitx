# `src/sesion/sumideros.py`

```text
Bus de eventos y sumideros: el extremo final del pipeline.

Viven aparte de pipeline.py por una razon concreta: aqui no se importa
mediapipe. Asi los sumideros, el bus y sus tests se pueden usar sin la pila de
vision instalada, igual que types.py.
```

## class `EventBus`

```text
Un solo flujo de eventos, consumido por igual por la ventana y el panel web.
```

### `EventBus.__init__`

`def __init__(self) -> None`

_sin docstring_

### `EventBus.subscribe`

`def subscribe(self, fn: Callable[[Evento], None]) -> None`

_sin docstring_

### `EventBus.emit`

`def emit(self, evento: Evento) -> None`

_sin docstring_

## class `Sink`

_sin docstring_

### `Sink.on_start`

`def on_start(self, pipe: Pipeline) -> None`

_sin docstring_

### `Sink.on_raw_frame`

`def on_raw_frame(self, pipe: Pipeline, frame: Frame) -> None`

_sin docstring_

### `Sink.on_frame`

`def on_frame(self, pipe: Pipeline, frame: Frame, fv: FeatureVec | None) -> None`

_sin docstring_

### `Sink.on_rep`

`def on_rep(self, pipe: Pipeline, seg: Segment) -> None`

_sin docstring_

### `Sink.on_stop`

`def on_stop(self, pipe: Pipeline) -> None`

_sin docstring_

## class `MultiSink`

```text
Reparte los eventos a varios sumideros en orden.

Es lo que permite que archivar el video sea un sumidero mas y no una rama
dentro del pipeline: grabar base + archivar, o evaluar + archivar, son la
misma composicion.
```

### `MultiSink.__init__`

`def __init__(self, *sinks: Sink) -> None`

_sin docstring_

### `MultiSink.find`

`def find(self, tipo)`

_sin docstring_

### `MultiSink.on_start`

`def on_start(self, pipe)`

_sin docstring_

### `MultiSink.on_raw_frame`

`def on_raw_frame(self, pipe, frame)`

_sin docstring_

### `MultiSink.on_frame`

`def on_frame(self, pipe, frame, fv)`

_sin docstring_

### `MultiSink.on_rep`

`def on_rep(self, pipe, seg)`

_sin docstring_

### `MultiSink.on_stop`

`def on_stop(self, pipe)`

_sin docstring_

## class `Recorder`

```text
Modo grabacion: acumula la toma y al cerrar construye la plantilla.
```

### `Recorder.__init__`

`def __init__(self, out_path, radius_frac: float=0.15) -> None`

_sin docstring_

### `Recorder.on_frame`

`def on_frame(self, pipe: Pipeline, frame: Frame, fv: FeatureVec | None) -> None`

_sin docstring_

### `Recorder.on_stop`

`def on_stop(self, pipe: Pipeline) -> None`

_sin docstring_

## class `Evaluator`

```text
Modo evaluacion: puntua cada repeticion y la registra.

Corre TODOS los modelos de src/evaluacion/comparadores/ en cada repeticion (son
baratos: milisegundos) para poder comparar puntaje y tiempo entre
arquitecturas con la misma toma. Solo el modelo activo (`modelo`) decide
el puntaje "oficial" que se guarda y que mueve el semaforo del panel.
```

### `Evaluator.__init__`

`def __init__(self, template: Template, storage=None, target_reps: int=0, session_id: int | None=None, modelo: str=scorers.DEFAULT_MODEL, clasificador: scorers.Clasificador | None=None) -> None`

_sin docstring_

### `Evaluator.n`

`def n(self) -> int`

_sin docstring_

### `Evaluator.on_rep`

`def on_rep(self, pipe: Pipeline, seg: Segment) -> None`

_sin docstring_

## class `Contador`

```text
Vista previa con camara prendida: cuenta cada repeticion (con la base) y, si hay modelo entrenado, la clasifica,
sin guardar nada (storage=None). Es lo que deja ver en el panel si el modelo esta contando.
```

### `Contador.__init__`

`def __init__(self, template: Template, clasificador: scorers.Clasificador | None=None, modelo: str=scorers.CLAVE_CLASIFICADOR) -> None`

_sin docstring_

## class `ContadorModelo`

```text
Vista previa que cuenta ciclos SOLO con el modelo entrenado (clase "fuera" + ventana deslizante): no
necesita base ni umbrales. Emite el mismo evento "rep" que Evaluator.
```

### `ContadorModelo.__init__`

`def __init__(self, clasificador: scorers.Clasificador) -> None`

_sin docstring_

### `ContadorModelo.on_frame`

`def on_frame(self, pipe: Pipeline, frame: Frame, fv: FeatureVec | None) -> None`

_sin docstring_

