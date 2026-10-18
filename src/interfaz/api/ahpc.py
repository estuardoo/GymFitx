"""AHPC: modulo independiente para armar, con los datos ya generados (table_frames_fix en SQL), el paquete
completo para correr la busqueda de features en un cluster/supercomputador: el .npz autocontenido de cada
ejercicio elegido + el script standalone scripts/busqueda_features_slurm.py (sin SQL, sin FastAPI, sin el
resto de GYMFITX) + un .sbatch por ejercicio ya apuntando a su dataset. Se sube el .zip al cluster, se
descomprime y se corre "sbatch slurm_<ejercicio>.sbatch" ahi mismo. No genera datos nuevos: solo empaqueta
lo que ya esta en las tablas SQL."""

from __future__ import annotations

import json
import zipfile
from io import BytesIO

from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response

from scripts.busqueda_features_slurm import MODELOS_CODIGO
from src.almacenamiento import dataset_sql as SQL
from src.entrenamiento.exportar_slurm import exportar
from src.etiquetado.manifest import _manifest
from src.nucleo.config import ROOT, SLURM_DIR
from src.nucleo.ejercicio import puntos_de_ejercicio

router = APIRouter()

SCRIPT = ROOT / "scripts" / "busqueda_features_slurm.py"
RESUMEN_SCRIPT = ROOT / "scripts" / "resumen_busqueda_slurm.py"
ESTADO_SCRIPT = ROOT / "scripts" / "estado_busqueda_slurm.py"
DIAGNOSTICO_SCRIPT = ROOT / "scripts" / "diagnostico_hpc.sh"
SBATCH_PLANTILLA = ROOT / "scripts" / "slurm_busqueda_features.sbatch"
RESUMEN_SBATCH_PLANTILLA = ROOT / "scripts" / "slurm_resumen_features.sbatch"
LANZADOR_PLANTILLA = ROOT / "scripts" / "lanzar_busqueda_slurm.sh"

