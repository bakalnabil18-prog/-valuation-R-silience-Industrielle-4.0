"""
forms_innovant.py
══════════════════════════════════════════════════════════════════
Formulaire Streamlit pour les 20 indicateurs innovants.
S'intègre dans le stepper existant comme une 6e étape optionnelle.
══════════════════════════════════════════════════════════════════
"""

import streamlit as st
from ..engine.scoring_innovant import InnovatifInput


# ─── Helpers ────────────────────────────────────────────────────────────────

def _bool(key, label, help_txt=None):
    """Sélecteur Oui / Non avec valeur None si non renseigné."""
    val = st.selectbox(
        label,
        ["— Non renseigné —", "Oui", "Non"],
        key=key,
        help=help_txt,
    )
    if val == "Oui":
        return "oui"
    elif val == "Non":
        return "non"
    return None


def _pct(key, label, help_txt=None):
    """Saisie pourcentage 0–100 avec None si non renseigné."""
    val = st.number_input(
        label,
        min_value=0.0,
        max_value=100.0,
        value=None,
        step=1.0,
        placeholder="— Non renseigné —",
        key=key,
        help=help_txt,
    )
    return val


def _section(title, icon):
    st.markdown(
        f"""<div style="
            background: linear-gradient(135deg, #0f2244, #1d4ed8);
            border-radius: 8px; padding: 10px 16px; margin: 18px 0 10px 0;
        ">
        <span style="font-size:18px">{icon}</span>
        <span style="color:white; font-weight:700; font-size:15px; margin-left:8px">{title}</span>
        </div>""",
        unsafe_allow_html=True,
    )


def _info_badge(text):
    st.markdown(
        f'<div style="background:#eff6ff; border-left:3px solid #1d4ed8; '
        f'padding:8px 12px; border-radius:4px; font-size:12px; color:#1e3a6e; '
        f'margin-bottom:8px">{text}</div>',
        unsafe_allow_html=True,
    )


# ─── Formulaire principal ────────────────────────────────────────────────────

