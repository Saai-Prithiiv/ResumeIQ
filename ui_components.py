"""UI Components, Theme, and Visualization Helpers for ResumeIQ.

Design System:
- Background: #0B1020
- Sidebar: #111827
- Cards: #1E293B
- Primary Purple: #8B5CF6
- Secondary Blue: #6366F1
- Success Green: #22C55E
- Warning Orange: #F59E0B
- Text White: #F8FAFC
- Muted Text: #94A3B8
"""

from __future__ import annotations

import html
from typing import Any
import plotly.graph_objects as go
import streamlit as st


def inject_custom_css() -> None:
    """Inject premium dark-mode SaaS styling into Streamlit."""
    custom_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg-main: #0B1020;
        --bg-sidebar: #111827;
        --bg-card: #1E293B;
        --bg-card-subtle: #162032;
        --bg-card-hover: #26354D;
        --primary-purple: #8B5CF6;
        --primary-purple-glow: rgba(139, 92, 246, 0.35);
        --secondary-blue: #6366F1;
        --secondary-blue-glow: rgba(99, 102, 241, 0.35);
        --success-green: #22C55E;
        --success-green-bg: rgba(34, 197, 94, 0.12);
        --warning-orange: #F59E0B;
        --warning-orange-bg: rgba(245, 158, 11, 0.12);
        --text-white: #F8FAFC;
        --text-muted: #94A3B8;
        --border-color: #334155;
        --border-subtle: rgba(255, 255, 255, 0.08);
        --radius-lg: 16px;
        --radius-md: 12px;
        --radius-sm: 8px;
    }

    /* Overall Page Background & Typography */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: var(--bg-main) !important;
        color: var(--text-white) !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }

    /* Main Container Spacing */
    .block-container {
        padding-top: 1.8rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 1240px !important;
    }

    /* Header transparency */
    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: var(--bg-sidebar) !important;
        border-right: 1px solid var(--border-color) !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.25);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.5rem;
        padding-left: 1.2rem;
        padding-right: 1.2rem;
    }

    /* Custom Scrollbars */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: var(--bg-main);
    }
    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-purple);
    }

    /* Buttons: Base & Primary Gradient */
    div.stButton > button,
    div.stButton > button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #8B5CF6 0%, #6366F1 100%) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: var(--radius-md) !important;
        padding: 0.65rem 1.4rem !important;
        box-shadow: 0 4px 14px 0 rgba(139, 92, 246, 0.35) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        letter-spacing: 0.01em !important;
    }

    div.stButton > button:hover,
    div.stButton > button[data-testid="baseButton-primary"]:hover {
        background: linear-gradient(135deg, #7C3AED 0%, #4F46E5 100%) !important;
        box-shadow: 0 6px 20px 0 rgba(139, 92, 246, 0.55) !important;
        transform: translateY(-2px) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
    }

    div.stButton > button:active,
    div.stButton > button[data-testid="baseButton-primary"]:active {
        transform: translateY(0px) !important;
        box-shadow: 0 2px 10px 0 rgba(139, 92, 246, 0.4) !important;
    }

    /* Secondary / Flat Buttons */
    div.stButton > button[data-testid="baseButton-secondary"],
    div.stButton > button[kind="secondary"] {
        background: #1E293B !important;
        color: #F8FAFC !important;
        border: 1px solid var(--border-color) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
    }

    div.stButton > button[data-testid="baseButton-secondary"]:hover,
    div.stButton > button[kind="secondary"]:hover {
        background: #27354A !important;
        border-color: var(--primary-purple) !important;
        color: #FFFFFF !important;
    }

    /* Sidebar Navigation Buttons */
    [data-testid="stSidebar"] div.stButton > button {
        text-align: left !important;
        justify-content: flex-start !important;
        padding: 0.6rem 1rem !important;
        margin-bottom: 0.35rem !important;
        width: 100% !important;
        border-radius: var(--radius-sm) !important;
    }

    /* Form Inputs & Textarea */
    [data-testid="stTextArea"] textarea {
        background-color: var(--bg-card) !important;
        color: var(--text-white) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-md) !important;
        font-family: inherit !important;
        font-size: 0.92rem !important;
        padding: 0.9rem !important;
        line-height: 1.5 !important;
        transition: all 0.2s ease !important;
    }

    [data-testid="stTextArea"] textarea:focus {
        border-color: var(--primary-purple) !important;
        box-shadow: 0 0 0 2px var(--primary-purple-glow) !important;
        outline: none !important;
        background-color: #1a2333 !important;
    }

    [data-testid="stTextArea"] label {
        color: var(--text-white) !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.4rem !important;
    }

    /* File Uploader */
    [data-testid="stFileUploader"] {
        background-color: var(--bg-card) !important;
        border: 2px dashed #334155 !important;
        border-radius: var(--radius-md) !important;
        padding: 1.2rem !important;
        transition: all 0.2s ease !important;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: var(--primary-purple) !important;
        background-color: #1a2333 !important;
    }

    [data-testid="stFileUploader"] section {
        padding: 0 !important;
    }

    [data-testid="stFileUploader"] button {
        background: #334155 !important;
        color: #F8FAFC !important;
        border: 1px solid #475569 !important;
        border-radius: var(--radius-sm) !important;
        box-shadow: none !important;
    }

    [data-testid="stFileUploader"] button:hover {
        background: var(--primary-purple) !important;
        border-color: var(--primary-purple) !important;
        color: #FFFFFF !important;
    }

    /* Streamlit Tabs */
    [data-testid="stTabs"] {
        border-bottom: 1px solid var(--border-color) !important;
    }

    [data-testid="stTabs"] button[role="tab"] {
        color: var(--text-muted) !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        padding: 0.75rem 1.4rem !important;
        border: none !important;
        background: transparent !important;
        transition: all 0.2s ease !important;
    }

    [data-testid="stTabs"] button[role="tab"]:hover {
        color: var(--text-white) !important;
    }

    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        color: #FFFFFF !important;
        border-bottom: 2px solid var(--primary-purple) !important;
    }

    /* Streamlit Metric Overrides */
    [data-testid="stMetric"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-md) !important;
        padding: 1rem 1.2rem !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
    }

    [data-testid="stMetricLabel"] {
        color: var(--text-muted) !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    [data-testid="stMetricValue"] {
        color: var(--text-white) !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }

    /* Expander Container */
    [data-testid="stExpander"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-md) !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2) !important;
        overflow: hidden !important;
    }

    [data-testid="stExpander"] summary {
        color: var(--text-white) !important;
        font-weight: 600 !important;
        padding: 0.8rem 1rem !important;
    }

    [data-testid="stExpander"] summary:hover {
        color: var(--primary-purple) !important;
    }

    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #6366F1 0%, #8B5CF6 100%) !important;
        border-radius: 9999px !important;
    }
    .stProgress > div > div > div {
        background-color: #1E293B !important;
        border-radius: 9999px !important;
    }

    /* Custom SaaS UI Utility Classes */
    .riq-hero {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(139, 92, 246, 0.25);
        border-radius: var(--radius-lg);
        padding: 2.2rem 2.4rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }

    .riq-hero::after {
        content: '';
        position: absolute;
        top: -40%;
        right: -20%;
        width: 380px;
        height: 380px;
        background: radial-gradient(circle, rgba(139, 92, 246, 0.15) 0%, rgba(99, 102, 241, 0) 70%);
        pointer-events: none;
    }

    .riq-badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        padding: 4px 12px;
        border-radius: 9999px;
        margin-bottom: 0.8rem;
    }

    .riq-badge-purple {
        background: rgba(139, 92, 246, 0.18);
        color: #C4B5FD;
        border: 1px solid rgba(139, 92, 246, 0.35);
    }

    .riq-badge-green {
        background: var(--success-green-bg);
        color: #4ADE80;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }

    .riq-badge-orange {
        background: var(--warning-orange-bg);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }

    .riq-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: 1.4rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.22);
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
    }

    .riq-card:hover {
        border-color: rgba(139, 92, 246, 0.4);
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    }

    .riq-stat-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: 1.2rem;
        text-align: center;
        position: relative;
    }

    .riq-stat-value {
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.1;
        margin: 0.3rem 0;
        background: linear-gradient(135deg, #F8FAFC 0%, #CBD5E1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .riq-stat-label {
        color: var(--text-muted);
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .riq-pill-tag {
        display: inline-block;
        font-size: 0.82rem;
        font-weight: 500;
        padding: 5px 12px;
        border-radius: 9999px;
        margin: 3px 4px;
        transition: all 0.15s ease;
    }

    .riq-pill-tag-match {
        background: rgba(34, 197, 94, 0.15);
        color: #4ADE80;
        border: 1px solid rgba(34, 197, 94, 0.35);
    }

    .riq-pill-tag-match:hover {
        background: rgba(34, 197, 94, 0.25);
        border-color: rgba(34, 197, 94, 0.6);
        transform: scale(1.03);
    }

    .riq-pill-tag-missing {
        background: rgba(245, 158, 11, 0.14);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.35);
    }

    .riq-pill-tag-missing:hover {
        background: rgba(245, 158, 11, 0.24);
        border-color: rgba(245, 158, 11, 0.6);
        transform: scale(1.03);
    }

    .riq-step-box {
        display: flex;
        gap: 1rem;
        align-items: flex-start;
        padding: 1.1rem;
        background: #162032;
        border: 1px solid #283548;
        border-radius: var(--radius-md);
        margin-bottom: 0.8rem;
    }

    .riq-step-number {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 34px;
        height: 34px;
        border-radius: 9999px;
        background: linear-gradient(135deg, #8B5CF6, #6366F1);
        color: #FFFFFF;
        font-weight: 700;
        font-size: 0.9rem;
        flex-shrink: 0;
    }

    .riq-disclaimer-box {
        background: rgba(99, 102, 241, 0.08);
        border-left: 4px solid var(--secondary-blue);
        border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
        padding: 0.9rem 1.1rem;
        margin: 1.2rem 0;
        font-size: 0.88rem;
        color: #CBD5E1;
    }

    .riq-code-preview {
        background: #0D1324;
        border: 1px solid #232D3F;
        border-radius: var(--radius-sm);
        padding: 1rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        color: #E2E8F0;
        max-height: 340px;
        overflow-y: auto;
        white-space: pre-wrap;
        line-height: 1.6;
    }

    .sidebar-brand-container {
        padding-bottom: 1.2rem;
        border-bottom: 1px solid var(--border-color);
        margin-bottom: 1rem;
    }

    .sidebar-brand-title {
        font-size: 1.35rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #FFFFFF 0%, #C4B5FD 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .sidebar-brand-tagline {
        font-size: 0.72rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 2px;
        font-weight: 600;
    }

    .sidebar-footer-card {
        background: #162032;
        border: 1px solid #232D3F;
        border-radius: var(--radius-sm);
        padding: 0.8rem;
        margin-top: 1.5rem;
        font-size: 0.75rem;
        color: var(--text-muted);
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


def render_sidebar_branding() -> None:
    """Render the modern SaaS logo and branding in the sidebar."""
    st.sidebar.markdown(
        """
        <div class="sidebar-brand-container">
            <div class="sidebar-brand-title">
                <span style="display:inline-flex; align-items:center; justify-content:center; width:30px; height:30px; border-radius:8px; background:linear-gradient(135deg, #8B5CF6, #6366F1); color:white; font-size:1rem; box-shadow:0 2px 10px rgba(139,92,246,0.5);">⚡</span>
                <span>Resume<span style="color:#8B5CF6;">IQ</span></span>
            </div>
            <div class="sidebar-brand-tagline">AI Resume Intelligence</div>
            <div style="margin-top: 6px;">
                <span class="riq-badge-pill riq-badge-purple" style="font-size:0.65rem; padding:2px 8px;">v2.0 • Local NLP</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_footer() -> None:
    """Render system status and privacy card in the sidebar."""
    st.sidebar.markdown(
        """
        <div class="sidebar-footer-card">
            <div style="font-weight:700; color:#F8FAFC; margin-bottom:4px; display:flex; align-items:center; gap:6px;">
                <span style="color:#22C55E;">●</span> System Status
            </div>
            <div style="line-height:1.4;">
                <div>• Engine: <span style="color:#CBD5E1;">Scikit & Local NLP</span></div>
                <div>• Privacy: <span style="color:#22C55E;">100% Offline / Local</span></div>
                <div>• Deploy: <span style="color:#818CF8;">Docker Container</span></div>
            </div>
            <div style="margin-top:8px; font-size:0.7rem; color:#64748B;">
                Zero documents or analytics leave this container.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def create_match_gauge_chart(score: int) -> go.Figure:
    """Create a modern circular gauge chart with dark-mode styling."""
    if score >= 75:
        bar_color = "#22C55E"  # Success green
        status_text = "Strong Alignment"
    elif score >= 50:
        bar_color = "#8B5CF6"  # Primary purple
        status_text = "Moderate Alignment"
    else:
        bar_color = "#F59E0B"  # Warning orange
        status_text = "Optimization Recommended"

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={
                "suffix": "%",
                "font": {"size": 44, "color": "#F8FAFC", "family": "Plus Jakarta Sans"},
            },
            title={
                "text": f"<b>Match Overlap</b><br><span style='font-size:0.82em;color:#94A3B8'>{status_text}</span>",
                "font": {"size": 15, "color": "#CBD5E1", "family": "Plus Jakarta Sans"},
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 1,
                    "tickcolor": "#475569",
                    "tickvals": [0, 25, 50, 75, 100],
                    "ticktext": ["0%", "25%", "50%", "75%", "100%"],
                    "tickfont": {"size": 11, "color": "#94A3B8"},
                },
                "bar": {"color": bar_color, "thickness": 0.28},
                "bgcolor": "#162032",
                "borderwidth": 1,
                "bordercolor": "#334155",
                "steps": [
                    {"range": [0, 50], "color": "rgba(245, 158, 11, 0.08)"},
                    {"range": [50, 75], "color": "rgba(139, 92, 246, 0.08)"},
                    {"range": [75, 100], "color": "rgba(34, 197, 94, 0.08)"},
                ],
                "threshold": {
                    "line": {"color": "#FFFFFF", "width": 3},
                    "thickness": 0.75,
                    "value": score,
                },
            },
        )
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=25, r=25, t=45, b=25),
        height=250,
    )
    return fig