LEEME = """AHPC -- paquete listo para el cluster
=====================================

Estructura de esta carpeta (ver tambien config.json):
  input/       el .npz de cada ejercicio (insumos: puntos x,y,z, angulos, proporciones)
  resultados/  un .csv y un .estado.json por tarea del array -- los crea el .sbatch solo (mkdir -p), NO
               vienen en el zip
  logs/        salida de cada tarea SLURM -- lo crea el .sbatch solo (mkdir -p), NO viene en el zip
  resumen_<ejercicio>/  detalle.csv, matriz_resumen.csv, graficos/, resumen.txt -- si usaste
                 lanzar_<ejercicio>.sh, esto lo arma SOLO el cluster (no viene en el zip); si corriste
                 resumen_busqueda_slurm.py a mano, queda donde le hayas puesto --salida

1. Sube esta carpeta descomprimida al supercomputador (scp/rsync/lo que uses).
2. ANTES de mandar nada grande, corre (en el login node, dentro de esta misma carpeta):
     bash diagnostico_hpc.sh
   Te deja un .txt con: que particion tiene nodos sin GPU (no hace falta GPU, sklearn no la usa), si estan
   libres ahora, los limites de cada particion, y una prueba real de 10 combinaciones para medir cuanto
   tarda una combinacion EN ESE cluster -- con eso decides --partition/--array del .sbatch con datos
   reales, no a ciegas.
3. Abre cada slurm_<ejercicio>.sbatch y ajusta partition/modulos/venv segun lo que te dijo el diagnostico.
   Si vas a usar el paso 4 (recomendado), ese modulo/venv necesita TAMBIEN matplotlib instalado, ademas de
   numpy/scikit-learn (resumen_busqueda_slurm.py lo usa para las graficas).
4. Por cada ejercicio, UN SOLO comando -- lanza la busqueda (el array de 72 tareas) y, apenas ese array
   termine (aunque alguna tarea haya fallado), el resumen (detalle.csv/matriz_resumen.csv/graficos/
   resumen.txt), encadenados con --dependency de SLURM: no hace falta que vuelvas a entrar ni que corras
   nada a mano entre uno y otro.
     bash lanzar_<ejercicio>.sh
   (Reusa la particion/modulo que pusiste en el paso 3, los lee de ese mismo .sbatch.) Si preferis lanzar
   solo la busqueda, sin el resumen automatico, seguis pudiendo: sbatch slurm_<ejercicio>.sbatch
5. Mientras corre (o despues), para saber el avance sin adivinar por squeue/sacct (en el login node, dentro
   de resultados/):
     python ../estado_busqueda_slurm.py --resultados .
   Te arma una tabla por tarea: cuantas combinaciones hizo de las que le tocan, %, si termino o si fallo.
   No necesita numpy/sklearn -- se puede correr aunque el modulo de python este roto.
6. Cuando ambos jobs de lanzar_<ejercicio>.sh terminen (squeue -u $USER vacio para ellos), la matriz ya esta
   lista en resumen_<ejercicio>/ DENTRO DEL CLUSTER -- baja esa carpeta a tu PC (scp/rsync) y listo.
   Si en cambio lanzaste solo el .sbatch (paso 4, alternativa manual), la busqueda se corto antes de tiempo
   pero ya tenes .csv en resultados/ que alcanzan, o queres sumar mas corridas viejas que bajaste antes,
   podes armar/actualizar el resumen sin esperar a lanzar_<ejercicio>.sh de nuevo -- 2 formas:
     sbatch slurm_resumen_<ejercicio>.sbatch                                        (como job, en el cluster)
     python resumen_busqueda_slurm.py --csv resultados_*.csv --salida resumen_<ejercicio>/   (a mano, cluster o PC)
   Te deja detalle.csv (una fila por combinacion+modelo probada, todo codificado: ver "codigos" abajo),
   matriz_resumen.csv (formato largo, listo para pivotear en Excel: type/accuracy_bucket/modelo/escenario/
   n_elementos/llave -- una fila por bucket de accuracy de 1% sin colisionar) y graficos/ (progreso.png,
   costo.png, matriz_calor.png).

Todo en detalle.csv y matriz_resumen.csv esta CODIFICADO (sin nombres ni texto) -- para eso esta tu tabla
SQL. Lo unico que no esta en otro lado es el codigo numerico de cada modelo: ver "modelos_codigo" en
config.json. llave = escenario*100 + codigo_modelo (identifica una fila sin coordinacion entre tareas
paralelas). Las columnas K01..KN/A01..AN/P01..PN son 0/1: si ese kpoint/angulo/proporcion (por su POSICION,
1 a N) se uso en esa combinacion o no. K0N es la posicion EN ESTE ejercicio, no el landmark en si -- para
saber a que punto real corresponde, ver "kpoints_codigo" en config.json (codigo universal C../M../D.. por
ejercicio).

busqueda_features_slurm.py es standalone: solo necesita numpy y scikit-learn, no depende de SQL ni de
FastAPI ni del resto de GYMFITX. Prueba el catalogo COMPLETO de modelos (los mismos del panel Entrenamiento)
contra subconjuntos al azar de kpoints/angulos/proporciones. Cada combinacion probada queda anotada en
<ejercicio>.historial.json junto al .npz, con un numero de escenario global que nunca se repite ni se
reasigna: si vuelves a correr el script sobre el mismo .npz (para agregar mas pruebas), las combinaciones
nuevas NO repiten las que ya se probaron antes y siguen la numeracion donde se quedo.

Por default el sorteo es puro azar. Agregando --heuristico al comando del .sbatch, antes de sortear se
entrena una referencia rapida para medir que kpoint/angulo/proporcion importa mas, y el sorteo queda sesgado
hacia eso (sin dejar de explorar el resto) -- con el mismo --z suele encontrar mejores combinaciones mas
rapido que el azar puro.

Agregando --escalada, cada tarea deja de sortear combinaciones sueltas y hace su propio hill-climbing local:
prueba un lote inicial, se queda con la mejor, y prueba vecinos (un kpoint/angulo/proporcion agregado o
quitado a la vez) -- se mueve ahi si mejora, descarta si no. Con --escalada, --z es el presupuesto POR
TAREA, no el total repartido entre las 72 como sin ella. Se puede combinar con --heuristico. Todo sigue
comparandose contra la linea_base de siempre (escenario=-1).

Agregando ADEMAS --arranques N (requiere --escalada), en vez de escalar desde LA mejor del lote nomas, cada
tarea escala desde las N mejores del lote -- una cadena de vecinos independiente por cada una, repartiendo
el presupuesto restante entre todas -- y se queda con la mejor de todas las cadenas. Mas robusto contra
quedarse pegado en el primer optimo local que encuentra, mismo --z total. --arranques 1 (default) = una
sola cadena, como sin esta opcion.

Si el cluster corta corridas que intentan las 72 tareas (cada una con el catalogo de ~18 modelos) a la vez,
--modelo <nombre> (ver "modelos_codigo" arriba, en texto: random_forest/svm/xgboost/etc.) reparte el
paralelismo POR MODELO en vez de por tarea -- una tarea por modelo, cada una entrena SOLO el suyo (mucho
mas liviano). Cambia --array del .sbatch de 0-71 a 0-(N_MODELOS-1) y agrega --modelo a mano, un modelo
distinto por indice del array (ver el bloque comentado al final de slurm_<ejercicio>.sbatch, ya armado).
Cada tarea deja, ademas de su .estado.json, un <su .csv>.avance.txt (texto plano, se actualiza cada 5
minutos, con inicio/fin/duracion_seg de esa tarea al terminar) -- 'cat resultados/*.avance.txt' alcanza
para ver el avance de todas sin json.loads.
"""


