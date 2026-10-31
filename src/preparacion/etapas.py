"""Las 5 tareas de la etapa 3 de CRISP-DM como etapas ejecutables (las llama dvc.yaml, una por ejercicio):

    python -m src.preparacion.etapas <seleccionar|limpiar|construir|integrar|formatear|todo> <ejercicio>

    3.1 seleccionar  qué clips entran y por qué los que no          -> output/reportes/<n>/seleccion.json
    3.2 limpiar      calidad de cada clip contra parameters/config.json -> output/reportes/<n>/limpieza.json|.md
    3.3 construir    variables derivadas (angulos/proporciones) y registros generados (ventanas "fuera") -> input/plate/<n>/
    3.4 integrar     une clip + clase + grabacion de origen (grupo para la validacion)
    3.5 formatear    normaliza, remuestrea y aplana: un vector por clip -> input/gold/<n>/<id>.npy + docs/diccionario/<ej>.csv|.md

<n> es el numero del ejercicio (parameters/exercise.json) y <id> el del clip: bronze, plate y gold comparten numeracion.
Cada etapa lee la salida de la anterior desde input/plate/<n>/ (nada en memoria entre etapas), asi dvc puede
saltarse las que no cambiaron. Salidas deterministas: sin fechas, sin aleatoriedad."""

from __future__ import annotations

import argparse
import json
from collections import Counter

import numpy as np

from src.nucleo import config as CFG
from src.nucleo.config import params
from src.preparacion import documentar as DOC
from src.preparacion import tabla as T
from src.procesamiento.puntos import normalizacion as NORM
from src.procesamiento.puntos import vectorizar


def _plate(ejercicio):
    return T.carpeta(CFG.PLATE_DIR, ejercicio)


def _gold(ejercicio):
    return T.carpeta(CFG.GOLD_DIR, ejercicio)


def _json_w(ruta, obj) -> None:
    DOC._escribir(ruta, json.dumps(obj, indent=1, ensure_ascii=False, sort_keys=True) + "\n")


def _json_r(ruta):
    return json.loads(ruta.read_text("utf-8"))


# ---------------------------------------------------------------- 3.1
def seleccionar(ejercicio: str) -> list[dict]:
    excluir, sel = set(params("seleccion")["excluir_clases"]), T.seleccion()
    items = []
    for r in T.clips_de(ejercicio):
        motivo = ("clase excluida (params.seleccion.excluir_clases)" if r["clase"] in excluir else
                  "desmarcado a mano en el panel" if sel.get(r["clip"]) is False else
                  "sin .npz" if not T.ruta_npz(r).exists() else None)
        items.append({"clip": r["clip"], "clase": r["clase"], "incluido": motivo is None, "motivo": motivo, "npz": r.get("npz")})
    items.sort(key=lambda i: i["clip"])
    _json_w(_plate(ejercicio) / "seleccion.json", items)
    _json_w(DOC.ruta_reporte(ejercicio, "seleccion.json"), {
        "ejercicio": ejercicio, "clips_en_manifest": len(items), "incluidos": sum(i["incluido"] for i in items),
        "por_clase_incluidos": dict(Counter(i["clase"] for i in items if i["incluido"])),
        "excluidos": [{"clip": i["clip"], "motivo": i["motivo"]} for i in items if not i["incluido"]]})
    return items


