"""
normaliser.py — Normalisation des entrées Streamlit vers FormData
"""

from .data_models import (
    FormData, Identification,
    ModuleRobots, RobotsIdentification, RobotsQuantitatif, RobotsScoring,
    ModuleCNC, CNCIdentification, CNCTechnique, CNCRisque,
    ModuleCPS, CPSArchitecture, CPSInfrastructureIT, CPSAssurantiel,
    ModuleElectrique, ElectriqueEquipement, ElectriqueDonnees, ElectriqueImpact,
    ModuleMaintenance, MaintenanceOrganisation, MaintenanceIndicateurs, MaintenanceMaturite,
    ModuleManutention, ManutentionEquipements, ManutentionScoring,
    ModuleStockage, StockageInfrastructure, StockageGestionNumerique,
    StockagePerformance, StockageAssurantiel,
    ModuleIntervention, InterventionOrganisation, InterventionIndicateurs, InterventionDigitalisation,
)


def _bool_field(val) -> str:
    """Convertit un widget Streamlit (True/False/str) en 'oui'/'non'."""
    if isinstance(val, bool):
        return "oui" if val else "non"
    if isinstance(val, str):
        return val.lower().strip()
    return ""


def _safe_float(val) -> float:
    """Conversion sécurisée en float."""
    try:
        return float(val) if val not in (None, "", 0) else None
    except (ValueError, TypeError):
        return None


def _safe_int(val) -> int:
    try:
        return int(val) if val not in (None, "") else None
    except (ValueError, TypeError):
        return None


