"""
charts.py — Visualisations : jauge, radar, barres, heatmap
"""

import math
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from .theme import MODULE_COLORS, MODULE_ICONS, MODULE_LABELS, score_color


def gauge_chart(score: int, title: str = "SCORE FINAL") -> go.Figure:
    """Jauge semi-circulaire style tableau de bord."""
    color = score_color(score)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": title, "font": {"size": 13, "family": "Sora", "color": "#64748b"}},
        number={"font": {"size": 36, "family": "Sora, sans-serif", "color": "#0f2244"}, "suffix": "/100"},
        gauge={
            "axis": {"range": [0, 100], "tickfont": {"size": 10, "family": "Sora"}},
            "bar":  {"color": color, "thickness": 0.25},
            "bgcolor": "white",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 30],   "color": "#fef2f2"},
                {"range": [30, 50],  "color": "#fff7ed"},
                {"range": [50, 70],  "color": "#fffbeb"},
                {"range": [70, 100], "color": "#f0fdf4"},
            ],
            "threshold": {
                "line": {"color": color, "width": 4},
                "thickness": 0.75,
                "value": score
            }
        }
    ))

    fig.update_layout(
        height=220,
        margin=dict(t=40, b=10, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Sora, sans-serif"},
    )
    return fig


def radar_chart(module_scores: dict) -> go.Figure:
    """Radar chart 8 axes pour les scores modulaires."""
    labels = [f"{MODULE_ICONS.get(k,'🔹')} {MODULE_LABELS.get(k, k)}" for k in module_scores]
    values = list(module_scores.values())
    values_closed = values + [values[0]]
    labels_closed = labels + [labels[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=labels_closed,
        fill="toself",
        fillcolor="rgba(59,130,246,0.15)",
        line={"color": "#3b82f6", "width": 2},
        name="Score modules",
        hovertemplate="%{theta}: %{r}/100<extra></extra>"
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True, range=[0, 100],
                tickfont={"size": 9, "family": "Sora"},
                gridcolor="#e2e8f0",
            ),
            angularaxis=dict(
                tickfont={"size": 9, "family": "Sora", "color": "#374151"},
                gridcolor="#e2e8f0",
            ),
            bgcolor="rgba(0,0,0,0)",
        ),
        showlegend=False,
        height=340,
        margin=dict(t=20, b=20, l=60, r=60),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": "Sora, sans-serif"},
    )
    return fig


def module_bar_chart(module_scores: dict) -> go.Figure:
    """Barres horizontales des scores par module."""
    labels = [f"{MODULE_ICONS.get(k,'🔹')} {MODULE_LABELS.get(k, k)}" for k in module_scores]
    values = list(module_scores.values())
    colors = [score_color(v) for v in values]

    fig = go.Figure(go.Bar(
        x=values,
        y=labels,
        orientation="h",
        marker_color=colors,
        text=[f"{v}/100" for v in values],
        textposition="outside",
        textfont={"size": 11, "family": "Sora", "color": "#374151"},
        hovertemplate="%{y}: %{x}/100<extra></extra>"
    ))

    fig.update_layout(
        xaxis=dict(range=[0, 115], showgrid=True, gridcolor="#f1f5f9", tickfont={"size": 10}),
        yaxis=dict(tickfont={"size": 10, "family": "Sora", "color": "#374151"}),
        height=300,
        margin=dict(t=10, b=10, l=10, r=60),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Sora, sans-serif"},
    )
    return fig


def indices_bar_chart(maturite: int, resilience: int, vulnerabilite: int) -> go.Figure:
    """Barres comparatives des 3 indices."""
    labels = ["🔬 Maturité\nMécatronique", "🛡️ Résilience\nOpérationnelle", "⚠️ Vulnérabilité\nSystémique (inv.)"]
    values = [maturite, resilience, 100 - vulnerabilite]
    colors = [score_color(v) for v in values]
    desc = ["Plus élevé = Plus mature", "Plus élevé = Plus résilient", "Plus élevé = Moins vulnérable"]

    fig = go.Figure(go.Bar(
        x=labels,
        y=values,
        marker_color=colors,
        text=[f"{v}" for v in values],
        textposition="outside",
        textfont={"size": 14, "family": "Sora", "color": "#0f2244", "weight": "bold"},
        customdata=desc,
        hovertemplate="<b>%{x}</b><br>Score: %{y}/100<br>%{customdata}<extra></extra>",
        width=0.5,
    ))

    fig.update_layout(
        yaxis=dict(range=[0, 115], showgrid=True, gridcolor="#f1f5f9", tickfont={"size": 10}),
        xaxis=dict(tickfont={"size": 11, "family": "Sora", "color": "#374151"}),
        height=280,
        margin=dict(t=30, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Sora, sans-serif"},
        bargap=0.4,
    )
    return fig


def benchmark_chart(benchmark: dict) -> go.Figure:
    """Comparaison entreprise vs benchmark sectoriel."""
    if not benchmark or not benchmark.get("mtbf_entreprise"):
        return None

    categories = ["MTBF (heures)", "MTTR (heures inversé)"]
    entreprise = [
        benchmark.get("mtbf_entreprise", 0),
        max(0, 100 - (benchmark.get("mttr_entreprise", 10) * 5))
    ]
    ref = [
        benchmark.get("mtbf_benchmark", 0),
        max(0, 100 - (benchmark.get("mttr_benchmark", 4) * 5))
    ]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Votre entreprise", x=categories, y=entreprise,
        marker_color="#3b82f6",
        text=[f"{benchmark.get('mtbf_entreprise', 0):.0f}h",
              f"{benchmark.get('mttr_entreprise', 0):.1f}h"],
        textposition="outside",
    ))
    fig.add_trace(go.Bar(
        name=f"Benchmark {benchmark.get('secteur', '')}", x=categories, y=ref,
        marker_color="#e2e8f0",
        text=[f"{benchmark.get('mtbf_benchmark', 0):.0f}h",
              f"{benchmark.get('mttr_benchmark', 0):.1f}h"],
        textposition="outside",
    ))

    fig.update_layout(
        barmode="group",
        height=260,
        margin=dict(t=20, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Sora, sans-serif"},
        legend={"font": {"size": 10}},
    )
    return fig
