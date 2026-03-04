"""
Engine package — Moteur de scoring Risque Industriel 4.0
=========================================================
Pipeline complet : données → normalisation → scoring → outputs
"""

from .data_models import FormData, ScoreResult, ZoneCritique, Recommandation
from .pipeline import ScoringPipeline

__all__ = [
    "FormData",
    "ScoreResult",
    "ZoneCritique",
    "Recommandation",
    "ScoringPipeline",
]

__version__ = "2.0.0"
