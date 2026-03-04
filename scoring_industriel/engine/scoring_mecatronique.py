"""
scoring_mecatronique.py
═══════════════════════
Score de Maturité Mécatronique (0-100)
Mesure : degré automatisation + qualité capteurs + intégration CPS + robustesse infra
"""

from .data_models import FormData


def score_robots(data: FormData) -> int:
    r = data.robots
    s = 0

    # Intégration réseau (connectivité = maturité numérique)
    reseau_map = {"Connecté Cloud": 25, "Connecté MES": 15, "Isolé": 0}
    s += reseau_map.get(r.identification.integration_reseau, 0)

    # Cobots = collaboration humain-robot
    if r.identification.cobots == "oui": s += 6
    if r.identification.cellule_modulaire == "oui": s += 5

    # Capteurs prédictifs = IA terrain
    if r.scoring.capteurs_predictifs == "oui": s += 20

    # Firmware à jour = maturité maintenance
    if r.scoring.maj_firmware == "oui": s += 8

    # Contrat maintenance constructeur
    if r.scoring.contrat_maintenance == "oui": s += 10

    # Historique pannes (fiabilité démontrée)
    pannes_map = {"0 panne": 10, "1-2 pannes": 6, "3-5 pannes": 2, "> 5 pannes": 0}
    s += pannes_map.get(r.scoring.historique_pannes, 0)

    # Redondance (résilience architecturale)
    redond_map = {"Élevé": 8, "Moyen": 4, "Faible": 0}
    s += redond_map.get(r.scoring.niveau_redondance, 0)

    return min(100, max(0, s))


def score_cnc(data: FormData) -> int:
    c = data.cnc
    s = 0

    automation_map = {"Full auto": 28, "Semi-auto": 15, "Manuel": 0}
    s += automation_map.get(c.identification.automation_cnc, 0)

    if c.identification.interface_mes_erp == "oui": s += 12

    if c.risque.maintenance_pred_cnc == "oui": s += 20

    freq_map = {
        "Mensuelle": 15, "Trimestrielle": 10,
        "Semestrielle": 6, "Annuelle": 2, "Aucune": 0
    }
    s += freq_map.get(c.risque.freq_maintenance_prev, 0)

    if c.risque.ups_dedie == "oui": s += 10
    if c.risque.protection_surtension == "oui": s += 8
    if c.technique.variateur_freq == "oui": s += 5

    return min(100, max(0, s))


def score_cps_maturite(data: FormData) -> int:
    cps = data.cps
    s = 0

    if cps.architecture.presence_scada == "oui": s += 15
    if cps.architecture.mes_integre == "oui": s += 12
    if cps.architecture.erp_connecte == "oui": s += 8

    proto_map = {"OPC-UA": 10, "Profinet": 6, "Modbus": 2, "Autre": 1}
    s += proto_map.get(cps.architecture.protocole_industriel, 0)

    seg_map = {"Élevée": 10, "Moyenne": 5, "Faible": 0}
    s += seg_map.get(cps.architecture.segmentation_reseau, 0)

    if cps.infrastructure_it.audit_cyber == "oui": s += 12
    if cps.infrastructure_it.backup_quotidien == "oui": s += 8
    if cps.infrastructure_it.parefeu_industriel == "oui": s += 8
    if cps.infrastructure_it.redondance_serveurs == "oui": s += 12

    return min(100, max(0, s))


def score_manutention_maturite(data: FormData) -> int:
    m = data.manutention
    s = 15  # base

    if m.equipements.presence_agv == "oui": s += 22
    if m.scoring.manutention_auto == "oui": s += 15
    if m.scoring.disponibilite_247 == "oui": s += 18

    dispo = m.equipements.disponibilite_pct or 0
    if dispo > 95: s += 10
    elif dispo > 85: s += 6

    return min(100, max(0, s))


def score_maintenance_maturite(data: FormData) -> int:
    """Composante maturité du module maintenance (pour l'indice mécatronique)."""
    maint = data.maintenance
    s = 0

    nd = int(maint.maturite.niveau_digitalisation or 0)
    s += nd * 4  # max 20

    if maint.maturite.ia_predictive == "oui": s += 25
    if maint.maturite.maint_conditionnelle == "oui": s += 15
    if maint.organisation.gmao_utilisee == "oui": s += 10

    pred_map = {"Prédictive": 20, "Préventive": 10, "Corrective": 0}
    s += pred_map.get(maint.organisation.type_maintenance, 0)

    return min(100, max(0, s))


def score_stockage_maturite(data: FormData) -> int:
    st = data.stockage
    s = 10

    if st.gestion_numerique.integration_erp_stock == "oui": s += 15
    if st.gestion_numerique.analyse_abc == "oui": s += 12
    if st.infrastructure.stockage_vertical_auto == "oui": s += 18
    if st.performance.prediction_conso == "oui": s += 15
    if st.gestion_numerique.suivi_consommation == "oui": s += 10

    return min(100, max(0, s))


def compute_score_maturite(data: FormData) -> int:
    """
    Score de Maturité Mécatronique global (0–100).
    Moyenne pondérée des composantes.
    """
    scores = {
        "robots":        score_robots(data),
        "cnc":           score_cnc(data),
        "cps":           score_cps_maturite(data),
        "manutention":   score_manutention_maturite(data),
        "maintenance":   score_maintenance_maturite(data),
        "stockage":      score_stockage_maturite(data),
    }

    poids = {
        "robots":      0.28,
        "cnc":         0.18,
        "cps":         0.22,
        "manutention": 0.10,
        "maintenance": 0.12,
        "stockage":    0.10,
    }

    total = sum(scores[k] * poids[k] for k in scores)
    return min(100, max(0, round(total)))
