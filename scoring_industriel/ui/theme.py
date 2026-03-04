"""
theme.py — Système de design : couleurs, polices, CSS global
Inspiré du design communiqué : bleu marine, bleu vif, vert/amber/rouge pour les scores.
"""

import streamlit as st

# ── PALETTE ───────────────────────────────────────────────────
COLORS = {
    "navy":       "#0f2244",
    "blue":       "#1d4ed8",
    "blue_light": "#3b82f6",
    "bg":         "#f0f4ff",
    "white":      "#ffffff",
    "border":     "#e2e8f0",
    "text":       "#1e293b",
    "muted":      "#64748b",
    "green":      "#10b981",
    "amber":      "#f59e0b",
    "red":        "#ef4444",
    "red_dark":   "#7f1d1d",
}

MODULE_COLORS = {
    "robots":       "#3b82f6",
    "cnc":          "#8b5cf6",
    "cps":          "#06b6d4",
    "electrique":   "#f59e0b",
    "maintenance":  "#10b981",
    "manutention":  "#f97316",
    "stockage":     "#ec4899",
    "intervention": "#ef4444",
}

MODULE_ICONS = {
    "robots":       "🤖",
    "cnc":          "⚙️",
    "cps":          "🌐",
    "electrique":   "⚡",
    "maintenance":  "🔧",
    "manutention":  "🏗️",
    "stockage":     "📦",
    "intervention": "🚨",
}

MODULE_LABELS = {
    "robots":       "Robots Industriels",
    "cnc":          "Machines CNC & Usinage",
    "cps":          "Système Cyber-Physique",
    "electrique":   "Infrastructure Électrique",
    "maintenance":  "Système de Maintenance",
    "manutention":  "Équipements & Manutention",
    "stockage":     "Stockage & Pièces de Rechange",
    "intervention": "Efficacité Intervention",
}


def score_color(score: int) -> str:
    if score >= 70: return COLORS["green"]
    if score >= 40: return COLORS["amber"]
    return COLORS["red"]


def score_label(score: int) -> str:
    if score >= 70: return "Risque Faible"
    if score >= 40: return "Risque Modéré"
    return "Risque Élevé"


def traffic_light(score: int) -> dict:
    if score >= 70:
        return {"color": COLORS["green"],  "label": "BON",      "emoji": "🟢"}
    if score >= 40:
        return {"color": COLORS["amber"],  "label": "MOYEN",    "emoji": "🟡"}
    return   {"color": COLORS["red"],      "label": "CRITIQUE",  "emoji": "🔴"}


def inject_css():
    """Injecte le CSS global dans l'application Streamlit."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Sora', sans-serif !important;
    }

    /* Fond global */
    .stApp {
        background: linear-gradient(135deg, #f0f4ff 0%, #e8f0fe 100%) !important;
    }

    /* Masquer le menu hamburger Streamlit */
    #MainMenu { visibility: hidden; }
    footer    { visibility: hidden; }
    header    { visibility: hidden; }

    /* Boutons principaux */
    .stButton > button {
        background: linear-gradient(90deg, #1d4ed8, #3b82f6) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 28px !important;
        font-family: 'Sora', sans-serif !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        box-shadow: 0 4px 12px rgba(59,130,246,0.35) !important;
        transition: all 0.2s !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 18px rgba(59,130,246,0.45) !important;
    }

    /* Inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        font-family: 'Sora', sans-serif !important;
        font-size: 13px !important;
        background: #fff !important;
    }

    /* Cards / containers */
    .score-card {
        background: white;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        padding: 20px;
        box-shadow: 0 2px 16px rgba(0,0,0,0.06);
    }

    /* Metric overrides */
    [data-testid="metric-container"] {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 14px !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #f1f5f9;
        border-radius: 10px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        font-family: 'Sora', sans-serif !important;
        font-weight: 600 !important;
        font-size: 12px !important;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        font-family: 'Sora', sans-serif !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        color: #0f2244 !important;
    }

    /* Dividers */
    hr { border-color: #e2e8f0 !important; }

    /* Custom progress bar */
    .progress-bar-container {
        background: #f1f5f9;
        border-radius: 6px;
        height: 8px;
        overflow: hidden;
    }

    /* Zone critique card */
    .zone-critique {
        border-left: 4px solid #ef4444;
        background: #fef2f2;
        border-radius: 6px;
        padding: 10px 14px;
        margin-bottom: 8px;
    }
    .zone-majeure {
        border-left: 4px solid #f59e0b;
        background: #fffbeb;
        border-radius: 6px;
        padding: 10px 14px;
        margin-bottom: 8px;
    }

    /* Recommendation card */
    .rec-urgente   { border-left: 4px solid #ef4444; background: #fef2f2; }
    .rec-prioritaire { border-left: 4px solid #f59e0b; background: #fffbeb; }
    .rec-recommandee { border-left: 4px solid #10b981; background: #f0fdf4; }
    .rec-card {
        border-radius: 6px;
        padding: 10px 14px;
        margin-bottom: 8px;
        font-size: 13px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #0f2244 !important;
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }

    </style>
    """, unsafe_allow_html=True)


def header_html(title: str, subtitle: str) -> str:
    return f"""
    <div style="
        background: linear-gradient(135deg, #0f2244 0%, #1e3a8a 60%, #1d4ed8 100%);
        border-radius: 14px; padding: 18px 24px; margin-bottom: 20px;
        display: flex; align-items: center; justify-content: space-between;
        box-shadow: 0 4px 24px rgba(29,78,216,0.25);
    ">
        <div>
            <div style="font-size:10px; color:#93c5fd; font-weight:700;
                        letter-spacing:2px; text-transform:uppercase; font-family:'Sora',sans-serif;">
                Prototype PFE — Scoring Risque
            </div>
            <div style="font-size:20px; font-weight:800; color:#fff; margin-top:4px; font-family:'Sora',sans-serif;">
                {title}
            </div>
            <div style="font-size:11px; color:#bfdbfe; margin-top:2px; font-family:'Sora',sans-serif;">
                {subtitle}
            </div>
        </div>
        <div style="font-size:36px;">🏭</div>
    </div>
    """