def create_keyword_breakdown_chart(matched_count: int, missing_count: int) -> go.Figure:
    """Create a sleek comparison bar chart showing matched vs missing keywords."""
    categories = ["Matched Terms", "Missing Terms"]
    counts = [matched_count, missing_count]
    colors = ["#22C55E", "#F59E0B"]

    fig = go.Figure(
        go.Bar(
            x=counts,
            y=categories,
            orientation="h",
            marker=dict(
                color=colors,
                line=dict(color=["rgba(34, 197, 94, 0.5)", "rgba(245, 158, 11, 0.5)"], width=1),
                cornerradius=6,
            ),
            text=[f"<b>{c} terms</b>" for c in counts],
            textposition="auto",
            textfont=dict(color="#F8FAFC", family="Plus Jakarta Sans", size=13),
        )
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=20, t=20, b=20),
        height=190,
        xaxis=dict(
            showgrid=True,
            gridcolor="#232D3F",
            zeroline=False,
            showticklabels=True,
            tickfont=dict(color="#94A3B8"),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            tickfont=dict(color="#F8FAFC", size=13, family="Plus Jakarta Sans"),
        ),
    )
    return fig


def render_stat_card(label: str, value: str | int, subtext: str = "", badge: str = "") -> str:
    """Return an HTML snippet for a sleek SaaS metric card."""
    badge_html = f'<div style="margin-bottom:6px;"><span class="riq-badge-pill riq-badge-purple">{html.escape(badge)}</span></div>' if badge else ""
    subtext_html = f'<div style="color:#94A3B8; font-size:0.75rem; margin-top:4px;">{html.escape(subtext)}</div>' if subtext else ""
    return f"""
    <div class="riq-stat-card">
        {badge_html}
        <div class="riq-stat-label">{html.escape(label)}</div>
        <div class="riq-stat-value">{html.escape(str(value))}</div>
        {subtext_html}
    </div>
    """


def render_badge_cloud(items: list[str], badge_type: str = "match") -> str:
    """Render a list of string items as responsive interactive CSS pill badges."""
    if not items:
        return '<div style="color:#94A3B8; font-style:italic; padding:0.5rem 0;">None detected.</div>'
    
    cls = "riq-pill-tag-match" if badge_type == "match" else "riq-pill-tag-missing"
    icon = "✓" if badge_type == "match" else "+"
    badges = [
        f'<span class="riq-pill-tag {cls}">{icon} {html.escape(item)}</span>'
        for item in items
    ]
    return f'<div style="display:flex; flex-wrap:wrap; gap:4px; padding:0.4rem 0;">{"".join(badges)}</div>'
