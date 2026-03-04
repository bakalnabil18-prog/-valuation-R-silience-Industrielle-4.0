"""
scoring_innovant.py
═══════════════════════════════════════════════════════════════════
Module des 20 Indicateurs Innovants — Rapport Expert Comité 2025
═══════════════════════════════════════════════════════════════════

Ajoute une couche avancée au moteur de scoring existant en intégrant
les 20 indicateurs identifiés par le comité d'experts comme prédicteurs
de sinistres industriels non couverts par les modèles classiques.

Chaque indicateur est documenté avec :
  - Sa justification terrain
  - Sa formule de scoring
  - Son indice cible (A=Maturité, B=Résilience, C=Vulnérabilité)

Structure des scores retournés :
  InnovatifScores.score_maturite_bonus    → ajout à l'Indice A (0–20)
  InnovatifScores.score_resilience_bonus  → ajout à l'Indice B (0–20)
  InnovatifScores.score_vulnerabilite_bonus → malus Indice C (0–20)
  InnovatifScores.detail                  → dict détail par indicateur
"""

from dataclasses import dataclass, field
from typing import Optional
from .data_models import FormData


# ─── Dataclass d'entrée pour les 20 indicateurs innovants ───────────────────

@dataclass
class InnovatifInput:
    """
    Saisie des 20 indicateurs innovants.
    Tous les champs sont optionnels (None = non renseigné = score neutre).
    """

    # ── IND-01 : Digital Twin Coverage ──────────────────────────────────────
    # % des actifs critiques couverts par un jumeau numérique actif (0–100)
    digital_twin_coverage_pct: Optional[float] = None

    # ── IND-02 : Indice de Spaghetti Technologique ──────────────────────────
    # % des interfaces système documentées (0–100)
    # 100% = tout est documenté = risque faible
    interfaces_documentees_pct: Optional[float] = None

    # ── IND-03 : Taux de Faux Positifs Maintenance ──────────────────────────
    # % d'alertes GMAO déclenchant une intervention inutile (0–100)
    taux_faux_positifs_pct: Optional[float] = None

    # ── IND-04 : Score de Criticité RCM ─────────────────────────────────────
    # Présence d'une analyse RCM formelle et récente (<5 ans)
    analyse_rcm_presente: Optional[str] = None  # "oui" / "non"
    # Périmètre de l'analyse : "Complet" / "Partiel" / "Aucun"
    rcm_perimetre: Optional[str] = None

    # ── IND-05 : Cyber-Physical Coupling Index ───────────────────────────────
    # Actionneurs critiques commandés directement par logiciel sans validation HW
    actionneurs_sans_validation_hw: Optional[str] = None  # "oui" / "non"
    # Présence de safety relays hardware indépendants
    safety_relays_hw: Optional[str] = None  # "oui" / "non"

    # ── IND-06 : Indice de Résilience Fournisseur ────────────────────────────
    # % des références critiques avec ≥2 fournisseurs qualifiés (0–100)
    fournisseurs_multiples_pct: Optional[float] = None
    # Délai moyen d'approvisionnement alternatif en jours
    delai_appro_alternatif_j: Optional[float] = None

    # ── IND-07 : Score de Dérive de Process (SPC) ────────────────────────────
    # Analyse SPC active sur processus critiques
    spc_actif: Optional[str] = None  # "oui" / "non"
    # Taux de sorties de limites de contrôle (%/mois)
    taux_hors_limites_pct: Optional[float] = None

    # ── IND-08 : Vitesse de Réponse aux Anomalies (MTTD) ────────────────────
    # Mean Time To Detect en minutes
    mttd_minutes: Optional[float] = None

    # ── IND-09 : Indice de Fragmentation de la Connaissance ─────────────────
    # Nombre de compétences critiques détenues par un seul individu
    competences_uniques_nb: Optional[int] = None
    # Plan de succession / knowledge management documenté
    knowledge_management: Optional[str] = None  # "oui" / "non"

    # ── IND-10 : Taux de Satisfaction des Gammes ─────────────────────────────
    # % des interventions critiques tracées conformes aux gammes (0–100)
    conformite_gammes_pct: Optional[float] = None

    # ── IND-11 : Indice de Maturité Énergétique ISO 50001 ───────────────────
    # Certification ISO 50001 active
    iso_50001: Optional[str] = None  # "oui" / "non"
    # Suivi IPE par équipement
    suivi_ipe: Optional[str] = None  # "oui" / "non"

    # ── IND-12 : Score de Simulation Pré-Production ──────────────────────────
    # % des nouvelles configurations testées en simulation avant déploiement (0–100)
    simulation_avant_deploiement_pct: Optional[float] = None

    # ── IND-13 : Indice de Cyber-Hygiène OT ─────────────────────────────────
    # Score composite 0–100 basé sur IEC 62443 / CIS Controls OT
    cyber_hygiene_score: Optional[float] = None

    # ── IND-14 : Taux de Couverture des Tests de Régression ─────────────────
    # % des fonctions critiques PLC/SCADA couvertes par tests de régression (0–100)
    tests_regression_pct: Optional[float] = None

    # ── IND-15 : Indice d'Interdépendance Énergétique ───────────────────────
    # % de la production dépendant d'une source énergétique unique (0–100)
    dependance_source_unique_pct: Optional[float] = None

    # ── IND-16 : Score de Robustesse aux Transitoires Thermiques ────────────
    # Présence de climatisation d'armoire sur variateurs/servos en ambiance >35°C
    climatisation_armoires: Optional[str] = None  # "oui" / "non" / "non_applicable"
    # Température ambiante moyenne atelier en °C
    temp_ambiante_moy_c: Optional[float] = None

    # ── IND-17 : Indice de Modularité de la Production ──────────────────────
    # Nombre de zones de production indépendantes (pouvant tourner isolément)
    zones_independantes_nb: Optional[int] = None
    # % du CA maintenu si une zone tombe en panne (0–100)
    ca_maintenu_si_panne_zone_pct: Optional[float] = None

    # ── IND-18 : Historique de Performance des Sauvegardes ──────────────────
    # Fréquence des backups PLC/SCADA/robots : "Quotidien" / "Hebdo" / "Mensuel" / "Aucun"
    frequence_backup_programmes: Optional[str] = None
    # Dernier test de restauration réussi (en mois)
    dernier_test_restauration_mois: Optional[int] = None

    # ── IND-19 : Score de Résilience aux Erreurs de Communication ───────────
    # Comportement testé sur perte de communication : "Arrêt sécurisé" / "Mode dégradé" / "Non testé"
    comportement_perte_comm: Optional[str] = None

    # ── IND-20 : Taux d'Actualisation des Plans de Masse Électrique ─────────
    # Date de dernière mise à jour des schémas électriques (en années)
    schemas_elec_age_ans: Optional[float] = None
    # Correspondance schémas vs réalité terrain
    schemas_conformes_terrain: Optional[str] = None  # "oui" / "non" / "partiel"


