"""Desglose por persona (validacion.por_persona): cuenta y acierto por persona, sin cambiar los folds."""
import numpy as np

from src.entrenamiento import validacion as VALID


def test_desglose_por_persona_cuenta_y_acierta():
    clases = ["bien", "mal"]
    y = np.array([0, 0, 1, 1, 1, 0])
    y_pred = np.array([0, 1, 1, 1, 0, 0])
    personas = ["P2", "P2", "P2", "P3", "P3", "P3"]
    r = VALID.por_persona(y, y_pred, personas, clases)
    assert r["P2"] == {"clips": 3, "reales": {"bien": 2, "mal": 1}, "accuracy": 0.6667}
    assert r["P3"] == {"clips": 3, "reales": {"bien": 1, "mal": 2}, "accuracy": 0.6667}


def test_sin_persona_en_el_manifest_no_rompe():
    r = VALID.por_persona(np.array([0, 1]), np.array([0, 1]), ["sin_persona", "sin_persona"], ["bien", "mal"])
    assert r["sin_persona"]["accuracy"] == 1.0


def test_cada_fold_de_prueba_tiene_todas_las_personas():
    """Folds condicionados a la persona: cada fold de prueba trae clips de P2, P3 y P4 (no de uno solo)."""
    from src.entrenamiento.validacion import PorGrabacion
    personas = ["P2", "P3", "P4"] * 8                 # 8 clips por persona, cada clip su propia grabacion
    clases = ["bien", "mal"] * 12
    grupos = [f"g{i}" for i in range(24)]
    estratos = [f"{c}|{p}" for c, p in zip(clases, personas)]
    y = np.array([0 if c == "bien" else 1 for c in clases])
    X = np.zeros((24, 1))
    skf = PorGrabacion(4, grupos, 7, estratos)
    for _, te in skf.split(X, y):
        assert {personas[i] for i in te} == {"P2", "P3", "P4"}


def test_pedido_acepta_tipo_numerico_del_panel():
    """El panel manda el type como numero (1); antes Pydantic lo rechazaba con 422 y el panel mostraba 'error desconocido'."""
    from src.interfaz.api.entrenamiento import EntrenarPedido, SeleccionPedido
    assert EntrenarPedido(tipo=1).tipo == 1
    assert EntrenarPedido(tipo="1").tipo == "1"
    assert SeleccionPedido(tipo=1, cambios={}).tipo == 1


def test_composicion_folds_cuenta_por_persona():
    from src.entrenamiento.validacion import PorGrabacion, composicion_folds
    personas = ["P2", "P3", "P4"] * 8
    clases = ["bien", "mal"] * 12
    estratos = [f"{c}|{p}" for c, p in zip(clases, personas)]
    y = np.array([0 if c == "bien" else 1 for c in clases])
    X = np.zeros((24, 1))
    comp = composicion_folds(PorGrabacion(4, [f"g{i}" for i in range(24)], 7, estratos), X, y, personas)
    assert len(comp) == 4
    for f in comp:
        assert all(f["prueba"][p] > 0 for p in ["P2", "P3", "P4"])
        assert sum(f["prueba"].values()) == 6
