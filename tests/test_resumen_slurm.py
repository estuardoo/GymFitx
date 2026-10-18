"""scripts/resumen_busqueda_slurm.py: junta uno o varios .csv de busqueda_features_slurm.py en la matriz
resumen (formato largo), la tabla de detalle y las graficas -- ver ese script para el formato esperado
(todo codificado: llave/type/modelo/escenario + K01../A01../P01.. en 0/1)."""

from __future__ import annotations

import csv

from scripts import resumen_busqueda_slurm as RES

CAMPOS = ["llave", "type", "modelo", "escenario", "K01", "K02", "A01", "P01", "accuracy", "f1_macro", "error"]


def _csv(ruta, filas):
    with ruta.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        w.writerows(filas)


def _fila(escenario, modelo, f1, acc, k1=1, k2=0, a1=1, p1=0, tipo=1, error=""):
    llave = -1 if escenario < 0 else escenario * 100 + modelo
    return {"llave": llave, "type": tipo, "modelo": modelo, "escenario": escenario,
            "K01": k1, "K02": k2, "A01": a1, "P01": p1, "accuracy": acc, "f1_macro": f1, "error": error}


def test_armar_detalle_numera_iteraciones_por_escenario_y_bucket_1_por_ciento(tmp_path):
    a = tmp_path / "a.csv"
    b = tmp_path / "b.csv"
    _csv(a, [_fila(-1, 0, 0.5, 0.5), _fila(1, 1, 0.9, 0.95), _fila(1, 11, 0.6, 0.65)])
    _csv(b, [_fila(2, 1, 0.3, 0.35)])   # otra corrida -- escenario=2 sigue la numeracion global, no se repite

    detalle = RES.armar_detalle([str(a), str(b)])
    assert len(detalle) == 4
    iters = {r["escenario"]: r["iteracion"] for r in detalle}
    assert iters[-1] == 0          # linea_base no cuenta como eleccion
    assert iters[1] == 1
    assert iters[2] == 2           # sigue la numeracion del escenario, no del archivo
    rangos = {r["rango_accuracy"] for r in detalle if r["modelo"] == 1}
    assert rangos == {"95-96%", "35-36%"}   # bucket de 1%, no de 10%


def test_armar_detalle_calcula_n_elementos_de_las_columnas_kap(tmp_path):
    a = tmp_path / "a.csv"
    _csv(a, [_fila(1, 1, 0.9, 0.8, k1=1, k2=1, a1=1, p1=0)])
    detalle = RES.armar_detalle([str(a)])
    r = detalle[0]
    assert (r["n_kpoints"], r["n_angulos"], r["n_proporciones"], r["n_elementos"]) == (2, 1, 0, 3)


def test_armar_matriz_formato_largo_sin_colisionar_por_bucket(tmp_path):
    a = tmp_path / "a.csv"
    _csv(a, [_fila(-1, 0, 0.5, 0.5), _fila(1, 1, 0.9, 0.95), _fila(2, 1, 0.91, 0.96), _fila(3, 1, 0.4, 0.45)])
    matriz = RES.armar_matriz(RES.armar_detalle([str(a)]))
    assert len(matriz) == 3   # sin la linea base (modelo=0)
    claves = {(m["escenario"], m["accuracy_bucket"], m["modelo"]) for m in matriz}
    assert claves == {(1, "95-96%", 1), (2, "96-97%", 1), (3, "45-46%", 1)}
    assert all(m["llave"] == m["escenario"] * 100 + m["modelo"] for m in matriz)


def test_grafico_progreso_se_genera_si_hay_elecciones(tmp_path):
    a = tmp_path / "a.csv"
    _csv(a, [_fila(1, 1, 0.9, 0.8), _fila(2, 1, 0.95, 0.85)])
    detalle = RES.armar_detalle([str(a)])
    destino = tmp_path / "progreso.png"
    assert RES.grafico_progreso(detalle, destino) is True
    assert destino.exists() and destino.stat().st_size > 0


def test_grafico_costo_se_genera(tmp_path):
    a = tmp_path / "a.csv"
    _csv(a, [_fila(1, 1, 0.9, 0.7, k1=1, k2=0), _fila(2, 1, 0.95, 0.9, k1=1, k2=1)])
    detalle = RES.armar_detalle([str(a)])
    destino = tmp_path / "costo.png"
    assert RES.grafico_costo(detalle, destino) is True
    assert destino.exists() and destino.stat().st_size > 0


