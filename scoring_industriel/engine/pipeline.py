"""
pipeline.py
═══════════════════════════════════════════════════════════════════
Pipeline de scoring complet v2 — avec 20 indicateurs innovants.

Flux :
  FormData
    → compute_score_maturite()      → Score A (base)
    → compute_score_resilience()    → Score B (base)
    → compute_score_vulnerabilite() → Score C (base)
    → compute_module_scores()       → Radar 8 axes
    → compute_innovant_scores()     → Bonus/Malus 20 indicateurs
    → apply_innovant_to_pipeline()  → Scores finaux A, B, C, Global
    → detect_zones_critiques()      → Output D
    → generate_recommandations()    → Recommandations
    → build_synthese()              → Synthèse souscripteur
    → ScoreResult
"""

from .data_models import FormData, ScoreResult
from .scoring_mecatronique import compute_score_maturite
from .scoring_maintenance import compute_score_resilience
from .scoring_gouvernance import compute_score_vulnerabilite
from .health_score import compute_module_scores
from .risk_matrix import detect_zones_critiques
from .recommendation_engine import generate_recommandations
from .underwriting import (
    build_synthese,
    get_facteurs_aggravants,
    compute_benchmark_secteur,
    get_profil,
    get_niveau_risque,
)
from .scoring_innovant import (
    InnovatifInput,
    compute_innovant_scores,
    apply_innovant_to_pipeline,
)


class ScoringPipeline:
    """
    Pipeline principal de scoring risque industriel 4.0 v2.
    Supporte les 20 indicateurs innovants via innovant_input optionnel.
    """

    def run(self, data: FormData, innovant_input: InnovatifInput = None) -> ScoreResult:
        result = ScoreResult()

        # ── 1. TROIS INDICES DE BASE ─────────────────────────────────────────
        result.score_maturite      = compute_score_maturite(data)
        result.score_resilience    = compute_score_resilience(data)
        result.score_vulnerabilite = compute_score_vulnerabilite(data)

        # Garder les scores de base pour affichage comparatif
        result.score_maturite_base      = result.score_maturite
        result.score_resilience_base    = result.score_resilience
        result.score_vulnerabilite_base = result.score_vulnerabilite

        # ── 2. INDICATEURS INNOVANTS ─────────────────────────────────────────
        if innovant_input is not None:
            inno = compute_innovant_scores(innovant_input)
            result.innovant_scores = inno
            (
                result.score_maturite,
                result.score_resilience,
                result.score_vulnerabilite,
                _,
            ) = apply_innovant_to_pipeline(
                result.score_maturite,
                result.score_resilience,
                result.score_vulnerabilite,
                inno,
            )
        else:
            result.innovant_scores = None

        # ── 3. SCORE GLOBAL ──────────────────────────────────────────────────
        result.score_global = min(100, max(0, round(
            result.score_maturite * 0.35
            + result.score_resilience * 0.45
            + (100 - result.score_vulnerabilite) * 0.20
        )))

        result.score_global_base = min(100, max(0, round(
            result.score_maturite_base * 0.35
            + result.score_resilience_base * 0.45
            + (100 - result.score_vulnerabilite_base) * 0.20
        )))

        # ── 4. SCORES PAR MODULE (radar) ──────────────────────────────────────
        result.module_scores = compute_module_scores(data)

        # ── 5. PROFIL & RISQUE ────────────────────────────────────────────────
        profil = get_profil(result.score_global)
        risque = get_niveau_risque(result.score_global)
        result.profil_industriel = profil["label"]
        result.niveau_risque     = risque["label"]

        # ── 6. OUTPUT D — ZONES CRITIQUES ─────────────────────────────────────
        result.zones_critiques = detect_zones_critiques(data, result)

        # ── 7. RECOMMANDATIONS ────────────────────────────────────────────────
        result.recommandations = generate_recommandations(data, result)

        # ── 8. SYNTHÈSE SOUSCRIPTEUR ──────────────────────────────────────────
        result.synthese = build_synthese(data, result)

        # ── 9. FACTEURS AGGRAVANTS ────────────────────────────────────────────
        result.facteurs_aggravants = get_facteurs_aggravants(data, result)

        # ── 10. BENCHMARK SECTORIEL ───────────────────────────────────────────
        result.benchmark_secteur = compute_benchmark_secteur(data, result)

        return result

    def run_partial(self, data: FormData, innovant_input: InnovatifInput = None) -> ScoreResult:
        """Version allégée pour calcul temps réel (live dashboard)."""
        result = ScoreResult()

        result.score_maturite      = compute_score_maturite(data)
        result.score_resilience    = compute_score_resilience(data)
        result.score_vulnerabilite = compute_score_vulnerabilite(data)

        result.score_maturite_base      = result.score_maturite
        result.score_resilience_base    = result.score_resilience
        result.score_vulnerabilite_base = result.score_vulnerabilite

        if innovant_input is not None:
            inno = compute_innovant_scores(innovant_input)
            result.innovant_scores = inno
            (
                result.score_maturite,
                result.score_resilience,
                result.score_vulnerabilite,
                _,
            ) = apply_innovant_to_pipeline(
                result.score_maturite,
                result.score_resilience,
                result.score_vulnerabilite,
                inno,
            )
        else:
            result.innovant_scores = None

        result.score_global = min(100, max(0, round(
            result.score_maturite * 0.35
            + result.score_resilience * 0.45
            + (100 - result.score_vulnerabilite) * 0.20
        )))

        result.score_global_base = min(100, max(0, round(
            result.score_maturite_base * 0.35
            + result.score_resilience_base * 0.45
            + (100 - result.score_vulnerabilite_base) * 0.20
        )))

        result.module_scores = compute_module_scores(data)
        profil = get_profil(result.score_global)
        result.profil_industriel = profil["label"]

        return result
