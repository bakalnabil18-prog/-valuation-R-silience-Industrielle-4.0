"""
validators.py — Validation des données du formulaire
"""

from engine.data_models import FormData


def validate_form(data: FormData) -> list[str]:
    """
    Valide les champs obligatoires et retourne la liste des erreurs.
    Retourne [] si tout est valide.
    """
    errors = []

    # Identification
    if not data.identification.entreprise:
        errors.append("Le nom de l'entreprise est obligatoire.")
    if not data.identification.secteur or data.identification.secteur == "—":
        errors.append("Le secteur d'activité est obligatoire.")

    # Robots
    if not data.robots.identification.type_robot or data.robots.identification.type_robot == "—":
        errors.append("Le type de robot est obligatoire.")
    if not data.robots.identification.integration_reseau or data.robots.identification.integration_reseau == "—":
        errors.append("L'intégration réseau des robots est obligatoire.")
    if not data.robots.scoring.niveau_redondance or data.robots.scoring.niveau_redondance == "—":
        errors.append("Le niveau de redondance est obligatoire.")
    if not data.robots.scoring.dependance_production or data.robots.scoring.dependance_production == "—":
        errors.append("La dépendance production est obligatoire.")

    # Maintenance
    if not data.maintenance.organisation.type_maintenance or data.maintenance.organisation.type_maintenance == "—":
        errors.append("Le type de maintenance est obligatoire.")

    # CPS
    if not data.cps.assurantiel.dependance_cps or data.cps.assurantiel.dependance_cps == "—":
        errors.append("La dépendance au CPS est obligatoire.")

    return errors


def compute_completeness(data: FormData) -> float:
    """
    Calcule le taux de complétion du formulaire (0.0 à 1.0).
    """
    total_fields = 0
    filled_fields = 0

    def _check(val):
        nonlocal total_fields, filled_fields
        total_fields += 1
        if val not in (None, "", "—", 0):
            filled_fields += 1

    # Identification
    _check(data.identification.entreprise)
    _check(data.identification.secteur)
    _check(data.identification.ville)

    # Robots
    _check(data.robots.identification.type_robot)
    _check(data.robots.identification.cobots)
    _check(data.robots.identification.integration_reseau)
    _check(data.robots.quantitatif.nombre_robots)
    _check(data.robots.quantitatif.mtbf_heures)
    _check(data.robots.quantitatif.mttr_heures)
    _check(data.robots.scoring.niveau_redondance)
    _check(data.robots.scoring.capteurs_predictifs)
    _check(data.robots.scoring.dependance_production)

    # CNC
    _check(data.cnc.identification.automation_cnc)
    _check(data.cnc.risque.freq_maintenance_prev)
    _check(data.cnc.risque.ups_dedie)

    # CPS
    _check(data.cps.architecture.presence_scada)
    _check(data.cps.infrastructure_it.redondance_serveurs)
    _check(data.cps.infrastructure_it.backup_quotidien)
    _check(data.cps.infrastructure_it.parefeu_industriel)
    _check(data.cps.infrastructure_it.audit_cyber)
    _check(data.cps.assurantiel.dependance_cps)
    _check(data.cps.assurantiel.plan_continuite)

    # Électrique
    _check(data.electrique.equipement.ups_industriel)
    _check(data.electrique.donnees.mise_a_la_terre)
    _check(data.electrique.donnees.incidents_electriques)

    # Maintenance
    _check(data.maintenance.organisation.type_maintenance)
    _check(data.maintenance.organisation.gmao_utilisee)
    _check(data.maintenance.indicateurs.mtbf_global)
    _check(data.maintenance.indicateurs.mttr_global)
    _check(data.maintenance.maturite.niveau_digitalisation)
    _check(data.maintenance.maturite.ia_predictive)

    # Stockage
    _check(data.stockage.assurantiel.pieces_crit_redond)
    _check(data.stockage.assurantiel.fournisseurs_multiples)
    _check(data.stockage.gestion_numerique.taux_rupture_stock)

    # Intervention
    _check(data.intervention.organisation.astreinte_247)
    _check(data.intervention.indicateurs.mttr_moyen)
    _check(data.intervention.indicateurs.pct_interv_4h)

    return round(filled_fields / total_fields, 2) if total_fields > 0 else 0.0
