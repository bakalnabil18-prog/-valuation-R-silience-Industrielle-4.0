"""
layout.py — Orchestrateur principal de l'interface Streamlit
Structure : Header + [Formulaire gauche | Dashboard droit]
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
    if "step" not in st.session_state:
        st.session_state.step = 0
    if "result" not in st.session_state:
        st.session_state.result = None
    if "calculated" not in st.session_state:
        st.session_state.calculated = False


def render_app():
    """Point d'entrée principal de l'interface."""
    from engine.normaliser import normalise_form
    from engine.pipeline import ScoringPipeline

    init_session_state()
    inject_css()

    # ── HEADER ───────────────────────────────────────────────
    st.markdown(header_html(
        "Évaluation Résilience Industrielle 4.0",
        "8 modules · 3 indices · 4 outputs · Mécatronique × Maintenance × IARD"
    ), unsafe_allow_html=True)

    # ── LAYOUT PRINCIPAL ─────────────────────────────────────
    col_form, col_dash = st.columns([6, 4], gap="large")

    with col_form:
        # Stepper
        with st.container():
            st.markdown("""
            <div style="background:white; border-radius:12px;
                border:1px solid #e2e8f0; padding:14px 18px; margin-bottom:14px;">
                <div style="font-size:13px; font-weight:700; color:#0f2244;
                    font-family:'Sora',sans-serif; margin-bottom:10px;">
                    Formulaire d'Analyse — Scoring Industriel 4.0 — Nouveau Scoring
                </div>
            """, unsafe_allow_html=True)
            render_stepper(st.session_state.step)
            st.markdown("</div>", unsafe_allow_html=True)

        # Formulaire
        with st.container():
            render_step_forms(st.session_state.step)

        # Navigation
        nav_cols = st.columns([1, 2, 1])
        with nav_cols[0]:
            if st.session_state.step > 0:
                if st.button("← Précédent", use_container_width=True):
                    st.session_state.step -= 1
                    st.rerun()

        with nav_cols[1]:
            st.markdown(f"""
            <div style="text-align:center; font-size:11px; color:#64748b;
                padding-top:8px; font-family:'Sora',sans-serif;">
                Étape {st.session_state.step + 1} / {len(STEPS)}
            </div>
            """, unsafe_allow_html=True)

        with nav_cols[2]:
            if st.session_state.step < len(STEPS) - 1:
                if st.button("Suivant →", use_container_width=True):
                    st.session_state.step += 1
                    st.rerun()
            else:
                if st.button("✅ Valider et Calculer", use_container_width=True):
                    data = normalise_form(dict(st.session_state))
                    pipeline = ScoringPipeline()
                    st.session_state.result = pipeline.run(data)
                    st.session_state.calculated = True
                    st.rerun()

    # ── DASHBOARD DROIT ──────────────────────────────────────
    with col_dash:
        with st.container():
            st.markdown("""
            <div style="font-size:13px; font-weight:700; color:#0f2244;
                font-family:'Sora',sans-serif; margin-bottom:10px;
                display:flex; justify-content:space-between; align-items:center;">
                <span>Résultats en Temps Réel</span>
                <span style="font-size:14px; cursor:pointer;">🌐 ℹ️</span>
            </div>
            """, unsafe_allow_html=True)

            result = st.session_state.result

            if result:
                # Gauge
                render_gauge(result.score_global)

                # 3 indices
                render_three_indices(
                    result.score_maturite,
                    result.score_resilience,
                    result.score_vulnerabilite,
                )

                st.divider()

                # Tabs de navigation
                tab1, tab2, tab3, tab4 = st.tabs(["📡 Radar", "📊 Barres", "🗺️ Zones", "✅ Recs"])

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
                            st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

                with tab3:
                    render_synthese(result.synthese, result.score_global)
                    render_zones_critiques(result.zones_critiques)

                    if result.facteurs_aggravants:
                        st.markdown("**⚠️ Facteurs Aggravants**")
                        for fa in result.facteurs_aggravants:
                            st.markdown(f"""
                            <div style="background:#fff7ed; border-left:3px solid #f59e0b;
                                border-radius:4px; padding:6px 10px; margin-bottom:4px;
                                font-size:10px; color:#374151; font-family:'Sora',sans-serif;">
                                ⚠️ {fa}
                            </div>
                            """, unsafe_allow_html=True)

                with tab4:
                    render_recommandations(result.recommandations)

            else:
                render_placeholder()
