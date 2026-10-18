"""Exportar dataset para SLURM (src/entrenamiento/exportar_slurm.py): un .npz autocontenido por ejercicio,
sin aplanar, para el script standalone scripts/busqueda_features_slurm.py -- ver ambos para el flujo completo."""
import numpy as np
import pytest


@pytest.fixture
def entorno(tmp_path, monkeypatch):
    from src.almacenamiento import dataset_sql as SQL
    from src.entrenamiento import datos as DATOS
    from src.entrenamiento import exportar_slurm as EXP
    from src.etiquetado import manifest as MAN
    from src.nucleo import ejercicio as EJ

    nombres = ["a", "b", "c"]
    feats = [{"name": "ang", "type": "angle", "points": ["a", "b", "c"]},
             {"name": "pro", "type": "proporcion", "points": ["a", "b"], "cadena": ["a", "b", "c"]}]
    filas = [{"clip": f"{'bien' if i % 2 else 'mal'}/c{i}.mp4", "clase": "bien" if i % 2 else "mal",
              "type": 1, "origen": f"x/{i}.mp4"} for i in range(6)]
    filas.append({"clip": "base/b.mp4", "clase": "base", "type": 1, "origen": "x"})
    crudos = {r["clip"]: (np.zeros((4, 3, 3), dtype=np.float32), np.zeros((4, 2), dtype=np.float32)) for r in filas}

    monkeypatch.setattr(EJ, "puntos_de_ejercicio", lambda ex: nombres)
    monkeypatch.setattr(EJ, "features_de_ejercicio", lambda ex: feats)
    monkeypatch.setattr(SQL, "tipo_de_ejercicio", lambda ex: 1)
    monkeypatch.setattr(SQL, "frames_fix_por_archivo", lambda t: crudos)
    monkeypatch.setattr(MAN, "_manifest", lambda: filas)
    monkeypatch.setattr(EXP, "_manifest", lambda: filas)
    monkeypatch.setattr(DATOS, "seleccion", lambda: {})
    monkeypatch.setattr(EXP, "seleccion", lambda: {})
    return EXP, tmp_path / "out.npz"


def test_exporta_solo_bien_mal_con_las_metricas_activadas(entorno):
    EXP, out = entorno
    resumen = EXP.exportar("cualquiera", out)
    assert resumen["clips"] == 6 and resumen["kpoints"] == 3 and resumen["metricas"] == 2   # 'base' fuera
    d = np.load(out, allow_pickle=True)
    assert d["points"].shape == (6, 4, 3, 3) and d["metrics"].shape == (6, 4, 2)
    assert set(d["metric_types"]) == {"angle", "proporcion"}
    assert set(d["y"]) == {"bien", "mal"}


def test_sin_clips_en_sql_avisa(entorno, monkeypatch):
    from src.almacenamiento import dataset_sql as SQL
    EXP, out = entorno
    monkeypatch.setattr(SQL, "frames_fix_por_archivo", lambda t: {})
    with pytest.raises(ValueError, match="genera cortes"):
        EXP.exportar("cualquiera", out)


def _npz_sintetico(ruta, n=20, T=5, N=4, A=2, semilla=0):
    import numpy as np
    rng = np.random.default_rng(semilla)
    y = np.array(["bien" if i % 2 == 0 else "mal" for i in range(n)])
    np.savez_compressed(ruta, points=rng.normal(size=(n, T, N, 3)).astype(np.float32),
                        point_names=np.array([f"kp{i}" for i in range(N)]),
                        metrics=rng.uniform(size=(n, T, A)).astype(np.float32),
                        metric_names=np.array(["ang1", "prop1"]), metric_types=np.array(["angle", "proporcion"]),
                        clips=np.array([f"c{i}.mp4" for i in range(n)]), y=y, ejercicio="prueba", tipo=1)


def _n_modelos():
    from scripts import busqueda_features_slurm as BUS
    return len(BUS.modelos())


