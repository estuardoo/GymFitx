"""Trae los datos del proyecto viejo (GYMFITX, con core/ + fgml/) a este.

    python -m src.nucleo.migrar                 # origen por defecto: ../GYMFITX
    python -m src.nucleo.migrar --origen D:\\otro\\GYMFITX

Solo COPIA: el proyecto viejo queda intacto como respaldo. Nunca pisa un
archivo que ya exista aca. Se corre sola una vez desde GYMFITX.bat y deja
datos/.migrado.json; despues no vuelve a hacer nada.

Que se trae (y a donde):
    recordings/                 -> datos/grabaciones/
    templates/*.npz             -> datos/plantillas/
    models/*.task               -> modelos/
    fgml/dataset/               -> datos/clips/
    fgml/entrenamientos/        -> datos/entrenamientos/
    fgml/labels.json            -> datos/etiquetas.json   (y el resto de json del cortador)
    fgml/pipeline.yaml          -> datos/ajustes.yaml
    fgml/pitch/                 -> docs/pitch/
    exercises/*.yaml            -> ejercicios/            (tus catalogos de puntos editados)
    gymfitx.db, acceso.json, pendientes_sql.jsonl, cloudflared.exe
No se trae: fgml/data/ (copia vieja de recordings), .preview_cache (se
regenera sola) ni codigo.
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path

from src.nucleo.config import DATOS_DIR, ROOT


def plan(origen: Path, raiz: Path, datos: Path) -> list[tuple[Path, Path]]:
    """(origen, destino) de cada carpeta o archivo a copiar."""
    f = origen / "fgml"
    pares = [
        (origen / "recordings", datos / "grabaciones"),
        (origen / "templates", datos / "plantillas"),
        (origen / "models", raiz / "modelos"),
        (f / "dataset", datos / "clips"),
        (f / "entrenamientos", datos / "entrenamientos"),
        (f / "pitch", raiz / "docs" / "pitch"),
        (origen / "exercises", raiz / "ejercicios"),
        (f / "labels.json", datos / "etiquetas.json"),
        (f / "manifest.json", datos / "manifest.json"),
        (f / ".export_estado.json", datos / "export_estado.json"),
        (f / "seleccion_entrenamiento.json", datos / "seleccion_entrenamiento.json"),
        (f / "sql_config.json", datos / "sql_config.json"),
        (f / "sql_tipos.json", datos / "sql_tipos.json"),
        (f / "pipeline.yaml", datos / "ajustes.yaml"),
        (origen / "gymfitx.db", datos / "gymfitx.db"),
        (origen / "pendientes_sql.jsonl", datos / "pendientes_sql.jsonl"),
        (origen / "acceso.json", datos / "acceso.json"),
        (f / "acceso.json", datos / "acceso.json"),
        (origen / "tools" / "cloudflared.exe", raiz / "herramientas" / "cloudflared.exe"),
        (f / "tools" / "cloudflared.exe", raiz / "herramientas" / "cloudflared.exe"),
    ]
    return [(a, b) for a, b in pares if a.exists()]


def _copiar(a: Path, b: Path, sobrescribir: bool) -> int:
    """Copia a -> b (archivo o carpeta). Devuelve cuantos archivos copio."""
    if a.is_file():
        if b.exists() and not sobrescribir:
            return 0
        b.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(a, b)
        return 1
    n = 0
    for archivo in a.rglob("*"):
        if archivo.is_file() and not archivo.name.endswith((".bak", ".part")):
            n += _copiar(archivo, b / archivo.relative_to(a), sobrescribir)
    return n


def migrar(origen: Path, raiz: Path = ROOT, datos: Path = DATOS_DIR) -> dict:
    marca = datos / ".migrado.json"
    if marca.exists():
        return {"hecho": False, "motivo": "ya migrado", **json.loads(marca.read_text("utf-8"))}
    if not (origen / "fgml").exists() and not (origen / "recordings").exists():
        return {"hecho": False, "motivo": f"no hay proyecto viejo en {origen}"}
    copiados = {}
    for a, b in plan(origen, raiz, datos):
        # los .yaml de ejercicio del proyecto viejo tienen tus catalogos de
        # puntos editados: esos si reemplazan a los que trae el codigo
        copiados[str(b.relative_to(raiz)) if b.is_relative_to(raiz) else str(b)] = \
            _copiar(a, b, sobrescribir=(b.name == "ejercicios"))
    resumen = {"origen": str(origen), "fecha": datetime.now().isoformat(timespec="seconds"),
               "archivos": sum(copiados.values()), "detalle": copiados}
    datos.mkdir(parents=True, exist_ok=True)
    marca.write_text(json.dumps(resumen, indent=1, ensure_ascii=False), "utf-8")
    return {"hecho": True, **resumen}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--origen", type=Path, default=ROOT.parent / "GYMFITX")
    r = migrar(ap.parse_args().origen)
    if r["hecho"]:
        print(f"  Datos del proyecto viejo copiados: {r['archivos']} archivos (el viejo no se toco).")
    elif r["motivo"] != "ya migrado":
        print(f"  Migracion: {r['motivo']}")


if __name__ == "__main__":
    main()
