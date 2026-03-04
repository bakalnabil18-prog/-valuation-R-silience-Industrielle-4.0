"""
risk_matrix.py
══════════════
Détection des zones critiques — Output D : Carte des Points Sensibles
Logique : Complexité × Interdépendance × Capacité d'absorption
"""

from .data_models import FormData, ScoreResult, ZoneCritique


def detect_zones_critiques(data: FormData, result: ScoreResult) -> list[ZoneCritique]:
    """
    Génère la liste des zones critiques et majeures.
    Chaque zone identifie : module source, niveau, description, impact assurantiel.
    """
    zones = []

    # ── CPS — Risque systémique ──────────────────────────────
    if (data.cps.assurantiel.dependance_cps == "Critique"
            and data.cps.infrastructure_it.redondance_serveurs != "oui"):
        zones.append(ZoneCritique(
            niveau="critique",
            module="CPS",
            description="Dépendance CPS critique + absence redondance serveurs MES/SCADA",
            impact="Arrêt total production possible — Perte d'exploitation maximale"
        ))

    if data.cps.assurantiel.plan_continuite != "oui":
        niveau = "critique" if data.cps.assurantiel.dependance_cps == "Critique" else "majeur"
        zones.append(ZoneCritique(
            niveau=niveau,
            module="CPS",
            description="Absence de Plan de Continuité d'Activité (PCA)",
            impact="Durée de sinistre non maîtrisée — Coût aggravé BDM"
        ))

    if data.cps.infrastructure_it.audit_cyber != "oui":
        zones.append(ZoneCritique(
            niveau="majeur",
            module="CPS",
            description="Absence d'audit cybersécurité annuel",
            impact="Vulnérabilité cyber non évaluée — Risque ransomware/intrusion"
        ))

    if data.cps.architecture.segmentation_reseau == "Faible":
        zones.append(ZoneCritique(
            niveau="critique",
            module="CPS",
            description="Réseau industriel non segmenté",
            impact="Propagation rapide en cas d'incident cyber"
        ))

    # ── MAINTENANCE — MTTR élevé ─────────────────────────────
    mttr = data.maintenance.indicateurs.mttr_global or 0
    if mttr > 12:
        zones.append(ZoneCritique(
            niveau="critique",
            module="Maintenance",
            description=f"MTTR global trop élevé ({mttr:.1f}h > seuil 12h)",
            impact="Allongement durée sinistre — Aggravation perte d'exploitation"
        ))
    elif mttr > 8:
        zones.append(ZoneCritique(
            niveau="majeur",
            module="Maintenance",
            description=f"MTTR global élevé ({mttr:.1f}h — seuil recommandé < 8h)",
            impact="Durée d'arrêt supérieure aux benchmarks sectoriels"
        ))

    if data.maintenance.organisation.type_maintenance == "Corrective":
        zones.append(ZoneCritique(
            niveau="critique",
            module="Maintenance",
            description="Maintenance uniquement corrective — aucune anticipation",
            impact="Pannes non prévues — MTTR non maîtrisé"
        ))

    # ── STOCKAGE — Pièces critiques ──────────────────────────
    if data.stockage.assurantiel.pieces_crit_redond != "oui":
        zones.append(ZoneCritique(
            niveau="critique",
            module="Stockage",
            description="Absence de stock de pièces critiques redondantes",
            impact="Allongement durée sinistre — Coût aggravé BDM"
        ))

    if data.stockage.assurantiel.fournisseurs_multiples != "oui":
        zones.append(ZoneCritique(
            niveau="majeur",
            module="Stockage",
            description="Fournisseur unique pour pièces critiques",
            impact="Dépendance totale — Délai approvisionnement non maîtrisé"
        ))

    rupture = data.stockage.gestion_numerique.taux_rupture_stock
    if rupture in ("> 15%", "5-15%"):
        zones.append(ZoneCritique(
            niveau="critique" if rupture == "> 15%" else "majeur",
            module="Stockage",
            description=f"Taux de rupture stock élevé ({rupture})",
            impact="Arrêts de production fréquents par manque pièces"
        ))

    # ── ÉLECTRIQUE ───────────────────────────────────────────
    if (data.electrique.equipement.ups_industriel != "oui"
            and data.electrique.equipement.protection_diff != "oui"):
        zones.append(ZoneCritique(
            niveau="critique",
            module="Électrique",
            description="Infrastructure électrique non protégée (pas d'UPS, pas de protection diff.)",
            impact="Dommages électriques — Court-circuit — Propagation incendie"
        ))
    elif data.electrique.equipement.ups_industriel != "oui":
        zones.append(ZoneCritique(
            niveau="majeur",
            module="Électrique",
            description="Absence d'onduleur industriel (UPS)",
            impact="Dommages équipements sur coupure électrique"
        ))

    if data.electrique.donnees.mise_a_la_terre != "oui":
        zones.append(ZoneCritique(
            niveau="critique",
            module="Électrique",
            description="Mise à la terre non conforme",
            impact="Risque dommage électrique grave — Responsabilité constructeur"
        ))

    # ── ROBOTS ───────────────────────────────────────────────
    if (data.robots.scoring.dependance_production == "Critique"
            and data.robots.scoring.niveau_redondance == "Faible"):
        zones.append(ZoneCritique(
            niveau="critique",
            module="Robots",
            description="Dépendance critique à des robots sans redondance",
            impact="Arrêt total en cas de panne — Perte exploitation totale"
        ))

    # ── INTERVENTION ─────────────────────────────────────────
    if data.intervention.organisation.astreinte_247 != "oui":
        zones.append(ZoneCritique(
            niveau="majeur",
            module="Intervention",
            description="Absence d'astreinte 24/7",
            impact="Pannes nocturnes ou week-end non traitées — MTTR aggravé"
        ))

    arret24 = data.intervention.indicateurs.historique_arret_24h or 0
    if arret24 > 3:
        zones.append(ZoneCritique(
            niveau="critique",
            module="Intervention",
            description=f"Historique d'arrêts > 24h : {arret24} arrêts sur 3 ans",
            impact="Pattern de sinistralité — Prime ajustée"
        ))

    # Trier par niveau (critique d'abord)
    zones.sort(key=lambda z: 0 if z.niveau == "critique" else 1)
    return zones
