"""
forms.py — Formulaires des 8 modules avec navigation par étapes
"""

import streamlit as st
from .theme import MODULE_COLORS, MODULE_ICONS, MODULE_LABELS


# ── HELPERS ───────────────────────────────────────────────────

def _bool_select(label: str, key: str, hint: str = "") -> str:
    help_txt = hint or None
    opts = ["—", "✅ Oui", "❌ Non"]
    val = st.selectbox(label, opts, key=key, help=help_txt)
    return "oui" if "Oui" in val else ("non" if "Non" in val else "")


def _section_header(title: str, module_key: str):
    color = MODULE_COLORS.get(module_key, "#3b82f6")
    icon  = MODULE_ICONS.get(module_key, "🔹")
    label = MODULE_LABELS.get(module_key, title)
    st.markdown(f"""
    <div style="
        display:flex; align-items:center; gap:10px;
        padding:12px 16px; background:{color}12;
        border-radius:10px; border:1px solid {color}30;
        margin: 8px 0 16px 0;
    ">
        <div style="font-size:22px;">{icon}</div>
        <div>
            <div style="font-size:14px; font-weight:800; color:#0f2244; font-family:'Sora',sans-serif;">{label}</div>
            <div style="font-size:10px; color:#64748b; font-family:'Sora',sans-serif;">{title}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _bloc_header(title: str, color: str = "#3b82f6"):
    st.markdown(f"""
    <div style="
        font-size:11px; font-weight:700; color:{color};
        text-transform:uppercase; letter-spacing:0.8px;
        border-bottom:1px solid {color}30; padding-bottom:4px;
        margin: 12px 0 10px 0; font-family:'Sora',sans-serif;
    ">{title}</div>
    """, unsafe_allow_html=True)


# ── ÉTAPE 0 : IDENTIFICATION ──────────────────────────────────

def form_identification():
    st.markdown("### 🏢 Identification du Client")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.text_input("Nom de l'entreprise *", key="entreprise", placeholder="AutoMaro SA")
    with c2:
        st.selectbox("Secteur d'activité *", [
            "—", "automobile", "aeronautique", "agroalimentaire",
            "chimie_pharma", "metalurgie", "electronique", "textile", "btp", "autre"
        ], key="secteur")
    with c3:
        st.text_input("Ville *", key="ville", placeholder="Casablanca")

    c4, c5 = st.columns(2)
    with c4:
        st.number_input("Effectif (personnes)", min_value=0, key="effectif")
    with c5:
        st.number_input("CA annuel (MAD)", min_value=0.0, key="ca_annuel_mad", format="%.0f")


# ── ÉTAPE 1 : ROBOTS INDUSTRIELS ─────────────────────────────

def form_robots():
    color = MODULE_COLORS["robots"]
    _section_header("Module 1 — Poids scoring : 18%", "robots")

    _bloc_header("Bloc 1 — Identification Technique", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.selectbox("Type de robot *", ["—","6 axes","5 axes","SCARA","Delta"], key="type_robot")
        _bool_select("Cobots présents *", "cobots")
    with c2:
        _bool_select("Cellules robotisées modulaires", "cellule_modulaire")
        st.text_input("Marque & Modèle", key="marque_modele", placeholder="FANUC R-2000iC")
    with c3:
        st.number_input("Année d'installation", min_value=1990, max_value=2026, value=2020, key="annee_install")
        st.selectbox("Intégration réseau *", ["—","Isolé","Connecté MES","Connecté Cloud"], key="integration_reseau")

    _bloc_header("Bloc 2 — Données Quantitatives", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.number_input("Nombre total robots *", min_value=0, key="nombre_robots")
        st.number_input("Valeur unitaire (MAD)", min_value=0.0, key="valeur_unitaire_mad", format="%.0f")
    with c2:
        st.number_input("Valeur totale parc (MAD)", min_value=0.0, key="valeur_totale_parc_mad", format="%.0f")
        st.number_input("Heures moy. fonctionnement / an", min_value=0.0, key="heures_fonct_an")
    with c3:
        st.number_input("MTBF (heures)", min_value=0.0, key="mtbf_robots", help="Mean Time Between Failures")
        st.number_input("MTTR (heures)", min_value=0.0, key="mttr_robots", help="Mean Time To Repair")

    _bloc_header("Bloc 3 — Variables de Scoring", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.selectbox("Niveau redondance *", ["—","Faible","Moyen","Élevé"], key="niveau_redondance")
        _bool_select("Contrat maintenance constructeur", "contrat_maintenance")
    with c2:
        _bool_select("Mise à jour firmware régulière", "maj_firmware")
        st.selectbox("Historique pannes 3 ans", ["—","0 panne","1-2 pannes","3-5 pannes","> 5 pannes"], key="historique_pannes")
    with c3:
        _bool_select("Capteurs prédictifs présents", "capteurs_predictifs")
        st.selectbox("Dépendance production *", ["—","Faible","Moyenne","Critique"], key="dependance_production")


# ── ÉTAPE 1 : CNC ─────────────────────────────────────────────

def form_cnc():
    color = MODULE_COLORS["cnc"]
    _section_header("Module 2 — Poids scoring : 14%", "cnc")

    _bloc_header("Bloc 1 — Identification CNC", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.selectbox("Type CNC *", ["—","3 axes","5 axes","Multi-broche"], key="type_cnc")
        st.text_input("Marque", key="marque_cnc", placeholder="DMG Mori")
    with c2:
        st.number_input("Année fabrication", min_value=1990, max_value=2026, value=2018, key="annee_cnc")
        st.selectbox("Automatisation *", ["—","Manuel","Semi-auto","Full auto"], key="automation_cnc")
    with c3:
        _bool_select("Interface MES / ERP", "interface_mes_erp")

    _bloc_header("Bloc 2 — Données Techniques", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.number_input("Nombre total CNC *", min_value=0, key="nombre_cnc")
        st.number_input("Valeur unitaire (MAD)", min_value=0.0, key="valeur_unit_cnc", format="%.0f")
    with c2:
        st.number_input("Heures fonctionnement cumulées", min_value=0.0, key="heures_cumul_cnc")
        st.selectbox("Type refroidissement", ["—","Air","Eau","Huile","Mixte"], key="type_refroid")
    with c3:
        _bool_select("Sensibilité électrique", "sensibilite_electrique")
        _bool_select("Variateurs de fréquence", "variateur_freq")

    _bloc_header("Bloc 3 — Indicateurs de Risque", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.selectbox("Fréquence maintenance préventive",
                     ["—","Mensuelle","Trimestrielle","Semestrielle","Annuelle","Aucune"],
                     key="freq_maintenance_prev")
        _bool_select("Maintenance prédictive", "maintenance_pred_cnc")
    with c2:
        st.selectbox("Historique dommage électrique",
                     ["—","Aucun","1-2 incidents","3+ incidents"],
                     key="historique_dom_elec")
        _bool_select("Protection surtension installée", "protection_surtension")
    with c3:
        _bool_select("Onduleur (UPS) dédié", "ups_dedie")


# ── ÉTAPE 2 : CPS ─────────────────────────────────────────────

def form_cps():
    color = MODULE_COLORS["cps"]
    _section_header("Module 3 — Poids scoring : 18%", "cps")

    _bloc_header("Bloc 1 — Architecture CPS", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        _bool_select("Présence SCADA *", "presence_scada")
        _bool_select("MES intégré", "mes_integre")
    with c2:
        _bool_select("ERP connecté production", "erp_connecte")
        _bool_select("Cloud externe", "cloud_externe")
    with c3:
        st.selectbox("Protocole industriel", ["—","OPC-UA","Modbus","Profinet","Autre"], key="protocole_industriel")
        st.selectbox("Segmentation réseau *", ["—","Faible","Moyenne","Élevée"], key="segmentation_reseau")

    _bloc_header("Bloc 2 — Infrastructure IT", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.selectbox("Type serveurs", ["—","Sur site","Cloud hybride","Cloud pur"], key="type_serveurs")
        _bool_select("Redondance serveurs *", "redondance_serveurs")
    with c2:
        _bool_select("Backup quotidien automatisé *", "backup_quotidien")
        st.number_input("RTO estimé (heures)", min_value=0.0, key="rto_heures", help="Recovery Time Objective")
    with c3:
        _bool_select("Pare-feu industriel *", "parefeu_industriel")
        _bool_select("Audit cybersécurité annuel *", "audit_cyber")

    _bloc_header("Bloc 3 — Indicateurs Assurantiels", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.selectbox("Dépendance production au CPS *", ["—","Faible","Moyen","Critique"], key="dependance_cps")
        st.selectbox("Historique incidents IT", ["—","Aucun","1-2/an","3+/an"], key="historique_incid_it")
    with c2:
        st.number_input("Temps moyen arrêt / incident IT (h)", min_value=0.0, key="temps_moy_arret_it_h")
        _bool_select("Plan de continuité (PCA) *", "plan_continuite")
    with c3:
        _bool_select("Simulation de crise annuelle", "simulation_crise")


# ── ÉTAPE 3 : ÉLECTRIQUE ──────────────────────────────────────

def form_electrique():
    color = MODULE_COLORS["electrique"]
    _section_header("Module 4 — Poids scoring : 10%", "electrique")

    _bloc_header("Bloc 1 — Équipements Électriques", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        _bool_select("Tableau BT/MT intelligent", "tableau_bt_mt")
        _bool_select("Protection différentiel avancée *", "protection_diff")
    with c2:
        _bool_select("Système monitoring énergétique", "monitoring_energie")
        _bool_select("UPS industriel *", "ups_industriel")
    with c3:
        _bool_select("Groupe électrogène", "groupe_electrogene")

    _bloc_header("Bloc 2 — Données Électriques", color)
    c1, c2 = st.columns(2)
    with c1:
        st.number_input("Puissance installée totale (kW)", min_value=0.0, key="puissance_installee_kw")
        st.number_input("Taux de charge moyen (%)", min_value=0.0, max_value=100.0, key="taux_charge_moyen_pct")
    with c2:
        st.selectbox("Incidents électriques / an *", ["—","0","1-2","3-5","> 5"], key="incidents_electriques")
        _bool_select("Mise à la terre conforme *", "mise_a_la_terre")

    _bloc_header("Bloc 3 — Impact Scoring", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.selectbox("Vulnérabilité dommage électrique", ["—","Faible","Modérée","Élevée"], key="vulnerabilite_dom_elec")
    with c2:
        _bool_select("Risque court-circuit évalué", "risque_court_circuit")
    with c3:
        st.selectbox("Risque propagation incendie", ["—","Faible","Modéré","Élevé"], key="risque_propag_incendie")


# ── ÉTAPE 3 : MAINTENANCE ─────────────────────────────────────

def form_maintenance():
    color = MODULE_COLORS["maintenance"]
    _section_header("Module 5 — Poids scoring : 20% (bloc central PFE)", "maintenance")

    _bloc_header("Bloc 1 — Organisation Maintenance", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        _bool_select("GMAO utilisée *", "gmao_utilisee")
    with c2:
        st.selectbox("Type maintenance dominant *", ["—","Corrective","Préventive","Prédictive"], key="type_maintenance")
    with c3:
        _bool_select("KPIs maintenance définis", "existence_kpi")

    _bloc_header("Bloc 2 — Indicateurs Quantifiables", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.number_input("MTBF global (heures)", min_value=0.0, key="mtbf_global", help="Mean Time Between Failures")
        st.number_input("MTTR global (heures)", min_value=0.0, key="mttr_global", help="Mean Time To Repair")
    with c2:
        st.number_input("Taux maintenance planifiée (%)", min_value=0.0, max_value=100.0, key="taux_maint_planifie_pct")
        st.number_input("Taux respect planning (%)", min_value=0.0, max_value=100.0, key="taux_respect_planning_pct")
    with c3:
        st.number_input("Budget maintenance / valeur parc (%)", min_value=0.0, key="budget_maintenance_pct_parc")

    _bloc_header("Bloc 3 — Maturité Maintenance", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.selectbox("Niveau digitalisation (1 à 5) *",
                     ["—","1","2","3","4","5"], key="niveau_digitalisation",
                     help="1=Papier 3=GMAO 5=IA prédictive")
    with c2:
        _bool_select("Maintenance conditionnelle capteurs", "maint_conditionnelle")
    with c3:
        _bool_select("IA prédictive utilisée", "ia_predictive")


# ── ÉTAPE 4 : MANUTENTION ─────────────────────────────────────

def form_manutention():
    color = MODULE_COLORS["manutention"]
    _section_header("Module 6 — Influence directe MTTR", "manutention")

    _bloc_header("Bloc 1 — Équipements de Manutention", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        _bool_select("AGV (véhicules autonomes)", "presence_agv")
        _bool_select("Chariots élévateurs", "chariots_elev")
        _bool_select("Ponts roulants", "ponts_roulants")
    with c2:
        _bool_select("Palans électriques", "palans_elec")
        _bool_select("Outillage spécialisé maintenance", "outillage_special")
        _bool_select("Atelier interne dédié", "atelier_interne")
    with c3:
        st.number_input("Nombre total équipements", min_value=0, key="nombre_equip_manu")
        st.number_input("Âge moyen (ans)", min_value=0.0, key="age_moyen_manu")
        st.number_input("Disponibilité (%)", min_value=0.0, max_value=100.0, key="disponibilite_manu_pct")

    _bloc_header("Bloc 2 — Variables Scoring Manutention", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        _bool_select("Manutention automatisée", "manutention_auto")
        st.number_input("Temps mobilisation moyen (min)", min_value=0.0, key="temps_mobilisation_min")
    with c2:
        _bool_select("Redondance équipements critiques", "redond_equip_crit")
    with c3:
        _bool_select("Disponibilité immédiate 24/7", "disponibilite_247")
        _bool_select("Dépendance prestataire externe", "dependance_prestataire")


# ── ÉTAPE 4 : STOCKAGE ────────────────────────────────────────

def form_stockage():
    color = MODULE_COLORS["stockage"]
    _section_header("Module 7 — Impact BDM & durée sinistre", "stockage")

    _bloc_header("Bloc 1 — Infrastructure de Stockage", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        _bool_select("Magasin central pièces", "magasin_central")
        _bool_select("Rayonnage intelligent", "rayonnage_intelligent")
    with c2:
        _bool_select("Stockage vertical automatisé", "stockage_vertical_auto")
        _bool_select("Zone pièces critiques dédiée", "zone_pieces_crit")
    with c3:
        _bool_select("Contrôle température/humidité", "controle_therm_humi")

    _bloc_header("Bloc 2 — Gestion Numérique Stock", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        _bool_select("Intégration ERP stock *", "integration_erp_stock")
        _bool_select("Stock minimum défini", "stock_minimum_defini")
    with c2:
        _bool_select("Analyse ABC des pièces", "analyse_abc")
        st.number_input("Délai réappro. fournisseur (jours)", min_value=0.0, key="delai_reappro_jours")
    with c3:
        st.selectbox("Taux rupture stock 12 mois *",
                     ["—","0%","< 5%","5-15%","> 15%"], key="taux_rupture_stock")
        _bool_select("Suivi consommation / demande réelle", "suivi_consommation")

    _bloc_header("Bloc 3 — Indicateurs de Performance", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.number_input("Temps moyen dispo pièce critique (h)", min_value=0.0, key="temps_moy_disp_piece_h")
        st.number_input("% pièces critiques en stock", min_value=0.0, max_value=100.0, key="pct_pieces_crit_stock")
    with c2:
        st.number_input("Taux rotation stock", min_value=0.0, key="taux_rotation_stock")
        st.number_input("Valeur stock / valeur parc (%)", min_value=0.0, key="valeur_stock_pct_parc")
    with c3:
        _bool_select("Prédiction conso via historique", "prediction_conso")

    _bloc_header("Bloc 4 — Variables Assurantielles", color)
    c1, c2, c3, c4 = st.columns(4)
    with c1: _bool_select("Pièces critiques redondantes *", "pieces_crit_redond")
    with c2: _bool_select("Fournisseurs multiples *", "fournisseurs_multiples")
    with c3: _bool_select("Contrat appro. prioritaire", "contrat_appro_prio")
    with c4: _bool_select("Simulation pénurie annuelle", "simulation_penurie")


# ── ÉTAPE 5 : INTERVENTION ────────────────────────────────────

def form_intervention():
    color = MODULE_COLORS["intervention"]
    _section_header("Module 8 — Maturité opérationnelle", "intervention")

    _bloc_header("Bloc 1 — Organisation Intervention", color)
    c1, c2, c3, c4 = st.columns(4)
    with c1: _bool_select("Équipe maintenance interne *", "equipe_interne")
    with c2: _bool_select("Techniciens certifiés constructeur", "techniciens_certif")
    with c3: _bool_select("Astreinte 24/7 *", "astreinte_247")
    with c4: st.number_input("SLA interne (heures)", min_value=0.0, key="sla_interne_h")

    _bloc_header("Bloc 2 — Indicateurs Quantifiés", color)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.number_input("MTTR moyen (heures)", min_value=0.0, key="mttr_moyen")
        st.number_input("% interventions < 4h", min_value=0.0, max_value=100.0, key="pct_interv_4h")
    with c2:
        st.number_input("% interventions planifiées", min_value=0.0, max_value=100.0, key="pct_interv_planif")
        st.number_input("Taux résolution 1er passage (%)", min_value=0.0, max_value=100.0, key="taux_resolution_pp")
    with c3:
        st.number_input("Arrêts > 24h (3 dernières années)", min_value=0, key="historique_arret_24h")

    _bloc_header("Bloc 3 — Digitalisation Intervention", color)
    c1, c2, c3, c4 = st.columns(4)
    with c1: _bool_select("GMAO mobile", "gmao_mobile")
    with c2: _bool_select("Traçabilité intervention temps réel", "tracabilite_rt")
    with c3: _bool_select("Historique pannes analysé", "historique_pannes_analyse")
    with c4: _bool_select("Dashboard KPI maintenance", "dashboard_kpi")


# ── STEPPER ───────────────────────────────────────────────────

STEPS = [
    {"label": "Identification & Robots",       "forms": [form_identification, form_robots]},
    {"label": "CNC & Système CPS",             "forms": [form_cnc, form_cps]},
    {"label": "Électrique & Maintenance",      "forms": [form_electrique, form_maintenance]},
    {"label": "Manutention & Stockage",        "forms": [form_manutention, form_stockage]},
    {"label": "Intervention & Résultats",      "forms": [form_intervention]},
]


def render_stepper(current_step: int):
    cols = st.columns(len(STEPS))
    for i, (col, step) in enumerate(zip(cols, STEPS)):
        with col:
            done = i < current_step
            active = i == current_step
            color = "#1d4ed8" if active else ("#10b981" if done else "#e2e8f0")
            text_c = "#fff" if (active or done) else "#94a3b8"
            border = f"box-shadow: 0 0 0 3px #3b82f680;" if active else ""
            st.markdown(f"""
            <div style="text-align:center;">
                <div style="width:28px; height:28px; border-radius:50%;
                    background:{color}; color:{text_c}; display:inline-flex;
                    align-items:center; justify-content:center;
                    font-size:12px; font-weight:800; {border}
                    font-family:'Sora',sans-serif;">{i+1}</div>
                <div style="font-size:9px; color:{'#1d4ed8' if active else '#64748b'};
                    font-weight:{'700' if active else '500'};
                    font-family:'Sora',sans-serif; margin-top:3px; line-height:1.2;">
                    {step['label']}
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_step_forms(step_idx: int):
    if step_idx < len(STEPS):
        for form_fn in STEPS[step_idx]["forms"]:
            form_fn()
            st.divider()
