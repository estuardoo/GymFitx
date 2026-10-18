"""Matriz de tiempos por proceso (src/nucleo/tiempos.py)."""
from src.nucleo import tiempos as T


def test_medir_arma_la_matriz_y_marca_lento(monkeypatch):
    monkeypatch.setattr(T, "_filas", {})
    monkeypatch.setattr(T, "LENTO_S", 0.5)
    with T.medir("rapido"):
        pass
    T.registrar("lento", T.T0, 0.9)
    T.registrar("lento", T.T0, 0.1)
    f = {x["proceso"]: x for x in T.filas()}
    assert f["rapido"]["n"] == 1 and f["lento"]["n"] == 2 and f["lento"]["max_ms"] == 900
    m = T.matriz().splitlines()
    assert m[0].startswith("proceso") and "LENTO" in next(r for r in m if r.startswith("lento"))
    assert "LENTO" not in next(r for r in m if r.startswith("rapido"))


def test_sin_filas_no_revienta(monkeypatch):
    monkeypatch.setattr(T, "_filas", {})
    assert T.matriz().startswith("proceso")