def _sbatch_para(ejercicio: str) -> str:
    """La plantilla de ejemplo, con --dataset/--job-name puestos para este ejercicio."""
    txt = SBATCH_PLANTILLA.read_text(encoding="utf-8")
    txt = txt.replace("gymfit_busqueda", f"gymfit_{ejercicio}")
    txt = txt.replace("input/manguito_rotador.npz", f"input/{ejercicio}.npz")
    return txt


def _resumen_sbatch_para(ejercicio: str) -> str:
    """sbatch del resumen SOLO (sin la busqueda), para cuando ya tenes todos los .csv en resultados/ (la
    busqueda termino, o se corto pero alcanza lo que hay) y queres correr/actualizar el resumen como un job
    aparte en vez de a mano en el login node -- ver LEEME.txt."""
    return RESUMEN_SBATCH_PLANTILLA.read_text(encoding="utf-8").replace("manguito_rotador", ejercicio)


def _lanzar_para(ejercicio: str) -> str:
    """La plantilla del lanzador (arma busqueda + resumen en 2 sbatch encadenados con --dependency, ver
    scripts/lanzar_busqueda_slurm.sh), con el nombre del ejercicio puesto en todos los placeholders."""
    return LANZADOR_PLANTILLA.read_text(encoding="utf-8").replace("manguito_rotador", ejercicio)


def _config_json(ejercicios: list[str], codigos_por_ejercicio: dict[str, list[str]]) -> str:
    """Un solo config.json para todo el paquete (las carpetas y los codigos de modelo son iguales para
    cualquier ejercicio) -- SIN nombres de kpoints/angulos/proporciones: eso ya esta en tu tabla SQL, aca
    solo las rutas y las leyendas que no existen en otro lado (codigo de cada modelo, y K0N -> codigo
    universal de landmark de cada ejercicio, para no confundirlos al leer resultados)."""
    return json.dumps({
        "carpetas": {
            "input": "input/ -- el .npz de cada ejercicio (insumos: puntos x,y,z, angulos, proporciones)",
            "resultados": "resultados/ -- un .csv y un .estado.json por tarea del array (los crea el .sbatch solo, con mkdir -p)",
            "logs": "logs/ -- salida de cada tarea SLURM (los crea el .sbatch solo, con mkdir -p)",
            "graficos": "resumen_<ejercicio>/graficos/ -- los arma lanzar_<ejercicio>.sh solo en el cluster "
            "(o resumen_busqueda_slurm.py a mano, ahi o en tu PC)",
        },
        "modelos_codigo": MODELOS_CODIGO,
        "kpoints_codigo": {ej: {f"K{i + 1:02d}": cod for i, cod in enumerate(codigos)}
                           for ej, codigos in codigos_por_ejercicio.items()},
        "ejercicios": sorted(ejercicios),
        "archivo_leeme": "LEEME.txt",
        "scripts": [SCRIPT.name, RESUMEN_SCRIPT.name, ESTADO_SCRIPT.name, DIAGNOSTICO_SCRIPT.name]
        + [f"slurm_{e}.sbatch" for e in sorted(ejercicios)]
        + [f"slurm_resumen_{e}.sbatch" for e in sorted(ejercicios)]
        + [f"lanzar_{e}.sh" for e in sorted(ejercicios)],
    }, ensure_ascii=False, indent=2)