# ─── Dataclass de résultat ───────────────────────────────────────────────────

@dataclass
class InnovatifScores:
    """Résultats des 20 indicateurs innovants."""

    # Bonus/malus par indice (intégrés dans le pipeline principal)
    score_maturite_bonus: int = 0      # s'ajoute à l'Indice A
    score_resilience_bonus: int = 0    # s'ajoute à l'Indice B
    score_vulnerabilite_bonus: int = 0 # s'ajoute à l'Indice C (vulnérabilité = score inversé)

    # Détail par indicateur (pour affichage UI)
    detail: dict = field(default_factory=dict)

    # Score innovant global normalisé 0–100
    score_global_innovant: int = 0


# ─── Fonctions de calcul par indicateur ──────────────────────────────────────

def _ind01_digital_twin(inp: InnovatifInput) -> dict:
    """
    IND-01 — Digital Twin Coverage
    Cible : Indice A (Maturité Mécatronique) — Bonus max +8
    Justification : Le jumeau numérique est l'indicateur le plus avancé de
    maturité 4.0. Permet simulation des défaillances sans arrêt production.
    """
    pct = inp.digital_twin_coverage_pct
    if pct is None:
        return {"score": 0, "indice": "A", "label": "Non renseigné", "max": 8}

    if pct >= 80:
        s, label = 8, "Excellent (≥80%)"
    elif pct >= 50:
        s, label = 5, "Bon (50–79%)"
    elif pct >= 20:
        s, label = 2, "Partiel (20–49%)"
    else:
        s, label = 0, "Absent ou minimal (<20%)"

    return {"score": s, "indice": "A", "label": label, "valeur": f"{pct}%", "max": 8}


def _ind02_spaghetti_tech(inp: InnovatifInput) -> dict:
    """
    IND-02 — Indice de Spaghetti Technologique (interfaces documentées)
    Cible : Indice A (Maturité) — Bonus max +5 / Indice C (Vulnérabilité) — Malus max +10
    Justification : Interfaces non documentées = risque de propagation de défaillance invisible.
    """
    pct = inp.interfaces_documentees_pct
    if pct is None:
        return {"score_a": 0, "score_c": 0, "indice": "A+C", "label": "Non renseigné", "max": 5}

    if pct >= 90:
        sa, sc, label = 5, 0, "Documentation complète (≥90%)"
    elif pct >= 70:
        sa, sc, label = 3, 3, "Documentation partielle (70–89%)"
    elif pct >= 50:
        sa, sc, label = 1, 6, "Documentation insuffisante (50–69%)"
    else:
        sa, sc, label = 0, 10, "Documentation critique (<50%)"

    return {"score_a": sa, "score_c": sc, "indice": "A+C",
            "label": label, "valeur": f"{pct}%", "max": 5}


