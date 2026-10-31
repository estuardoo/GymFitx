"""API de etiquetado: videos para cortar, etiquetas, overlay de puntos, exportar clips, tablas SQL y editor de puntos.

Rutas sync ("def", no "async def"): FastAPI las corre en su threadpool, asi
que cortar/entrenar (CPU) no bloquea el websocket ni el video de la camara."""

from __future__ import annotations

from functools import lru_cache

import cv2
import numpy as np
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse, Response
from pydantic import BaseModel, ConfigDict

from src.almacenamiento import dataset_sql as SQL
from src.etiquetado import cortes as CORTES
from src.etiquetado import depurar as DEPURAR
from src.etiquetado import editor_puntos as PUNTOS
from src.etiquetado import exportar as EXPORTAR
from src.etiquetado import importar as IMPORTAR
from src.etiquetado import previews as PREVIEWS
from src.etiquetado import tablas as TABLAS
from src.etiquetado.manifest import _manifest, _ruta_video
from src.interfaz.control import sesion, store
from src.preparacion import tabla as TABLA

router = APIRouter()


try:  # previews huerfanos (nombres viejos): se regeneran solos si hacen falta
    PREVIEWS.limpiar_preview_huerfanos()
except Exception:
    pass


@router.get("/data/{name:path}")
def dataset_data(name: str):
    # name = ruta relativa a input/raw/ (ej. "1/000007.mp4"):
    # _ruta_video valida que no se escape de ahi (nada de "..").
    try:
        archivo = _ruta_video(name)
    except ValueError:
        raise HTTPException(404) from None
    if archivo.suffix.lower() == ".mp4":
        archivo = PREVIEWS.preview_de(archivo)
    if not archivo.exists():
        raise HTTPException(404)
    return FileResponse(archivo)


@router.get("/api/config")
def dataset_config():
    return CORTES.estado_config()


@router.get("/api/labels")
def dataset_labels_get():
    return CORTES.leer_labels()


class PersonaVideo(BaseModel):
    id: int                      # id del video en la tabla `raw`
    persona: str | None = None   # 'P1'..'Pn'; vacio = sin persona


@router.post("/api/raw/persona")
def raw_persona(body: PersonaVideo):
    """Con quien se grabo este video: llega solo a sus clips (la persona vive en `raw`)."""
    import re
    persona = (body.persona or "").strip() or None
    if persona is not None and not re.fullmatch(r"P\d{1,3}", persona):
        return JSONResponse({"error": "Persona invalida: usa P1, P2, P3..."}, status_code=400)
    from src.nucleo import inputs as INP
    try:
        return {"ok": True, **INP.asignar_persona(body.id, persona)}
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=404)


@router.post("/api/labels")
def dataset_labels_post(body: dict):
    return CORTES.guardar_labels(body)


@router.get("/api/overlay")
def dataset_overlay(file: str):
    try:
        return CORTES.overlay_de(file)
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@router.get("/api/export_estado")
def dataset_export_estado():
    return EXPORTAR.estado_export()


@router.get("/api/export_progreso")
def dataset_export_progreso():
    return EXPORTAR.PROGRESO


@router.post("/api/export")
def dataset_export(body: dict, todo: bool = False):
    return EXPORTAR.exportar(body, todo)


@router.get("/api/tipos")
def dataset_tipos():
    return TABLAS.tipos_disponibles()


@router.get("/api/sql/estado")
def dataset_sql_estado(tipo: str | None = None):
    return TABLAS.sql_estado(tipo)


@router.post("/api/sql/blanquear")
def dataset_sql_blanquear():
    try:
        return {"borradas": SQL.blanquear_datos()}
    except SQL.SQLServerNoDisponible as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@router.post("/api/sql/generar")
def dataset_sql_generar():
    try:
        return EXPORTAR.sql_generar()
    except SQL.SQLServerNoDisponible as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@router.get("/api/puntos/ejercicios")
def dataset_puntos_ejercicios():
    return PUNTOS.listar_ejercicios()


@router.get("/api/puntos/tipos")
def dataset_puntos_tipos():
    return PUNTOS.TIPOS_FEATURE


