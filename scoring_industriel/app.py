"""
app.py — Point d'entrée principal de l'application Streamlit
Scoring Risque Industriel 4.0 — Prototype PFE

Lancement :
    streamlit run app.py
"""

import streamlit as st

# ── Configuration page (doit être le premier appel Streamlit) ─
st.set_page_config(
    page_title="Scoring Risque Industriel 4.0",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Import de l'orchestrateur UI ──────────────────────────────
from ui.layout import render_app

# ── Lancement ─────────────────────────────────────────────────
if __name__ == "__main__" or True:
    render_app()