# ---------------------------------------------------------------- 3.2
def limpiar(ejercicio: str) -> dict:
    p, spec = params("limpieza"), T.spec_de(ejercicio)
    filas = {r["clip"]: r for r in T.clips_de(ejercicio)}
    clips, motivos, quedan = [], Counter(), []
    items = [it for it in _json_r(_plate(ejercicio) / "seleccion.json") if it["incluido"]]
    plates = T.plates([filas[it["clip"]] for it in items], spec)
    for it in items:
        c = plates[it["clip"]]
        m = T.motivos_limpieza(c["cuadros"], c["nan_pct"]) + (["copia (_N) de otro ciclo"] if filas[it["clip"]].get("copia") else [])
        motivos.update(x.split(" (")[0] for x in m)
        clips.append({"clip": it["clip"], "clase": it["clase"], "cuadros": c["cuadros"], "nan_pct": c["nan_pct"], "motivos": m})
        sale = c["prep"] is None or (p["aplicar"] and T.motivos_limpieza(c["cuadros"], c["nan_pct"]))
        if not sale:
            quedan.append(it["clip"])
    clips.sort(key=lambda c: c["clip"])
    inf = {"ejercicio": ejercicio, "parametros": p, "clips_total": len(filas), "entran": len(clips), "quedan": len(quedan),
           "salen": len(clips) - len(quedan), "motivos": dict(motivos), "copias": sum(1 for c in clips if c["clip"] in quedan and any(m.startswith("copia") for m in c["motivos"])),
           "por_clase_quedan": dict(Counter(c["clase"] for c in clips if c["clip"] in quedan)), "clips": clips}
    _json_w(DOC.ruta_reporte(ejercicio, "limpieza.json"), inf)
    DOC.escribir_limpieza_md(inf)
    _json_w(_plate(ejercicio) / "limpio.json", sorted(quedan))
    return inf


# ---------------------------------------------------------------- 3.3
def construir(ejercicio: str) -> int:
    """Escribe en input/plate/<n>/ los puntos (<id>.p.npy) y angulos (<id>.a.npy) de cada clip limpio, y los de las ventanas
    "fuera" generadas (f000001...). construido.json = registro de lo escrito."""
    spec, filas = T.spec_de(ejercicio), {r["clip"]: r for r in T.clips_de(ejercicio)}
    d = _plate(ejercicio)
    limpios = _json_r(d / "limpio.json")
    plates = T.plates([filas[c] for c in limpios], spec)
    registros, vistos = [], set()
    for clip in limpios:
        puntos, nombres, angulos, nombres_ang = plates[clip]["prep"]
        k = T.llave(filas[clip])
        vistos.add(k)
        registros.append({"key": k, "clip": clip, "clase": filas[clip]["clase"], "generado": False,
                          "nombres": nombres, "nombres_ang": nombres_ang})
    for viejo in d.glob("f*.npy"):   # las ventanas "fuera" se rehacen cada vez
        viejo.unlink()
    if params("construccion")["fuera"]["incluir"]:   # registros generados: tramos de las grabaciones sin ningun ciclo
        cand, _ = T.ventanas_crudas(ejercicio, tope=len(limpios))
        n = 0
        for pts, pn, nombre in cand:
            prep = vectorizar.preparar(pts, pn, spec["point_names"] or None, spec["kpoints"], spec["features_def"])
            if prep is None:
                continue
            n += 1
            k = f"f{n:06d}"
            np.save(d / f"{k}.p.npy", np.asarray(prep[0], dtype=np.float32))
            np.save(d / f"{k}.a.npy", np.asarray(prep[2], dtype=np.float32))
            registros.append({"key": k, "clip": nombre, "clase": "fuera", "generado": True,
                              "nombres": prep[1], "nombres_ang": prep[3]})
    _json_w(d / "construido.json", registros)
    return len(registros)


# ---------------------------------------------------------------- 3.4
def integrar(ejercicio: str) -> dict:
    regs = _json_r(_plate(ejercicio) / "construido.json")
    tabla = [{"key": r["key"], "clip": r["clip"], "clase": r["clase"], "grupo": T.grupo_de(r["clip"]), "generado": r["generado"]} for r in regs]
    por_clase = Counter(t["clase"] for t in tabla)
    if len(por_clase) < 2:
        raise ValueError(f"'{ejercicio}': hace falta al menos 2 clases para entrenar y hay {dict(por_clase)}")
    resumen = {"ejercicio": ejercicio, "registros": len(tabla), "por_clase": dict(por_clase),
               "grabaciones": len({t["grupo"] for t in tabla}), "generados": sum(t["generado"] for t in tabla), "tabla": tabla}
    _json_w(_plate(ejercicio) / "integrado.json", resumen)
    return resumen


