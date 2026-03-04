"""
recommendation_engine.py
═══════════════════════
Génère les recommandations techniques priorisées.
Trois niveaux : Urgente / Prioritaire / Recommandée
"""

from .data_models import FormData, ScoreResult, Recommandation


def generate_recommandations(data: FormData, result: ScoreResult) -> list[Recommandation]:
    recs = []

    # ── URGENTES (score faible sur modules critiques) ────────

    if result.score_resilience < 40:
        recs.append(Recommandation(
            priorite="Urgente",
            module="Maintenance",
            action="Migrer vers une maintenance prédictive via IA — impact direct sur MTTR et perte d'exploitation.",
            impact_estime="Réduction MTTR estimée 40-60%"
        ))

    if data.cps.infrastructure_it.redondance_serveurs != "oui":
        recs.append(Recommandation(
            priorite="Urgente",
            module="CPS",
            action="Implémenter la redondance serveurs MES/SCADA — risque d'arrêt total de production.",
            impact_estime="Réduction risque arrêt systémique de 70%"
        ))

    if data.electrique.donnees.mise_a_la_terre != "oui":
        recs.append(Recommandation(
            priorite="Urgente",
            module="Électrique",
            action="Mettre en conformité la mise à la terre selon norme NF C 15-100.",
            impact_estime="Élimination risque dommage électrique grave"
        ))

    mttr = data.maintenance.indicateurs.mttr_global or 0
    if mttr > 12:
        recs.append(Recommandation(
            priorite="Urgente",
            module="Maintenance",
            action=f"Réduire le MTTR global (actuellement {mttr:.1f}h) — cible sectorielle < 4h.",
            impact_estime="Réduction durée sinistre directe"
        ))

    # ── PRIORITAIRES ─────────────────────────────────────────

    if data.cps.assurantiel.plan_continuite != "oui":
        recs.append(Recommandation(
            priorite="Prioritaire",
            module="CPS",
            action="Établir un Plan de Continuité d'Activité (PCA) avec simulation annuelle documentée.",
            impact_estime="Réduction franchise perte d'exploitation"
        ))

    if data.cps.infrastructure_it.audit_cyber != "oui":
        recs.append(Recommandation(
            priorite="Prioritaire",
            module="CPS",
            action="Programmer un audit cybersécurité annuel sur l'infrastructure industrielle (IEC 62443).",
            impact_estime="Couverture cyber améliorée"
        ))

    if data.stockage.assurantiel.pieces_crit_redond != "oui":
        recs.append(Recommandation(
            priorite="Prioritaire",
            module="Stockage",
            action="Constituer un stock de pièces critiques redondantes pour les équipements à longue durée d'approvisionnement.",
            impact_estime="Réduction durée sinistre BDM de 30-50%"
        ))

    if data.electrique.equipement.ups_industriel != "oui":
        recs.append(Recommandation(
            priorite="Prioritaire",
            module="Électrique",
            action="Installer un onduleur industriel (UPS) avec autonomie minimum 15 min sur circuits critiques.",
            impact_estime="Protection dommages électriques"
        ))

    if data.cps.architecture.segmentation_reseau in ("Faible", ""):
        recs.append(Recommandation(
            priorite="Prioritaire",
            module="CPS",
            action="Segmenter le réseau industriel (zones DMZ, VLAN par zone de sécurité).",
            impact_estime="Containment incident cyber"
        ))

    # ── RECOMMANDÉES ─────────────────────────────────────────

    if data.stockage.assurantiel.fournisseurs_multiples != "oui":
        recs.append(Recommandation(
            priorite="Recommandée",
            module="Stockage",
            action="Diversifier les fournisseurs de pièces critiques — minimum 2 fournisseurs homologués.",
            impact_estime="Réduction risque pénurie"
        ))

    if data.robots.scoring.niveau_redondance == "Faible":
        recs.append(Recommandation(
            priorite="Recommandée",
            module="Robots",
            action="Augmenter le niveau de redondance robotique (cellule de remplacement ou robot polyvalent en réserve).",
            impact_estime="Réduction criticité robotique"
        ))

    nd = int(data.maintenance.maturite.niveau_digitalisation or 0)
    if nd < 3:
        recs.append(Recommandation(
            priorite="Recommandée",
            module="Maintenance",
            action="Déployer une GMAO complète avec module mobile et dashboard KPIs maintenance.",
            impact_estime="Amélioration visibilité et planification"
        ))

    if data.manutention.equipements.presence_agv != "oui":
        recs.append(Recommandation(
            priorite="Recommandée",
            module="Manutention",
            action="Étudier l'intégration d'AGV pour réduire le temps de mobilisation lors d'interventions.",
            impact_estime="Réduction MTTR de 20-30%"
        ))

    if data.intervention.organisation.astreinte_247 != "oui":
        recs.append(Recommandation(
            priorite="Recommandée",
            module="Intervention",
            action="Mettre en place une astreinte 24/7 pour les équipements à dépendance critique.",
            impact_estime="Réduction MTTR hors heures ouvrées"
        ))

    if data.stockage.gestion_numerique.analyse_abc != "oui":
        recs.append(Recommandation(
            priorite="Recommandée",
            module="Stockage",
            action="Réaliser une analyse ABC des pièces de rechange pour optimiser le stock.",
            impact_estime="Optimisation coût stockage 15-25%"
        ))

    # Limiter à 8 recommandations max, priorisées
    order = {"Urgente": 0, "Prioritaire": 1, "Recommandée": 2}
    recs.sort(key=lambda r: order.get(r.priorite, 3))
    return recs[:8]