def test_busqueda_features_slurm_corre_de_punta_a_punta(tmp_path):
    """El script de scripts/ es standalone (sin 'from src'): se prueba como se usaria de verdad, por
    subprocess con un .npz sintetico -- incluido el reparto en tareas (SLURM array) igual de reproducible.
    Cada comparacion usa su PROPIO .npz (y por lo tanto su propio historial.json) para que el 'no repetir
    entre corridas' de otro test no le cambie el reparto a este."""
    import subprocess
    import sys

    script = "scripts/busqueda_features_slurm.py"
    n_modelos = _n_modelos()

    ds = tmp_path / "ds_entero.npz"
    _npz_sintetico(ds)
    salida = tmp_path / "res.csv"
    subprocess.run([sys.executable, script, "--dataset", str(ds), "--z", "6", "--semilla", "1",
                    "--no-escalada", "--salida", str(salida)], check=True, capture_output=True, text=True)
    filas = salida.read_text("utf-8").strip().splitlines()
    assert len(filas) == 1 + 6 * n_modelos + 1   # header + 6 combos x N modelos + linea_base

    # el mismo reparto (misma semilla, dataset nuevo sin historial previo) entre 2 tareas suma lo mismo
    # que una sola corrida (menos la linea_base repetida)
    ds2 = tmp_path / "ds_repartido.npz"
    _npz_sintetico(ds2)
    partes = []
    for t in (0, 1):
        s = tmp_path / f"res_{t}.csv"
        subprocess.run([sys.executable, script, "--dataset", str(ds2), "--z", "6", "--semilla", "1", "--no-escalada",
                        "--tarea-id", str(t), "--n-tareas", "2", "--salida", str(s)], check=True, capture_output=True)
        partes.append(len(s.read_text("utf-8").strip().splitlines()) - 1)
    assert sum(partes) == len(filas) - 1


def test_busqueda_deja_estado_json_con_avance_y_terminado(tmp_path):
    """<salida>.estado.json (ver guardar_estado): terminado=true al final, combos/objetivo/filas coherentes
    con lo que de verdad se corrio -- es lo que lee estado_busqueda_slurm.py para armar la tabla de avance."""
    import json
    import subprocess
    import sys

    script = "scripts/busqueda_features_slurm.py"
    n_modelos = _n_modelos()
    ds = tmp_path / "ds_estado.npz"
    _npz_sintetico(ds)
    salida = tmp_path / "res_estado.csv"
    subprocess.run([sys.executable, script, "--dataset", str(ds), "--z", "6", "--semilla", "1", "--no-escalada",
                    "--salida", str(salida)], check=True, capture_output=True, text=True)

    estado = json.loads(salida.with_suffix(".estado.json").read_text("utf-8"))
    assert estado["terminado"] is True and estado["error"] == ""
    assert estado["combos"] == estado["objetivo"] == 6
    assert estado["pct"] == 100.0
    assert estado["filas"] == 1 + 6 * n_modelos   # linea_base + 6 combos x N modelos (sin el header)


