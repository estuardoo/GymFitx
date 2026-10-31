#!/usr/bin/env python3
"""Junta el/los .csv que salieron de busqueda_features_slurm.py (una o varias corridas, uno o varios
--tarea-id de un mismo SLURM array, incluso de corridas separadas en el tiempo -- el historial de ese script
ya evita que se repitan escenarios) y arma esto para decidir que combinacion de kpoints/angulos/proporciones
conviene, con que modelo, al minimo costo:

  detalle.csv          una fila por (escenario, modelo) ya probada -- TODO codificado igual que en el .csv de
                        entrada (llave, type, modelo, escenario, K01..KN/A01..AN/P01..PN en 0/1, accuracy,
                        f1_macro) mas n_kpoints/n_angulos/n_proporciones/n_elementos (sumas simples) e
                        iteracion (orden de eleccion -- se deriva del numero de escenario, que ya es global y
                        nunca se reasigna). Va CRECIENDO: cada vez que corres esto con mas .csv (de corridas
                        nuevas), vuelve a armar el archivo completo con todo lo que le pasaste.
  matriz_resumen.csv   formato LARGO (una fila por type+accuracy_bucket+modelo+escenario -- nunca hay
                        choques aunque el bucket sea de 1%) lista para pivotear en Excel: Tabla dinamica,
                        filas=accuracy_bucket, columnas=modelo, valores=contar 'escenario' (o promediar
                        accuracy). Cada fila trae 'llave' para ir directo al detalle de ese resultado.
  graficos/progreso.png     accuracy (Y) segun el orden en que se fue eligiendo cada escenario (X) -- punto
                        gris = mejor accuracy de ese escenario (cualquier modelo), linea azul = el mejor
                        accuracy visto hasta ese punto.
  graficos/costo.png    accuracy (Y) vs cuantos elementos uso ese escenario -- n_kpoints+n_angulos+
                        n_proporciones (X). Linea azul = mejor accuracy visto hasta ese costo (la "frontera":
                        para cada presupuesto de elementos, lo maximo que se consiguio) -- para elegir al
                        minimo costo como pediste.
  graficos/matriz_calor.png    accuracy_bucket (Y) x modelo (X), color = cuantos escenarios cayeron ahi.
  resumen.txt           analisis en texto (unico lugar con nombres, para que se lea facil): mejor combinacion
                        encontrada (y cuanto mejora sobre la linea base), ranking de los 5 modelos con mejor
                        F1 promedio, correlacion entre n_kpoints/n_angulos/n_proporciones y el accuracy, y si
                        la busqueda ya se estanco o vale la pena seguir corriendo.

No hace falta el cluster para esto -- se corre en tu PC, donde ya tienes numpy/matplotlib (requirements.txt
de GYMFITX). Uso:

    python scripts/hpc/resumen_busqueda_slurm.py --csv resultados_*.csv --salida resumen_manguito_rotador/

Sirve igual para 1 corrida o para varias (por ejemplo si corriste busqueda_features_slurm.py mas de una vez
sobre el mismo ejercicio para agregar mas combinaciones)."""

from __future__ import annotations

import argparse
import csv
import glob
import statistics
from collections import defaultdict
from pathlib import Path

try:
    from busqueda_features_slurm import MODELOS_CODIGO  # mismo directorio (el .zip del AHPC los deja juntos)
except ImportError:
    MODELOS_CODIGO = {}
NOMBRE_MODELO = {v: k for k, v in MODELOS_CODIGO.items()}   # solo para que resumen.txt sea legible


