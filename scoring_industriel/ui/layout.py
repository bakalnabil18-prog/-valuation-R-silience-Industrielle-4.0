"""
layout.py — Orchestrateur principal v2
Correction bug : résultats figés après calcul, non recalculés à chaque rerun.
"""

import streamlit as st
from .theme import inject_css, header_html, COLORS
from .forms import STEPS, render_stepper, render_step_forms
from .dashboard import (
    render_gauge, render_three_indices, render_module_traffic_lights,
    render_synthese, render_zones_critiques, render_recommandations, render_placeholder,
)
from .charts import radar_chart, indices_bar_chart, benchmark_chart


def init_session_state():
    """Initialise l'état de session Streamlit."""
    defaults = {
        "step": 0,
        "result": None,
        "calculated": False,
        # Snapshot des données au moment du calcul (figé)
        "_frozen_result": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def _render_matrice_calcul(result):
    """
    Matrice de calcul détaillée — explique chaque point du score.
    """
    st.markdown("### 🧮 Matrice de Calcul Détaillée")

    st.markdown("""
    <div style="background:#f0f4ff; border-radius:8px; padding:12px 16px; 
         margin-bottom:14px; border-left:4px solid #1d4ed8">
        <b style="color:#0f2244">Formule globale :</b>
        <code style="background:#1d4ed8; color:white; padding:2px 8px; border-radius:4px; margin-left:8px">
        Score = Maturité × 35% + Résilience × 45% + (100 − Vulnérabilité) × 20%
        </code>
    </div>
    """, unsafe_allow_html=True)

    sm  = result.score_maturite
    sr  = result.score_resilience
    sv  = result.score_vulnerabilite
    sg  = result.score_global

    contrib_a = round(sm * 0.35, 1)
    contrib_b = round(sr * 0.45, 1)
    contrib_c = round((100 - sv) * 0.20, 1)
    total_check = round(contrib_a + contrib_b + contrib_c, 1)

    # ── Tableau de contribution ──────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns([3, 1, 1, 2])
    with col1:
        st.markdown("**Indice**")
    with col2:
        st.markdown("**Score**")
    with col3:
        st.markdown("**Poids**")
    with col4:
        st.markdown("**Contribution**")
    st.markdown("---")

    rows = [
        ("⚙️ Maturité Mécatronique (A)", sm, "35%", contrib_a, "#3b82f6"),
        ("🛡️ Résilience Opérationnelle (B)", sr, "45%", contrib_b, "#10b981"),
        (f"🔎 Robustesse (100−{sv}) = {100-sv}", 100-sv, "20%", contrib_c, "#0891b2"),
    ]

    for label, score, poids, contrib, color in rows:
        c1, c2, c3, c4 = st.columns([3, 1, 1, 2])
        with c1:
            st.markdown(f"<span style='color:{color};font-weight:600'>{label}</span>",
                        unsafe_allow_html=True)
        with c2:
            st.markdown(f"**{score}**")
        with c3:
            st.markdown(poids)
        with c4:
            bar_pct = int(contrib / sg * 100) if sg > 0 else 0
            st.markdown(
                f"<div style='display:flex;align-items:center;gap:8px'>"
                f"<div style='background:#e2e8f0;border-radius:3px;width:80px;height:8px'>"
                f"<div style='background:{color};width:{bar_pct}%;height:100%;border-radius:3px'></div>"
                f"</div>"
                f"<b>+{contrib} pts</b></div>",
                unsafe_allow_html=True
            )

    st.markdown("---")
    st.markdown(
        f"<div style='text-align:right; font-size:16px; font-weight:800; color:#0f2244'>"
        f"= **{total_check} / 100** → Score final : <span style='color:#1d4ed8'>{sg}</span>"
        f"</div>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ── Détail Indice A — Maturité ────────────────────────────────────────────
    with st.expander("⚙️ Détail Indice A — Maturité Mécatronique", expanded=False):
        st.markdown("""
        **Formule :** Moyenne pondérée de 6 composantes

        | Composante | Poids | Score estimé |
        |---|---|---|
        | Robots (intégration, capteurs, redondance) | 28% | ⟶ via `score_robots()` |
        | CNC (automation, UPS, prédictif) | 18% | ⟶ via `score_cnc()` |
        | CPS/SCADA (architecture, cyber, segmentation) | 22% | ⟶ via `score_cps_maturite()` |
        | Manutention (AGV, automation, disponibilité) | 10% | ⟶ via `score_manutention_maturite()` |
        | Maintenance (digitalisation, IA, GMAO) | 12% | ⟶ via `score_maintenance_maturite()` |
        | Stockage (ERP, ABC, prédiction) | 10% | ⟶ via `score_stockage_maturite()` |

        **Variables clés qui font monter le score :**
        - Robots connectés Cloud → **+25 pts**
        - Capteurs prédictifs actifs → **+20 pts**
        - SCADA présent → **+15 pts**
        - AGV présent → **+22 pts**
        - IA prédictive maintenance → **+25 pts**
        - CNC full auto → **+28 pts**
        """)

    # ── Détail Indice B — Résilience ──────────────────────────────────────────
    with st.expander("🛡️ Détail Indice B — Résilience Opérationnelle", expanded=False):
        st.markdown("""
        **Formule :** Moyenne pondérée de 6 composantes

        | Composante | Poids | Variables principales |
        |---|---|---|
        | Organisation maintenance | 20% | GMAO, type maintenance, KPIs |
        | KPIs maintenance (MTBF/MTTR) | 18% | MTBF ≥3000h, MTTR <2h |
        | Maturité maintenance | 17% | Niveau digitalisation, IA, conditionnel |
        | Stockage pièces de rechange | 20% | Redondance, fournisseurs, taux rupture |
        | Efficacité intervention | 15% | Astreinte 24/7, SLA, GMAO mobile |
        | Redondance systèmes | 10% | Robots, serveurs, PCA |

        **Variables clés qui font monter le score :**
        - Maintenance prédictive → **+30 pts** (organisation)
        - MTBF ≥ 3000h → **+15 pts**
        - MTTR < 2h → **+12 pts**
        - Pièces redondantes en stock → **+22 pts**
        - Astreinte 24/7 → **+18 pts**
        - PCA documenté → **+25 pts** (redondance)
        """)

    # ── Détail Indice C — Vulnérabilité ──────────────────────────────────────
    with st.expander("🔎 Détail Indice C — Vulnérabilité Systémique (score inversé)", expanded=False):
        st.markdown("""
        **⚠️ Score INVERSÉ** : plus il est élevé, plus l'entreprise est vulnérable.
        Dans la formule finale : contribution = **(100 − C) × 20%**

        | Composante | Poids | Ce qui fait monter la vulnérabilité |
        |---|---|---|
        | Dépendance CPS/Robots | 30% | Dépendance critique + absence PCA |
        | Fragilité infrastructure IT | 28% | Pas de redondance serveurs, pas de backup, pas de pare-feu |
        | Fragilité électrique | 22% | Pas d'UPS, terre déficiente, incidents fréquents |
        | Absence de redondance | 20% | Réseau non segmenté, fournisseur unique, ruptures >15% |

        **Variables clés qui font monter la vulnérabilité (malus) :**
        - Dépendance CPS critique → **+22 pts**
        - Absence redondance serveurs → **+15 pts**
        - Pas de backup quotidien → **+10 pts**
        - Pas de pare-feu industriel → **+10 pts**
        - Réseau non segmenté (Faible) → **+12 pts**
        - Robots sans redondance → **+15 pts**
        """)

    # ── Scores par module (radar) ─────────────────────────────────────────────
    with st.expander("📡 Scores des 8 modules (radar)", expanded=False):
        ms = result.module_scores
        module_data = {
            "🤖 Robots":        ms.robots,
            "⚙️ CNC":           ms.cnc,
            "🌐 CPS/SCADA":     ms.cps,
            "⚡ Électrique":    ms.electrique,
            "🔧 Maintenance":   ms.maintenance,
            "🏗️ Manutention":   ms.manutention,
            "📦 Stockage":      ms.stockage,
            "🚨 Intervention":  ms.intervention,
        }

        for label, score in module_data.items():
            color = "#10b981" if score >= 70 else ("#f59e0b" if score >= 40 else "#ef4444")
            emoji = "🟢" if score >= 70 else ("🟡" if score >= 40 else "🔴")
            pct = score
            st.markdown(
                f"<div style='display:flex;align-items:center;gap:10px;margin-bottom:6px'>"
                f"<span style='width:140px;font-size:13px'>{label}</span>"
                f"<div style='flex:1;background:#e2e8f0;border-radius:4px;height:10px'>"
                f"<div style='background:{color};width:{pct}%;height:100%;border-radius:4px'></div>"
                f"</div>"
                f"<span style='width:50px;text-align:right;font-weight:700;color:{color}'>{score}</span>"
                f"<span>{emoji}</span>"
                f"</div>",
                unsafe_allow_html=True
            )


def render_app():
    """Point d'entrée principal de l'interface."""
    from engine.normaliser import normalise_form
    from engine.pipeline import ScoringPipeline

    init_session_state()
    inject_css()

    # ── HEADER ───────────────────────────────────────────────────────────────
    st.markdown(header_html(
        "Évaluation Résilience Industrielle 4.0",
        "8 modules · 3 indices · 4 outputs · Mécatronique × Maintenance × IARD"
    ), unsafe_allow_html=True)

    col_form, col_dash = st.columns([6, 4], gap="large")

    with col_form:
        with st.container():
            st.markdown("""
            <div style="background:white; border-radius:12px;
                border:1px solid #e2e8f0; padding:14px 18px; margin-bottom:14px;">
                <div style="font-size:13px; font-weight:700; color:#0f2244;
                    font-family:'Sora',sans-serif; margin-bottom:10px;">
                    Formulaire d'Analyse — Scoring Industriel 4.0
                </div>
            """, unsafe_allow_html=True)
            render_stepper(st.session_state.step)
            st.markdown("</div>", unsafe_allow_html=True)

        with st.container():
            render_step_forms(st.session_state.step)

        nav_cols = st.columns([1, 2, 1])
        with nav_cols[0]:
            if st.session_state.step > 0:
                if st.button("← Précédent", use_container_width=True):
                    st.session_state.step -= 1
                    st.rerun()

        with nav_cols[1]:
            st.markdown(
                f"<div style='text-align:center; font-size:11px; color:#64748b; "
                f"padding-top:8px; font-family:Sora,sans-serif;'>"
                f"Étape {st.session_state.step + 1} / {len(STEPS)}</div>",
                unsafe_allow_html=True
            )

        with nav_cols[2]:
            if st.session_state.step < len(STEPS) - 1:
                if st.button("Suivant →", use_container_width=True):
                    st.session_state.step += 1
                    st.rerun()
            else:
                if st.button("✅ Valider et Calculer", use_container_width=True):
                    # ══ CORRECTION BUG : snapshot figé au moment du clic ══
                    # On capture l'état courant dans un dict séparé
                    snapshot = {
                        k: v for k, v in st.session_state.items()
                        if not k.startswith("_") and k not in ("step", "result", "calculated")
                    }
                    data = normalise_form(snapshot)
                    pipeline = ScoringPipeline()
                    # Stocker le résultat dans _frozen_result (jamais retouché ensuite)
                    st.session_state._frozen_result = pipeline.run(data)
                    st.session_state.result = st.session_state._frozen_result
                    st.session_state.calculated = True
                    st.rerun()

        # Bouton Reset
        if st.session_state.calculated:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 Nouveau calcul", use_container_width=True):
                st.session_state.result = None
                st.session_state._frozen_result = None
                st.session_state.calculated = False
                st.session_state.step = 0
                st.rerun()

    # ── DASHBOARD DROIT ──────────────────────────────────────────────────────
    with col_dash:
        st.markdown("""
        <div style="font-size:13px; font-weight:700; color:#0f2244;
            font-family:'Sora',sans-serif; margin-bottom:10px;
            display:flex; justify-content:space-between; align-items:center;">
            <span>Résultats en Temps Réel</span>
            <span style="font-size:14px;">🌐 ℹ️</span>
        </div>
        """, unsafe_allow_html=True)

        # ══ CORRECTION : lire depuis _frozen_result, jamais recalculé ══
        result = st.session_state.get("_frozen_result", None)

        if result:
            render_gauge(result.score_global)

            render_three_indices(
                result.score_maturite,
                result.score_resilience,
                result.score_vulnerabilite,
            )

            st.divider()

            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📡 Radar", "📊 Barres", "🗺️ Zones", "✅ Recs", "🧮 Matrice"
            ])

            with tab1:
                module_dict = {
                    "robots":       result.module_scores.robots,
                    "cnc":          result.module_scores.cnc,
                    "cps":          result.module_scores.cps,
                    "electrique":   result.module_scores.electrique,
                    "maintenance":  result.module_scores.maintenance,
                    "manutention":  result.module_scores.manutention,
                    "stockage":     result.module_scores.stockage,
                    "intervention": result.module_scores.intervention,
                }
                fig = radar_chart(module_dict)
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                render_module_traffic_lights(module_dict)

            with tab2:
                fig2 = indices_bar_chart(
                    result.score_maturite,
                    result.score_resilience,
                    result.score_vulnerabilite,
                )
                st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

                if result.benchmark_secteur:
                    fig3 = benchmark_chart(result.benchmark_secteur)
                    if fig3:
                        st.markdown("**Comparaison sectorielle**")
                        st.plotly_chart(fig3, use_container_width=True,
                                        config={"displayModeBar": False})

            with tab3:
                render_synthese(result.synthese, result.score_global)
                render_zones_critiques(result.zones_critiques)

                if result.facteurs_aggravants:
                    st.markdown("**⚠️ Facteurs Aggravants**")
                    for fa in result.facteurs_aggravants:
                        st.markdown(f"""
                        <div style="background:#fff7ed; border-left:3px solid #f59e0b;
                            border-radius:4px; padding:6px 10px; margin-bottom:4px;
                            font-size:10px; color:#374151;">
                            ⚠️ {fa}
                        </div>
                        """, unsafe_allow_html=True)

            with tab4:
                render_recommandations(result.recommandations)

            with tab5:
                _render_matrice_calcul(result)

        else:
            render_placeholder()
