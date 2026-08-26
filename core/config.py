"""Rutas del proyecto en un solo lugar. Ningun otro archivo arma rutas a mano."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXERCISES_DIR = ROOT / "exercises"
TEMPLATES_DIR = ROOT / "templates"
MODELS_DIR = ROOT / "models"
WEB_DIR = ROOT / "web"
RECORDINGS_DIR = ROOT / "recordings"
DB_PATH = ROOT / "gymfitx.db"

for _d in (TEMPLATES_DIR, MODELS_DIR, RECORDINGS_DIR):
    _d.mkdir(parents=True, exist_ok=True)