# ---------------------------------------------------------------- 3.5
def _subir_sql(ejercicio: str) -> dict:
    """Copia la tabla normalizada a SQL (table_frames_fix; guia_fix = la formula). Sin conexion queda pendiente: el siguiente
    respaldo (cortar / entrenar / «Copiar ahora») la sube porque la guia de esos clips ya no coincide. Nunca lanza."""
    try:
        from src.etiquetado import manifest, tablas
        r = tablas.respaldar_sql([x for x in manifest._manifest() if x.get("exercise") == ejercicio])
    except Exception as e:   # sin pyodbc, sin servidor, sin permisos...
        return {"estado": "pendiente", "error": str(e)[:200]}
    return {"estado": "pendiente" if r["error"] else "subido", "error": r["error"], "resumen": r["resumen"]}


def formatear(ejercicio: str, subir_sql: bool = True) -> dict:
    spec, d = T.spec_de(ejercicio), _plate(ejercicio)
    regs = {r["key"]: r for r in _json_r(d / "construido.json")}
    tabla = _json_r(d / "integrado.json")["tabla"]
    vecs = []
    for t in tabla:
        r = regs[t["key"]]
        prep = (np.load(d / f"{t['key']}.p.npy"), r["nombres"], np.load(d / f"{t['key']}.a.npy"), r["nombres_ang"])
        vecs.append(vectorizar.vector_de_prep(prep, spec))
    largo = Counter(len(v) for v in vecs if len(v)).most_common(1)[0][0] if any(len(v) for v in vecs) else 0   # los de otro catalogo de puntos o sin escala no entran
    if not largo:
        raise ValueError(f"'{ejercicio}': ningun clip se pudo normalizar con la formula (escala 0 o kpoints ausentes); revisa Kpoints -> Normalizacion")
    ok = [k for k, v in enumerate(vecs) if len(v) == largo]
    nombres = regs[tabla[ok[0]]["key"]]["nombres"]
    filas = DOC.columnas(spec, nombres)
    DOC.escribir_diccionario(ejercicio, spec, filas, largo)
    usados, out = set(ok), _gold(ejercicio)
    for k in ok:
        np.save(out / f"{tabla[k]['key']}.npy", np.asarray(vecs[k], dtype=np.float32))
    _json_w(out / "meta.json", {"ejercicio": ejercicio, "n_features": largo, "componentes": spec["features"],
                                "hash": T.hash_gold(spec), "columnas": [f["columna"] for f in filas],
                                "filas": [{c: tabla[k][c] for c in ("key", "clip", "clase", "grupo", "generado")} for k in ok],
                                "normalizacion": NORM.guia(spec["cfg"]),
                                "descartados_otro_catalogo": [tabla[k]["clip"] for k in range(len(tabla)) if k not in usados]})
    return {"ejercicio": ejercicio, "filas": len(ok), "descartados": len(tabla) - len(ok), "columnas": largo,
            "normalizacion": NORM.guia(spec["cfg"]), "sql": _subir_sql(ejercicio) if subir_sql else None}


ETAPAS = {"seleccionar": seleccionar, "limpiar": limpiar, "construir": construir, "integrar": integrar, "formatear": formatear}


def todo(ejercicio: str) -> dict:
    """Las 5 etapas seguidas (boton «Generar documentacion» de Sistema)."""
    return {nombre: _resumen(f(ejercicio)) for nombre, f in ETAPAS.items()}


def _resumen(r):
    return {k: v for k, v in r.items() if k not in ("clips", "tabla")} if isinstance(r, dict) else (len(r) if isinstance(r, list) else r)


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("etapa", choices=[*ETAPAS, "todo"])
    ap.add_argument("ejercicio")
    a = ap.parse_args(argv)
    if a.ejercicio.isdigit():   # dvc los llama por numero (parameters/exercise.json)
        from src.nucleo import inputs as INP
        a.ejercicio = INP.slug_de(a.ejercicio)
    print(json.dumps(todo(a.ejercicio) if a.etapa == "todo" else _resumen(ETAPAS[a.etapa](a.ejercicio)), ensure_ascii=False))


if __name__ == "__main__":
    main()