def _ind03_faux_positifs(inp: InnovatifInput) -> dict:
    """
    IND-03 — Taux de Faux Positifs Maintenance
    Cible : Indice B (Résilience) — Bonus/Malus max ±6
    Justification : Taux élevé = fatigue des alertes, dégradation réactivité réelle.
    """
    pct = inp.taux_faux_positifs_pct
    if pct is None:
        return {"score": 0, "indice": "B", "label": "Non renseigné", "max": 6}

    if pct <= 10:
        s, label = 6, "Excellent (≤10%)"
    elif pct <= 25:
        s, label = 3, "Acceptable (11–25%)"
    elif pct <= 40:
        s, label = 0, "Problématique (26–40%)"
    else:
        s, label = -4, "Critique (>40%) — Fatigue d'alerte"

    return {"score": s, "indice": "B", "label": label, "valeur": f"{pct}%", "max": 6}


def _ind04_rcm(inp: InnovatifInput) -> dict:
    """
    IND-04 — Score de Criticité RCM (Reliability-Centered Maintenance)
    Cible : Indice B (Résilience) — Bonus max +10
    Justification : Analyse RCM = meilleure preuve d'approche structurée du risque.
    """
    presente = inp.analyse_rcm_presente
    perimetre = inp.rcm_perimetre or "Aucun"

    if presente != "oui":
        return {"score": 0, "indice": "B", "label": "Absente — risque non structuré", "max": 10}

    peri_map = {"Complet": 10, "Partiel": 6, "Aucun": 0}
    s = peri_map.get(perimetre, 0)
    label = f"RCM présente — Périmètre {perimetre}"

    return {"score": s, "indice": "B", "label": label, "max": 10}


def _ind05_cyber_physical_coupling(inp: InnovatifInput) -> dict:
    """
    IND-05 — Cyber-Physical Coupling Index
    Cible : Indice C (Vulnérabilité) — Malus max +12
    Justification : Actionneurs haute énergie sans validation HW = risque physique direct
    si compromission logicielle.
    """
    sans_hw = inp.actionneurs_sans_validation_hw
    relays = inp.safety_relays_hw

    if sans_hw is None:
        return {"score": 0, "indice": "C", "label": "Non renseigné", "max": 12}

    v = 0
    if sans_hw == "oui":
        v += 8
        label = "Actionneurs critiques sans validation HW"
    else:
        label = "Validation HW présente sur actionneurs"

    if relays != "oui":
        v += 4
        label += " — Absence safety relays"

    return {"score": v, "indice": "C", "label": label, "max": 12}


def _ind06_resilience_fournisseur(inp: InnovatifInput) -> dict:
    """
    IND-06 — Indice de Résilience Fournisseur
    Cible : Indice B (Résilience) — Bonus max +8
    Justification : Fournisseur unique = MTTR illimité en cas de rupture stock.
    """
    pct = inp.fournisseurs_multiples_pct
    delai = inp.delai_appro_alternatif_j

    if pct is None:
        return {"score": 0, "indice": "B", "label": "Non renseigné", "max": 8}

    if pct >= 80:
        s = 8
    elif pct >= 60:
        s = 5
    elif pct >= 40:
        s = 3
    else:
        s = 0

    label = f"{pct}% références avec multi-fournisseurs"
    if delai is not None:
        if delai > 30:
            s = max(0, s - 3)
            label += f" — Délai alternatif long ({delai}j)"
        elif delai <= 7:
            s = min(8, s + 1)
            label += f" — Délai alternatif rapide ({delai}j)"

    return {"score": s, "indice": "B", "label": label, "max": 8}


def _ind07_process_drift(inp: InnovatifInput) -> dict:
    """
    IND-07 — Score de Dérive de Process (SPC)
    Cible : Indice A (Maturité) — Bonus max +6
    Justification : SPC actif = détection proactive de dégradation avant la panne.
    """
    spc = inp.spc_actif
    taux = inp.taux_hors_limites_pct

    if spc != "oui":
        return {"score": 0, "indice": "A",
                "label": "SPC absent — dérive non détectée", "max": 6}

    s = 4  # base pour SPC actif
    label = "SPC actif"

    if taux is not None:
        if taux <= 2:
            s += 2
            label += f" — Excellent (taux hors limites {taux}%)"
        elif taux <= 5:
            label += f" — Bon ({taux}%)"
        else:
            s = max(0, s - 2)
            label += f" — Dérive fréquente ({taux}%) — à surveiller"

    return {"score": s, "indice": "A", "label": label, "max": 6}


