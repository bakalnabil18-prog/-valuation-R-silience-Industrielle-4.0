"""
scoring_gouvernance.py
══════════════════════
Score de Vulnérabilité Systémique (0-100) — SCORE INVERSÉ
Plus le score est élevé → plus l'entreprise est vulnérable.
Dans l'indice global : contribution = (100 - vulnerabilite) × 0.20
"""

from .data_models import FormData


def _vulne_dependance_production(data: FormData) -> int:
    """Dépendance au CPS et aux robots pour la production."""
    v = 0

    dep_cps = {"Critique": 22, "Moyen": 12, "Faible": 0}
    v += dep_cps.get(data.cps.assurantiel.dependance_cps, 0)

    dep_robots = {"Critique": 18, "Moyenne": 10, "Faible": 0}
    v += dep_robots.get(data.robots.scoring.dependance_production, 0)

    # Absence PCA avec dépendance critique = facteur aggravant
    if (data.cps.assurantiel.dependance_cps == "Critique"
            and data.cps.assurantiel.plan_continuite != "oui"):
        v += 10

    return v


def _vulne_fragilite_it(data: FormData) -> int:
    """Fragilité infrastructure IT industrielle."""
    v = 0

    if data.cps.infrastructure_it.redondance_serveurs != "oui": v += 15
    if data.cps.infrastructure_it.backup_quotidien != "oui": v += 10
    if data.cps.infrastructure_it.parefeu_industriel != "oui": v += 10
    if data.cps.infrastructure_it.audit_cyber != "oui": v += 8
    if data.cps.assurantiel.simulation_crise != "oui": v += 5

    incid_map = {"3+/an": 10, "1-2/an": 5, "Aucun": 0}
    v += incid_map.get(data.cps.assurantiel.historique_incid_it, 0)

    # RTO trop long
    rto = data.cps.infrastructure_it.rto_heures or 0
    if rto > 24: v += 8
    elif rto > 8: v += 4

    return v


def _vulne_fragilite_electrique(data: FormData) -> int:
    """Fragilité infrastructure électrique."""
    v = 0

    if data.electrique.equipement.ups_industriel != "oui": v += 8
    if data.electrique.donnees.mise_a_la_terre != "oui": v += 8
    if data.electrique.equipement.protection_diff != "oui": v += 6
    if data.electrique.equipement.groupe_electrogene != "oui": v += 5

    inc_map = {"> 5": 10, "3-5": 6, "1-2": 3, "0": 0}
    v += inc_map.get(data.electrique.donnees.incidents_electriques, 0)

    taux = data.electrique.donnees.taux_charge_moyen_pct or 0
    if taux > 90: v += 8
    elif taux > 80: v += 4

    vuln_map = {"Élevée": 10, "Modérée": 5, "Faible": 0}
    v += vuln_map.get(data.electrique.impact.vulnerabilite_dom_elec, 0)

    propag_map = {"Élevé": 8, "Modéré": 4, "Faible": 0}
    v += propag_map.get(data.electrique.impact.risque_propag_incendie, 0)

    return v


def _vulne_absence_redondance(data: FormData) -> int:
    """Centralisation et absence de redondance."""
    v = 0

    seg_map = {"Faible": 12, "Moyenne": 5, "Élevée": 0}
    v += seg_map.get(data.cps.architecture.segmentation_reseau, 0)

    redond_map = {"Faible": 15, "Moyen": 7, "Élevé": 0}
    v += redond_map.get(data.robots.scoring.niveau_redondance, 0)

    if data.manutention.scoring.dependance_prestataire == "oui": v += 8
    if data.stockage.assurantiel.fournisseurs_multiples != "oui": v += 8

    rupture_map = {"> 15%": 10, "5-15%": 5, "< 5%": 2, "0%": 0}
    v += rupture_map.get(data.stockage.gestion_numerique.taux_rupture_stock, 0)

    return v


def compute_score_vulnerabilite(data: FormData) -> int:
    """
    Score de Vulnérabilité Systémique (0–100).
    Score INVERSÉ : haut = vulnérable, bas = résilient.
    """
    composantes = {
        "dependance":  _vulne_dependance_production(data),
        "fragilite_it": _vulne_fragilite_it(data),
        "fragilite_elec": _vulne_fragilite_electrique(data),
        "absence_redond": _vulne_absence_redondance(data),
    }

    poids = {
        "dependance":     0.30,
        "fragilite_it":   0.28,
        "fragilite_elec": 0.22,
        "absence_redond": 0.20,
    }

    raw = sum(composantes[k] * poids[k] for k in composantes)
    # Normaliser sur 100 (le max brut théorique est ~100)
    return min(100, max(0, round(raw)))
