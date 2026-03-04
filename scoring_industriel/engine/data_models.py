"""
data_models.py — Modèles de données complets (8 modules × tous blocs)
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict


# ── IDENTIFICATION ────────────────────────────────────────────
@dataclass
class Identification:
    entreprise: str = ""
    secteur: str = ""
    ville: str = ""
    effectif: Optional[int] = None
    ca_annuel_mad: Optional[float] = None


# ── MODULE 1 : ROBOTS INDUSTRIELS ────────────────────────────
@dataclass
class RobotsIdentification:
    type_robot: str = ""           # 6 axes / 5 axes / SCARA / Delta
    cobots: str = ""               # oui / non
    cellule_modulaire: str = ""    # oui / non
    marque_modele: str = ""
    annee_install: Optional[int] = None
    integration_reseau: str = ""   # Isolé / Connecté MES / Connecté Cloud

@dataclass
class RobotsQuantitatif:
    nombre_robots: Optional[int] = None
    valeur_unitaire_mad: Optional[float] = None
    valeur_totale_parc_mad: Optional[float] = None
    heures_fonct_an: Optional[float] = None
    mtbf_heures: Optional[float] = None
    mttr_heures: Optional[float] = None

@dataclass
class RobotsScoring:
    niveau_redondance: str = ""       # Faible / Moyen / Élevé
    contrat_maintenance: str = ""     # oui / non
    maj_firmware: str = ""            # oui / non
    historique_pannes: str = ""       # 0 panne / 1-2 / 3-5 / > 5
    capteurs_predictifs: str = ""     # oui / non
    dependance_production: str = ""   # Faible / Moyenne / Critique

@dataclass
class ModuleRobots:
    identification: RobotsIdentification = field(default_factory=RobotsIdentification)
    quantitatif: RobotsQuantitatif = field(default_factory=RobotsQuantitatif)
    scoring: RobotsScoring = field(default_factory=RobotsScoring)


# ── MODULE 2 : MACHINES CNC ───────────────────────────────────
@dataclass
class CNCIdentification:
    type_cnc: str = ""            # 3 axes / 5 axes / Multi-broche
    marque: str = ""
    annee_fabrication: Optional[int] = None
    automation_cnc: str = ""      # Manuel / Semi-auto / Full auto
    interface_mes_erp: str = ""   # oui / non

@dataclass
class CNCTechnique:
    nombre_cnc: Optional[int] = None
    valeur_unitaire_mad: Optional[float] = None
    heures_cumul: Optional[float] = None
    type_refroid: str = ""        # Air / Eau / Huile / Mixte
    sensibilite_electrique: str = ""  # oui / non
    variateur_freq: str = ""      # oui / non

@dataclass
class CNCRisque:
    freq_maintenance_prev: str = ""   # Mensuelle / Trimestrielle / Semestrielle / Annuelle / Aucune
    maintenance_pred_cnc: str = ""    # oui / non
    historique_dom_elec: str = ""     # Aucun / 1-2 incidents / 3+ incidents
    protection_surtension: str = ""   # oui / non
    ups_dedie: str = ""               # oui / non

@dataclass
class ModuleCNC:
    identification: CNCIdentification = field(default_factory=CNCIdentification)
    technique: CNCTechnique = field(default_factory=CNCTechnique)
    risque: CNCRisque = field(default_factory=CNCRisque)


# ── MODULE 3 : SYSTÈME CYBER-PHYSIQUE ─────────────────────────
@dataclass
class CPSArchitecture:
    presence_scada: str = ""          # oui / non
    mes_integre: str = ""             # oui / non
    erp_connecte: str = ""            # oui / non
    cloud_externe: str = ""           # oui / non
    protocole_industriel: str = ""    # OPC-UA / Modbus / Profinet / Autre
    segmentation_reseau: str = ""     # Faible / Moyenne / Élevée

@dataclass
class CPSInfrastructureIT:
    type_serveurs: str = ""           # Sur site / Cloud hybride / Cloud pur
    redondance_serveurs: str = ""     # oui / non
    backup_quotidien: str = ""        # oui / non
    rto_heures: Optional[float] = None
    parefeu_industriel: str = ""      # oui / non
    audit_cyber: str = ""             # oui / non

@dataclass
class CPSAssurantiel:
    dependance_cps: str = ""          # Faible / Moyen / Critique
    historique_incid_it: str = ""     # Aucun / 1-2/an / 3+/an
    temps_moy_arret_it_h: Optional[float] = None
    plan_continuite: str = ""         # oui / non
    simulation_crise: str = ""        # oui / non

@dataclass
class ModuleCPS:
    architecture: CPSArchitecture = field(default_factory=CPSArchitecture)
    infrastructure_it: CPSInfrastructureIT = field(default_factory=CPSInfrastructureIT)
    assurantiel: CPSAssurantiel = field(default_factory=CPSAssurantiel)


# ── MODULE 4 : INFRASTRUCTURE ÉLECTRIQUE ──────────────────────
@dataclass
class ElectriqueEquipement:
    tableau_bt_mt: str = ""           # oui / non
    protection_diff: str = ""         # oui / non
    monitoring_energie: str = ""      # oui / non
    ups_industriel: str = ""          # oui / non
    groupe_electrogene: str = ""      # oui / non

@dataclass
class ElectriqueDonnees:
    puissance_installee_kw: Optional[float] = None
    taux_charge_moyen_pct: Optional[float] = None
    incidents_electriques: str = ""   # 0 / 1-2 / 3-5 / > 5
    mise_a_la_terre: str = ""         # oui / non

@dataclass
class ElectriqueImpact:
    vulnerabilite_dom_elec: str = ""  # Faible / Modérée / Élevée
    risque_court_circuit: str = ""    # oui / non
    risque_propag_incendie: str = ""  # Faible / Modéré / Élevé

@dataclass
class ModuleElectrique:
    equipement: ElectriqueEquipement = field(default_factory=ElectriqueEquipement)
    donnees: ElectriqueDonnees = field(default_factory=ElectriqueDonnees)
    impact: ElectriqueImpact = field(default_factory=ElectriqueImpact)


# ── MODULE 5 : SYSTÈME DE MAINTENANCE ─────────────────────────
@dataclass
class MaintenanceOrganisation:
    gmao_utilisee: str = ""           # oui / non
    type_maintenance: str = ""        # Corrective / Préventive / Prédictive
    existence_kpi: str = ""           # oui / non

@dataclass
class MaintenanceIndicateurs:
    mtbf_global: Optional[float] = None
    mttr_global: Optional[float] = None
    taux_maint_planifie_pct: Optional[float] = None
    taux_respect_planning_pct: Optional[float] = None
    budget_maintenance_pct_parc: Optional[float] = None

@dataclass
class MaintenanceMaturite:
    niveau_digitalisation: str = ""   # 1 à 5
    maint_conditionnelle: str = ""    # oui / non
    ia_predictive: str = ""           # oui / non

@dataclass
class ModuleMaintenance:
    organisation: MaintenanceOrganisation = field(default_factory=MaintenanceOrganisation)
    indicateurs: MaintenanceIndicateurs = field(default_factory=MaintenanceIndicateurs)
    maturite: MaintenanceMaturite = field(default_factory=MaintenanceMaturite)


# ── MODULE 6 : MANUTENTION ────────────────────────────────────
@dataclass
class ManutentionEquipements:
    presence_agv: str = ""
    chariots_elev: str = ""
    ponts_roulants: str = ""
    palans_elec: str = ""
    outillage_special: str = ""
    atelier_interne: str = ""
    nombre_equip: Optional[int] = None
    age_moyen_ans: Optional[float] = None
    disponibilite_pct: Optional[float] = None
    temps_mobilisation_min: Optional[float] = None

@dataclass
class ManutentionScoring:
    manutention_auto: str = ""
    redond_equip_crit: str = ""
    disponibilite_247: str = ""
    dependance_prestataire: str = ""

@dataclass
class ModuleManutention:
    equipements: ManutentionEquipements = field(default_factory=ManutentionEquipements)
    scoring: ManutentionScoring = field(default_factory=ManutentionScoring)


# ── MODULE 7 : STOCKAGE & PIÈCES ──────────────────────────────
@dataclass
class StockageInfrastructure:
    magasin_central: str = ""
    rayonnage_intelligent: str = ""
    stockage_vertical_auto: str = ""
    zone_pieces_crit: str = ""
    controle_therm_humi: str = ""

@dataclass
class StockageGestionNumerique:
    integration_erp_stock: str = ""
    stock_minimum_defini: str = ""
    analyse_abc: str = ""
    delai_reappro_jours: Optional[float] = None
    taux_rupture_stock: str = ""      # 0% / < 5% / 5-15% / > 15%
    suivi_consommation: str = ""

@dataclass
class StockagePerformance:
    temps_moy_disp_piece_h: Optional[float] = None
    pct_pieces_crit_stock: Optional[float] = None
    taux_rotation_stock: Optional[float] = None
    valeur_stock_pct_parc: Optional[float] = None
    prediction_conso: str = ""

@dataclass
class StockageAssurantiel:
    pieces_crit_redond: str = ""
    fournisseurs_multiples: str = ""
    contrat_appro_prio: str = ""
    simulation_penurie: str = ""

@dataclass
class ModuleStockage:
    infrastructure: StockageInfrastructure = field(default_factory=StockageInfrastructure)
    gestion_numerique: StockageGestionNumerique = field(default_factory=StockageGestionNumerique)
    performance: StockagePerformance = field(default_factory=StockagePerformance)
    assurantiel: StockageAssurantiel = field(default_factory=StockageAssurantiel)


# ── MODULE 8 : EFFICACITÉ INTERVENTION ───────────────────────
@dataclass
class InterventionOrganisation:
    equipe_interne: str = ""
    techniciens_certif: str = ""
    astreinte_247: str = ""
    sla_interne_h: Optional[float] = None

@dataclass
class InterventionIndicateurs:
    mttr_moyen: Optional[float] = None
    pct_interv_4h: Optional[float] = None
    pct_interv_planif: Optional[float] = None
    taux_resolution_pp: Optional[float] = None
    historique_arret_24h: Optional[int] = None

@dataclass
class InterventionDigitalisation:
    gmao_mobile: str = ""
    tracabilite_rt: str = ""
    historique_pannes_analyse: str = ""
    dashboard_kpi: str = ""

@dataclass
class ModuleIntervention:
    organisation: InterventionOrganisation = field(default_factory=InterventionOrganisation)
    indicateurs: InterventionIndicateurs = field(default_factory=InterventionIndicateurs)
    digitalisation: InterventionDigitalisation = field(default_factory=InterventionDigitalisation)


# ── FORM DATA GLOBAL ──────────────────────────────────────────
@dataclass
class FormData:
    """Structure de données complète du formulaire — 8 modules"""
    identification: Identification = field(default_factory=Identification)
    robots: ModuleRobots = field(default_factory=ModuleRobots)
    cnc: ModuleCNC = field(default_factory=ModuleCNC)
    cps: ModuleCPS = field(default_factory=ModuleCPS)
    electrique: ModuleElectrique = field(default_factory=ModuleElectrique)
    maintenance: ModuleMaintenance = field(default_factory=ModuleMaintenance)
    manutention: ModuleManutention = field(default_factory=ModuleManutention)
    stockage: ModuleStockage = field(default_factory=ModuleStockage)
    intervention: ModuleIntervention = field(default_factory=ModuleIntervention)


# ── RÉSULTATS ─────────────────────────────────────────────────
@dataclass
class ZoneCritique:
    niveau: str              # "critique" / "majeur"
    module: str
    description: str
    impact: str = ""

@dataclass
class Recommandation:
    priorite: str            # "Urgente" / "Prioritaire" / "Recommandée"
    action: str
    module: str = ""
    impact_estime: str = ""

@dataclass
class ModuleScores:
    robots: int = 0
    cnc: int = 0
    cps: int = 0
    electrique: int = 0
    maintenance: int = 0
    manutention: int = 0
    stockage: int = 0
    intervention: int = 0

@dataclass
class ScoreResult:
    """Résultat complet du scoring — 3 indices + 4 outputs"""
    # Scores principaux
    score_global: int = 0
    score_maturite: int = 0
    score_resilience: int = 0
    score_vulnerabilite: int = 0

    # Scores par module
    module_scores: ModuleScores = field(default_factory=ModuleScores)

    # Profil
    profil_industriel: str = ""
    niveau_risque: str = ""

    # Output D — Carte des points sensibles
    zones_critiques: List[ZoneCritique] = field(default_factory=list)

    # Recommandations
    recommandations: List[Recommandation] = field(default_factory=list)

    # Synthèse souscripteur
    synthese: Dict[str, str] = field(default_factory=dict)

    # Facteurs aggravants
    facteurs_aggravants: List[str] = field(default_factory=list)

    # Comparaison sectorielle
    benchmark_secteur: Dict[str, float] = field(default_factory=dict)
