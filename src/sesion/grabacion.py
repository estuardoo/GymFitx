"""Registro en disco de cada sesion: video crudo + features + metadatos.

Se guarda el video SIN anotaciones a proposito. Las anotaciones se pueden
regenerar en cualquier momento reproduciendo el archivo con VideoSource por el
mismo pipeline (scripts/reprocesar.py); los pixeles originales, no. Guardar el video
limpio deja la puerta abierta a reprocesar con otro modelo, otro YAML o otros
umbrales dentro de un año, que es justamente para lo que sirve archivarlos.

Estructura en disco -- cada ejercicio en su propia carpeta, y dentro por dia:

    datos/grabaciones/<ejercicio>/<AAAA-MM-DD>/<HHMMSS>_<modo>.mp4
    datos/grabaciones/<ejercicio>/<AAAA-MM-DD>/<HHMMSS>_<modo>.npz
    datos/grabaciones/<ejercicio>/<AAAA-MM-DD>/<HHMMSS>_<modo>.json

Junto al .mp4 quedan:
  .npz   la serie de features ya extraida  -> reanalisis sin volver a trackear,
         y es lo que usa el panel para recalibrar la plantilla desde una
         grabacion vieja sin tener que redecodificar el video
  .json  metadatos de la sesion            -> que ejercicio, cuando, con que

Detalle de precision temporal: la camara entrega cuadros a un ritmo irregular
(20-30 fps con saltos, y con huecos cuando la sesion se pausa). Escribir esos
cuadros a una tasa nominal fija produciria un video que corre mas rapido o mas
lento que la realidad. Aqui cada cuadro se escribe tantas veces como haga
falta para llenar su lugar en una linea de tiempo de 30 fps: el video
resultante dura exactamente lo que duro la sesion (sin contar las pausas, que
el pipeline ya descuenta antes de que estos cuadros lleguen aqui).
"""

from __future__ import annotations

import csv
import io
import json
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np

from src.nucleo import landmarks

FPS_SALIDA = 30.0

# mp4v por defecto: viene de fabrica en opencv-python y abre en cualquier
# maquina. No se prueba H.264 automaticamente a proposito: cuando el codec no
# existe, ffmpeg escupe un bloque de errores en rojo por cada intento, y una
# sesion que arranca con una pared de rojo parece rota sin estarlo. Quien tenga
# H.264 disponible lo pide expresamente con --video-codec avc1 y ahorra ~3x.
CODEC_POR_DEFECTO = "mp4v"

# Referencia medida (contenido tipo webcam, 30 fps, mp4v):
#   1280x720 -> ~13 MB/min      960x540 -> ~8 MB/min      640x360 -> ~4 MB/min


