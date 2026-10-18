"""Las 5 tareas de la etapa 3 de CRISP-DM como etapas ejecutables (las llama dvc.yaml, una por ejercicio):

    python -m src.preparacion.etapas <seleccionar|limpiar|construir|integrar|formatear|todo> <ejercicio>

    3.1 seleccionar  qué clips entran y por qué los que no          -> reportes/seleccion_<ej>.json
    3.2 limpiar      calidad de cada clip contra params.yaml        -> reportes/limpieza_<ej>.json|.md
    3.3 construir    variables derivadas (angulos/proporciones) y registros generados (ventanas "fuera")
    3.4 integrar     une clip + clase + grabacion de origen (grupo para la validacion)
    3.5 formatear    normaliza, remuestrea y aplana -> datos/final/<ej>/X.npy + docs/diccionario/<ej>.csv|.md

Cada etapa lee la salida de la anterior desde datos/intermedio/<ej>/ (nada en memoria entre etapas), asi dvc puede
saltarse las que no cambiaron. Salidas deterministas: sin fechas, sin aleatoriedad."""

from __future__ import annotations

import argparse
import json
from collections import Counter

import numpy as np

from src.nucleo.config import DATOS_DIR, REPORTES_DIR, params
from src.preparacion import documentar as DOC
from src.preparacion import tabla as T
from src.procesamiento.puntos import vectorizar

INTERMEDIO, FINAL = DATOS_DIR / "intermedio", DATOS_DIR / "final"


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
    _json_w(INTERMEDIO / ejercicio / "seleccion.json", items)
    _json_w(REPORTES_DIR / f"seleccion_{ejercicio}.json", {
        "ejercicio": ejercicio, "clips_en_manifest": len(items), "incluidos": sum(i["incluido"] for i in items),
        "por_clase_incluidos": dict(Counter(i["clase"] for i in items if i["incluido"])),
        "excluidos": [{"clip": i["clip"], "motivo": i["motivo"]} for i in items if not i["incluido"]]})
    return items


# ---------------------------------------------------------------- 3.2
def limpiar(ejercicio: str) -> dict:
    p, spec = params("limpieza"), T.spec_de(ejercicio)
    filas = {r["clip"]: r for r in T.clips_de(ejercicio)}
    clips, motivos, quedan = [], Counter(), []
    for it in _json_r(INTERMEDIO / ejercicio / "seleccion.json"):
        if not it["incluido"]:
            continue
        c = T.leer_clip(filas[it["clip"]], spec)
        m = T.motivos_limpieza(c["cuadros"], c["nan_pct"]) + (["copia (_N) de otro ciclo"] if T.COPIA.search(it["clip"].rsplit(".", 1)[0]) else [])
        motivos.update(x.split(" (")[0] for x in m)
        clips.append({"clip": it["clip"], "clase": it["clase"], "cuadros": c["cuadros"], "nan_pct": c["nan_pct"], "motivos": m})
        sale = c["prep"] is None or (p["aplicar"] and T.motivos_limpieza(c["cuadros"], c["nan_pct"]))
        if not sale:
            quedan.append(it["clip"])
    clips.sort(key=lambda c: c["clip"])
    inf = {"ejercicio": ejercicio, "parametros": p, "clips_total": len(filas), "entran": len(clips), "quedan": len(quedan),
           "salen": len(clips) - len(quedan), "motivos": dict(motivos), "copias": sum(1 for c in clips if c["clip"] in quedan and any(m.startswith("copia") for m in c["motivos"])),
           "por_clase_quedan": dict(Counter(c["clase"] for c in clips if c["clip"] in quedan)), "clips": clips}
    _json_w(REPORTES_DIR / f"limpieza_{ejercicio}.json", inf)
    DOC.escribir_limpieza_md(inf)
    _json_w(INTERMEDIO / ejercicio / "limpio.json", sorted(quedan))
    return inf