def _leer(ruta) -> list[dict]:
    with open(ruta, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _entero(v, default=0):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def _contar_prefijo(fila: dict, prefijo: str) -> int:
    """Suma las columnas K01/K02.../A01.../P01... (1 si se uso ese kpoint/angulo/proporcion) -- el ancho
    cambia segun el ejercicio, por eso se cuenta por prefijo de columna en vez de un numero fijo."""
    return sum(_entero(v) for k, v in fila.items() if k.startswith(prefijo) and k[len(prefijo):].isdigit())


def _rango_accuracy(acc):
    """Bucket de 1%: 0.873 -> '87-88%'. acc=1.0 cae en el ultimo bucket ('99-100%')."""
    if acc is None:
        return "sin-medir"
    lo = min(int(acc * 100), 99)
    return f"{lo}-{lo + 1}%"


def _iteraciones(escenarios: set) -> dict:
    """orden de eleccion = orden de aparicion del numero de escenario (ya es global y creciente -- asignado
    UNA vez por busqueda_features_slurm.py y nunca reasignado, asi que no hace falta mirar de que archivo
    vino cada fila para saber el orden real en que se eligio)."""
    return {e: i + 1 for i, e in enumerate(sorted(escenarios))}


def armar_detalle(rutas: list[str]) -> list[dict]:
    crudo = [r for ruta in rutas for r in _leer(ruta)]
    iteracion_de = _iteraciones({_entero(r["escenario"]) for r in crudo if _entero(r["escenario"], -1) >= 0})
    detalle = []
    for r in crudo:
        fila = dict(r)
        fila["llave"] = _entero(r.get("llave"), -1)
        fila["type"] = _entero(r.get("type"))
        fila["modelo"] = _entero(r.get("modelo"), -1)
        fila["escenario"] = _entero(r.get("escenario"), -1)
        fila["accuracy"] = _num(r.get("accuracy"))
        fila["f1_macro"] = _num(r.get("f1_macro"))
        fila["n_kpoints"] = _contar_prefijo(r, "K")
        fila["n_angulos"] = _contar_prefijo(r, "A")
        fila["n_proporciones"] = _contar_prefijo(r, "P")
        fila["n_elementos"] = fila["n_kpoints"] + fila["n_angulos"] + fila["n_proporciones"]
        fila["iteracion"] = 0 if fila["escenario"] < 0 else iteracion_de.get(fila["escenario"], 0)
        fila["rango_accuracy"] = _rango_accuracy(fila["accuracy"])
        detalle.append(fila)
    detalle.sort(key=lambda r: (r["f1_macro"] is not None, r["f1_macro"]), reverse=True)
    return detalle


def armar_matriz(detalle: list[dict]) -> list[dict]:
    """Formato LARGO (una fila por resultado, sin agrupar) -- con un bucket de 1% chocarian demasiado
    escenarios distintos en la misma celda de una tabla ancha; asi no se pierde ninguno, y en Excel se arma
    la vista ancha con una tabla dinamica (filas=accuracy_bucket, columnas=modelo, valores=contar/promediar)."""
    filas = [{"type": r["type"], "accuracy_bucket": r["rango_accuracy"], "modelo": r["modelo"],
              "escenario": r["escenario"], "n_elementos": r["n_elementos"], "llave": r["llave"],
              "accuracy": r["accuracy"], "f1_macro": r["f1_macro"]}
             for r in detalle if r["modelo"] != MODELOS_CODIGO.get("linea_base", 0) and r["accuracy"] is not None]
    filas.sort(key=lambda f: (f["type"], -(f["accuracy"] or 0), f["modelo"]))
    return filas


def grafico_progreso(detalle: list[dict], destino: Path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    mejor_por_iter = {}
    for r in detalle:
        if r["iteracion"] and r["accuracy"] is not None:
            mejor_por_iter[r["iteracion"]] = max(mejor_por_iter.get(r["iteracion"], 0), r["accuracy"])
    if not mejor_por_iter:
        return False
    xs = sorted(mejor_por_iter)
    ys = [mejor_por_iter[x] for x in xs]
    mejor_hasta_ahora, m = [], 0.0
    for y in ys:
        m = max(m, y)
        mejor_hasta_ahora.append(m)

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.scatter(xs, ys, s=22, color="#b0b6c0", zorder=2, label="mejor accuracy de esa eleccion")
    ax.plot(xs, mejor_hasta_ahora, color="#2f6feb", lw=2, zorder=3, label="mejor visto hasta ahi")
    ax.set_xlabel("Eleccion (orden en que se probo el escenario)")
    ax.set_ylabel("Accuracy")
    ax.set_ylim(-0.02, 1.02)
    ax.set_title("Progreso de la busqueda por eleccion")
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    fig.savefig(destino, dpi=110)
    plt.close(fig)
    return True


def grafico_costo(detalle: list[dict], destino: Path):
    """accuracy vs n_elementos (kpoints+angulos+proporciones) -- la linea es la 'frontera': para cada
    presupuesto de elementos, el mejor accuracy que se consiguio gastando eso o menos. Para elegir la
    combinacion mas chica que ya te da un accuracy aceptable, en vez de la que mas kpoints/angulos usa."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    validos = [r for r in detalle if r["modelo"] != MODELOS_CODIGO.get("linea_base", 0) and r["accuracy"] is not None]
    if not validos:
        return False
    xs_todos = [r["n_elementos"] for r in validos]
    ys_todos = [r["accuracy"] for r in validos]

    mejor_por_costo = {}
    for x, y in zip(xs_todos, ys_todos):
        mejor_por_costo[x] = max(mejor_por_costo.get(x, 0), y)
    xs_f = sorted(mejor_por_costo)
    frontera, m = [], 0.0
    for x in xs_f:
        m = max(m, mejor_por_costo[x])
        frontera.append(m)

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.scatter(xs_todos, ys_todos, s=18, color="#b0b6c0", zorder=2, label="cada escenario probado")
    ax.plot(xs_f, frontera, color="#2f6feb", lw=2, zorder=3, label="mejor accuracy para ese costo o menos")
    ax.set_xlabel("Elementos usados (kpoints + angulos + proporciones)")
    ax.set_ylabel("Accuracy")
    ax.set_ylim(-0.02, 1.02)
    ax.set_title("Costo (cantidad de elementos) vs accuracy")
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    fig.savefig(destino, dpi=110)
    plt.close(fig)
    return True


def armar_calor(matriz: list[dict]) -> dict:
    """{(accuracy_bucket, modelo): conteo} -- a partir de la matriz larga."""
    grupos = defaultdict(int)
    for r in matriz:
        grupos[(r["accuracy_bucket"], r["modelo"])] += 1
    return dict(grupos)


def grafico_calor(matriz: list[dict], destino: Path) -> bool:
    """accuracy_bucket (Y, solo los buckets con datos) x modelo (X) -- color = cuantos escenarios cayeron ahi."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    celdas = armar_calor(matriz)
    if not celdas:
        return False
    buckets = sorted({k[0] for k in celdas}, key=lambda b: int(b.split("-")[0]))
    modelos = sorted({k[1] for k in celdas})
    grid = np.zeros((len(buckets), len(modelos)))
    for (b, mo), n in celdas.items():
        grid[buckets.index(b), modelos.index(mo)] = n

    fig, ax = plt.subplots(figsize=(max(4, len(modelos) * 0.7 + 1.5), max(3, len(buckets) * 0.35 + 1)))
    im = ax.imshow(grid, cmap="YlGnBu", aspect="auto")
    for i in range(len(buckets)):
        for j in range(len(modelos)):
            if grid[i, j]:
                ax.text(j, i, int(grid[i, j]), ha="center", va="center", fontsize=7.5)
    ax.set_xticks(range(len(modelos)))
    ax.set_xticklabels([NOMBRE_MODELO.get(mo, mo) for mo in modelos], rotation=45, ha="right", fontsize=7.5)
    ax.set_yticks(range(len(buckets)))
    ax.set_yticklabels(buckets, fontsize=7.5)
    ax.set_xlabel("modelo")
    ax.set_ylabel("accuracy (bucket 1%)")
    ax.set_title("Cuantos escenarios cayeron en cada accuracy x modelo")
    fig.colorbar(im, ax=ax, label="conteo")
    fig.tight_layout()
    fig.savefig(destino, dpi=110)
    plt.close(fig)
    return True


def analisis_convergencia(detalle: list[dict]) -> dict:
    """Sin probar TODAS las combinaciones (inviable, ver docstring de busqueda_features_slurm.py): la forma
    de saber si el mejor resultado encontrado ya es "suficientemente bueno" es ver si la busqueda se
    estanco -- si hace rato que ninguna eleccion nueva supera al mejor visto hasta ahora, agregar mas --z
    probablemente no va a cambiar mucho; si la mejora fue en una de las ultimas elecciones, todavia vale la
    pena seguir."""
    mejor_por_iter = {}
    for r in detalle:
        if r["iteracion"] and r["accuracy"] is not None:
            mejor_por_iter[r["iteracion"]] = max(mejor_por_iter.get(r["iteracion"], 0), r["accuracy"])
    if not mejor_por_iter:
        return {}
    xs = sorted(mejor_por_iter)
    total = xs[-1]
    mejor, iter_mejor = -1.0, xs[0]
    for x in xs:
        if mejor_por_iter[x] > mejor:
            mejor, iter_mejor = mejor_por_iter[x], x
    sin_mejora = total - iter_mejor
    return {"total_elecciones": total, "eleccion_del_mejor": iter_mejor,
            "elecciones_sin_mejora_despues": sin_mejora,
            "porcentaje_sin_mejora": sin_mejora / total if total else 0.0}


def resumen_ejecutivo(detalle: list[dict]) -> str:
    """Texto corto tipo informe -- el UNICO lugar donde se traducen los codigos a nombre de modelo (para que
    se lea facil); mejor combinacion (y cuanto mejora sobre la linea base), ranking de modelos, y si usar mas
    kpoints/angulos/proporciones realmente ayuda (correlacion simple con el accuracy)."""
    import numpy as np

    base_cod = MODELOS_CODIGO.get("linea_base", 0)
    validos = [r for r in detalle if r["modelo"] != base_cod and r["accuracy"] is not None]
    base = next((r for r in detalle if r["modelo"] == base_cod and r["accuracy"] is not None), None)
    lineas = ["RESUMEN EJECUTIVO -- busqueda de features", "=" * 42, ""]
    n_escenarios = len({r["escenario"] for r in validos})
    lineas.append(f"{len(validos)} pruebas validas (escenario x modelo), {n_escenarios} escenarios distintos.")
    if base:
        lineas.append(f"Linea base (todo activado, clasificador que solo predice la clase mas frecuente): "
                      f"accuracy={base['accuracy']:.3f}")
    if not validos:
        lineas.append("\nSin pruebas validas todavia -- corre busqueda_features_slurm.py primero.")
        return "\n".join(lineas)

    mejor = validos[0]   # detalle ya viene ordenado por f1_macro descendente
    nombre_mejor = NOMBRE_MODELO.get(mejor["modelo"], f"modelo#{mejor['modelo']}")
    lineas += ["", f"Mejor combinacion encontrada: {nombre_mejor}  f1={mejor['f1_macro']:.3f} acc={mejor['accuracy']:.3f}",
              f"  escenario={mejor['escenario']}  llave={mejor['llave']}",
              f"  {mejor['n_kpoints']} kpoints + {mejor['n_angulos']} angulos + {mejor['n_proporciones']} proporciones"
              f" = {mejor['n_elementos']} elementos (ver detalle.csv fila llave={mejor['llave']} para el detalle exacto)"]
    if base:
        mejora = mejor["accuracy"] - base["accuracy"]
        lineas.append(f"  mejora sobre la linea base: {mejora:+.3f} ({mejora / max(base['accuracy'], 1e-9):+.0%})")

    por_modelo = defaultdict(list)
    for r in validos:
        por_modelo[r["modelo"]].append(r["f1_macro"])
    ranking = sorted(por_modelo.items(), key=lambda kv: statistics.mean(kv[1]), reverse=True)[:5]
    lineas += ["", "Top 5 modelos por F1 promedio (sobre todos los escenarios que probaron):"]
    lineas += [f"  {i + 1}. {NOMBRE_MODELO.get(mo, f'modelo#{mo}'):20s} f1_prom={statistics.mean(f1s):.3f}  (n={len(f1s)})"
              for i, (mo, f1s) in enumerate(ranking)]

    def _corr(campo):
        xs = np.array([r[campo] for r in validos], dtype=float)
        ys = np.array([r["accuracy"] for r in validos], dtype=float)
        if xs.std() == 0 or ys.std() == 0:
            return 0.0
        return float(np.corrcoef(xs, ys)[0, 1])

    lineas += ["", "Correlacion tamano-de-combinacion vs accuracy (cerca de 0 = no importa cuantos uses;",
              "positivo = usar mas ayuda; negativo = usar menos es mejor):",
              f"  n_kpoints:      r={_corr('n_kpoints'):+.2f}",
              f"  n_angulos:      r={_corr('n_angulos'):+.2f}",
              f"  n_proporciones: r={_corr('n_proporciones'):+.2f}"]

    conv = analisis_convergencia(detalle)
    if conv:
        pct = conv["porcentaje_sin_mejora"]
        if pct >= 0.3:
            veredicto = ("la busqueda parece ESTANCADA: hace rato que ninguna eleccion nueva supera al "
                        "mejor -- correr mas --z probablemente no mejora mucho mas esto.")
        else:
            veredicto = ("el mejor resultado es RECIENTE -- todavia esta mejorando, conviene correr mas "
                        "combinaciones (mas --z, o re-correr: el historial no repite lo ya probado).")
        lineas += ["", "Convergencia (¿ya probaste suficiente, o vale la pena seguir?):",
                  f"  mejor resultado en la eleccion #{conv['eleccion_del_mejor']} de {conv['total_elecciones']} totales",
                  f"  {conv['elecciones_sin_mejora_despues']} elecciones despues sin superarlo ({pct:.0%} del total)",
                  f"  -> {veredicto}"]
    return "\n".join(lineas)


def _escribir_csv(filas, ruta):
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        campos = list(filas[0].keys()) if filas else []
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(filas)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", nargs="+", required=True, help="uno o mas .csv de busqueda_features_slurm.py (admite patrones, p.ej. resultados/resultados_*.csv)")
    ap.add_argument("--salida", default="resumen_slurm", help="carpeta donde dejar detalle.csv / matriz_resumen.csv / graficos/")
    args = ap.parse_args(argv)

    rutas = sorted({r for patron in args.csv for r in (glob.glob(patron) or [patron])})
    faltantes = [r for r in rutas if not Path(r).exists()]
    if faltantes:
        raise SystemExit(f"No existen: {', '.join(faltantes)}")
    if not rutas:
        raise SystemExit("Ningun .csv coincide con --csv")

    destino = Path(args.salida)
    graficos = destino / "graficos"
    graficos.mkdir(parents=True, exist_ok=True)

    detalle = armar_detalle(rutas)
    _escribir_csv(detalle, destino / "detalle.csv")
    matriz = armar_matriz(detalle)
    _escribir_csv(matriz, destino / "matriz_resumen.csv")
    tiene_progreso = grafico_progreso(detalle, graficos / "progreso.png")
    tiene_costo = grafico_costo(detalle, graficos / "costo.png")
    tiene_calor = grafico_calor(matriz, graficos / "matriz_calor.png")
    texto = resumen_ejecutivo(detalle)
    (destino / "resumen.txt").write_text(texto, encoding="utf-8")

    print(f"{len(rutas)} archivo(s) de entrada, {len(detalle)} filas de detalle, {len(matriz)} filas en la matriz resumen")
    print(f"-> {destino / 'detalle.csv'}")
    print(f"-> {destino / 'matriz_resumen.csv'}")
    print(f"-> {graficos / 'progreso.png'}" if tiene_progreso else "  (sin escenarios para graficar progreso)")
    print(f"-> {graficos / 'costo.png'}" if tiene_costo else "  (sin escenarios para graficar costo)")
    print(f"-> {graficos / 'matriz_calor.png'}" if tiene_calor else "  (sin escenarios para la matriz de calor)")
    print(f"-> {destino / 'resumen.txt'}")
    print()
    print(texto)


if __name__ == "__main__":
    main()