def _ind08_mttd(inp: InnovatifInput) -> dict:
    """
    IND-08 — Vitesse de Réponse aux Anomalies (MTTD)
    Cible : Indice B (Résilience) — Bonus max +8
    Justification : MTTD court = propagation limitée, sinistre moins grave.
    """
    mttd = inp.mttd_minutes
    if mttd is None:
        return {"score": 0, "indice": "B", "label": "Non mesuré", "max": 8}

    if mttd <= 5:
        s, label = 8, f"Excellent MTTD ({mttd} min)"
    elif mttd <= 15:
        s, label = 6, f"Bon MTTD ({mttd} min)"
    elif mttd <= 30:
        s, label = 3, f"Acceptable MTTD ({mttd} min)"
    elif mttd <= 60:
        s, label = 1, f"Lent MTTD ({mttd} min)"
    else:
        s, label = 0, f"Critique MTTD ({mttd} min) — propagation non maîtrisée"

    return {"score": s, "indice": "B", "label": label, "valeur": f"{mttd} min", "max": 8}


def _ind09_fragmentation_connaissance(inp: InnovatifInput) -> dict:
    """
    IND-09 — Indice de Fragmentation de la Connaissance
    Cible : Indice C (Vulnérabilité) — Malus max +8
    Justification : Sur-dépendance à un individu = risque opérationnel immédiat si départ.
    """
    nb = inp.competences_uniques_nb
    km = inp.knowledge_management

    if nb is None:
        return {"score": 0, "indice": "C", "label": "Non renseigné", "max": 8}

    if nb == 0:
        v, label = 0, "Aucune compétence en situation de dépendance unique"
    elif nb <= 2:
        v, label = 3, f"{nb} compétence(s) critique(s) non transférée(s)"
    elif nb <= 5:
        v, label = 6, f"{nb} compétences critiques — risque fragmentation élevé"
    else:
        v, label = 8, f"{nb} compétences critiques — risque fragmentation très élevé"

    if km == "oui" and v > 0:
        v = max(0, v - 2)
        label += " — Atténué par KM documenté"

    return {"score": v, "indice": "C", "label": label, "max": 8}


def _ind10_conformite_gammes(inp: InnovatifInput) -> dict:
    """
    IND-10 — Taux de Satisfaction des Gammes de Maintenance
    Cible : Indice B (Résilience) — Bonus max +6
    Justification : Non-conformité aux gammes = erreur humaine = cause de sinistre.
    """
    pct = inp.conformite_gammes_pct
    if pct is None:
        return {"score": 0, "indice": "B", "label": "Non mesuré", "max": 6}

    if pct >= 90:
        s, label = 6, f"Excellent ({pct}% conformes aux gammes)"
    elif pct >= 75:
        s, label = 4, f"Bon ({pct}%)"
    elif pct >= 60:
        s, label = 2, f"Insuffisant ({pct}%) — interventions improvisées"
    else:
        s, label = 0, f"Critique ({pct}%) — gammes non suivies"

    return {"score": s, "indice": "B", "label": label, "valeur": f"{pct}%", "max": 6}


def _ind11_iso50001(inp: InnovatifInput) -> dict:
    """
    IND-11 — Indice de Maturité Énergétique ISO 50001
    Cible : Indice A (Maturité) — Bonus max +5
    Justification : ISO 50001 + suivi IPE = détection précoce de dérive électrique.
    """
    iso = inp.iso_50001
    ipe = inp.suivi_ipe

    s = 0
    if iso == "oui":
        s += 3
        label = "ISO 50001 certifié"
    else:
        label = "Pas de certification ISO 50001"

    if ipe == "oui":
        s += 2
        label += " + Suivi IPE par équipement"

    return {"score": s, "indice": "A", "label": label, "max": 5}


def _ind12_simulation_preproduction(inp: InnovatifInput) -> dict:
    """
    IND-12 — Score de Simulation Pré-Production
    Cible : Indice A (Maturité) — Bonus max +7
    Justification : Simulation avant déploiement = réduction drastique des sinistres
    liés aux erreurs de programmation/configuration.
    """
    pct = inp.simulation_avant_deploiement_pct
    if pct is None:
        return {"score": 0, "indice": "A", "label": "Non renseigné", "max": 7}

    if pct >= 90:
        s, label = 7, f"Excellent — simulation systématique ({pct}%)"
    elif pct >= 70:
        s, label = 5, f"Bon — simulation majoritaire ({pct}%)"
    elif pct >= 40:
        s, label = 2, f"Partiel — simulation occasionnelle ({pct}%)"
    else:
        s, label = 0, f"Absent ou rare ({pct}%) — risque déploiement élevé"

    return {"score": s, "indice": "A", "label": label, "valeur": f"{pct}%", "max": 7}