class VideoLogger:
    """Sumidero que archiva la sesion. Se combina con Recorder o Evaluator."""

    def __init__(self, base_dir: Path | str, guardar_video: bool = True,
                 max_width: int = 0, codec: str = CODEC_POR_DEFECTO) -> None:
        self.base_dir = Path(base_dir)
        self.guardar_video = guardar_video
        self.max_width = int(max_width)   # 0 = guardar a resolucion de captura
        self.codec = codec
        self.video_path: Path | None = None
        self.npz_path: Path | None = None
        self.json_path: Path | None = None

        self._writer: cv2.VideoWriter | None = None
        self._escritos = 0
        self._t0: int | None = None
        self._t_ultimo: int | None = None
        self._cuadros_camara = 0
        self._unicos = 0          # cuadros distintos escritos (sin contar repeticiones)
        self._valores: list[np.ndarray] = []
        self._tiempos: list[int] = []
        self._puntos: list[np.ndarray] = []   # world landmarks crudos por cuadro (para dataset externo)
        self._inicio = ""
        self._tam: tuple[int, int] = (0, 0)
        self._escala = 1.0

    # -- Sink --
    def on_start(self, pipe) -> None:
        ahora = datetime.now()
        self._inicio = ahora.isoformat(timespec="seconds")
        # "referencia" = toma que calibra la plantilla (antes se llamaba "base",
        # igual que la clase "base" del cortador: dos cosas distintas).
        modo = "referencia" if pipe.segmenter is None else "serie"
        carpeta = self.base_dir / pipe.exercise.slug / ahora.strftime("%Y-%m-%d")
        carpeta.mkdir(parents=True, exist_ok=True)

        # Dos sesiones en el mismo segundo no pueden pisarse: un archivo
        # sobrescrito es material perdido para siempre.
        base = f"{ahora.strftime('%H%M%S')}_{modo}"
        tallo, n = base, 1
        while (carpeta / f"{tallo}.json").exists():
            tallo = f"{base}_{n}"
            n += 1
        self.video_path = carpeta / f"{tallo}.mp4"
        self.npz_path = carpeta / f"{tallo}.npz"
        self.json_path = carpeta / f"{tallo}.json"

    def on_frame(self, pipe, frame, fv) -> None:
        """Cuadros PROCESADOS (con deteccion): guarda las features."""
        if fv is not None:
            self._valores.append(fv.values.copy())
            if fv.raw is not None:
                self._puntos.append(fv.raw.copy())
            self._tiempos.append(frame.t_ms)

    def on_raw_frame(self, pipe, frame) -> None:
        """TODOS los cuadros de la camara (hilo de captura): escribe el video.
        Antes el video se escribia desde el hilo de deteccion (~7 fps) y cada
        cuadro se repetia ~4 veces: 70 % de cuadros congelados. Ahora el video
        lleva los cuadros reales de la camara y solo rellena huecos reales."""
        if self._t0 is None:
            self._t0 = frame.t_ms
        self._t_ultimo = frame.t_ms
        self._cuadros_camara += 1
        if not self.guardar_video:
            return
        if self._writer is None:
            h, w = frame.image.shape[:2]
            if self.max_width and w > self.max_width:
                self._escala = self.max_width / w
                w, h = self.max_width, int(round(h * self._escala))
            self._tam = (w, h)
            vw = cv2.VideoWriter(
                str(self.video_path), cv2.VideoWriter_fourcc(*self.codec), FPS_SALIDA, (w, h)
            )
            if not vw.isOpened():   # sin codec: se archiva sin video, no se cae
                vw.release()
                self.guardar_video = False
                self.video_path = None
                pipe.bus.emit({"type": "aviso",
                               "message": f"El codec '{self.codec}' no esta disponible; "
                                          f"la sesion se archiva sin video. "
                                          f"Prueba con --video-codec mp4v."})
                return
            self._writer = vw

        # Rellena la linea de tiempo: el video dura lo que duro la sesion. Un
        # cuadro que llega antes de su turno (camara > 30 fps) se salta.
        objetivo = int(round((frame.t_ms - self._t0) / 1000.0 * FPS_SALIDA)) + 1
        repeticiones = min(objetivo - self._escritos, 90)   # tope: 3 s de congelado
        if repeticiones <= 0:
            return
        img = frame.image
        if self._escala != 1.0:
            img = cv2.resize(img, self._tam, interpolation=cv2.INTER_AREA)
        for _ in range(repeticiones):
            self._writer.write(img)
        self._escritos += repeticiones
        self._unicos += 1

    def on_rep(self, pipe, seg) -> None:
        pass

    def on_stop(self, pipe) -> None:
        if self._writer is not None:
            self._writer.release()
            self._writer = None

        valores = (np.vstack(self._valores) if self._valores
                   else np.empty((0, pipe.extractor.size), dtype=np.float32))

        # Puntos crudos (x,y,z) por cuadro, para quien quiera un dataset aparte
        # de landmarks en vez de solo los angulos/razones invariantes -- ver
        # types.FeatureVec.raw. Si algo dejo desalineados puntos y valores
        # (no deberia pasar: ambos salen del mismo FeatureVec), se guarda
        # vacio en vez de un array que no calza con t_ms.
        fuente = pipe.exercise.source
        n_puntos = landmarks.N_POINTS.get(fuente, 0)
        if self._puntos and len(self._puntos) == len(self._tiempos):
            puntos = np.stack(self._puntos)
        else:
            puntos = np.empty((0, n_puntos, 3), dtype=np.float32)
        nombres_puntos = landmarks.POSE_LANDMARKS

        np.savez_compressed(
            self.npz_path,
            values=valores,
            t_ms=np.array(self._tiempos, dtype=np.int64),
            names=np.array(pipe.extractor.names),
            units=np.array(pipe.extractor.units),
            points=puntos,
            point_names=np.array(nombres_puntos),
        )

        dur_ms = (self._tiempos[-1] - self._tiempos[0]) if len(self._tiempos) > 1 else 0
        dur_cam_ms = (self._t_ultimo - self._t0) if self._t0 is not None and self._t_ultimo is not None else 0
        self.meta = {
            "exercise": pipe.exercise.slug,
            "exercise_name": pipe.exercise.name,
            "source": pipe.exercise.source,
            "modo": "referencia" if pipe.segmenter is None else "serie",
            "started_at": self._inicio,
            "ended_at": datetime.now().isoformat(timespec="seconds"),
            "frames": pipe.frames_vistos,
            "frames_con_deteccion": len(self._tiempos),
            "duration_ms": dur_ms,
            "fps_medio": round(len(self._tiempos) / (dur_ms / 1000.0), 1) if dur_ms else 0.0,  # deteccion
            "frames_camara": self._cuadros_camara,
            "fps_camara": round(self._cuadros_camara / (dur_cam_ms / 1000.0), 1) if dur_cam_ms else 0.0,
            # cuadros DISTINTOS en el video / segundo (el resto son relleno de huecos)
            "fps_video_real": round(self._unicos / (dur_cam_ms / 1000.0), 1) if dur_cam_ms else 0.0,
            "reps": 0 if pipe.segmenter is None else pipe.segmenter.reps,
            "resolucion": list(self._tam),
            "codec": self.codec,
            "video": self.video_path.name if self.video_path else None,
            "features": self.npz_path.name,
            "feature_names": pipe.extractor.names,
        }
        self.json_path.write_text(
            json.dumps(self.meta, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        pipe.bus.emit({"type": "grabacion", **self.meta})

    # -- consulta --
    @property
    def rutas(self) -> dict:
        return {
            "video": str(self.video_path) if self.video_path else None,
            "features": str(self.npz_path) if self.npz_path else None,
            "meta": str(self.json_path) if self.json_path else None,
        }


def listar_grabaciones(base_dir: Path | str, limite: int = 40,
                       exercise: str | None = None) -> list[dict]:
    """Las sesiones archivadas, mas recientes primero. Lee los .json, no los videos.

    exercise: si se pasa, solo las de ese slug (equivalente a listar esa
    subcarpeta) -- es lo que usa el panel para el filtro por ejercicio.
    """
    base = Path(base_dir)
    patron = f"{exercise}/*/*.json" if exercise else "*/*/*.json"
    salida: list[dict] = []
    for j in sorted(base.glob(patron), reverse=True)[:limite]:
        try:
            m = json.loads(j.read_text(encoding="utf-8"))
        except Exception:
            continue
        video = j.with_suffix(".mp4")
        npz = j.with_suffix(".npz")
        m["dia"] = j.parent.name
        m["ruta_relativa"] = f"{j.parent.parent.name}/{j.parent.name}/{video.name}"
        m["npz_relativo"] = f"{j.parent.parent.name}/{j.parent.name}/{npz.name}"
        m["bytes"] = video.stat().st_size if video.exists() else 0
        m["existe_video"] = video.exists()
        m["existe_features"] = npz.exists()
        salida.append(m)
    return salida


def uso_en_disco(base_dir: Path | str) -> dict:
    base = Path(base_dir)
    archivos = list(base.glob("*/*/*"))
    total = sum(f.stat().st_size for f in archivos if f.is_file())
    videos = [f for f in archivos if f.suffix == ".mp4"]
    return {
        "bytes": total,
        "mb": round(total / 1e6, 1),
        "videos": len(videos),
        "sesiones": len([f for f in archivos if f.suffix == ".json"]),
    }


def features_a_csv(npz_path: Path | str) -> str:
    """El contenido del .npz de una grabacion, como texto CSV (t_ms + cada feature).

    Los "movimientos" (angulos de cada dedo, apertura, etc.) ya se guardan
    solos en el .npz al terminar cualquier sesion -- de mano o de cuerpo
    completo. Esto solo los pasa a un formato que se abre en Excel/Sheets en
    vez del binario de numpy, para el boton "Movimientos (CSV)" del panel.
    """
    data = np.load(npz_path, allow_pickle=True)
    nombres = [str(n) for n in data["names"]]
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["t_ms", *nombres])
    for t, fila in zip(data["t_ms"], data["values"]):
        w.writerow([int(t), *[round(float(v), 4) for v in fila]])
    return buf.getvalue()


def resolver_json(base_dir: Path | str, ruta_relativa: str) -> Path:
    """De la ruta relativa que maneja el panel (ej. 'slug/2026-08-25/073012_serie.mp4')
    al .json de metadatos correspondiente, validando que no se escape de datos/grabaciones/.
    """
    base = Path(base_dir).resolve()
    candidato = (base / ruta_relativa).resolve()
    if base not in candidato.parents and candidato != base:
        raise ValueError("ruta fuera de datos/grabaciones/")
    return candidato.with_suffix(".json")
