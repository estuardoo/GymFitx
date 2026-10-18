"""Dibujo sobre el cuadro. Lo usan por igual la app de escritorio y el panel web.

Una sola implementacion del overlay: si el panel y la ventana dibujaran cosas
distintas, comparar lo que ves con lo que registra el sistema seria imposible.
"""

from __future__ import annotations

import cv2
import numpy as np

from src.nucleo.landmarks import POSE_CONNECTIONS, region_indices, resolve
from src.nucleo.tipos import Landmarks

COLOR_BONE = (210, 210, 210)
GROSOR_HUESO = 2
GROSOR_PIERNA = 5   # el trazo fino se pierde de vista en pantallas grandes / camara lejos
_PIERNAS = region_indices(["piernas"])
COLOR_JOINT = (0, 220, 255)
COLOR_TEXT = (245, 245, 245)
COLOR_PANEL = (28, 28, 28)
COLOR_OK = (120, 230, 120)
COLOR_WARN = (60, 190, 255)
COLOR_BAD = (90, 90, 240)

RADIO_JUNTA = 3
RADIO_JUNTA_GRANDE = RADIO_JUNTA * 3   # hombro/codo/rodilla: se ven mejor de lejos

# --- geometria "robot humanoide" del esqueleto de cuerpo completo (pose) ---
# El PoseLandmarker (33 puntos) no trae ni ojos/orejas/nariz utiles para
# dibujar una cara, ni nudillos de los dedos: con esos puntos sueltos la
# cabeza terminaba siendo un triangulo y las manos, puntos flotando sin
# forma. Estas formas (capsulas de cabeza/torso, palma aproximada) usan
# esos mismos puntos de otra manera, sin agregar ningun modelo nuevo.
_idx = lambda nombre: resolve(nombre, "pose")  # noqa: E731

_NARIZ = _idx("NOSE")
_HOMBRO = (_idx("LEFT_SHOULDER"), _idx("RIGHT_SHOULDER"))
_CODO = (_idx("LEFT_ELBOW"), _idx("RIGHT_ELBOW"))
_RODILLA = (_idx("LEFT_KNEE"), _idx("RIGHT_KNEE"))
_CADERA = (_idx("LEFT_HIP"), _idx("RIGHT_HIP"))
_MUNECA = (_idx("LEFT_WRIST"), _idx("RIGHT_WRIST"))
_PULGAR = (_idx("LEFT_THUMB"), _idx("RIGHT_THUMB"))
_INDICE = (_idx("LEFT_INDEX"), _idx("RIGHT_INDEX"))
_MENIQUE = (_idx("LEFT_PINKY"), _idx("RIGHT_PINKY"))

_ARTICULACIONES_GRANDES = set(_HOMBRO + _CODO + _RODILLA)
_PUNTOS_CARA = {_idx(n) for n in (
    "NOSE", "LEFT_EYE_INNER", "LEFT_EYE", "LEFT_EYE_OUTER",
    "RIGHT_EYE_INNER", "RIGHT_EYE", "RIGHT_EYE_OUTER",
    "LEFT_EAR", "RIGHT_EAR", "MOUTH_LEFT", "MOUTH_RIGHT",
)}
_PUNTOS_PALMA = set(_PULGAR + _INDICE + _MENIQUE)
_PUNTOS_MANO_APARTE = _PUNTOS_PALMA | set(_MUNECA)  # los dibuja _dibujar_palma, no el loop generico

# el viejo "triangulo" cabeza-hombros ya no se dibuja como linea recta (la
# cabeza es su propia capsula, ver _dibujar_cabeza), y el torso tampoco es ya
# un trapezoide de una sola pieza (ver _dibujar_torso: pecho + caja de cadera).
_SIN_LINEA = {
    (_idx("MOUTH_LEFT"), _idx("MOUTH_RIGHT")),
    (_NARIZ, _HOMBRO[0]),
    (_NARIZ, _HOMBRO[1]),
    (_HOMBRO[0], _HOMBRO[1]),
    (_HOMBRO[0], _CADERA[0]),
    (_HOMBRO[1], _CADERA[1]),
    (_CADERA[0], _CADERA[1]),
}


def score_color(score: float) -> tuple[int, int, int]:
    if score >= 85:
        return COLOR_OK
    if score >= 65:
        return COLOR_WARN
    return COLOR_BAD


