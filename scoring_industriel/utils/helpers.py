"""
helpers.py — Fonctions utilitaires générales
"""

import json
import os
from pathlib import Path


DATA_DIR = Path(__file__).parent.parent / "data"


def load_json(filename: str) -> dict:
    """Charge un fichier JSON du dossier data/."""
    path = DATA_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def clamp(value: float, min_val: float = 0, max_val: float = 100) -> int:
    """Borne une valeur entre min et max et retourne un entier."""
    return int(max(min_val, min(max_val, round(value))))


def format_mad(value: float) -> str:
    """Formate un montant en MAD."""
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M MAD"
    if value >= 1_000:
        return f"{value/1_000:.0f}K MAD"
    return f"{value:.0f} MAD"


def score_to_label(score: int) -> str:
    if score >= 70: return "Bon"
    if score >= 40: return "Moyen"
    return "Critique"


def get_industry_reference() -> dict:
    return load_json("industry_reference.json")


def get_scoring_parameters() -> dict:
    return load_json("scoring_parameters.json")


def get_maintenance_benchmark() -> dict:
    return load_json("maintenance_benchmark.json")


def get_equipment_catalog() -> dict:
    return load_json("equipment_catalog.json")


def get_sample_input() -> dict:
    return load_json("sample_input.json")