@router.get("/api/ahpc/ejercicios")
def ahpc_ejercicios():
    """Un ejercicio por fila: cuantos clips tiene en el manifest (bien/mal, sin 'base') y si ya tiene
    catalogo de kpoints (si no, no se puede exportar)."""
    conteo: dict[str, int] = {}
    for r in _manifest():
        if r["clase"] not in ("base",):
            conteo[r["exercise"]] = conteo.get(r["exercise"], 0) + 1
    return [{"ejercicio": ej, "clips": n, "listo": bool(puntos_de_ejercicio(ej))}
            for ej, n in sorted(conteo.items())]


@router.post("/api/ahpc/exportar")
def ahpc_exportar(body: dict):
    """body: {ejercicios: [nombre, ...]}. Arma un .zip con el .npz de cada ejercicio (rehecho con lo que hay
    ahora mismo en SQL), el script standalone busqueda_features_slurm.py y un .sbatch por ejercicio ya
    apuntando a su dataset -- listo para subir al cluster y correr sbatch ahi. Los ejercicios que fallen
    (sin datos, sin catalogo) van en la cabecera X-Ahpc-Errores y no rompen el zip de los demas."""
    ejercicios = body.get("ejercicios") or []
    if not ejercicios:
        return JSONResponse({"error": "Elige al menos un ejercicio"}, status_code=400)

    ok, ok_ejercicios, errores = [], [], {}
    buf = BytesIO()
    try:
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
            for ej in ejercicios:
                try:
                    resumen = exportar(ej, SLURM_DIR / f"{ej}.npz")
                except ValueError as e:
                    errores[ej] = str(e)
                    continue
                z.write(resumen["archivo"], arcname=f"input/{ej}.npz")
                z.writestr(f"slurm_{ej}.sbatch", _sbatch_para(ej))
                z.writestr(f"slurm_resumen_{ej}.sbatch", _resumen_sbatch_para(ej))
                z.writestr(f"lanzar_{ej}.sh", _lanzar_para(ej))
                ok.append(resumen)
                ok_ejercicios.append(ej)
            if ok:
                z.write(SCRIPT, arcname=SCRIPT.name)
                z.write(RESUMEN_SCRIPT, arcname=RESUMEN_SCRIPT.name)
                z.write(ESTADO_SCRIPT, arcname=ESTADO_SCRIPT.name)
                z.write(DIAGNOSTICO_SCRIPT, arcname=DIAGNOSTICO_SCRIPT.name)
                z.writestr("LEEME.txt", LEEME)
                codigos = {ej: r["point_codes"] for ej, r in zip(ok_ejercicios, ok)}
                z.writestr("config.json", _config_json(ok_ejercicios, codigos))
    except SQL.SQLServerNoDisponible as e:
        return JSONResponse({"error": f"SQL Server no disponible: {e}"}, status_code=400)
    if not ok:
        return JSONResponse({"error": "Ninguno se pudo exportar", "detalle": errores}, status_code=400)

    headers = {"Content-Disposition": 'attachment; filename="ahpc_slurm.zip"'}
    if errores:
        headers["X-Ahpc-Errores"] = json.dumps(errores, ensure_ascii=False)
    return Response(content=buf.getvalue(), media_type="application/zip", headers=headers)