# lienzo del diagrama de Kpoints: viewBox "-22 -32 144 138" de #kpSvg (puntos.js), a 5 px por unidad
_FIG_W, _FIG_H, _FIG_U, _FIG_CABEZA = 720, 690, 5, 2.4   # _FIG_CABEZA: el diagrama agranda la cara para poder tocar sus puntos


@lru_cache(maxsize=1)
def _figura_png() -> bytes:
    """El mismo esqueleto del video (sesion/overlay.py) sobre el catalogo de puntos, de fondo del diagrama."""
    from src.nucleo.landmarks import resolve
    from src.nucleo.tipos import Landmarks
    from src.sesion import overlay
    p = np.zeros((33, 3))
    for n, (x, y, _g) in PUNTOS.POSE_PUNTOS.items():
        p[resolve(n, "pose")] = ((x * 100 + 22) * _FIG_U / _FIG_W, ((1 - y) * 100 + 32) * _FIG_U / _FIG_H, 0)
    img = np.full((_FIG_H, _FIG_W, 3), (22, 18, 16), np.uint8)   # #101216, el fondo del svg
    overlay.draw_landmarks(img, Landmarks("pose", p.copy(), p), cabeza_escala=_FIG_CABEZA)
    return cv2.imencode(".png", img)[1].tobytes()


@router.get("/api/puntos/figura.png")
def dataset_puntos_figura():
    return Response(_figura_png(), media_type="image/png", headers={"Cache-Control": "no-cache"})


@router.get("/api/puntos/catalogo")
def dataset_puntos_catalogo(source: str = "pose"):
    return PUNTOS.catalogo(source)


@router.get("/api/puntos/definicion")
def dataset_puntos_definicion_get(ejercicio: str = ""):
    data = PUNTOS.leer_ejercicio(ejercicio)
    if data is None:
        return JSONResponse({"error": "no existe"}, status_code=404)
    return data


class NombrePedido(BaseModel):
    nombre: str | None = None


class PuntosPedido(BaseModel):
    model_config = ConfigDict(extra="allow")   # el resto son puntos y angulos del ejercicio
    nombre: str | None = None


class SlugsPedido(BaseModel):
    slugs: list[str] | None = None


@router.post("/api/puntos/crear")
def dataset_puntos_crear(body: NombrePedido):
    try:
        return PUNTOS.crear_ejercicio(body.nombre)
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@router.get("/api/puntos/sincronizar")
def dataset_puntos_sincronizar(ejercicio: str = ""):
    return PUNTOS.sincronizar(ejercicio)


@router.post("/api/puntos/modificar")
def dataset_puntos_modificar(body: PuntosPedido):
    try:
        datos = body.model_dump()
        return PUNTOS.modificar_ejercicio(datos.pop("nombre", None), datos)
    except (ValueError, KeyError) as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@router.post("/api/puntos/eliminar")
def dataset_puntos_eliminar(body: NombrePedido):
    nombre = body.nombre
    if sesion.activa and sesion.info.get("exercise") == nombre:
        return JSONResponse({"error": "Detén la sesión de este ejercicio antes de archivarlo."}, status_code=409)
    try:
        r = PUNTOS.eliminar_ejercicio(nombre)
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    try:   # fuera de la rutina; sin SQL queda pendiente y load_all ya no lo lista
        store.set_routine([i for i in store.routine() if i["exercise"] != nombre])
    except Exception:
        r["rutina"] = "no se pudo actualizar (sin conexion a SQL)"
    try:   # y con el: sus clips salen del manifest, de los cortes y de SQL (los archivos pasan a sistema/archivados/)
        r["depurado"] = DEPURAR.depurar(nombre)
    except Exception as e:
        r["depurado"] = {"error": str(e)[:200]}
    return r


@router.get("/api/archivados/plan")
def archivados_plan():
    """Ejercicios archivados que aun dejan clips o datos en SQL (lo que quitaria el boton de Sistema)."""
    return DEPURAR.plan()


@router.post("/api/archivados/depurar")
def archivados_depurar(body: SlugsPedido):
    return DEPURAR.depurar_todos(body.slugs)


