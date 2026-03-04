"""
health_score.py
═══════════════
Calcule les scores individuels des 8 modules pour le radar chart
et les feux tricolores.
"""

from .data_models import FormData, ModuleScores
from .scoring_mecatronique import score_robots, score_cnc, score_cps_maturite
from .scoring_mecatronique import score_manutention_maturite, score_maintenance_maturite


def module_robots(data: FormData) -> int:
    r = data.robots
    s = 0

    reseau_map = {"Connecté Cloud": 25, "Connecté MES": 15, "Isolé": 0}
    s += reseau_map.get(r.identification.integration_reseau, 0)

    redond_map = {"Élevé": 25, "Moyen": 12, "Faible": 0}
    s += redond_map.get(r.scoring.niveau_redondance, 0)

    if r.scoring.contrat_maintenance == "oui": s += 15
    if r.scoring.capteurs_predictifs == "oui": s += 20

    pannes_map = {"0 panne": 15, "1-2 pannes": 8, "3-5 pannes": 3, "> 5 pannes": 0}
    s += pannes_map.get(r.scoring.historique_pannes, 0)

    return min(100, max(0, s))


def module_cnc(data: FormData) -> int:
    c = data.cnc
    s = 0

    auto_map = {"Full auto": 28, "Semi-auto": 15, "Manuel": 0}
    s += auto_map.get(c.identification.automation_cnc, 0)

    if c.risque.ups_dedie == "oui": s += 20
    if c.risque.protection_surtension == "oui": s += 15
    if c.risque.maintenance_pred_cnc == "oui": s += 22

    freq_map = {"Mensuelle": 15, "Trimestrielle": 10, "Semestrielle": 6, "Annuelle": 2, "Aucune": 0}
    s += freq_map.get(c.risque.freq_maintenance_prev, 0)

    return min(100, max(0, s))


def module_cps(data: FormData) -> int:
    cps = data.cps
    s = 0

    if cps.architecture.presence_scada == "oui": s += 12
    if cps.architecture.mes_integre == "oui": s += 12
    if cps.infrastructure_it.redondance_serveurs == "oui": s += 18
    if cps.infrastructure_it.backup_quotidien == "oui": s += 12
    if cps.infrastructure_it.parefeu_industriel == "oui": s += 12
    if cps.infrastructure_it.audit_cyber == "oui": s += 12
    if cps.assurantiel.plan_continuite == "oui": s += 12

    seg_map = {"Élevée": 10, "Moyenne": 5, "Faible": 0}
    s += seg_map.get(cps.architecture.segmentation_reseau, 0)

    return min(100, max(0, s))


def module_electrique(data: FormData) -> int:
    e = data.electrique
    s = 20  # base

    if e.equipement.tableau_bt_mt == "oui": s += 15
    if e.equipement.protection_diff == "oui": s += 15
    if e.equipement.ups_industriel == "oui": s += 15
    if e.equipement.groupe_electrogene == "oui": s += 12
    if e.donnees.mise_a_la_terre == "oui": s += 15

    inc_map = {"0": 8, "1-2": -2, "3-5": -10, "> 5": -20}
    s += inc_map.get(e.donnees.incidents_electriques, 0)

    return min(100, max(0, s))


def module_maintenance(data: FormData) -> int:
    m = data.maintenance
    s = 0

    pred_map = {"Prédictive": 30, "Préventive": 18, "Corrective": 0}
    s += pred_map.get(m.organisation.type_maintenance, 0)

    if m.organisation.gmao_utilisee == "oui": s += 15
    if m.maturite.ia_predictive == "oui": s += 22
    if m.maturite.maint_conditionnelle == "oui": s += 15

    nd = int(m.maturite.niveau_digitalisation or 0)
    s += nd * 4

    return min(100, max(0, s))


def module_manutention(data: FormData) -> int:
    manu = data.manutention
    s = 15

    if manu.equipements.presence_agv == "oui": s += 22
    if manu.scoring.manutention_auto == "oui": s += 15
    if manu.scoring.disponibilite_247 == "oui": s += 20
    if manu.scoring.redond_equip_crit == "oui": s += 15
    if manu.scoring.dependance_prestataire != "oui": s += 13

    return min(100, max(0, s))


def module_stockage(data: FormData) -> int:
    st = data.stockage
    s = 10

    if st.assurantiel.pieces_crit_redond == "oui": s += 22
    if st.assurantiel.fournisseurs_multiples == "oui": s += 18
    if st.gestion_numerique.integration_erp_stock == "oui": s += 12
    if st.gestion_numerique.analyse_abc == "oui": s += 10
    if st.gestion_numerique.stock_minimum_defini == "oui": s += 10

    rupture_map = {"0%": 18, "< 5%": 10, "5-15%": 0, "> 15%": -15}
    s += rupture_map.get(st.gestion_numerique.taux_rupture_stock, 0)

    return min(100, max(0, s))


def module_intervention(data: FormData) -> int:
    org = data.intervention.organisation
    ind = data.intervention.indicateurs
    dig = data.intervention.digitalisation
    s = 0

    if org.astreinte_247 == "oui": s += 18
    if org.equipe_interne == "oui": s += 15
    if org.techniciens_certif == "oui": s += 12
    if dig.gmao_mobile == "oui": s += 10
    if dig.tracabilite_rt == "oui": s += 10
    if dig.dashboard_kpi == "oui": s += 10

    pct4h = ind.pct_interv_4h or 0
    if pct4h > 80: s += 15
    elif pct4h > 60: s += 8

    res = ind.taux_resolution_pp or 0
    if res > 85: s += 10

    return min(100, max(0, s))


def compute_module_scores(data: FormData) -> ModuleScores:
    """Calcule les 8 scores individuels pour le radar chart."""
    return ModuleScores(
        robots=module_robots(data),
        cnc=module_cnc(data),
        cps=module_cps(data),
        electrique=module_electrique(data),
        maintenance=module_maintenance(data),
        manutention=module_manutention(data),
        stockage=module_stockage(data),
        intervention=module_intervention(data),
    )


def get_traffic_light(score: int) -> dict:
    """Retourne couleur et label pour feu tricolore."""
    if score >= 70:
        return {"color": "#10b981", "label": "BON", "emoji": "🟢"}
    elif score >= 40:
        return {"color": "#f59e0b", "label": "MOYEN", "emoji": "🟡"}
    else:
        return {"color": "#ef4444", "label": "CRITIQUE", "emoji": "🔴"}
