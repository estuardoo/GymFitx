"""Casillas de persona del panel: armar() deja fuera las personas no marcadas."""
import pytest

from src.entrenamiento import datos as DATOS


def _rows():
    spec = [("P1", "bien"), ("P1", "mal"), ("P2", "bien"), ("P2", "mal"), ("P3", "bien"), ("P3", "mal")]
    return [{"clip": f"zancada/{p}_{c}_{i}.mp4", "type": 1, "clase": c, "persona": p, "origen": "v.mp4"}
            for i, (p, c) in enumerate(spec)]


@pytest.fixture
def vectores(monkeypatch):
    monkeypatch.setattr(DATOS, "seleccion", lambda: {})   # sin desmarcas a mano del disco real
    rows = _rows()
    return rows, {r["clip"]: [float(i)] for i, r in enumerate(rows)}


def test_sin_personas_entran_todas(vectores):
    rows, vec = vectores
    ds = DATOS.armar(rows, 1, "ambos", None, vec)
    assert len(ds["clips"]) == 6 and ds["excluidos_persona"] == []


def test_personas_no_marcadas_quedan_fuera(vectores):
    rows, vec = vectores
    ds = DATOS.armar(rows, 1, "ambos", None, vec, personas=["P2", "P3"])
    assert len(ds["clips"]) == 4
    assert not any(c.startswith("zancada/P1_") for c in ds["clips"])
    assert sorted(ds["excluidos_persona"]) == ["zancada/P1_bien_0.mp4", "zancada/P1_mal_1.mp4"]


def test_clips_entrenamiento_trae_la_persona(monkeypatch):
    monkeypatch.setattr(DATOS, "_manifest", _rows)
    monkeypatch.setattr(DATOS, "seleccion", lambda: {})
    assert {c["persona"] for c in DATOS.clips_entrenamiento(1)} == {"P1", "P2", "P3"}


def test_entrenar_rechaza_lista_de_personas_vacia(monkeypatch):
    from src.entrenamiento.entrenar import entrenar
    monkeypatch.setattr(DATOS, "_manifest", _rows)
    with pytest.raises(ValueError, match="Marca al menos una persona"):
        entrenar(personas=[])