def _ind13_cyber_hygiene(inp: InnovatifInput) -> dict:
    """
    IND-13 — Indice de Cyber-Hygiène OT (0–100)
    Cible : Indice C (Vulnérabilité) — Malus max +15
    Justification : Score IEC 62443 faible = surface d'attaque OT non maîtrisée.
    """
    score = inp.cyber_hygiene_score
    if score is None:
        return {"score": 0, "indice": "C", "label": "Non évalué", "max": 15}

    if score >= 80:
        v, label = 0, f"Cyber-hygiène OT excellente ({score}/100)"
    elif score >= 60:
        v, label = 4, f"Cyber-hygiène OT correcte ({score}/100)"
    elif score >= 40:
        v, label = 8, f"Cyber-hygiène OT insuffisante ({score}/100)"
    else:
        v, label = 15, f"Cyber-hygiène OT critique ({score}/100) — exposition majeure"

    return {"score": v, "indice": "C", "label": label,
            "valeur": f"{score}/100", "max": 15}


def _ind14_tests_regression(inp: InnovatifInput) -> dict:
    """
    IND-14 — Taux de Couverture des Tests de Régression
    Cible : Indice A (Maturité) — Bonus max +5
    Justification : Tests de régression sur PLC/SCADA = protection contre les
    mises à jour défaillantes.
    """
    pct = inp.tests_regression_pct
    if pct is None:
        return {"score": 0, "indice": "A", "label": "Non mesuré", "max": 5}

    if pct >= 80:
        s, label = 5, f"Excellent ({pct}% fonctions couvertes)"
    elif pct >= 60:
        s, label = 3, f"Bon ({pct}%)"
    elif pct >= 30:
        s, label = 1, f"Partiel ({pct}%)"
    else:
        s, label = 0, f"Insuffisant ({pct}%) — risque mise à jour élevé"

    return {"score": s, "indice": "A", "label": label, "valeur": f"{pct}%", "max": 5}


def _ind15_interdependance_energetique(inp: InnovatifInput) -> dict:
    """
    IND-15 — Indice d'Interdépendance Énergétique
    Cible : Indice C (Vulnérabilité) — Malus max +10
    Justification : Source énergétique unique = SPOF énergétique absolu.
    """
    pct = inp.dependance_source_unique_pct
    if pct is None:
        return {"score": 0, "indice": "C", "label": "Non renseigné", "max": 10}

    if pct >= 80:
        v, label = 10, f"Dépendance totale à une source unique ({pct}%) — SPOF critique"
    elif pct >= 60:
        v, label = 6, f"Forte dépendance ({pct}%)"
    elif pct >= 40:
        v, label = 3, f"Dépendance modérée ({pct}%)"
    else:
        v, label = 0, f"Architecture énergétique résiliente ({pct}%)"

    return {"score": v, "indice": "C", "label": label,
            "valeur": f"{pct}%", "max": 10}


def _ind16_thermique(inp: InnovatifInput) -> dict:
    """
    IND-16 — Score de Robustesse aux Transitoires Thermiques
    Cible : Indice C (Vulnérabilité) — Malus max +6
    Justification : Variateurs/servos sans climatisation en ambiance >35°C = risque
    dommage électrique thermique élevé.
    """
    clim = inp.climatisation_armoires
    temp = inp.temp_ambiante_moy_c

    if clim == "non_applicable" or temp is None:
        return {"score": 0, "indice": "C", "label": "Non applicable", "max": 6}

    if temp is not None and temp > 35:
        if clim != "oui":
            v, label = 6, f"Armoires sans climatisation à {temp}°C — risque thermique élevé"
        else:
            v, label = 0, f"Climatisation armoires présente (ambiance {temp}°C)"
    elif temp is not None and temp > 28:
        if clim != "oui":
            v, label = 3, f"Ambiance chaude ({temp}°C) sans climatisation — surveillance recommandée"
        else:
            v, label = 0, f"Climatisation armoires présente (ambiance {temp}°C)"
    else:
        v, label = 0, f"Ambiance thermique acceptable ({temp}°C)"

    return {"score": v, "indice": "C", "label": label, "max": 6}


def _ind17_modularite_production(inp: InnovatifInput) -> dict:
    """
    IND-17 — Indice de Modularité de la Production
    Cible : Indice B (Résilience) — Bonus max +8
    Justification : Architecture modulaire = perte d'exploitation partielle
    au lieu de totale.
    """
    zones = inp.zones_independantes_nb
    ca_maintenu = inp.ca_maintenu_si_panne_zone_pct

    if zones is None:
        return {"score": 0, "indice": "B", "label": "Non renseigné", "max": 8}

    if zones >= 4:
        s = 6
    elif zones >= 2:
        s = 4
    elif zones == 1:
        s = 1
    else:
        s = 0

    label = f"{zones} zone(s) indépendante(s)"

    if ca_maintenu is not None:
        if ca_maintenu >= 70:
            s = min(8, s + 2)
            label += f" — {ca_maintenu}% CA maintenu en cas de panne partielle"
        elif ca_maintenu >= 40:
            label += f" — {ca_maintenu}% CA maintenu"
        else:
            s = max(0, s - 1)
            label += f" — Seulement {ca_maintenu}% CA maintenu — forte dépendance"

    return {"score": s, "indice": "B", "label": label, "max": 8}


