"""
scoring_maintenance.py
══════════════════════
Score de Résilience Opérationnelle (0-100)
Mesure : efficacité maintenance + pièces critiques + rapidité intervention + redondance
Poids dans score global : 45%
"""

from .data_models import FormData


def _score_organisation_maintenance(data: FormData) -> int:
    maint = data.maintenance.organisation
    s = 0
    if maint.gmao_utilisee == "oui": s += 15
    if maint.existence_kpi == "oui": s += 8

    pred_map = {"Prédictive": 30, "Préventive": 18, "Corrective": 0}
    s += pred_map.get(maint.type_maintenance, 0)

    return min(53, s)


def _score_kpi_maintenance(data: FormData) -> int:
    ind = data.maintenance.indicateurs
    s = 0

    # MTBF global
    mtbf = ind.mtbf_global or 0
    if mtbf >= 3000: s += 15
    elif mtbf >= 2000: s += 10
    elif mtbf >= 1000: s += 5

    # MTTR global
    mttr = ind.mttr_global or 99
    if mttr < 2: s += 12
    elif mttr < 4: s += 8
    elif mttr < 8: s += 4

    # Taux planifié
    taux = ind.taux_maint_planifie_pct or 0
    if taux > 80: s += 10
    elif taux > 60: s += 6

    # Taux respect planning
    respect = ind.taux_respect_planning_pct or 0
    if respect > 90: s += 8
    elif respect > 70: s += 4

    return min(45, s)


def _score_maturite_maintenance(data: FormData) -> int:
    mat = data.maintenance.maturite
    s = 0

    nd = int(mat.niveau_digitalisation or 0)
    s += nd * 4  # 0-20

    if mat.ia_predictive == "oui": s += 20
    if mat.maint_conditionnelle == "oui": s += 15

    return min(55, s)


def _score_stockage_resilience(data: FormData) -> int:
    st = data.stockage
    s = 10  # base

    if st.assurantiel.pieces_crit_redond == "oui": s += 22
    if st.assurantiel.fournisseurs_multiples == "oui": s += 18
    if st.assurantiel.contrat_appro_prio == "oui": s += 10
    if st.assurantiel.simulation_penurie == "oui": s += 8
    if st.gestion_numerique.stock_minimum_defini == "oui": s += 10

    rupture_map = {"0%": 18, "< 5%": 10, "5-15%": 0, "> 15%": -15}
    s += rupture_map.get(st.gestion_numerique.taux_rupture_stock, 0)

    pct = st.performance.pct_pieces_crit_stock or 0
    if pct > 90: s += 10
    elif pct > 70: s += 5

    return min(100, max(0, s))


def _score_intervention_resilience(data: FormData) -> int:
    org = data.intervention.organisation
    ind = data.intervention.indicateurs
    dig = data.intervention.digitalisation
    s = 0

    if org.astreinte_247 == "oui": s += 18
    if org.equipe_interne == "oui": s += 15
    if org.techniciens_certif == "oui": s += 12

    sla = org.sla_interne_h or 99
    if sla <= 1: s += 10
    elif sla <= 2: s += 7
    elif sla <= 4: s += 3

    pct4h = ind.pct_interv_4h or 0
    if pct4h > 80: s += 12
    elif pct4h > 60: s += 7

    res_pp = ind.taux_resolution_pp or 0
    if res_pp > 85: s += 8
    elif res_pp > 70: s += 4

    arret24 = ind.historique_arret_24h or 0
    if arret24 == 0: s += 8
    elif arret24 <= 2: s += 4
    else: s -= 8

    if dig.gmao_mobile == "oui": s += 8
    if dig.tracabilite_rt == "oui": s += 7
    if dig.dashboard_kpi == "oui": s += 7
    if dig.historique_pannes_analyse == "oui": s += 5

    return min(100, max(0, s))


def _score_redondance_systemes(data: FormData) -> int:
    s = 0

    redond_map = {"Élevé": 25, "Moyen": 12, "Faible": 0}
    s += redond_map.get(data.robots.scoring.niveau_redondance, 0)

    if data.cps.infrastructure_it.redondance_serveurs == "oui": s += 25
    if data.cps.assurantiel.plan_continuite == "oui": s += 25
    if data.cps.assurantiel.simulation_crise == "oui": s += 15
    if data.manutention.scoring.redond_equip_crit == "oui": s += 10

    return min(100, max(0, s))


def compute_score_resilience(data: FormData) -> int:
    """
    Score de Résilience Opérationnelle global (0–100).
    """
    scores = {
        "organisation":   _score_organisation_maintenance(data),
        "kpi_maintenance": _score_kpi_maintenance(data),
        "maturite":       _score_maturite_maintenance(data),
        "stockage":       _score_stockage_resilience(data),
        "intervention":   _score_intervention_resilience(data),
        "redondance":     _score_redondance_systemes(data),
    }

    poids = {
        "organisation":    0.20,
        "kpi_maintenance": 0.18,
        "maturite":        0.17,
        "stockage":        0.20,
        "intervention":    0.15,
        "redondance":      0.10,
    }

    total = sum(scores[k] * poids[k] for k in scores)
    return min(100, max(0, round(total)))
