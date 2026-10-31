# `src/interfaz/control.py`

```text
Estado del panel: la sesion de camara (una sola, hay una sola camara), el historial y el log de eventos.

Las rutas de interfaz/api/ solo llaman a esto.
```

## Constantes

`_LOGEAR`

## `plantilla_valida`

`def plantilla_valida(ex, ruta)`

```text
(Template | None, motivo). La base grabada solo sirve si sus features son las del ejercicio, en el mismo
orden: si se editaron las filas de la definicion (Kpoints), medir contra ella daria puntajes sin sentido.
```

## `_al_bus_archivo`

`def _al_bus_archivo(evento: dict) -> None`

_sin docstring_

## class `Session`

_sin docstring_

### `Session.__init__`

`def __init__(self) -> None`

_sin docstring_

### `Session._preparar_clasificador`

`def _preparar_clasificador(self, ex) -> None`

```text
Carga el ultimo modelo entrenado (pestana Entrenamiento) para este
ejercicio, si hay, y prende los kpoints en vivo que necesita.
```

### `Session._instalar_preview`

`def _instalar_preview(self) -> None`

```text
Camara prendida sin grabar. Modelo con clase "fuera": cuenta solo con el modelo (ContadorModelo);
si no, con base + modelo cuenta por segmentacion y clasifica (Contador); si no, Sink vacio.
```

### `Session.set_clasificador`

`def set_clasificador(self, run: str) -> dict`

```text
Cambia el entrenamiento (output/models/<n>/run_NNN, p.ej. '1/run_001') que clasifica en vivo, sin apagar la camara.
```

### `Session.activa`

`def activa(self) -> bool`

_sin docstring_

### `Session.camera_on`

`def camera_on(self, slug: str, camera: int, mirror: bool, reps: int, archivar: bool, video: bool, fps: int=30, regiones: list[str] | None=None, droidcam: str | None=None) -> dict`

```text
Prende la camara en modo previsualizacion: esqueleto en vivo (y el
umbral si ya existe una base), nada se guarda todavia. No hace falta
que el ejercicio ya tenga base -- si no la tiene, 'grabar_iniciar'
graba la primera toma como base; si ya la tiene, la evalua. La camara
no se reabre entre un caso y otro.
```

### `Session.set_persona`

`def set_persona(self, persona: str | None) -> dict`

```text
Con quien se graba. 'P1'..'Pn' o vacio (sin persona). Vale para las proximas grabaciones, incluso con el gesto.
```

### `Session.grabar_iniciar`

`def grabar_iniciar(self) -> dict`

_sin docstring_

### `Session.grabar_detener`

`def grabar_detener(self) -> dict`

```text
Detiene solo la toma actual: la camara sigue prendida para otra.
```

### `Session._resultados_de`

`def _resultados_de(sink) -> dict`

```text
Extrae plantilla/puntajes/rutas de un sumidero ya cerrado (on_stop
llamado), este solo o dentro de un MultiSink. Lo usan tanto apagar la
camara del todo como detener solo la toma en curso.
```

### `Session.stop`

`def stop(self) -> dict`

```text
Apaga la camara del todo. Si se estaba grabando, el 'finally' de
Pipeline.run() ya cerro ese sumidero (lo archivo) antes de que el
hilo termine: apagar a mitad de una toma no pierde el video.
```

### `Session.pause`

`def pause(self) -> dict`

_sin docstring_

### `Session.resume`

`def resume(self) -> dict`

_sin docstring_

### `Session.set_fps`

`def set_fps(self, fps: int) -> dict`

```text
Intenta cambiar el FPS en caliente. Si el driver no lo acepta
(aplicado=False), el panel reabre la camara del lado del navegador.
```

### `Session.set_exercise`

`def set_exercise(self, slug: str) -> dict`

```text
Cambia de ejercicio con la camara ya prendida, sin reabrirla (ver
Pipeline.set_exercise). No permitido a mitad de una grabacion: hay
que detenerla primero, si no la toma quedaria mezclando dos ejercicios.
```

### `Session.overlay_regiones`

`def overlay_regiones(self, regiones: list[str] | None) -> dict`

```text
Cambia en caliente que partes del cuerpo se dibujan, sin apagar
la camara (ver Pipeline.set_regiones).
```

### `Session.set_modelo`

`def set_modelo(self, modelo: str) -> dict`

```text
Elige que modelo de comparacion se usa como puntaje oficial en la
proxima evaluacion (Evaluator ya en curso no cambia a mitad de toma).
```

### `Session.estado`

`def estado(self) -> dict`

_sin docstring_

## `_al_bus_gestos`

`def _al_bus_gestos(evento: dict) -> None`

```text
El gesto (muneca en la esquina) alterna grabar/detener, igual que los
botones: si no se esta grabando, inicia; si ya se esta grabando, detiene
(y guarda). Corre en el hilo de captura (lo emite sesion/gesto.py
ahi mismo); EventBus.emit traga cualquier excepcion de aca para que un
gesto mal disparado nunca tumbe la sesion de camara -- pero eso tambien
significa que si esto revienta, no se ve en ningun lado: por eso el
try/except propio, solo para dejar rastro en el log de sesion.
```