def _ind18_backups_programmes(inp: InnovatifInput) -> dict:
    """
    IND-18 — Historique de Performance des Sauvegardes
    Cible : Indice C (Vulnérabilité) — Malus max +10
    Justification : Absence de backup PLC/SCADA = MTTR incontrôlé si sinistre
    sur le système de contrôle.
    """
    freq = inp.frequence_backup_programmes
    test_mois = inp.dernier_test_restauration_mois

    freq_map = {
        "Quotidien": 0,
        "Hebdo": 2,
        "Mensuel": 5,
        "Aucun": 10,
    }
    v = freq_map.get(freq, 5) if freq else 5
    label = f"Fréquence backups : {freq or 'Non renseigné'}"

    if test_mois is not None:
        if test_mois <= 3:
            v = max(0, v - 2)
            label += f" — Test restauration récent ({test_mois} mois)"
        elif test_mois <= 6:
            label += f" — Test restauration {test_mois} mois"
        else:
            v = min(10, v + 3)
            label += f" — Test restauration trop ancien ({test_mois} mois)"
    else:
        v = min(10, v + 2)
        label += " — Aucun test de restauration documenté"

    return {"score": v, "indice": "C", "label": label, "max": 10}


def _ind19_resilience_comm(inp: InnovatifInput) -> dict:
    """
    IND-19 — Score de Résilience aux Erreurs de Communication
    Cible : Indice B (Résilience) — Bonus max +6
    Justification : Comportement de repli sécurisé = protection contre les
    pannes en cascade sur perte de communication.
    """
    comp = inp.comportement_perte_comm
    if comp is None:
        return {"score": 0, "indice": "B", "label": "Non testé", "max": 6}

    comp_map = {
        "Arrêt sécurisé": (6, "Arrêt sécurisé testé — comportement nominal"),
        "Mode dégradé": (4, "Mode dégradé documenté — production partielle préservée"),
        "Non testé": (0, "Comportement non testé — risque propagation défaillance"),
    }
    s, label = comp_map.get(comp, (0, "Non renseigné"))

    return {"score": s, "indice": "B", "label": label, "max": 6}


def _ind20_schemas_electriques(inp: InnovatifInput) -> dict:
    """
    IND-20 — Taux d'Actualisation des Plans de Masse Électrique
    Cible : Indice C (Vulnérabilité) — Malus max +8
    Justification : Schémas périmés = interventions dangereuses, risque
    dommage électrique iatrogénique lors des maintenances.
    """
    age = inp.schemas_elec_age_ans
    conforme = inp.schemas_conformes_terrain

    v = 0
    label = ""

    if age is None:
        label = "Âge des schémas non renseigné"
    elif age > 5:
        v += 5
        label = f"Schémas électriques anciens ({age} ans sans mise à jour)"
    elif age > 2:
        v += 2
        label = f"Schémas électriques à mettre à jour ({age} ans)"
    else:
        label = f"Schémas électriques récents ({age} ans)"

    if conforme == "non":
        v += 3
        label += " — Non conformes au terrain (risque intervention)"
    elif conforme == "partiel":
        v += 1
        label += " — Conformité partielle au terrain"

    return {"score": min(8, v), "indice": "C", "label": label, "max": 8}


# ─── Fonction principale : calcul de tous les indicateurs ───────────────────