def grosor_hueso(a: int, b: int, source: str) -> int:
    """Las piernas se dibujan mas gruesas que el resto del esqueleto en el
    video: con la linea fina de siempre (2px) se pierden de vista en
    pantallas grandes o con la camara lejos.
    """
    if source == "pose" and a in _PIERNAS and b in _PIERNAS:
        return GROSOR_PIERNA
    return GROSOR_HUESO


CABEZA_ESCALA = 1.15   # tamano del ovalo de la cabeza (1 = como antes)
CUELLO_ACORTA = 0.5   # fraccion del cuello que se quita (0 = como antes, 0.5 = mitad)


def _dibujar_cabeza(frame: np.ndarray, pts: list[tuple[int, int]], vis, escala: float = 1.0) -> None:
    """Ovalo (base 10% mas angosta que la corona) en vez del viejo triangulo
    nariz-hombro-hombro, colgado de un cuello hasta el punto medio de los
    hombros si ambos son visibles.

    El CENTRO de la cabeza se calcula desde la nariz, no desde los hombros:
    version anterior anclaba la cabeza a un desplazamiento fijo sobre el
    punto medio de los hombros, asi que giros/inclinaciones de la cabeza (que
    mueven la nariz pero no necesariamente los hombros) no se veian -- la
    cabeza quedaba pegada al torso en vez de seguir el movimiento real.
    """
    if not vis(_NARIZ):
        return
    nariz = pts[_NARIZ]
    hombros_ok = vis(_HOMBRO[0]) and vis(_HOMBRO[1])
    if hombros_ok:
        mid_hombro = ((pts[_HOMBRO[0]][0] + pts[_HOMBRO[1]][0]) // 2,
                      (pts[_HOMBRO[0]][1] + pts[_HOMBRO[1]][1]) // 2)
        ancho_ref = abs(pts[_HOMBRO[1]][0] - pts[_HOMBRO[0]][0]) or 40
    else:
        mid_hombro, ancho_ref = nariz, 90  # sin hombros, tamano fijo razonable

    ancho = max(int(ancho_ref * 0.42), 10)
    alto = int(ancho * 1.35)
    rx, ry = ancho // 2, alto // 2
    # la nariz esta cerca de la base de la cara (no del centro): subimos
    # desde ahi para que el ovalo la rodee y se mueva con ella.
    centro = (nariz[0], int(nariz[1] - ry * 0.6))
    if hombros_ok:
        # cuello a la mitad: la cabeza baja hacia los hombros lo que se acorta (sigue la inclinacion)
        dx, dy = mid_hombro[0] - centro[0], mid_hombro[1] - (centro[1] + ry)
        if dy > 0:
            centro = (int(centro[0] + dx * CUELLO_ACORTA), int(centro[1] + dy * CUELLO_ACORTA))
    # cabeza 15% mas grande, creciendo hacia arriba: la base (y el cuello) quedan donde estaban
    rx, ry_nuevo = int(rx * CABEZA_ESCALA * escala), int(ry * CABEZA_ESCALA * escala)
    centro = (centro[0], centro[1] - (ry_nuevo - ry))
    ry = ry_nuevo

    cv2.ellipse(frame, centro, (rx, ry), 0, 180, 360, COLOR_BONE, GROSOR_HUESO, cv2.LINE_AA)
    cv2.ellipse(frame, centro, (int(rx * 0.9), ry), 0, 0, 180, COLOR_BONE, GROSOR_HUESO, cv2.LINE_AA)
    if hombros_ok:
        base = (centro[0], centro[1] + ry)
        cv2.line(frame, base, mid_hombro, COLOR_BONE, GROSOR_HUESO * 2, cv2.LINE_AA)


GROSOR_CAPSULA = GROSOR_HUESO * 2   # pecho/cadera se ven como piezas, no como huesos finos
_PECHO_FRAC = 0.42     # donde termina el trapezoide del pecho, bajando de hombro a cadera
_CAJA_ARRIBA_FRAC = 0.58   # donde empieza la caja de cadera, bajando de hombro a cadera
_CAJA_ABAJO_FRAC = 0.88    # donde termina -- <1.0 a proposito: deja hueco antes
                            # de la cadera real, para que la pierna no arranque
                            # pegada al borde de la caja (se conecta con un
                            # tramo corto, ver mas abajo)


def _rect_redondeado(frame: np.ndarray, p1: tuple[int, int], p2: tuple[int, int],
                      radio: int, color, grosor: int) -> None:
    (x1, y1), (x2, y2) = p1, p2
    radio = max(1, min(radio, abs(x2 - x1) // 2, abs(y2 - y1) // 2))
    cv2.line(frame, (x1 + radio, y1), (x2 - radio, y1), color, grosor, cv2.LINE_AA)
    cv2.line(frame, (x1 + radio, y2), (x2 - radio, y2), color, grosor, cv2.LINE_AA)
    cv2.line(frame, (x1, y1 + radio), (x1, y2 - radio), color, grosor, cv2.LINE_AA)
    cv2.line(frame, (x2, y1 + radio), (x2, y2 - radio), color, grosor, cv2.LINE_AA)
    cv2.ellipse(frame, (x1 + radio, y1 + radio), (radio, radio), 0, 180, 270, color, grosor, cv2.LINE_AA)
    cv2.ellipse(frame, (x2 - radio, y1 + radio), (radio, radio), 0, 270, 360, color, grosor, cv2.LINE_AA)
    cv2.ellipse(frame, (x1 + radio, y2 - radio), (radio, radio), 0, 90, 180, color, grosor, cv2.LINE_AA)
    cv2.ellipse(frame, (x2 - radio, y2 - radio), (radio, radio), 0, 0, 90, color, grosor, cv2.LINE_AA)


def _dibujar_torso(frame: np.ndarray, pts: list[tuple[int, int]], vis) -> None:
    """Pecho (trapezoide redondeado, de hombro a media altura) + caja de
    cadera (rectangulo redondeado) separados por un hueco, unidos por un
    tramo corto -- la "division pecho/cadera en el ombligo" pedida.
    """
    if not (vis(_HOMBRO[0]) and vis(_HOMBRO[1]) and vis(_CADERA[0]) and vis(_CADERA[1])):
        return
    hombro_i, hombro_d = np.array(pts[_HOMBRO[0]]), np.array(pts[_HOMBRO[1]])
    cadera_i, cadera_d = np.array(pts[_CADERA[0]]), np.array(pts[_CADERA[1]])

    pecho_i = hombro_i + _PECHO_FRAC * (cadera_i - hombro_i)
    pecho_d = hombro_d + _PECHO_FRAC * (cadera_d - hombro_d)

    cv2.line(frame, tuple(hombro_i.astype(int)), tuple(hombro_d.astype(int)),
              COLOR_BONE, GROSOR_CAPSULA, cv2.LINE_AA)
    cv2.line(frame, tuple(hombro_i.astype(int)), tuple(pecho_i.astype(int)),
              COLOR_BONE, GROSOR_CAPSULA, cv2.LINE_AA)
    cv2.line(frame, tuple(hombro_d.astype(int)), tuple(pecho_d.astype(int)),
              COLOR_BONE, GROSOR_CAPSULA, cv2.LINE_AA)
    cv2.line(frame, tuple(pecho_i.astype(int)), tuple(pecho_d.astype(int)),
              COLOR_BONE, GROSOR_CAPSULA, cv2.LINE_AA)
    radio_junta = GROSOR_CAPSULA  # redondea las 2 esquinas del pecho que no tienen articulacion grande
    cv2.circle(frame, tuple(pecho_i.astype(int)), radio_junta, COLOR_BONE, -1, cv2.LINE_AA)
    cv2.circle(frame, tuple(pecho_d.astype(int)), radio_junta, COLOR_BONE, -1, cv2.LINE_AA)

    # Cada lado interpola su PROPIA linea hombro->cadera real (no un promedio
    # fijo): si la cadera real sube, baja o un lado se mueve mas que el otro,
    # la caja y sobre todo el conector de abajo lo siguen.
    caja_arriba_i = hombro_i + _CAJA_ARRIBA_FRAC * (cadera_i - hombro_i)
    caja_arriba_d = hombro_d + _CAJA_ARRIBA_FRAC * (cadera_d - hombro_d)
    caja_abajo_i = hombro_i + _CAJA_ABAJO_FRAC * (cadera_i - hombro_i)
    caja_abajo_d = hombro_d + _CAJA_ABAJO_FRAC * (cadera_d - hombro_d)

    caja_izq, caja_der = int(cadera_i[0]), int(cadera_d[0])
    caja_arriba = int((caja_arriba_i[1] + caja_arriba_d[1]) / 2)
    caja_abajo = int((caja_abajo_i[1] + caja_abajo_d[1]) / 2)
    if caja_izq > caja_der:
        caja_izq, caja_der = caja_der, caja_izq
    radio_caja = max(4, int((caja_der - caja_izq) * 0.18))
    _rect_redondeado(frame, (caja_izq, caja_arriba), (caja_der, caja_abajo),
                      radio_caja, COLOR_BONE, GROSOR_CAPSULA)

    cv2.line(frame, tuple(pecho_i.astype(int)), (caja_izq, caja_arriba), COLOR_BONE, GROSOR_HUESO, cv2.LINE_AA)
    cv2.line(frame, tuple(pecho_d.astype(int)), (caja_der, caja_arriba), COLOR_BONE, GROSOR_HUESO, cv2.LINE_AA)
    # tramo corto caja -> cadera real, cada lado con su propio punto (no
    # pegado al borde de la caja, y la pierna sigue arrancando en la cadera
    # real de siempre -- ver POSE_CONNECTIONS).
    cv2.line(frame, (caja_izq, caja_abajo), tuple(cadera_i.astype(int)), COLOR_BONE, GROSOR_HUESO, cv2.LINE_AA)
    cv2.line(frame, (caja_der, caja_abajo), tuple(cadera_d.astype(int)), COLOR_BONE, GROSOR_HUESO, cv2.LINE_AA)


def _dibujar_palma(frame: np.ndarray, pts: list[tuple[int, int]],
                    muneca: int, pulgar: int, indice: int, menique: int, vis) -> None:
    """Palma aproximada con los 4 puntos que trae el PoseLandmarker (muneca +
    base de pulgar/indice/menique) y "dedos" sugeridos como trazos cortos
    hacia afuera. No son dedos medidos: el modelo de pose solo da muneca, menique,
    indice y pulgar (en la base de cada dedo); lo que sobresale es una extension visual.
    """
    if not (vis(muneca) and vis(pulgar) and vis(indice) and vis(menique)):
        return
    poligono = np.array([pts[muneca], pts[pulgar], pts[indice], pts[menique]], dtype=np.int32)
    cv2.polylines(frame, [poligono], True, COLOR_BONE, GROSOR_HUESO, cv2.LINE_AA)
    p_muneca = np.array(pts[muneca])
    for punta_idx in (pulgar, indice, menique):
        punta = np.array(pts[punta_idx])
        direccion = punta - p_muneca
        codo = punta + direccion * 0.55       # "nudillo" a mitad de dedo
        extremo = punta + direccion * 1.15    # punta del dedo
        cv2.line(frame, tuple(punta.astype(int)), tuple(codo.astype(int)),
                  COLOR_BONE, GROSOR_HUESO, cv2.LINE_AA)
        cv2.line(frame, tuple(codo.astype(int)), tuple(extremo.astype(int)),
                  COLOR_BONE, GROSOR_HUESO, cv2.LINE_AA)
    cv2.circle(frame, pts[muneca], RADIO_JUNTA, COLOR_JOINT, -1, cv2.LINE_AA)


def draw_landmarks(frame: np.ndarray, lms: Landmarks, visibles: set[int] | None = None,
                   cabeza_escala: float = 1.0) -> None:
    """visibles: indices a dibujar (None = todos, el comportamiento de siempre).
    Es el filtro que arma el selector de regiones del cuerpo en el panel.

    Esqueleto "tipo robot humanoide" -- cabeza y division pecho/cadera como
    capsulas, articulaciones grandes en hombro/codo/rodilla, manos aproximadas
    con palma + dedos sugeridos (el PoseLandmarker no trae nudillos).
    cabeza_escala: multiplica el ovalo de la cabeza (el diagrama de Kpoints agranda la cara para poder tocar sus puntos).
    """
    h, w = frame.shape[:2]
    pts = [(int(x * w), int(y * h)) for x, y, _ in lms.screen]
    n = len(pts)

    def vis(i: int) -> bool:
        return i < n and (visibles is None or i in visibles)

    for a, b in POSE_CONNECTIONS:
        if (a, b) in _SIN_LINEA:
            continue
        if vis(a) and vis(b):
            cv2.line(frame, pts[a], pts[b], COLOR_BONE, grosor_hueso(a, b, "pose"), cv2.LINE_AA)

    _dibujar_cabeza(frame, pts, vis, cabeza_escala)
    _dibujar_torso(frame, pts, vis)
    _dibujar_palma(frame, pts, _MUNECA[0], _PULGAR[0], _INDICE[0], _MENIQUE[0], vis)
    _dibujar_palma(frame, pts, _MUNECA[1], _PULGAR[1], _INDICE[1], _MENIQUE[1], vis)

    for i, p in enumerate(pts):
        if not vis(i) or i in _PUNTOS_CARA or i in _PUNTOS_MANO_APARTE:
            continue
        radio = RADIO_JUNTA_GRANDE if i in _ARTICULACIONES_GRANDES else RADIO_JUNTA
        cv2.circle(frame, p, radio, COLOR_JOINT, -1, cv2.LINE_AA)


def draw_panel(frame: np.ndarray, lines: list[tuple[str, tuple[int, int, int]]]) -> None:
    if not lines:
        return
    pad, lh, width = 10, 22, 320
    height = pad * 2 + lh * len(lines)
    # Mezcla solo el rectangulo del panel (antes copiaba y mezclaba el cuadro
    # ENTERO en cada frame: varios ms perdidos a 1280x720).
    h, w = frame.shape[:2]
    y1, x1 = min(10 + height, h), min(10 + width, w)
    if y1 > 10 and x1 > 10:
        roi = frame[10:y1, 10:x1]
        fondo = np.empty_like(roi)
        fondo[:] = COLOR_PANEL
        cv2.addWeighted(fondo, 0.65, roi, 0.35, 0, roi)
    for i, (text, color) in enumerate(lines):
        y = 10 + pad + lh * (i + 1) - 6
        cv2.putText(frame, text, (10 + pad, y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, color, 1, cv2.LINE_AA)


def draw_big_score(frame: np.ndarray, score: float, reps: int) -> None:
    h, w = frame.shape[:2]
    txt = f"{score:.0f}"
    cv2.putText(frame, txt, (w - 210, 90), cv2.FONT_HERSHEY_SIMPLEX,
                2.4, score_color(score), 5, cv2.LINE_AA)
    cv2.putText(frame, f"rep {reps}", (w - 205, 125), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, COLOR_TEXT, 2, cv2.LINE_AA)


def draw_signal_bar(frame: np.ndarray, value: float, low: float, high: float) -> None:
    """Barra lateral con la señal 1-D y sus dos umbrales de histeresis."""
    if not np.isfinite([value, low, high]).all() or high <= low:
        return
    h, w = frame.shape[:2]
    x, y0, y1, bw = w - 60, 160, h - 60, 26
    cv2.rectangle(frame, (x, y0), (x + bw, y1), (60, 60, 60), -1)
    frac = float(np.clip((value - low) / (high - low), 0.0, 1.0))
    y = int(y1 - frac * (y1 - y0))
    cv2.rectangle(frame, (x, y), (x + bw, y1), COLOR_JOINT, -1)
    cv2.line(frame, (x - 6, y0), (x + bw + 6, y0), COLOR_OK, 1)
    cv2.line(frame, (x - 6, y1), (x + bw + 6, y1), COLOR_OK, 1)


def draw_zona_gesto(frame: np.ndarray, frac: float, color: tuple[int, int, int]) -> None:
    """Tinta la esquina superior izquierda (misma zona que recorta
    sesion/gesto.py) mientras hay una muneca ahi: verde
    (COLOR_OK) si no se esta grabando -- sostenerla ahi inicia --, rojo
    (COLOR_BAD) si ya se esta grabando -- sostenerla ahi detiene y
    guarda. Solo se llama cuando hay muneca en la zona.
    """
    h, w = frame.shape[:2]
    x2, y2 = int(w * frac), int(h * frac)
    if x2 > 0 and y2 > 0:
        roi = frame[:y2, :x2]           # solo la esquina, no el cuadro entero
        capa = np.empty_like(roi)
        capa[:] = color
        cv2.addWeighted(capa, 0.25, roi, 0.75, 0, roi)
    cv2.rectangle(frame, (0, 0), (x2, y2), color, 2, cv2.LINE_AA)


def draw_reglas(frame: np.ndarray, reglas: list[dict]) -> None:
    """Reglas de postura (nucleo/reglas.py): la recta B->A en verde si el angulo esta dentro de la
    tolerancia, en rojo si no, con el angulo medido al lado."""
    for r in reglas:
        color = COLOR_OK if r["ok"] else COLOR_BAD
        extremos = [r["pa"], r["pb"]] + ([r["pc"]] if "pc" in r else [])
        cv2.line(frame, r["pb"], r["pa"], color, 4, cv2.LINE_AA)
        if "pc" in r:
            cv2.line(frame, r["pb"], r["pc"], color, 4, cv2.LINE_AA)
        for p in extremos:
            cv2.circle(frame, p, 7, color, -1, cv2.LINE_AA)
        cv2.putText(frame, f"{r['nombre']} {r['angulo']:.0f}", (r["pa"][0] + 10, r["pa"][1]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2, cv2.LINE_AA)