def test_armar_calor_cuenta_por_bucket_y_modelo(tmp_path):
    a = tmp_path / "a.csv"
    _csv(a, [_fila(1, 1, 0.9, 0.801), _fila(2, 1, 0.9, 0.805), _fila(3, 2, 0.9, 0.55)])
    matriz = RES.armar_matriz(RES.armar_detalle([str(a)]))
    calor = RES.armar_calor(matriz)
    assert calor[("80-81%", 1)] == 2   # 0.801 y 0.805 caen en el mismo bucket de 1%
    assert calor[("55-56%", 2)] == 1


def test_grafico_calor_se_genera(tmp_path):
    a = tmp_path / "a.csv"
    _csv(a, [_fila(1, 1, 0.9, 0.8), _fila(2, 2, 0.9, 0.6)])
    matriz = RES.armar_matriz(RES.armar_detalle([str(a)]))
    destino = tmp_path / "matriz_calor.png"
    assert RES.grafico_calor(matriz, destino) is True
    assert destino.exists() and destino.stat().st_size > 0


def test_resumen_ejecutivo_reporta_mejor_combo_y_correlacion(tmp_path):
    a = tmp_path / "a.csv"
    _csv(a, [_fila(-1, 0, 0.5, 0.5), _fila(1, 1, 0.9, 0.95, k1=1, k2=1, a1=1, p1=0),
             _fila(2, 11, 0.6, 0.65, k1=1, k2=0, a1=0, p1=0)])
    detalle = RES.armar_detalle([str(a)])
    texto = RES.resumen_ejecutivo(detalle)
    assert "Mejor combinacion encontrada" in texto
    assert "mejora sobre la linea base: +0.450" in texto
    assert "Top 5 modelos" in texto
    assert "n_kpoints:" in texto
    assert "Convergencia" in texto


def test_convergencia_detecta_estancado_vs_reciente(tmp_path):
    # mejor resultado en la eleccion 1 de 10 -> 9/10 = 90% sin mejora despues -> estancado
    a = tmp_path / "a.csv"
    _csv(a, [_fila(i + 1, 1, 0.5, 0.5 if i else 0.9) for i in range(10)])
    detalle = RES.armar_detalle([str(a)])
    conv = RES.analisis_convergencia(detalle)
    assert conv["eleccion_del_mejor"] == 1 and conv["porcentaje_sin_mejora"] == 0.9
    assert "ESTANCADA" in RES.resumen_ejecutivo(detalle)

    # mejor resultado justo en la ultima eleccion -> 0% sin mejora despues -> reciente, seguir probando
    b = tmp_path / "b.csv"
    _csv(b, [_fila(i + 1, 1, 0.5, 0.5 if i < 9 else 0.9) for i in range(10)])
    detalle2 = RES.armar_detalle([str(b)])
    conv2 = RES.analisis_convergencia(detalle2)
    assert conv2["eleccion_del_mejor"] == 10 and conv2["porcentaje_sin_mejora"] == 0.0
    assert "RECIENTE" in RES.resumen_ejecutivo(detalle2)


def test_main_de_punta_a_punta(tmp_path):
    a = tmp_path / "res_0.csv"
    b = tmp_path / "res_1.csv"
    _csv(a, [_fila(-1, 0, 0.5, 0.5), _fila(1, 1, 0.9, 0.95)])
    _csv(b, [_fila(2, 1, 0.4, 0.45)])
    salida = tmp_path / "resumen"

    RES.main(["--csv", str(a), str(b), "--salida", str(salida)])

    assert (salida / "detalle.csv").exists()
    assert (salida / "matriz_resumen.csv").exists()
    assert (salida / "graficos" / "progreso.png").exists()
    assert (salida / "graficos" / "costo.png").exists()
    assert (salida / "graficos" / "matriz_calor.png").exists()
    assert (salida / "resumen.txt").exists() and "Mejor combinacion" in (salida / "resumen.txt").read_text("utf-8")
    with (salida / "detalle.csv").open(encoding="utf-8") as f:
        assert len(list(csv.DictReader(f))) == 3
