"""
dashboard.py — Panneau de résultats en temps réel
Affiche : Jauge + 3 indices + Radar + Feux tricolores + Zones critiques + Recommandations
"""

import streamlit as st
from .theme import MODULE_COLORS, MODULE_ICONS, MODULE_LABELS, traffic_light, score_color, COLORS
from .charts import gauge_chart, radar_chart, module_bar_chart, indices_bar_chart, benchmark_chart


def render_gauge(score: int):
    """Jauge score final."""
    from .charts import gauge_chart
    fig = gauge_chart(score)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_three_indices(maturite: int, resilience: int, vulnerabilite: int):
    """Affiche les 3 indices en cartes côte à côte."""
    c1, c2, c3 = st.columns(3)

    def _card(col, score, icon, label, sublabel, color):
        with col:
            st.markdown(f"""
            <div style="
                background:{color}12; border:1px solid {color}30;
                border-radius:10px; padding:12px; text-align:center;
            ">
                <div style="font-size:20px;">{icon}</div>
                <div style="font-size:24px; font-weight:800; color:{color};
                    font-family:'Sora',sans-serif; line-height:1;">{score}</div>
                <div style="font-size:9px; color:#64748b; font-weight:600;
                    font-family:'Sora',sans-serif; margin-top:3px; line-height:1.3;">{label}</div>
                <div style="font-size:8px; color:{color}; font-weight:700;
                    font-family:'Sora',sans-serif; margin-top:2px;">{sublabel}</div>
            </div>
            """, unsafe_allow_html=True)

    _card(c1, maturite,     "⚙️",  "Maturité\nMécatronique",      "Auto + CPS + Capteurs",    COLORS["blue_light"])
    _card(c2, resilience,   "🛡️",  "Résilience\nOpérationnelle",  "Maint + Stock + Interv.",  COLORS["green"])
    _card(c3, 100-vulnerabilite, "🔎", "Robustesse\nSystémique",   "↑ = Moins vulnérable",     COLORS["amber"])