def test_busqueda_con_modelo_evalua_solo_ese_modelo(tmp_path):
    """--modelo (paralelismo por modelo en vez de por --n-tareas, ver slurm_busqueda_features.sbatch):
    filtra el catalogo a un solo modelo -- la linea_base (tarea 0, aparte del catalogo) sigue saliendo."""
    import csv
    import subprocess
    import sys

    from scripts.busqueda_features_slurm import MODELOS_CODIGO

    script = "scripts/busqueda_features_slurm.py"
    ds = tmp_path / "ds_modelo.npz"
    _npz_sintetico(ds)
    salida = tmp_path / "res_modelo.csv"
    subprocess.run([sys.executable, script, "--dataset", str(ds), "--z", "3", "--semilla", "1", "--no-escalada",
                    "--modelo", "random_forest", "--salida", str(salida)], check=True, capture_output=True, text=True)

    with salida.open(encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    assert len(filas) == 1 + 3   # linea_base + 3 combos x 1 modelo
    modelos_vistos = {int(r["modelo"]) for r in filas}
    assert modelos_vistos == {MODELOS_CODIGO["linea_base"], MODELOS_CODIGO["random_forest"]}


def test_busqueda_con_modelo_desconocido_falla_claro(tmp_path):
    import subprocess
    import sys

    script = "scripts/busqueda_features_slurm.py"
    ds = tmp_path / "ds_modelo_malo.npz"
    _npz_sintetico(ds)
    r = subprocess.run([sys.executable, script, "--dataset", str(ds), "--z", "3", "--modelo", "no_existe",
                        "--salida", str(tmp_path / "res.csv")], capture_output=True, text=True)
    assert r.returncode != 0 and "no es un modelo conocido" in r.stderr


def test_busqueda_deja_avance_txt_con_inicio_fin_y_duracion(tmp_path):
    """<salida>.avance.txt (ver guardar_avance_txt): texto plano con el mismo avance que estado.json, mas
    inicio/fin/duracion_seg de esta tarea -- pensado para un vistazo rapido en el cluster sin json.loads."""
    import subprocess
    import sys

    script = "scripts/busqueda_features_slurm.py"
    ds = tmp_path / "ds_avance.npz"
    _npz_sintetico(ds)
    salida = tmp_path / "res_avance.csv"
    subprocess.run([sys.executable, script, "--dataset", str(ds), "--z", "4", "--semilla", "1", "--no-escalada",
                    "--modelo", "random_forest", "--salida", str(salida)], check=True, capture_output=True, text=True)

    txt = salida.with_suffix(".avance.txt").read_text(encoding="utf-8")
    assert "modelo: random_forest" in txt
    assert "avance: 4/4" in txt
    assert "inicio:" in txt and "fin:" in txt and "duracion_seg:" in txt


def test_busqueda_no_repite_combinaciones_entre_corridas(tmp_path):
    """Correr el script 2 veces sobre el MISMO dataset (mismo --semilla, mismo --z) no repite combinaciones:
    la 2da corrida agrega escenarios NUEVOS (numeracion global, nunca reasignada), no vuelve a probar ni
    renumera los de la 1ra."""
    import subprocess
    import sys

    script = "scripts/busqueda_features_slurm.py"
    ds = tmp_path / "ds.npz"
    _npz_sintetico(ds, N=4)   # 4 kpoints, 1 angulo, 1 proporcion -> 15 combinaciones posibles (espacio > 2*z)

    escenarios_por_corrida = []
    for i in (1, 2):
        s = tmp_path / f"res_{i}.csv"
        subprocess.run([sys.executable, script, "--dataset", str(ds), "--z", "6", "--semilla", "1", "--no-escalada",
                        "--salida", str(s)], check=True, capture_output=True, text=True)
        import csv
        with s.open(encoding="utf-8") as f:
            filas = [r for r in csv.DictReader(f) if r["escenario"] != "-1"]   # sin la linea_base
        escenarios_por_corrida.append({r["escenario"] for r in filas})

    assert escenarios_por_corrida[0] and escenarios_por_corrida[1]
    assert not (escenarios_por_corrida[0] & escenarios_por_corrida[1])   # ningun escenario se repite entre corridas
    assert (ds.parent / "ds.historial.json").exists()


def test_eleccion_ponderada_favorece_los_indices_de_mas_peso():
    """Tamano de subconjunto fijo en 1 (se pisa rng.randint) para medir SOLO el sesgo por peso, sin que lo
    tape el tamano al azar -- con k=1 por sorteo, el indice de mas peso debe salir elegido mucho mas seguido."""
    import random

    from scripts import busqueda_features_slurm as BUS

    class _RngK1(random.Random):
        def randint(self, a, b):
            return 1

    rng = _RngK1(0)
    pesos = [0.01] * 10
    pesos[5] = 5.0
    conteo = [0] * 10
    for _ in range(1000):
        for i in BUS._elige_subconjunto(rng, 10, pesos):
            conteo[i] += 1
    assert conteo[5] == max(conteo)
    assert conteo[5] > conteo[0] * 5   # claramente mas que un indice de peso bajo


def test_importancias_devuelve_pesos_positivos_del_tamano_correcto(tmp_path):
    from scripts import busqueda_features_slurm as BUS

    ds_ruta = tmp_path / "ds.npz"
    _npz_sintetico(ds_ruta, n=20, T=5, N=4, A=2)
    ds = BUS.cargar(ds_ruta)
    idx_ang = [i for i, t in enumerate(ds["metric_types"]) if t == "angle"]
    idx_pro = [i for i, t in enumerate(ds["metric_types"]) if t == "proporcion"]

    pesos_m, pesos_p, pesos_q = BUS.importancias(ds, idx_ang, idx_pro)
    assert len(pesos_m) == 4 and len(pesos_p) == 1 and len(pesos_q) == 1
    assert all(w > 0 for w in pesos_m + pesos_p + pesos_q)


def test_repetir_semilla_sobre_historial_grande_no_se_traba():
    """Bug real: si la 2da corrida usa la MISMA semilla que ya lleno el historial, el sorteo reproduce
    la secuencia identica de la 1ra -- si esa 1ra corrida ya paso de 200 (intentos_por_combo), la 2da se
    queda sin encontrar NINGUNA combinacion nueva (se agota el reintento antes de llegar a terreno nuevo).
    Fix: sumar len(vistas) a la semilla (lo que hace main()) corre el punto de partida del sorteo."""
    import random

    from scripts import busqueda_features_slurm as BUS

    m, p, q = 10, 1, 1   # 1023 combos posibles (angulos/proporciones no aportan variedad: solo 1 opcion cada uno)
    vistas = {}   # {firma: escenario_id}
    primeras = BUS.combinaciones_nuevas(random.Random(0), m, p, q, 220, vistas)
    assert len(primeras) == 220

    # misma semilla base (0), pero ajustada como en main(): rng = Random(semilla + len(vistas))
    segundas = BUS.combinaciones_nuevas(random.Random(0 + len(vistas)), m, p, q, 30, vistas)
    assert len(segundas) == 30   # sin el fix esto da 0 -- se agota a los 200 intentos repitiendo la 1ra secuencia


def test_campos_y_fila_codifican_todo_sin_texto():
    """La tabla detalle no debe llevar nombres/texto -- todo codigo. campos() define el ancho segun m/p/q
    de CADA ejercicio; _fila() calcula llave = escenario*100 + codigo_modelo (ver MODELOS_CODIGO)."""
    from scripts import busqueda_features_slurm as BUS

    assert BUS.campos(3, 2, 1) == (["llave", "type", "modelo", "escenario"] + ["K01", "K02", "K03"]
                                    + ["A01", "A02"] + ["P01"] + ["accuracy", "f1_macro", "error"])

    ds = {"tipo": 1}
    fila = BUS._fila(7, [0, 2], [1], [], ds, 3, 2, 1, {"modelo": "svm", "accuracy": 0.8, "f1_macro": 0.7, "error": ""})
    assert fila["llave"] == 7 * 100 + BUS.MODELOS_CODIGO["svm"]
    assert fila["escenario"] == 7 and fila["modelo"] == BUS.MODELOS_CODIGO["svm"]
    assert [fila["K01"], fila["K02"], fila["K03"]] == [1, 0, 1]
    assert (fila["A01"], fila["A02"], fila["P01"]) == (0, 1, 0)

    base = BUS._fila(-1, [0, 1, 2], [0, 1], [0], ds, 3, 2, 1,
                      {"modelo": "linea_base", "accuracy": 0.5, "f1_macro": 0.3, "error": ""})
    assert base["llave"] == -1 and base["escenario"] == -1 and base["modelo"] == 0   # linea_base


def test_vecino_cambia_un_solo_elemento():
    import random

    from scripts import busqueda_features_slurm as BUS

    rng = random.Random(0)
    combo = ([0, 2], [0], [])   # m=4 kpoints, p=1 angulo, q=0 proporciones
    for _ in range(30):
        v = BUS.vecino(rng, combo, 4, 1, 0)
        dif_k = set(combo[0]) ^ set(v[0])
        dif_a = set(combo[1]) ^ set(v[1])
        dif_p = set(combo[2]) ^ set(v[2])
        # cambia EXACTAMENTE 1 elemento, en UNA sola categoria (las otras dos quedan igual)
        assert len(dif_k) + len(dif_a) + len(dif_p) in (0, 1)   # 0 solo si tocaba quitar el ultimo de esa categoria (no se permite)


def test_vecino_no_deja_una_categoria_vacia():
    import random

    from scripts import busqueda_features_slurm as BUS

    rng = random.Random(0)
    combo = ([0], [], [])   # K con un solo elemento activo
    for _ in range(30):
        combo = BUS.vecino(rng, combo, 3, 0, 0)
        assert len(combo[0]) >= 1


def test_escalada_sube_el_score_mas_alla_del_lote_inicial():
    """Con un score que solo puede crecer agregando kpoints (evaluar_combo = cuantos K activos), la escalada
    deberia llegar a MAS elementos que el mejor del lote inicial al azar -- si no, no esta escalando de
    verdad, solo evaluando el lote y parando."""
    import random

    from scripts import busqueda_features_slurm as BUS

    rng = random.Random(1)
    vistas = {}
    m = 6
    llamadas = []

    def evaluar_combo(escenario, combo):
        llamadas.append((escenario, combo))
        return len(combo[0])   # score = cuantos kpoints activos -- max posible es m=6

    mejor_combo, mejor_score = BUS.escalada(rng, m, 0, 0, 50, vistas, evaluar_combo, lote=3, intentos_sin_mejora=30)

    assert mejor_score == m   # con m=6 y presupuesto de sobra, deberia saturar los 6 kpoints
    assert len(mejor_combo[0]) == m
    assert len(llamadas) > 3   # escalo mas alla del lote inicial (3), no se quedo solo con eso


def test_escalada_respeta_el_presupuesto_z():
    import random

    from scripts import busqueda_features_slurm as BUS

    rng = random.Random(2)
    vistas = {}
    llamadas = []

    def evaluar_combo(escenario, combo):
        llamadas.append(escenario)
        return len(combo[0])

    BUS.escalada(rng, 10, 0, 0, 7, vistas, evaluar_combo, lote=3, intentos_sin_mejora=100)
    assert len(llamadas) <= 7   # nunca evalua mas combinaciones nuevas que z, aunque intentos_sin_mejora sea generoso


def test_escalada_sin_espacio_no_revienta():
    """Si el lote inicial ya no encuentra NADA nuevo (espacio agotado desde el arranque), escalada() no debe
    fallar -- debe devolver None/-1.0 sin intentar escalar desde un combo inexistente."""
    import random

    from scripts import busqueda_features_slurm as BUS

    rng = random.Random(0)
    vistas = {BUS._firma(([0], [], [])): 1}   # el unico combo posible con m=1,p=0,q=0 ya esta visto
    mejor_combo, mejor_score = BUS.escalada(rng, 1, 0, 0, 5, vistas, lambda e, c: 1.0, lote=3)
    assert mejor_combo is None and mejor_score == -1.0


def test_multi_arranque_escapa_un_optimo_local_que_un_solo_arranque_no(monkeypatch):
    """--arranques>1: si la mejor del lote inicial es un pico aislado (todos sus vecinos valen menos), un
    solo arranque se queda pegado ahi -- con varios arranques, la cadena que sale de la SEGUNDA mejor del
    lote puede seguir creciendo y terminar superando la trampa. combinaciones_nuevas/vecino se reemplazan
    por versiones deterministas (fijan el lote y el camino de cada cadena) para no depender de que el rng
    real elija el vecino que hace falta -- lo que se prueba es la logica de escalada() (reparto del
    presupuesto entre arranques, cual gana al final), no vecino() (ya tiene sus propios tests)."""
    import random

    from scripts import busqueda_features_slurm as BUS

    def puntaje(combo):
        s = frozenset(combo[0])
        if s == frozenset({5}):
            return 50.0   # la trampa: alta al principio...
        if 5 in s:
            return 0.5    # ...pero CUALQUIER vecino suyo vale muy poco (pico aislado, sin escape)
        return len(s) * 30.0 if 0 in s else 0.1   # la rama que si puede crecer, sin tocar el 5

    def lote_fijo(rng, m, p, q, cantidad, vistas, **kw):
        opciones = [(101, ([5], [], [])), (102, ([0], [], []))]
        elegidas = opciones[:cantidad]
        for eid, combo in elegidas:
            vistas[BUS._firma(combo)] = eid
        return elegidas

    def vecino_determinista(rng, combo, m, p, q):
        pts = set(combo[0])
        if pts == {5}:
            return (sorted(pts | {1}), [], [])   # desde la trampa, siempre el mismo vecino (que vale poco)
        libres = [i for i in range(m) if i not in pts and i != 5]
        return (sorted(pts | {libres[0]}), [], []) if libres else (sorted(pts), [], [])

    monkeypatch.setattr(BUS, "combinaciones_nuevas", lote_fijo)
    monkeypatch.setattr(BUS, "vecino", vecino_determinista)

    llamadas = []

    def evaluar_combo(escenario, combo):
        llamadas.append(combo)
        return puntaje(combo)

    _, score_1 = BUS.escalada(random.Random(0), 6, 0, 0, 12, {}, evaluar_combo, lote=2, intentos_sin_mejora=3, arranques=1)
    assert score_1 == 50.0   # el unico arranque es la trampa: no tiene de donde escapar

    llamadas.clear()
    _, score_2 = BUS.escalada(random.Random(0), 6, 0, 0, 12, {}, evaluar_combo, lote=2, intentos_sin_mejora=3, arranques=2)
    assert score_2 > 50.0    # la segunda cadena (arranca en {0}, sin tocar el 5) escapa y supera la trampa
    assert len(llamadas) <= 12   # nunca evalua mas combinaciones nuevas que z, ni con varias cadenas


def test_busqueda_con_escalada_corre_de_punta_a_punta_y_reparte_historial_por_tarea(tmp_path):
    """--escalada con 2 tareas: cada una explora sola y guarda su PROPIO <dataset>.historial.tN.json (no se
    pisan entre si) -- el .csv de cada una tiene filas validas (header + N combos x modelos, sin contar la
    linea_base que solo escribe la tarea 0)."""
    import csv
    import json
    import subprocess
    import sys

    script = "scripts/busqueda_features_slurm.py"
    n_modelos = _n_modelos()
    ds = tmp_path / "ds.npz"
    _npz_sintetico(ds, N=6)   # mas kpoints: espacio grande, para que la escalada tenga donde moverse

    csvs = []
    for t in (0, 1):
        s = tmp_path / f"res_{t}.csv"
        subprocess.run([sys.executable, script, "--dataset", str(ds), "--z", "6", "--semilla", "1",
                        "--escalada", "--lote", "2", "--arranques", "2", "--tarea-id", str(t), "--n-tareas", "2",
                        "--salida", str(s)], check=True, capture_output=True, text=True)
        csvs.append(s)

    assert (tmp_path / "ds.historial.t0.json").exists() and (tmp_path / "ds.historial.t1.json").exists()
    hist0 = json.loads((tmp_path / "ds.historial.t0.json").read_text("utf-8"))
    hist1 = json.loads((tmp_path / "ds.historial.t1.json").read_text("utf-8"))
    assert not (set(hist0) & set(hist1))          # ninguna combinacion se repite entre las 2 tareas
    assert not (set(hist0.values()) & set(hist1.values()))   # ni sus escenario_id (bloques reservados sin chocar)

    with csvs[0].open(encoding="utf-8") as f:
        filas0 = list(csv.DictReader(f))
    with csvs[1].open(encoding="utf-8") as f:
        filas1 = list(csv.DictReader(f))
    assert filas0[0]["escenario"] == "-1"          # tarea 0 escribe la linea_base primero
    assert len(filas0) - 1 == len(hist0) * n_modelos
    assert len(filas1) == len(hist1) * n_modelos   # tarea 1 no escribe linea_base


def test_lote_y_arranques_usa_los_porcentajes_por_defecto_si_no_se_pasan():
    """--escalada es default ahora: sin --lote/--arranques explicitos, _lote_y_arranques() calcula 20%/10%
    de --z (ver PARAMETROS POR DEFECTO) -- un --lote/--arranques explicito siempre gana, se usa tal cual."""
    from scripts.busqueda_features_slurm import _lote_y_arranques

    assert _lote_y_arranques(500, None, None) == (100, 10)   # 20% de 500 = 100; 10% de 100 = 10
    assert _lote_y_arranques(6, None, None) == (1, 1)         # round(6*0.2)=1, max(1, round(1*0.1))=1 (piso)
    assert _lote_y_arranques(500, 50, None) == (50, 5)        # --lote explicito gana, --arranques sigue calculado sobre ESE lote
    assert _lote_y_arranques(500, None, 3) == (100, 3)        # --arranques explicito gana tal cual


def test_busqueda_con_heuristico_corre_de_punta_a_punta(tmp_path):
    """--heuristico agrega una corrida de referencia (no cuenta contra --z) pero el resto del flujo es igual."""
    import subprocess
    import sys

    script = "scripts/busqueda_features_slurm.py"
    n_modelos = _n_modelos()
    ds = tmp_path / "ds.npz"
    _npz_sintetico(ds)
    salida = tmp_path / "res.csv"

    subprocess.run([sys.executable, script, "--dataset", str(ds), "--z", "4", "--semilla", "1", "--no-escalada",
                    "--heuristico", "--salida", str(salida)], check=True, capture_output=True, text=True)
    filas = salida.read_text("utf-8").strip().splitlines()
    assert len(filas) == 1 + 4 * n_modelos + 1   # header + 4 combos x N modelos + linea_base (la referencia no suma filas)