def compute_innovant_scores(inp: InnovatifInput) -> InnovatifScores:
    """
    Calcule les 20 indicateurs innovants et retourne un InnovatifScores.

    Les résultats sont intégrés dans le pipeline principal via :
        score_maturite_final    = min(100, score_maturite_base + bonus_A)
        score_resilience_final  = min(100, score_resilience_base + bonus_B)
        score_vulnerabilite_final = min(100, score_vulnerabilite_base + bonus_C)

    Parameters
    ----------
    inp : InnovatifInput
        Données des 20 indicateurs innovants.

    Returns
    -------
    InnovatifScores
        Scores détaillés et totaux par indice.
    """
    detail = {}
    bonus_a = 0   # Bonus Indice A (Maturité)
    bonus_b = 0   # Bonus Indice B (Résilience)
    bonus_c = 0   # Malus Indice C (Vulnérabilité, score inversé)

    # ── IND-01 Digital Twin ───────────────────────────────────────────────
    r01 = _ind01_digital_twin(inp)
    bonus_a += r01["score"]
    detail["IND-01 Digital Twin Coverage"] = r01

    # ── IND-02 Spaghetti Technologique ────────────────────────────────────
    r02 = _ind02_spaghetti_tech(inp)
    bonus_a += r02.get("score_a", 0)
    bonus_c += r02.get("score_c", 0)
    detail["IND-02 Spaghetti Technologique"] = r02

    # ── IND-03 Faux Positifs ──────────────────────────────────────────────
    r03 = _ind03_faux_positifs(inp)
    bonus_b += r03["score"]
    detail["IND-03 Taux Faux Positifs Maintenance"] = r03

    # ── IND-04 RCM ────────────────────────────────────────────────────────
    r04 = _ind04_rcm(inp)
    bonus_b += r04["score"]
    detail["IND-04 Score Criticité RCM"] = r04

    # ── IND-05 Cyber-Physical Coupling ────────────────────────────────────
    r05 = _ind05_cyber_physical_coupling(inp)
    bonus_c += r05["score"]
    detail["IND-05 Cyber-Physical Coupling Index"] = r05

    # ── IND-06 Résilience Fournisseur ─────────────────────────────────────
    r06 = _ind06_resilience_fournisseur(inp)
    bonus_b += r06["score"]
    detail["IND-06 Indice Résilience Fournisseur"] = r06

    # ── IND-07 Process Drift ──────────────────────────────────────────────
    r07 = _ind07_process_drift(inp)
    bonus_a += r07["score"]
    detail["IND-07 Score Dérive de Process (SPC)"] = r07

    # ── IND-08 MTTD ───────────────────────────────────────────────────────
    r08 = _ind08_mttd(inp)
    bonus_b += r08["score"]
    detail["IND-08 Vitesse Réponse Anomalies (MTTD)"] = r08

    # ── IND-09 Fragmentation Connaissance ─────────────────────────────────
    r09 = _ind09_fragmentation_connaissance(inp)
    bonus_c += r09["score"]
    detail["IND-09 Fragmentation de la Connaissance"] = r09

    # ── IND-10 Conformité Gammes ──────────────────────────────────────────
    r10 = _ind10_conformite_gammes(inp)
    bonus_b += r10["score"]
    detail["IND-10 Conformité Gammes Maintenance"] = r10

    # ── IND-11 ISO 50001 ──────────────────────────────────────────────────
    r11 = _ind11_iso50001(inp)
    bonus_a += r11["score"]
    detail["IND-11 Maturité Énergétique ISO 50001"] = r11

    # ── IND-12 Simulation Pré-Production ─────────────────────────────────
    r12 = _ind12_simulation_preproduction(inp)
    bonus_a += r12["score"]
    detail["IND-12 Simulation Pré-Production"] = r12

    # ── IND-13 Cyber-Hygiène OT ──────────────────────────────────────────
    r13 = _ind13_cyber_hygiene(inp)
    bonus_c += r13["score"]
    detail["IND-13 Indice Cyber-Hygiène OT"] = r13

    # ── IND-14 Tests de Régression ────────────────────────────────────────
    r14 = _ind14_tests_regression(inp)
    bonus_a += r14["score"]
    detail["IND-14 Couverture Tests de Régression"] = r14

    # ── IND-15 Interdépendance Énergétique ────────────────────────────────
    r15 = _ind15_interdependance_energetique(inp)
    bonus_c += r15["score"]
    detail["IND-15 Interdépendance Énergétique"] = r15

    # ── IND-16 Robustesse Thermique ───────────────────────────────────────
    r16 = _ind16_thermique(inp)
    bonus_c += r16["score"]
    detail["IND-16 Robustesse Transitoires Thermiques"] = r16

    # ── IND-17 Modularité Production ──────────────────────────────────────
    r17 = _ind17_modularite_production(inp)
    bonus_b += r17["score"]
    detail["IND-17 Modularité de la Production"] = r17

    # ── IND-18 Backups Programmes ─────────────────────────────────────────
    r18 = _ind18_backups_programmes(inp)
    bonus_c += r18["score"]
    detail["IND-18 Performance des Sauvegardes"] = r18

    # ── IND-19 Résilience Communication ──────────────────────────────────
    r19 = _ind19_resilience_comm(inp)
    bonus_b += r19["score"]
    detail["IND-19 Résilience Erreurs Communication"] = r19

    # ── IND-20 Schémas Électriques ────────────────────────────────────────
    r20 = _ind20_schemas_electriques(inp)
    bonus_c += r20["score"]
    detail["IND-20 Actualisation Plans Électriques"] = r20

    # ── Clamp des bonus/malus ─────────────────────────────────────────────
    # Limite l'impact maximal des indicateurs innovants sur chaque indice
    # pour éviter de trop déséquilibrer le modèle de base
    MAX_BONUS_A = 20  # +20 pts max sur l'Indice A
    MAX_BONUS_B = 20  # +20 pts max sur l'Indice B
    MAX_BONUS_C = 20  # +20 pts max sur l'Indice C (vulnérabilité)

    bonus_a = max(-5, min(MAX_BONUS_A, bonus_a))
    bonus_b = max(-5, min(MAX_BONUS_B, bonus_b))
    bonus_c = max(0, min(MAX_BONUS_C, bonus_c))

    # ── Score innovant global (pour affichage) ────────────────────────────
    # Combine les 3 bonus en un score lisible 0–100
    score_global = round(
        (bonus_a / MAX_BONUS_A * 0.35 +
         bonus_b / MAX_BONUS_B * 0.45 +
         (1 - bonus_c / MAX_BONUS_C) * 0.20) * 100
    )

    return InnovatifScores(
        score_maturite_bonus=bonus_a,
        score_resilience_bonus=bonus_b,
        score_vulnerabilite_bonus=bonus_c,
        detail=detail,
        score_global_innovant=max(0, min(100, score_global)),
    )


