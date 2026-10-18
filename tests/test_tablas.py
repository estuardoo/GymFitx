"""catalogo_puntos_disponible/poblar_desde_manifest (src/etiquetado/tablas.py): ubican el .npz de cada
fila por la carpeta del propio row['clip'] (<ejercicio>/<clase>/archivo), no por row['clase'] solo --
asi sirve tanto para la estructura vieja (plana) como para la nueva (anidada por ejercicio)."""
import numpy as np

from src.etiquetado import tablas as T


def test_catalogo_puntos_disponible_ubica_npz_anidado_por_ejercicio(tmp_path):
    d = tmp_path / "sentadilla" / "bien"
    d.mkdir(parents=True)
    np.savez(d / "c1.npz", point_names=np.array(["P1", "P2"]))
    fila = {"clip": "sentadilla/bien/c1.mp4", "clase": "bien", "npz": "c1.npz", "exercise": "no_existe"}

    assert T.catalogo_puntos_disponible([fila], tmp_path) == ["P1", "P2"]
