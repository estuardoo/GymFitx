# `src/sesion/overlay.py`

```text
Dibujo sobre el cuadro. Lo usan por igual la app de escritorio y el panel web.

Una sola implementacion del overlay: si el panel y la ventana dibujaran cosas
distintas, comparar lo que ves con lo que registra el sistema seria imposible.
```

## Constantes

`COLOR_BONE`, `GROSOR_HUESO`, `GROSOR_PIERNA`, `_PIERNAS`, `COLOR_JOINT`, `COLOR_TEXT`, `COLOR_PANEL`, `COLOR_OK`, `COLOR_WARN`, `COLOR_BAD`, `RADIO_JUNTA`, `RADIO_JUNTA_GRANDE`, `_NARIZ`, `_HOMBRO`, `_CODO`, `_RODILLA`, `_CADERA`, `_MUNECA`, `_PULGAR`, `_INDICE`, `_MENIQUE`, `_ARTICULACIONES_GRANDES`, `_PUNTOS_CARA`, `_PUNTOS_PALMA`, `_PUNTOS_MANO_APARTE`, `_SIN_LINEA`, `CABEZA_ESCALA`, `CUELLO_ACORTA`, `GROSOR_CAPSULA`, `_PECHO_FRAC`, `_CAJA_ARRIBA_FRAC`, `_CAJA_ABAJO_FRAC`

## `score_color`

`def score_color(score: float) -> tuple[int, int, int]`

_sin docstring_

## `grosor_hueso`

`def grosor_hueso(a: int, b: int, source: str) -> int`

```text
Las piernas se dibujan mas gruesas que el resto del esqueleto en el
video: con la linea fina de siempre (2px) se pierden de vista en
pantallas grandes o con la camara lejos.
```

## `_dibujar_cabeza`

`def _dibujar_cabeza(frame: np.ndarray, pts: list[tuple[int, int]], vis, escala: float=1.0) -> None`

```text
Ovalo (base 10% mas angosta que la corona) en vez del viejo triangulo
nariz-hombro-hombro, colgado de un cuello hasta el punto medio de los
hombros si ambos son visibles.

El CENTRO de la cabeza se calcula desde la nariz, no desde los hombros:
version anterior anclaba la cabeza a un desplazamiento fijo sobre el
punto medio de los hombros, asi que giros/inclinaciones de la cabeza (que
mueven la nariz pero no necesariamente los hombros) no se veian -- la
cabeza quedaba pegada al torso en vez de seguir el movimiento real.
```

## `_rect_redondeado`

`def _rect_redondeado(frame: np.ndarray, p1: tuple[int, int], p2: tuple[int, int], radio: int, color, grosor: int) -> None`

_sin docstring_

## `_dibujar_torso`

`def _dibujar_torso(frame: np.ndarray, pts: list[tuple[int, int]], vis) -> None`

```text
Pecho (trapezoide redondeado, de hombro a media altura) + caja de
cadera (rectangulo redondeado) separados por un hueco, unidos por un
tramo corto -- la "division pecho/cadera en el ombligo" pedida.
```

## `_dibujar_palma`

`def _dibujar_palma(frame: np.ndarray, pts: list[tuple[int, int]], muneca: int, pulgar: int, indice: int, menique: int, vis) -> None`

```text
Palma aproximada con los 4 puntos que trae el PoseLandmarker (muneca +
base de pulgar/indice/menique) y "dedos" sugeridos como trazos cortos
hacia afuera. No son dedos medidos: el modelo de pose solo da muneca, menique,
indice y pulgar (en la base de cada dedo); lo que sobresale es una extension visual.
```

## `draw_landmarks`

`def draw_landmarks(frame: np.ndarray, lms: Landmarks, visibles: set[int] | None=None, cabeza_escala: float=1.0) -> None`

```text
visibles: indices a dibujar (None = todos, el comportamiento de siempre).
Es el filtro que arma el selector de regiones del cuerpo en el panel.

Esqueleto "tipo robot humanoide" -- cabeza y division pecho/cadera como
capsulas, articulaciones grandes en hombro/codo/rodilla, manos aproximadas
con palma + dedos sugeridos (el PoseLandmarker no trae nudillos).
cabeza_escala: multiplica el ovalo de la cabeza (el diagrama de Kpoints agranda la cara para poder tocar sus puntos).
```

## `draw_panel`

`def draw_panel(frame: np.ndarray, lines: list[tuple[str, tuple[int, int, int]]]) -> None`

_sin docstring_

## `draw_big_score`

`def draw_big_score(frame: np.ndarray, score: float, reps: int) -> None`

_sin docstring_

## `draw_signal_bar`

`def draw_signal_bar(frame: np.ndarray, value: float, low: float, high: float) -> None`

```text
Barra lateral con la señal 1-D y sus dos umbrales de histeresis.
```

## `draw_zona_gesto`

`def draw_zona_gesto(frame: np.ndarray, frac: float, color: tuple[int, int, int]) -> None`

```text
Tinta la esquina superior izquierda (misma zona que recorta
sesion/gesto.py) mientras hay una muneca ahi: verde
(COLOR_OK) si no se esta grabando -- sostenerla ahi inicia --, rojo
(COLOR_BAD) si ya se esta grabando -- sostenerla ahi detiene y
guarda. Solo se llama cuando hay muneca en la zona.
```

## `draw_reglas`

`def draw_reglas(frame: np.ndarray, reglas: list[dict]) -> None`

```text
Reglas de postura (nucleo/reglas.py): la recta B->A en verde si el angulo esta dentro de la
tolerancia, en rojo si no, con el angulo medido al lado.
```

