"""
underwriting.py
═══════════════
Génère le profil industriel, la synthèse souscripteur
et les facteurs aggravants pour la souscription IARD.
"""

from .data_models import FormData, ScoreResult


PROFILS = [
    {"label": "Industrie 4.0 Avancé",        "min": 75, "couleur": "#10b981"},
    {"label": "Industrie 4.0 Intermédiaire",  "min": 50, "couleur": "#3b82f6"},
    {"label": "Industrie 3.0 en Transition",  "min": 30, "couleur": "#f59e0b"},
    {"label": "Industrie Traditionnelle",     "min": 0,  "couleur": "#ef4444"},
]

NIVEAUX_RISQUE = [
    {"label": "Risque Faible",    "min": 70, "couleur": "#10b981"},
    {"label": "Risque Modéré",    "min": 40, "couleur": "#f59e0b"},
    {"label": "Risque Élevé",     "min": 20, "couleur": "#ef4444"},
    {"label": "Risque Critique",  "min": 0,  "couleur": "#7f1d1d"},
]


def get_profil(score_global: int) -> dict:
    for p in PROFILS:
        if score_global >= p["min"]:
            return p
    return PROFILS[-1]


def get_niveau_risque(score_global: int) -> dict:
    for n in NIVEAUX_RISQUE:
        if score_global >= n["min"]:
            return n
    return NIVEAUX_RISQUE[-1]


def get_integration_digitale(score_maturite: int) -> str:
    if score_maturite >= 70: return "Élevée"
    if score_maturite >= 40: return "Modérée"
    return "Faible"


def get_resilience_label(score_resilience: int) -> str:
    if score_resilience >= 70: return "Solide"
    if score_resilience >= 45: return "Modérée"
    return "Insuffisante"


def get_vulnerabilite_it_label(score_vulnerabilite: int) -> str:
    if score_vulnerabilite > 65: return "Critique"
    if score_vulnerabilite > 35: return "Modérée"
    return "Faible"


def build_synthese(data: FormData, result: ScoreResult) -> dict:
    """Construit la synthèse souscripteur (4 indicateurs clés)."""
    nom = data.identification.entreprise or "L'entreprise"
    sg = result.score_global

    if sg >= 75:
        narrative = (
            f"{nom} présente une résilience industrielle avancée avec une capacité "
            "d'absorption élevée. Profil favorable pour la souscription standard."
        )
    elif sg >= 50:
        narrative = (
            f"{nom} présente un profil intermédiaire avec des zones de fragilité "
            "opérationnelle identifiées. Conditions de souscription avec exigences de prévention ciblées."
        )
    elif sg >= 30:
        narrative = (
            f"{nom} présente un niveau de vulnérabilité modéré à élevé. "
            "Un plan d'amélioration obligatoire est requis avant souscription optimale."
        )
    else:
        narrative = (
            f"{nom} présente un niveau de vulnérabilité critique. "
            "Conditions restrictives — audit industriel préalable requis."
        )

    return {
        "profil_industriel": get_profil(sg)["label"],
        "integration_digitale": get_integration_digitale(result.score_maturite),
        "resilience_maintenance": get_resilience_label(result.score_resilience),
        "vulnerabilite_it": get_vulnerabilite_it_label(result.score_vulnerabilite),
        "narrative": narrative,
        "recommandation_souscription": get_profil(sg).get("recommandation", "Analyse approfondie requise"),
    }


def get_facteurs_aggravants(data: FormData, result: ScoreResult) -> list:
    """Identifie les facteurs aggravants pour la souscription."""
    facteurs = []

    if data.cps.assurantiel.dependance_cps == "Critique":
        facteurs.append("Dépendance totale à un CPS non redondant — risque perte exploitation totale")

    if data.cps.infrastructure_it.redondance_serveurs != "oui":
        facteurs.append("Absence redondance serveurs MES/SCADA")

    if data.cps.assurantiel.plan_continuite != "oui":
        facteurs.append("Aucun Plan de Continuité d'Activité (PCA) documenté")

    mttr = data.maintenance.indicateurs.mttr_global or 0
    if mttr > 12:
        facteurs.append(f"MTTR global > 12h ({mttr:.1f}h) — durée sinistre prolongée")

    if data.stockage.assurantiel.pieces_crit_redond != "oui":
        facteurs.append("Stock pièces critiques insuffisant — risque BDM aggravé")

    if data.electrique.equipement.ups_industriel != "oui":
        facteurs.append("Absence d'onduleur industriel — vulnérabilité dommages électriques")

    if data.cps.infrastructure_it.audit_cyber != "oui":
        facteurs.append("Absence d'audit cybersécurité annuel sur infrastructure industrielle")

    if data.robots.scoring.dependance_production == "Critique" and data.robots.scoring.niveau_redondance == "Faible":
        facteurs.append("Dépendance critique à des robots sans redondance")

    return facteurs


def compute_benchmark_secteur(data: FormData, result: ScoreResult) -> dict:
    """Compare les KPIs de l'entreprise aux benchmarks sectoriels."""
    import json, os

    benchmarks = {
        "automobile":     {"mtbf_ref": 2200, "mttr_ref": 3.5},
        "aeronautique":   {"mtbf_ref": 3500, "mttr_ref": 2.8},
        "agroalimentaire":{"mtbf_ref": 1800, "mttr_ref": 4.2},
        "chimie_pharma":  {"mtbf_ref": 2800, "mttr_ref": 3.0},
        "metalurgie":     {"mtbf_ref": 1600, "mttr_ref": 5.5},
        "electronique":   {"mtbf_ref": 3000, "mttr_ref": 2.5},
        "textile":        {"mtbf_ref": 1200, "mttr_ref": 6.0},
        "autre":          {"mtbf_ref": 2000, "mttr_ref": 4.5},
    }

    secteur = data.identification.secteur.lower().replace(" ", "_")
    ref = benchmarks.get(secteur, benchmarks["autre"])

    mtbf_ent = data.maintenance.indicateurs.mtbf_global or 0
    mttr_ent = data.maintenance.indicateurs.mttr_global or 0

    return {
        "mtbf_entreprise": mtbf_ent,
        "mtbf_benchmark": ref["mtbf_ref"],
        "mtbf_ratio": round(mtbf_ent / ref["mtbf_ref"], 2) if ref["mtbf_ref"] else 0,
        "mttr_entreprise": mttr_ent,
        "mttr_benchmark": ref["mttr_ref"],
        "mttr_ratio": round(ref["mttr_ref"] / mttr_ent, 2) if mttr_ent else 0,
        "secteur": secteur,
    }