@router.post("/api/ejercicio/base-clip")
def ejercicio_base_clip(body: dict):
    """Rehace la base del ejercicio desde un clip (por defecto el primero de 'bien'). Reinicia la camara para tomarla."""
    from src.evaluacion.base_clip import base_desde_clip
    from src.nucleo.ejercicio import load_exercise
    try:
        ex = load_exercise(body["ejercicio"])
        return {"ok": True, **base_desde_clip(ex, body.get("clip"), body.get("clase", "bien"))}
    except (ValueError, KeyError, FileNotFoundError) as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@router.post("/api/puntos/reglas")
def dataset_puntos_reglas(body: dict):
    try:
        return {"ok": True, "reglas": PUNTOS.guardar_reglas(body["ejercicio"], body.get("reglas") or [])}
    except (ValueError, KeyError) as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@router.post("/api/puntos/normalizacion")
def dataset_puntos_normalizacion(body: dict):
    try:
        return {"ok": True, **PUNTOS.guardar_normalizacion(body["ejercicio"], body)}
    except (ValueError, KeyError) as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@router.post("/api/puntos/normalizacion/previa")
def dataset_puntos_normalizacion_previa(body: dict):
    try:
        return {"ok": True, **TABLA.previa_normalizacion(body["ejercicio"], body, body.get("clip"))}
    except (ValueError, KeyError) as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@router.post("/api/puntos/definicion")
def dataset_puntos_definicion_post(body: dict):
    try:
        body = dict(body)
        ejercicio = body.pop("ejercicio")
        antes = [f["name"] for f in (PUNTOS.leer_ejercicio(ejercicio) or {}).get("features", [])]
        PUNTOS.guardar_ejercicio(ejercicio, body)
        despues = [f["name"] for f in PUNTOS.leer_ejercicio(ejercicio)["features"]]
        sql = PUNTOS.subir(ejercicio)   # sin conexion queda pendiente y se sube solo despues
        # otro orden o otras filas = la base (plantilla) grabada ya no corresponde a este ejercicio
        return {"ok": True, "sql": sql, "features_cambiaron": antes != despues}
    except (ValueError, KeyError) as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@router.get("/api/ejercicio/clips")
def ejercicio_clips(slug: str):
    """Cuantos clips bien/mal tiene el ejercicio (para el dialogo de subida)."""
    cuenta = dict.fromkeys(IMPORTAR.CLASES, 0)
    for r in _manifest():
        if r.get("exercise") == slug and r.get("clase") in cuenta:
            cuenta[r["clase"]] += 1
    return cuenta


@router.post("/api/ejercicio/clips/carpeta")
def ejercicio_importar_carpeta(body: dict):
    """Importa una carpeta Bien/Mal/P1..Pn del disco del servidor (segundo plano; avance en .../progreso)."""
    try:
        IMPORTAR.iniciar_carpeta(body.get("slug", ""), body.get("carpeta", ""))
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    return {"ok": True}


@router.get("/api/ejercicio/clips/carpeta/progreso")
def ejercicio_importar_progreso():
    return IMPORTAR.PROGRESO


def _subir_clips(slug, clase, reemplazar, archivos):
    tmp, rutas = IMPORTAR.guardar_subidas([(a.filename, a.file) for a in archivos])
    try:
        return IMPORTAR.importar_clips(slug, clase, rutas, reemplazar)
    except (ValueError, IMPORTAR.deteccion.DeteccionNoDisponible) as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    finally:
        tmp.cleanup()


try:   # sin python-multipart, FastAPI tira RuntimeError al definir la ruta y NO arranca todo el panel
    try:
        import python_multipart  # noqa: F401
    except ImportError:
        import multipart  # noqa: F401

    @router.post("/api/ejercicio/clips")
    def ejercicio_subir_clips(slug: str = Form(...), clase: str = Form(...), reemplazar: bool = Form(False),
                              archivos: list[UploadFile] = File(...)):
        """Videos ya cortados de una clase -> clips del ejercicio + npz con puntos + manifest + SQL."""
        return _subir_clips(slug, clase, reemplazar, archivos)
except ImportError:
    @router.post("/api/ejercicio/clips")
    def ejercicio_subir_clips_sin_multipart():
        return JSONResponse({"error": "Falta python-multipart: ejecuta UPDATE.bat (pip install python-multipart)"},
                            status_code=503)