# ─── Intégration dans le pipeline principal ──────────────────────────────────

def apply_innovant_to_pipeline(
    score_maturite: int,
    score_resilience: int,
    score_vulnerabilite: int,
    innovant: InnovatifScores,
) -> tuple[int, int, int, int]:
    """
    Applique les scores innovants aux 3 indices existants et recalcule
    le score global.

    Parameters
    ----------
    score_maturite : int
        Indice A de base (0–100).
    score_resilience : int
        Indice B de base (0–100).
    score_vulnerabilite : int
        Indice C de base (0–100, inversé).
    innovant : InnovatifScores
        Résultat des 20 indicateurs innovants.

    Returns
    -------
    tuple (score_maturite_final, score_resilience_final,
           score_vulnerabilite_final, score_global_final)
    """
    sm = min(100, max(0, score_maturite + innovant.score_maturite_bonus))
    sr = min(100, max(0, score_resilience + innovant.score_resilience_bonus))
    sv = min(100, max(0, score_vulnerabilite + innovant.score_vulnerabilite_bonus))

    sg = min(100, max(0, round(
        sm * 0.35 + sr * 0.45 + (100 - sv) * 0.20
    )))

    return sm, sr, sv, sg


# ─── Utilitaires UI ──────────────────────────────────────────────────────────

def get_innovant_summary(innovant: InnovatifScores) -> list[dict]:
    """
    Retourne une liste triée des indicateurs innovants avec leur impact,
    prête pour affichage dans le dashboard Streamlit.

    Format de chaque entrée :
        {"indicateur": str, "indice": str, "score": int, "label": str, "impact": str}
    """
    items = []
    for nom, data in innovant.detail.items():
        score_val = data.get("score", data.get("score_a", 0))
        max_val = data.get("max", 10)
        indice = data.get("indice", "?")

        if indice == "C":
            # Vulnérabilité : élevé = mauvais
            if score_val >= max_val * 0.7:
                impact = "🔴 Malus fort"
            elif score_val >= max_val * 0.3:
                impact = "🟡 Malus modéré"
            else:
                impact = "🟢 Faible impact négatif"
        else:
            # Maturité / Résilience : élevé = bon
            if score_val >= max_val * 0.7:
                impact = "🟢 Bonus fort"
            elif score_val >= max_val * 0.3:
                impact = "🟡 Bonus modéré"
            else:
                impact = "🔴 Faible contribution"

        items.append({
            "indicateur": nom,
            "indice": indice,
            "score": score_val,
            "max": max_val,
            "label": data.get("label", ""),
            "impact": impact,
        })

    # Trier : d'abord les impacts négatifs (C à score élevé),
    # puis les contributions positives faibles
    items.sort(key=lambda x: (
        -(x["score"] if x["indice"] == "C" else -x["max"] + x["score"])
    ))

    return items


def get_top_innovant_risks(innovant: InnovatifScores, n: int = 5) -> list[dict]:
    """
    Retourne les N indicateurs innovants les plus préoccupants
    pour la fiche de souscription.
    """
    all_items = get_innovant_summary(innovant)
    # Priorité aux indicateurs C (vulnérabilité) avec score élevé
    # et aux indicateurs A/B avec score faible
    risks = [
        i for i in all_items
        if (i["indice"] == "C" and i["score"] >= i["max"] * 0.5)
        or (i["indice"] in ("A", "B") and i["score"] < i["max"] * 0.3
            and i["score"] < 3)
    ]
    return risks[:n]