def render_module_traffic_lights(module_scores: dict):
    """Feux tricolores par module."""
    st.markdown("""
    <div style="font-size:12px; font-weight:700; color:#0f2244;
        font-family:'Sora',sans-serif; margin: 12px 0 8px 0;">
        Feu Tricolore — 8 Modules
    </div>
    """, unsafe_allow_html=True)

    for key, score in module_scores.items():
        tl = traffic_light(score)
        icon  = MODULE_ICONS.get(key, "🔹")
        label = MODULE_LABELS.get(key, key)
        color = MODULE_COLORS.get(key, "#3b82f6")

        st.markdown(f"""
        <div style="
            display:flex; align-items:center; justify-content:space-between;
            padding: 6px 10px; background:#f8fafc; border-radius:7px;
            margin-bottom:5px; border-left: 3px solid {color};
        ">
            <span style="font-size:11px; color:#1e293b;
                font-family:'Sora',sans-serif; font-weight:500;">
                {icon} {label}
            </span>
            <div style="display:flex; align-items:center; gap:5px;">
                <span style="font-size:11px; font-weight:800;
                    color:{tl['color']}; font-family:'Sora',sans-serif;">{score}</span>
                <span style="font-size:9px; color:{tl['color']}; font-weight:700;
                    background:{tl['color']}20; border-radius:4px;
                    padding:1px 6px;">{tl['label']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_synthese(synthese: dict, score_global: int):
    """Synthèse souscripteur."""
    st.markdown("""
    <div style="
        background:#eff6ff; border-radius:10px; padding:14px;
        border:1px solid #bfdbfe; margin-top:12px;
    ">
        <div style="font-size:10px; font-weight:800; color:#1d4ed8;
            text-transform:uppercase; letter-spacing:1px;
            margin-bottom:8px; font-family:'Sora',sans-serif;">
            Synthèse Souscripteur
        </div>
    """, unsafe_allow_html=True)

    grid_items = [
        ("Profil industriel",      synthese.get("profil_industriel", "—")),
        ("Intégration digitale",   synthese.get("integration_digitale", "—")),
        ("Résilience maintenance", synthese.get("resilience_maintenance", "—")),
        ("Vulnérabilité IT/Cyber", synthese.get("vulnerabilite_it", "—")),
    ]

    cols = st.columns(2)
    for i, (label, val) in enumerate(grid_items):
        with cols[i % 2]:
            st.markdown(f"""
            <div style="background:white; border-radius:6px; padding:7px 10px;
                border:1px solid #dbeafe; margin-bottom:5px;">
                <div style="font-size:9px; color:#64748b; font-weight:600;
                    font-family:'Sora',sans-serif;">{label}</div>
                <div style="font-size:12px; color:#1d4ed8; font-weight:700;
                    font-family:'Sora',sans-serif;">{val}</div>
            </div>
            """, unsafe_allow_html=True)

    if synthese.get("narrative"):
        st.markdown(f"""
        <div style="font-size:11px; color:#374151; line-height:1.6;
            margin-top:8px; font-family:'Sora',sans-serif;">
            {synthese['narrative']}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def render_zones_critiques(zones: list):
    """Carte des points sensibles."""
    if not zones:
        return

    st.markdown("""
    <div style="font-size:12px; font-weight:700; color:#dc2626;
        font-family:'Sora',sans-serif; margin: 12px 0 8px 0;">
        🗺️ Carte des Points Sensibles
    </div>
    """, unsafe_allow_html=True)

    for i, zone in enumerate(zones[:6], 1):
        is_crit = zone.niveau == "critique"
        border_c = "#ef4444" if is_crit else "#f59e0b"
        bg_c     = "#fef2f2" if is_crit else "#fffbeb"
        lvl_lbl  = "CRITIQUE" if is_crit else "MAJEURE"

        st.markdown(f"""
        <div style="
            border-left:3px solid {border_c}; background:{bg_c};
            border-radius:5px; padding:8px 12px; margin-bottom:6px;
        ">
            <div style="font-size:10px; font-weight:800; color:{border_c};
                font-family:'Sora',sans-serif;">
                Zone {i} — {lvl_lbl} ({zone.module})
            </div>
            <div style="font-size:10px; color:#374151; margin-top:2px;
                font-family:'Sora',sans-serif; line-height:1.4;">{zone.description}</div>
            {f'<div style="font-size:9px; color:#64748b; margin-top:2px; font-style:italic;">→ {zone.impact}</div>' if zone.impact else ''}
        </div>
        """, unsafe_allow_html=True)


def render_recommandations(recommandations: list):
    """Recommandations priorisées."""
    if not recommandations:
        return

    st.markdown("""
    <div style="font-size:12px; font-weight:700; color:#0f2244;
        font-family:'Sora',sans-serif; margin: 12px 0 8px 0;">
        Recommandations
    </div>
    """, unsafe_allow_html=True)

    colors_map = {
        "Urgente":     ("#ef4444", "#fef2f2"),
        "Prioritaire": ("#f59e0b", "#fffbeb"),
        "Recommandée": ("#10b981", "#f0fdf4"),
    }

    for rec in recommandations:
        c, bg = colors_map.get(rec.priorite, ("#3b82f6", "#eff6ff"))
        st.markdown(f"""
        <div style="border-left:3px solid {c}; background:{bg};
            border-radius:5px; padding:8px 12px; margin-bottom:6px;
            display:flex; gap:8px; align-items:flex-start;">
            <span style="font-size:8px; font-weight:800; padding:2px 6px;
                border-radius:4px; background:{c}25; color:{c};
                white-space:nowrap; margin-top:1px;
                font-family:'Sora',sans-serif;">{rec.priorite}</span>
            <span style="font-size:10px; color:#374151; line-height:1.5;
                font-family:'Sora',sans-serif;">{rec.action}</span>
        </div>
        """, unsafe_allow_html=True)


def render_placeholder():
    """Placeholder quand aucun calcul n'a été fait."""
    st.markdown("""
    <div style="
        padding:30px 20px; background:#f8fafc; border-radius:10px;
        text-align:center; margin-top:20px;
    ">
        <div style="font-size:40px; margin-bottom:10px;">📊</div>
        <div style="font-size:12px; color:#64748b; line-height:1.6;
            font-family:'Sora',sans-serif;">
            Remplissez les 5 étapes du formulaire<br>
            puis cliquez sur <strong style="color:#1d4ed8;">Valider et Calculer</strong><br>
            pour générer l'analyse complète.
        </div>
    </div>
    """, unsafe_allow_html=True)
