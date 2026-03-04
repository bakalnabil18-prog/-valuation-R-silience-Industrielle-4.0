"""
dashboard_innovant.py
══════════════════════════════════════════════════════════════════
Panneau de résultats pour les 20 indicateurs innovants.
Affiche dans le dashboard : impact sur les 3 indices,
tableau des 20 indicateurs avec feux tricolores, top risques.
══════════════════════════════════════════════════════════════════
"""

import streamlit as st
from ..engine.scoring_innovant import InnovatifScores, get_innovant_summary, get_top_innovant_risks


def _badge(text, color, bg):
    return (
        f'<span style="background:{bg}; color:{color}; padding:3px 10px; '
        f'border-radius:12px; font-size:12px; font-weight:600">{text}</span>'
    )


def render_innovant_impact(innovant: InnovatifScores):
    """
    Carte synthèse : impact des 20 indicateurs sur les 3 indices.
    """
    st.markdown("### 🔬 Impact des Indicateurs Innovants")

    col1, col2, col3 = st.columns(3)

    with col1:
        bonus_a = innovant.score_maturite_bonus
        color = "#10b981" if bonus_a > 0 else ("#ef4444" if bonus_a < 0 else "#6b7280")
        sign = "+" if bonus_a >= 0 else ""
        st.markdown(f"""
        <div style="background:#eff6ff; border-radius:10px; padding:14px; text-align:center; border:1px solid #bfdbfe">
            <div style="font-size:11px; color:#3b82f6; font-weight:700; text-transform:uppercase; letter-spacing:1px">
                Indice A — Maturité
            </div>
            <div style="font-size:28px; font-weight:800; color:{color}; margin:6px 0">
                {sign}{bonus_a} pts
            </div>
            <div style="font-size:11px; color:#555">
                Bonus/malus sur l'Indice A de base
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        bonus_b = innovant.score_resilience_bonus
        color = "#10b981" if bonus_b > 0 else ("#ef4444" if bonus_b < 0 else "#6b7280")
        sign = "+" if bonus_b >= 0 else ""
        st.markdown(f"""
        <div style="background:#ecfdf5; border-radius:10px; padding:14px; text-align:center; border:1px solid #a7f3d0">
            <div style="font-size:11px; color:#059669; font-weight:700; text-transform:uppercase; letter-spacing:1px">
                Indice B — Résilience
            </div>
            <div style="font-size:28px; font-weight:800; color:{color}; margin:6px 0">
                {sign}{bonus_b} pts
            </div>
            <div style="font-size:11px; color:#555">
                Bonus/malus sur l'Indice B de base
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        bonus_c = innovant.score_vulnerabilite_bonus
        color = "#ef4444" if bonus_c > 5 else ("#f59e0b" if bonus_c > 0 else "#10b981")
        sign = "+" if bonus_c > 0 else ""
        st.markdown(f"""
        <div style="background:#fef2f2; border-radius:10px; padding:14px; text-align:center; border:1px solid #fecaca">
            <div style="font-size:11px; color:#dc2626; font-weight:700; text-transform:uppercase; letter-spacing:1px">
                Indice C — Vulnérabilité
            </div>
            <div style="font-size:28px; font-weight:800; color:{color}; margin:6px 0">
                {sign}{bonus_c} pts
            </div>
            <div style="font-size:11px; color:#555">
                Malus additionnel sur l'Indice C
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_innovant_table(innovant: InnovatifScores):
    """
    Tableau des 20 indicateurs avec score, indice et label.
    """
    st.markdown("### 📋 Détail des 20 Indicateurs Innovants")

    items = get_innovant_summary(innovant)

    if not items:
        st.info("Aucun indicateur innovant renseigné.")
        return

    # Grouper par indice
    for indice_label, indice_key, bg in [
        ("⚙️ Indice A — Maturité Mécatronique", "A", "#eff6ff"),
        ("🛡️ Indice B — Résilience Opérationnelle", "B", "#ecfdf5"),
        ("🔎 Indice C — Vulnérabilité Systémique", "C", "#fef2f2"),
    ]:
        group = [i for i in items if i["indice"] == indice_key
                 or (i["indice"] == "A+C" and indice_key == "A")]
        if not group:
            continue

        st.markdown(f"""
        <div style="background:{bg}; border-radius:8px; padding:8px 14px;
             margin:14px 0 6px 0; font-weight:700; font-size:14px">
            {indice_label}
        </div>
        """, unsafe_allow_html=True)

        for item in group:
            score = item["score"]
            max_s = item["max"]
            pct = int(score / max_s * 100) if max_s > 0 else 0
            impact = item["impact"]
            nom = item["indicateur"]
            label = item["label"]

            # Couleur barre de progression
            if indice_key == "C":
                bar_color = "#ef4444" if pct > 60 else ("#f59e0b" if pct > 30 else "#10b981")
            else:
                bar_color = "#10b981" if pct > 60 else ("#f59e0b" if pct > 30 else "#ef4444")

            st.markdown(f"""
            <div style="background:white; border-radius:6px; padding:10px 14px;
                 margin-bottom:6px; border:1px solid #e2e8f0">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px">
                    <span style="font-size:13px; font-weight:600; color:#1e293b">
                        {nom.split(" — ")[0]}
                        <span style="font-weight:400; color:#64748b"> — {nom.split(" — ", 1)[-1]}</span>
                    </span>
                    <span style="font-size:12px; margin-left:12px; white-space:nowrap">
                        {impact}
                        <span style="color:#475569; margin-left:8px">
                            {score}/{max_s}
                        </span>
                    </span>
                </div>
                <div style="background:#f1f5f9; border-radius:3px; height:5px; overflow:hidden">
                    <div style="background:{bar_color}; width:{pct}%; height:100%; border-radius:3px"></div>
                </div>
                <div style="font-size:11px; color:#64748b; margin-top:4px">{label}</div>
            </div>
            """, unsafe_allow_html=True)


def render_innovant_top_risks(innovant: InnovatifScores):
    """
    Top 5 signaux d'alerte issus des indicateurs innovants.
    Pour la fiche souscripteur.
    """
    risks = get_top_innovant_risks(innovant, n=5)
    if not risks:
        st.success("✅ Aucun signal d'alerte majeur détecté sur les indicateurs innovants.")
        return

    st.markdown("### ⚠️ Signaux d'Alerte — Indicateurs Innovants")
    st.markdown(
        '<p style="font-size:12px; color:#64748b; margin-top:-8px">'
        'Points d\'attention spécifiques aux usines Industry 4.0 — '
        'non couverts par les questionnaires classiques</p>',
        unsafe_allow_html=True
    )

    for r in risks:
        nom = r["indicateur"]
        label = r["label"]
        indice = r["indice"]
        score = r["score"]
        max_s = r["max"]

        border = "#ef4444" if indice == "C" and score >= max_s * 0.6 else "#f59e0b"
        icon = "🔴" if border == "#ef4444" else "🟡"
        indice_badge_color = {
            "A": "#3b82f6", "B": "#10b981", "C": "#ef4444", "A+C": "#8b5cf6"
        }.get(indice, "#6b7280")

        st.markdown(f"""
        <div style="background:white; border-left:4px solid {border}; border-radius:6px;
             padding:12px 16px; margin-bottom:8px; box-shadow:0 1px 3px rgba(0,0,0,.06)">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px">
                <span style="font-size:14px">{icon}</span>
                <span style="font-weight:700; font-size:13px; color:#1e293b">{nom}</span>
                <span style="background:{indice_badge_color}; color:white; padding:1px 8px;
                    border-radius:10px; font-size:11px; font-weight:600">
                    Indice {indice}
                </span>
            </div>
            <div style="font-size:12px; color:#475569">{label}</div>
            <div style="font-size:11px; color:#94a3b8; margin-top:3px">
                Score : {score}/{max_s}
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_innovant_score_comparison(
    base_global: int,
    final_global: int,
    base_maturite: int,
    final_maturite: int,
    base_resilience: int,
    final_resilience: int,
    base_vulnerabilite: int,
    final_vulnerabilite: int,
):
    """
    Comparaison avant/après intégration des indicateurs innovants.
    """
    st.markdown("### 📊 Impact sur le Score Global")

    delta = final_global - base_global
    color = "#10b981" if delta > 0 else ("#ef4444" if delta < 0 else "#6b7280")
    sign = "+" if delta >= 0 else ""

    st.markdown(f"""
    <div style="background:linear-gradient(135deg, #0f2244, #1d4ed8);
         border-radius:12px; padding:20px; text-align:center; margin-bottom:14px">
        <div style="color:#93c5fd; font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:1px">
            Score Global avec indicateurs innovants
        </div>
        <div style="display:flex; justify-content:center; align-items:center; gap:20px; margin-top:10px">
            <div style="text-align:center">
                <div style="color:#94a3b8; font-size:11px">Base</div>
                <div style="color:white; font-size:32px; font-weight:800">{base_global}</div>
            </div>
            <div style="color:#60a5fa; font-size:24px">→</div>
            <div style="text-align:center">
                <div style="color:#93c5fd; font-size:11px">Final</div>
                <div style="color:white; font-size:40px; font-weight:900">{final_global}</div>
            </div>
            <div style="text-align:center">
                <div style="color:#94a3b8; font-size:11px">Variation</div>
                <div style="color:{color}; font-size:28px; font-weight:800">{sign}{delta}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tableau comparatif par indice
    rows = [
        ("⚙️ Maturité (A)", base_maturite, final_maturite),
        ("🛡️ Résilience (B)", base_resilience, final_resilience),
        ("🔎 Vulnérabilité (C)", base_vulnerabilite, final_vulnerabilite),
    ]

    cols = st.columns(3)
    for idx, (label, base_val, final_val) in enumerate(rows):
        d = final_val - base_val
        dc = "#10b981" if (d > 0 and idx < 2) or (d < 0 and idx == 2) else (
             "#ef4444" if d != 0 else "#6b7280")
        ds = "+" if d >= 0 else ""
        with cols[idx]:
            st.markdown(f"""
            <div style="background:#f8fafc; border-radius:8px; padding:12px; text-align:center;
                 border:1px solid #e2e8f0">
                <div style="font-size:12px; color:#64748b; font-weight:600">{label}</div>
                <div style="font-size:11px; color:#94a3b8; margin:4px 0">
                    {base_val} → <strong style="color:#1e293b">{final_val}</strong>
                </div>
                <div style="font-size:18px; font-weight:800; color:{dc}">{ds}{d}</div>
            </div>
            """, unsafe_allow_html=True)