def render_form_innovant() -> InnovatifInput:
    """
    Affiche le formulaire des 20 indicateurs innovants.
    Retourne un InnovatifInput avec les valeurs saisies.
    """
    st.markdown("""
    <div style="background:#f0f4ff; border-radius:10px; padding:14px 18px; margin-bottom:18px">
        <h4 style="margin:0; color:#0f2244">🔬 Indicateurs Innovants — Rapport Expert</h4>
        <p style="margin:6px 0 0 0; font-size:13px; color:#555">
        Ces 20 indicateurs avancés complètent le scoring de base avec des critères
        non utilisés par les assureurs classiques. Tous les champs sont optionnels.
        </p>
    </div>
    """, unsafe_allow_html=True)

    inp = {}

    # ════════════════════════════════════════════════════════════════════════
    # BLOC A — INDICATEURS MATURITÉ MÉCATRONIQUE
    # ════════════════════════════════════════════════════════════════════════
    _section("Indicateurs de Maturité Mécatronique", "⚙️")
    _info_badge("Ces indicateurs complètent l'Indice A (Maturité Mécatronique) — bonus max +20 pts")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**IND-01 — Digital Twin Coverage**")
        inp["digital_twin_coverage_pct"] = _pct(
            "dt_cov",
            "% des actifs critiques avec jumeau numérique actif",
            "Un jumeau numérique permet de simuler les défaillances sans arrêt. "
            "C'est l'indicateur le plus avancé de maturité 4.0."
        )

        st.markdown("**IND-07 — Dérive de Process (SPC)**")
        inp["spc_actif"] = _bool(
            "spc",
            "Analyse SPC (Statistical Process Control) active sur processus critiques ?",
            "Détection proactive de dégradation de procédé avant la panne."
        )
        if inp["spc_actif"] == "oui":
            inp["taux_hors_limites_pct"] = _pct(
                "spc_taux",
                "Taux de sorties de limites de contrôle (%/mois)",
            )
        else:
            inp["taux_hors_limites_pct"] = None

        st.markdown("**IND-11 — Maturité Énergétique ISO 50001**")
        inp["iso_50001"] = _bool("iso50001", "Certification ISO 50001 active ?")
        inp["suivi_ipe"] = _bool(
            "ipe",
            "Suivi IPE (Indicateurs de Performance Énergétique) par équipement ?",
            "Permet de détecter les dérives électriques machine par machine."
        )

        st.markdown("**IND-14 — Tests de Régression PLC/SCADA**")
        inp["tests_regression_pct"] = _pct(
            "tests_reg",
            "% des fonctions PLC/SCADA couvertes par tests de régression automatiques",
            "Protège contre les mises à jour défaillantes du logiciel de contrôle."
        )

    with col2:
        st.markdown("**IND-02 — Documentation des Interfaces**")
        inp["interfaces_documentees_pct"] = _pct(
            "interfaces_doc",
            "% des interfaces système documentées (intégrations, protocoles, flux)",
            "Interfaces non documentées = risque de propagation de défaillance invisible."
        )

        st.markdown("**IND-12 — Simulation Pré-Production**")
        inp["simulation_avant_deploiement_pct"] = _pct(
            "sim_prod",
            "% des nouvelles configs/programmes testés en simulation avant déploiement",
            "Réduit drastiquement les sinistres liés aux erreurs de programmation."
        )

        st.markdown("**IND-04 — Analyse RCM**")
        inp["analyse_rcm_presente"] = _bool(
            "rcm",
            "Analyse RCM (Reliability-Centered Maintenance) formelle disponible ?",
            "RCM structurée < 5 ans = meilleure preuve d'approche structurée du risque."
        )
        if inp["analyse_rcm_presente"] == "oui":
            inp["rcm_perimetre"] = st.selectbox(
                "Périmètre de l'analyse RCM",
                ["Complet", "Partiel"],
                key="rcm_perimetre"
            )
        else:
            inp["rcm_perimetre"] = None

    # ════════════════════════════════════════════════════════════════════════
    # BLOC B — INDICATEURS RÉSILIENCE OPÉRATIONNELLE
    # ════════════════════════════════════════════════════════════════════════
    _section("Indicateurs de Résilience Opérationnelle", "🛡️")
    _info_badge("Ces indicateurs complètent l'Indice B (Résilience Opérationnelle) — bonus max +20 pts")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**IND-03 — Taux de Faux Positifs Maintenance**")
        inp["taux_faux_positifs_pct"] = _pct(
            "faux_pos",
            "% d'alertes GMAO déclenchant une intervention inutile",
            "Taux élevé = fatigue d'alerte. Les techniciens finissent par ignorer les vraies alertes."
        )

        st.markdown("**IND-08 — MTTD (Détection d'Anomalie)**")
        mttd = st.number_input(
            "Mean Time To Detect — Délai moyen de détection d'anomalie (minutes)",
            min_value=0.0,
            max_value=1440.0,
            value=None,
            step=1.0,
            placeholder="— Non mesuré —",
            key="mttd",
            help="Temps entre apparition d'une anomalie et sa détection par le système ou l'opérateur."
        )
        inp["mttd_minutes"] = mttd

        st.markdown("**IND-10 — Conformité aux Gammes de Maintenance**")
        inp["conformite_gammes_pct"] = _pct(
            "gammes",
            "% des interventions critiques réalisées conformément aux gammes définies",
            "Non-conformité = improvisation = source directe de sinistre."
        )

        st.markdown("**IND-17 — Modularité de la Production**")
        zones = st.number_input(
            "Nombre de zones de production pouvant fonctionner indépendamment",
            min_value=0,
            max_value=20,
            value=None,
            step=1,
            placeholder="— Non renseigné —",
            key="zones_ind",
        )
        inp["zones_independantes_nb"] = zones
        inp["ca_maintenu_si_panne_zone_pct"] = _pct(
            "ca_maintenu",
            "% du CA maintenu si une zone tombe en panne",
        )

    with col2:
        st.markdown("**IND-06 — Résilience Fournisseur**")
        inp["fournisseurs_multiples_pct"] = _pct(
            "fourmult",
            "% des références critiques avec ≥2 fournisseurs qualifiés",
            "Fournisseur unique = MTTR illimité si rupture stock."
        )
        delai_alt = st.number_input(
            "Délai moyen d'approvisionnement alternatif (jours)",
            min_value=0.0,
            max_value=365.0,
            value=None,
            step=1.0,
            placeholder="— Non renseigné —",
            key="delai_alt",
        )
        inp["delai_appro_alternatif_j"] = delai_alt

        st.markdown("**IND-09 — Fragmentation de la Connaissance**")
        nb_comp = st.number_input(
            "Nombre de compétences critiques détenues par un seul individu",
            min_value=0,
            max_value=50,
            value=None,
            step=1,
            placeholder="— Non renseigné —",
            key="comp_uniques",
            help="Compétences pour lesquelles il n'y a pas de doublon ni documentation de transfert."
        )
        inp["competences_uniques_nb"] = nb_comp
        inp["knowledge_management"] = _bool(
            "km",
            "Plan de succession / Knowledge Management documenté ?"
        )

        st.markdown("**IND-19 — Résilience aux Erreurs de Communication**")
        inp["comportement_perte_comm"] = st.selectbox(
            "Comportement du système sur perte de communication inter-systèmes",
            ["— Non renseigné —", "Arrêt sécurisé", "Mode dégradé", "Non testé"],
            key="comm_resilience",
            help="Testé = test documenté de déconnexion délibérée avec observation du comportement."
        )
        if inp["comportement_perte_comm"] == "— Non renseigné —":
            inp["comportement_perte_comm"] = None

    # ════════════════════════════════════════════════════════════════════════
    # BLOC C — INDICATEURS VULNÉRABILITÉ SYSTÉMIQUE
    # ════════════════════════════════════════════════════════════════════════
    _section("Indicateurs de Vulnérabilité Systémique", "🔎")
    _info_badge(
        "Ces indicateurs complètent l'Indice C (Vulnérabilité Systémique, score inversé). "
        "Un score élevé ici = malus sur le score global."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**IND-05 — Cyber-Physical Coupling**")
        inp["actionneurs_sans_validation_hw"] = _bool(
            "act_nohw",
            "Des actionneurs critiques (haute énergie/pression) sont-ils commandés "
            "directement par logiciel SANS validation hardware indépendante ?",
            "Un acteur sans safety relay = une commande logicielle erronée peut causer "
            "un dommage physique immédiat."
        )
        inp["safety_relays_hw"] = _bool(
            "safety_rel",
            "Safety relays hardware indépendants présents sur actionneurs critiques ?"
        )

        st.markdown("**IND-13 — Cyber-Hygiène OT**")
        inp["cyber_hygiene_score"] = st.number_input(
            "Score de cyber-hygiène OT (0–100, basé sur IEC 62443 / CIS Controls)",
            min_value=0.0,
            max_value=100.0,
            value=None,
            step=1.0,
            placeholder="— Non évalué —",
            key="cyber_hyg",
            help="Basé sur 10 critères : gestion mots de passe, inventaire actifs, "
                 "segmentation, accès distants, backups..."
        )

        st.markdown("**IND-15 — Interdépendance Énergétique**")
        inp["dependance_source_unique_pct"] = _pct(
            "dep_elec",
            "% de la production dépendant d'une source énergétique unique",
            "Absence de redondance énergétique = SPOF absolu."
        )

        st.markdown("**IND-20 — Actualisation Schémas Électriques**")
        schema_age = st.number_input(
            "Âge des schémas électriques (années depuis dernière mise à jour)",
            min_value=0.0,
            max_value=50.0,
            value=None,
            step=0.5,
            placeholder="— Non renseigné —",
            key="schema_age",
        )
        inp["schemas_elec_age_ans"] = schema_age
        inp["schemas_conformes_terrain"] = st.selectbox(
            "Les schémas électriques correspondent-ils à l'installation réelle ?",
            ["— Non renseigné —", "oui", "partiel", "non"],
            key="schema_conf",
        )
        if inp["schemas_conformes_terrain"] == "— Non renseigné —":
            inp["schemas_conformes_terrain"] = None

    with col2:
        st.markdown("**IND-16 — Robustesse Thermique**")
        temp_amb = st.number_input(
            "Température ambiante moyenne de l'atelier (°C)",
            min_value=5.0,
            max_value=60.0,
            value=None,
            step=1.0,
            placeholder="— Non renseigné —",
            key="temp_amb",
        )
        inp["temp_ambiante_moy_c"] = temp_amb
        inp["climatisation_armoires"] = st.selectbox(
            "Climatisation des armoires électriques (variateurs, servos) ?",
            ["— Non renseigné —", "oui", "non", "non_applicable"],
            key="clim_arm",
        )
        if inp["climatisation_armoires"] == "— Non renseigné —":
            inp["climatisation_armoires"] = None

        st.markdown("**IND-18 — Performance des Sauvegardes**")
        inp["frequence_backup_programmes"] = st.selectbox(
            "Fréquence des sauvegardes des programmes PLC/SCADA/Robots",
            ["— Non renseigné —", "Quotidien", "Hebdo", "Mensuel", "Aucun"],
            key="backup_freq",
        )
        if inp["frequence_backup_programmes"] == "— Non renseigné —":
            inp["frequence_backup_programmes"] = None

        test_rest = st.number_input(
            "Dernier test de restauration réussi (il y a combien de mois ?)",
            min_value=0,
            max_value=120,
            value=None,
            step=1,
            placeholder="— Jamais testé —",
            key="test_rest",
        )
        inp["dernier_test_restauration_mois"] = test_rest

        st.markdown("**IND-02 (vulnérabilité) — déjà saisi ci-dessus**")
        st.info("📝 L'indice de spaghetti technologique (IND-02) "
                "affecte à la fois la Maturité (bonus) et la Vulnérabilité (malus) "
                "selon le taux de documentation des interfaces.")

    # Retour de l'objet InnovatifInput
    return InnovatifInput(
        digital_twin_coverage_pct=inp.get("digital_twin_coverage_pct"),
        interfaces_documentees_pct=inp.get("interfaces_documentees_pct"),
        taux_faux_positifs_pct=inp.get("taux_faux_positifs_pct"),
        analyse_rcm_presente=inp.get("analyse_rcm_presente"),
        rcm_perimetre=inp.get("rcm_perimetre"),
        actionneurs_sans_validation_hw=inp.get("actionneurs_sans_validation_hw"),
        safety_relays_hw=inp.get("safety_relays_hw"),
        fournisseurs_multiples_pct=inp.get("fournisseurs_multiples_pct"),
        delai_appro_alternatif_j=inp.get("delai_appro_alternatif_j"),
        spc_actif=inp.get("spc_actif"),
        taux_hors_limites_pct=inp.get("taux_hors_limites_pct"),
        mttd_minutes=inp.get("mttd_minutes"),
        competences_uniques_nb=inp.get("competences_uniques_nb"),
        knowledge_management=inp.get("knowledge_management"),
        conformite_gammes_pct=inp.get("conformite_gammes_pct"),
        iso_50001=inp.get("iso_50001"),
        suivi_ipe=inp.get("suivi_ipe"),
        simulation_avant_deploiement_pct=inp.get("simulation_avant_deploiement_pct"),
        cyber_hygiene_score=inp.get("cyber_hygiene_score"),
        tests_regression_pct=inp.get("tests_regression_pct"),
        dependance_source_unique_pct=inp.get("dependance_source_unique_pct"),
        climatisation_armoires=inp.get("climatisation_armoires"),
        temp_ambiante_moy_c=inp.get("temp_ambiante_moy_c"),
        zones_independantes_nb=inp.get("zones_independantes_nb"),
        ca_maintenu_si_panne_zone_pct=inp.get("ca_maintenu_si_panne_zone_pct"),
        frequence_backup_programmes=inp.get("frequence_backup_programmes"),
        dernier_test_restauration_mois=inp.get("dernier_test_restauration_mois"),
        comportement_perte_comm=inp.get("comportement_perte_comm"),
        schemas_elec_age_ans=inp.get("schemas_elec_age_ans"),
        schemas_conformes_terrain=inp.get("schemas_conformes_terrain"),
    )