def normalise_form(state: dict) -> FormData:
    """
    Convertit le dictionnaire de session Streamlit (st.session_state)
    en objet FormData structuré pour le moteur de scoring.

    Parameters
    ----------
    state : dict
        Dictionnaire plat {clé: valeur} issu des widgets Streamlit.

    Returns
    -------
    FormData
        Objet de données structuré et validé.
    """
    s = state  # alias court

    return FormData(
        identification=Identification(
            entreprise=s.get("entreprise", ""),
            secteur=s.get("secteur", ""),
            ville=s.get("ville", ""),
            effectif=_safe_int(s.get("effectif")),
            ca_annuel_mad=_safe_float(s.get("ca_annuel_mad")),
        ),

        robots=ModuleRobots(
            identification=RobotsIdentification(
                type_robot=s.get("type_robot", ""),
                cobots=_bool_field(s.get("cobots")),
                cellule_modulaire=_bool_field(s.get("cellule_modulaire")),
                marque_modele=s.get("marque_modele", ""),
                annee_install=_safe_int(s.get("annee_install")),
                integration_reseau=s.get("integration_reseau", ""),
            ),
            quantitatif=RobotsQuantitatif(
                nombre_robots=_safe_int(s.get("nombre_robots")),
                valeur_unitaire_mad=_safe_float(s.get("valeur_unitaire_mad")),
                valeur_totale_parc_mad=_safe_float(s.get("valeur_totale_parc_mad")),
                heures_fonct_an=_safe_float(s.get("heures_fonct_an")),
                mtbf_heures=_safe_float(s.get("mtbf_robots")),
                mttr_heures=_safe_float(s.get("mttr_robots")),
            ),
            scoring=RobotsScoring(
                niveau_redondance=s.get("niveau_redondance", ""),
                contrat_maintenance=_bool_field(s.get("contrat_maintenance")),
                maj_firmware=_bool_field(s.get("maj_firmware")),
                historique_pannes=s.get("historique_pannes", ""),
                capteurs_predictifs=_bool_field(s.get("capteurs_predictifs")),
                dependance_production=s.get("dependance_production", ""),
            ),
        ),

        cnc=ModuleCNC(
            identification=CNCIdentification(
                type_cnc=s.get("type_cnc", ""),
                marque=s.get("marque_cnc", ""),
                annee_fabrication=_safe_int(s.get("annee_cnc")),
                automation_cnc=s.get("automation_cnc", ""),
                interface_mes_erp=_bool_field(s.get("interface_mes_erp")),
            ),
            technique=CNCTechnique(
                nombre_cnc=_safe_int(s.get("nombre_cnc")),
                valeur_unitaire_mad=_safe_float(s.get("valeur_unit_cnc")),
                heures_cumul=_safe_float(s.get("heures_cumul_cnc")),
                type_refroid=s.get("type_refroid", ""),
                sensibilite_electrique=_bool_field(s.get("sensibilite_electrique")),
                variateur_freq=_bool_field(s.get("variateur_freq")),
            ),
            risque=CNCRisque(
                freq_maintenance_prev=s.get("freq_maintenance_prev", ""),
                maintenance_pred_cnc=_bool_field(s.get("maintenance_pred_cnc")),
                historique_dom_elec=s.get("historique_dom_elec", ""),
                protection_surtension=_bool_field(s.get("protection_surtension")),
                ups_dedie=_bool_field(s.get("ups_dedie")),
            ),
        ),

        cps=ModuleCPS(
            architecture=CPSArchitecture(
                presence_scada=_bool_field(s.get("presence_scada")),
                mes_integre=_bool_field(s.get("mes_integre")),
                erp_connecte=_bool_field(s.get("erp_connecte")),
                cloud_externe=_bool_field(s.get("cloud_externe")),
                protocole_industriel=s.get("protocole_industriel", ""),
                segmentation_reseau=s.get("segmentation_reseau", ""),
            ),
            infrastructure_it=CPSInfrastructureIT(
                type_serveurs=s.get("type_serveurs", ""),
                redondance_serveurs=_bool_field(s.get("redondance_serveurs")),
                backup_quotidien=_bool_field(s.get("backup_quotidien")),
                rto_heures=_safe_float(s.get("rto_heures")),
                parefeu_industriel=_bool_field(s.get("parefeu_industriel")),
                audit_cyber=_bool_field(s.get("audit_cyber")),
            ),
            assurantiel=CPSAssurantiel(
                dependance_cps=s.get("dependance_cps", ""),
                historique_incid_it=s.get("historique_incid_it", ""),
                temps_moy_arret_it_h=_safe_float(s.get("temps_moy_arret_it_h")),
                plan_continuite=_bool_field(s.get("plan_continuite")),
                simulation_crise=_bool_field(s.get("simulation_crise")),
            ),
        ),

        electrique=ModuleElectrique(
            equipement=ElectriqueEquipement(
                tableau_bt_mt=_bool_field(s.get("tableau_bt_mt")),
                protection_diff=_bool_field(s.get("protection_diff")),
                monitoring_energie=_bool_field(s.get("monitoring_energie")),
                ups_industriel=_bool_field(s.get("ups_industriel")),
                groupe_electrogene=_bool_field(s.get("groupe_electrogene")),
            ),
            donnees=ElectriqueDonnees(
                puissance_installee_kw=_safe_float(s.get("puissance_installee_kw")),
                taux_charge_moyen_pct=_safe_float(s.get("taux_charge_moyen_pct")),
                incidents_electriques=s.get("incidents_electriques", ""),
                mise_a_la_terre=_bool_field(s.get("mise_a_la_terre")),
            ),
            impact=ElectriqueImpact(
                vulnerabilite_dom_elec=s.get("vulnerabilite_dom_elec", ""),
                risque_court_circuit=_bool_field(s.get("risque_court_circuit")),
                risque_propag_incendie=s.get("risque_propag_incendie", ""),
            ),
        ),

        maintenance=ModuleMaintenance(
            organisation=MaintenanceOrganisation(
                gmao_utilisee=_bool_field(s.get("gmao_utilisee")),
                type_maintenance=s.get("type_maintenance", ""),
                existence_kpi=_bool_field(s.get("existence_kpi")),
            ),
            indicateurs=MaintenanceIndicateurs(
                mtbf_global=_safe_float(s.get("mtbf_global")),
                mttr_global=_safe_float(s.get("mttr_global")),
                taux_maint_planifie_pct=_safe_float(s.get("taux_maint_planifie_pct")),
                taux_respect_planning_pct=_safe_float(s.get("taux_respect_planning_pct")),
                budget_maintenance_pct_parc=_safe_float(s.get("budget_maintenance_pct_parc")),
            ),
            maturite=MaintenanceMaturite(
                niveau_digitalisation=s.get("niveau_digitalisation", ""),
                maint_conditionnelle=_bool_field(s.get("maint_conditionnelle")),
                ia_predictive=_bool_field(s.get("ia_predictive")),
            ),
        ),

        manutention=ModuleManutention(
            equipements=ManutentionEquipements(
                presence_agv=_bool_field(s.get("presence_agv")),
                chariots_elev=_bool_field(s.get("chariots_elev")),
                ponts_roulants=_bool_field(s.get("ponts_roulants")),
                palans_elec=_bool_field(s.get("palans_elec")),
                outillage_special=_bool_field(s.get("outillage_special")),
                atelier_interne=_bool_field(s.get("atelier_interne")),
                nombre_equip=_safe_int(s.get("nombre_equip_manu")),
                age_moyen_ans=_safe_float(s.get("age_moyen_manu")),
                disponibilite_pct=_safe_float(s.get("disponibilite_manu_pct")),
                temps_mobilisation_min=_safe_float(s.get("temps_mobilisation_min")),
            ),
            scoring=ManutentionScoring(
                manutention_auto=_bool_field(s.get("manutention_auto")),
                redond_equip_crit=_bool_field(s.get("redond_equip_crit")),
                disponibilite_247=_bool_field(s.get("disponibilite_247")),
                dependance_prestataire=_bool_field(s.get("dependance_prestataire")),
            ),
        ),

        stockage=ModuleStockage(
            infrastructure=StockageInfrastructure(
                magasin_central=_bool_field(s.get("magasin_central")),
                rayonnage_intelligent=_bool_field(s.get("rayonnage_intelligent")),
                stockage_vertical_auto=_bool_field(s.get("stockage_vertical_auto")),
                zone_pieces_crit=_bool_field(s.get("zone_pieces_crit")),
                controle_therm_humi=_bool_field(s.get("controle_therm_humi")),
            ),
            gestion_numerique=StockageGestionNumerique(
                integration_erp_stock=_bool_field(s.get("integration_erp_stock")),
                stock_minimum_defini=_bool_field(s.get("stock_minimum_defini")),
                analyse_abc=_bool_field(s.get("analyse_abc")),
                delai_reappro_jours=_safe_float(s.get("delai_reappro_jours")),
                taux_rupture_stock=s.get("taux_rupture_stock", ""),
                suivi_consommation=_bool_field(s.get("suivi_consommation")),
            ),
            performance=StockagePerformance(
                temps_moy_disp_piece_h=_safe_float(s.get("temps_moy_disp_piece_h")),
                pct_pieces_crit_stock=_safe_float(s.get("pct_pieces_crit_stock")),
                taux_rotation_stock=_safe_float(s.get("taux_rotation_stock")),
                valeur_stock_pct_parc=_safe_float(s.get("valeur_stock_pct_parc")),
                prediction_conso=_bool_field(s.get("prediction_conso")),
            ),
            assurantiel=StockageAssurantiel(
                pieces_crit_redond=_bool_field(s.get("pieces_crit_redond")),
                fournisseurs_multiples=_bool_field(s.get("fournisseurs_multiples")),
                contrat_appro_prio=_bool_field(s.get("contrat_appro_prio")),
                simulation_penurie=_bool_field(s.get("simulation_penurie")),
            ),
        ),

        intervention=ModuleIntervention(
            organisation=InterventionOrganisation(
                equipe_interne=_bool_field(s.get("equipe_interne")),
                techniciens_certif=_bool_field(s.get("techniciens_certif")),
                astreinte_247=_bool_field(s.get("astreinte_247")),
                sla_interne_h=_safe_float(s.get("sla_interne_h")),
            ),
            indicateurs=InterventionIndicateurs(
                mttr_moyen=_safe_float(s.get("mttr_moyen")),
                pct_interv_4h=_safe_float(s.get("pct_interv_4h")),
                pct_interv_planif=_safe_float(s.get("pct_interv_planif")),
                taux_resolution_pp=_safe_float(s.get("taux_resolution_pp")),
                historique_arret_24h=_safe_int(s.get("historique_arret_24h")),
            ),
            digitalisation=InterventionDigitalisation(
                gmao_mobile=_bool_field(s.get("gmao_mobile")),
                tracabilite_rt=_bool_field(s.get("tracabilite_rt")),
                historique_pannes_analyse=_bool_field(s.get("historique_pannes_analyse")),
                dashboard_kpi=_bool_field(s.get("dashboard_kpi")),
            ),
        ),
    )