# ---------------------------------------------------------------- 3.3
def construir(ejercicio: str) -> int:
    spec, filas = T.spec_de(ejercicio), {r["clip"]: r for r in T.clips_de(ejercicio)}
    d = INTERMEDIO / ejercicio / "construido"
    d.mkdir(parents=True, exist_ok=True)
    for viejo in d.glob("*"):
        viejo.unlink()
    registros, preps = [], []
    for clip in _json_r(INTERMEDIO / ejercicio / "limpio.json"):
        preps.append((clip, filas[clip]["clase"], False, T.leer_clip(filas[clip], spec)["prep"]))
    if params("construccion")["fuera"]["incluir"]:   # registros generados: tramos de las grabaciones sin ningun ciclo
        cand, _ = T.ventanas_crudas(ejercicio, tope=len(preps))
        for pts, pn, nombre in cand:
            prep = vectorizar.preparar(pts, pn, spec["point_names"] or None, spec["kpoints"], spec["features_def"])
            if prep is not None:
                preps.append((nombre, "fuera", True, prep))
    for i, (clip, clase, generado, prep) in enumerate(preps):
        puntos, nombres, angulos, nombres_ang = prep
        np.save(d / f"p{i}.npy", np.asarray(puntos, dtype=np.float32))
        np.save(d / f"a{i}.npy", np.asarray(angulos, dtype=np.float32))
        registros.append({"i": i, "clip": clip, "clase": clase, "generado": generado, "nombres": nombres, "nombres_ang": nombres_ang})
    _json_w(d / "meta.json", registros)
    return len(registros)


# ---------------------------------------------------------------- 3.4
def integrar(ejercicio: str) -> dict:
    regs = _json_r(INTERMEDIO / ejercicio / "construido" / "meta.json")
    tabla = [{"i": r["i"], "clip": r["clip"], "clase": r["clase"], "grupo": T.grupo_de(r["clip"]), "generado": r["generado"]} for r in regs]
    por_clase = Counter(t["clase"] for t in tabla)
    if len(por_clase) < 2:
        raise ValueError(f"'{ejercicio}': hace falta al menos 2 clases para entrenar y hay {dict(por_clase)}")
    resumen = {"ejercicio": ejercicio, "registros": len(tabla), "por_clase": dict(por_clase),
               "grabaciones": len({t["grupo"] for t in tabla}), "generados": sum(t["generado"] for t in tabla), "tabla": tabla}
    _json_w(INTERMEDIO / ejercicio / "integrado.json", resumen)
    return resumen


# ---------------------------------------------------------------- 3.5
def formatear(ejercicio: str) -> dict:
    spec, d = T.spec_de(ejercicio), INTERMEDIO / ejercicio / "construido"
    regs = {r["i"]: r for r in _json_r(d / "meta.json")}
    tabla = _json_r(INTERMEDIO / ejercicio / "integrado.json")["tabla"]
    vecs = []
    for t in tabla:
        r = regs[t["i"]]
        prep = (np.load(d / f"p{t['i']}.npy"), r["nombres"], np.load(d / f"a{t['i']}.npy"), r["nombres_ang"])
        vecs.append(vectorizar.vector_de_prep(prep, spec))
    largo = Counter(len(v) for v in vecs).most_common(1)[0][0]   # los de otro catalogo de puntos no entran
    ok = [k for k, v in enumerate(vecs) if len(v) == largo]
    nombres = regs[tabla[ok[0]]["i"]]["nombres"]
    filas = DOC.columnas(spec, nombres)
    DOC.escribir_diccionario(ejercicio, spec, filas, largo)
    usados, out = set(ok), FINAL / ejercicio
    out.mkdir(parents=True, exist_ok=True)
    np.save(out / "X.npy", np.stack([vecs[k] for k in ok]).astype(np.float32))
    _json_w(out / "meta.json", {"ejercicio": ejercicio, "n_features": largo, "componentes": spec["features"],
                                "columnas": [f["columna"] for f in filas],
                                "filas": [{c: tabla[k][c] for c in ("clip", "clase", "grupo", "generado")} for k in ok],
                                "descartados_otro_catalogo": [tabla[k]["clip"] for k in range(len(tabla)) if k not in usados]})
    return {"ejercicio": ejercicio, "filas": len(ok), "columnas": largo}


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
    print(json.dumps(todo(a.ejercicio) if a.etapa == "todo" else _resumen(ETAPAS[a.etapa](a.ejercicio)), ensure_ascii=False))


if __name__ == "__main__":
    main()
