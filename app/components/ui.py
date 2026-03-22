"""
Reusable enterprise-grade UI components for Finance Audit System
"""

import streamlit as st
import pandas as pd
import os
from theme import (
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    ACCENT_COLOR,
    SUCCESS_COLOR,
    WARNING_COLOR,
    ERROR_COLOR,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BG_CARD,
    BORDER_COLOR,
    BORDER_RADIUS,
    SHADOW_SM,
    SHADOW_MD,
)

SIDEBAR_CSS = """
<style>
.sidebar-brand-card {
    background: linear-gradient(135deg, #312e81 0%, #4f46e5 40%, #6366f1 100%);
    border-radius: 12px;
    padding: 1rem 1rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 16px rgba(79,70,229,0.2);
}
.sidebar-brand-card::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background:
        radial-gradient(ellipse at 20% 80%, rgba(99,102,241,0.4) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, rgba(129,140,248,0.3) 0%, transparent 50%);
    pointer-events: none;
}
.sidebar-brand-inner {
    display: flex;
    align-items: center;
    gap: 0.625rem;
    position: relative;
    z-index: 1;
}
.sidebar-brand-icon {
    width: 36px;
    height: 36px;
    background: rgba(255,255,255,0.15);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    border: 1px solid rgba(255,255,255,0.2);
}
.sidebar-brand-icon svg {
    width: 18px;
    height: 18px;
    stroke: #ffffff;
    fill: none;
    stroke-width: 2;
    stroke-linecap: round;
    stroke-linejoin: round;
}
.sidebar-brand-text h1 {
    font-size: 0.9375rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
    letter-spacing: -0.01em;
}
.sidebar-brand-text p {
    font-size: 0.6875rem;
    color: rgba(255,255,255,0.7);
    margin: 0.125rem 0 0 0;
    font-weight: 400;
}
.sidebar-divider-light {
    height: 1px;
    background: #e8e0ff;
    margin: 0.75rem 0;
}
.sidebar-meta-light {
    padding: 0 0.25rem;
}
.sidebar-meta-item-light {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.75rem;
    color: #6b7280;
    margin-bottom: 0.375rem;
}
.sidebar-meta-item-light svg {
    width: 14px;
    height: 14px;
    flex-shrink: 0;
    stroke: currentColor;
    fill: none;
    stroke-width: 1.75;
    stroke-linecap: round;
    stroke-linejoin: round;
}
</style>
"""


def apply_theme():
    """Apply the enterprise theme CSS"""
    from theme import get_css

    st.markdown(get_css(), unsafe_allow_html=True)


def section_header(title: str, subtitle: str = None, icon: str = None):
    """Create a styled section header"""
    icon_html = f"<span style='margin-right:0.5rem'>{icon}</span>" if icon else ""
    subtitle_html = (
        f"<div class='section-subtitle'>{subtitle}</div>" if subtitle else ""
    )
    st.markdown(
        f"""
        <div class="enterprise-section">
            <h2>{icon_html}{title}</h2>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(col, label: str, value: str, delta: str = None, color: str = None):
    """Display a styled metric card in a column"""
    delta_html = ""
    if delta:
        is_positive = not delta.startswith("-")
        delta_class = "positive" if is_positive else "negative"
        delta_icon = "↑" if is_positive else "↓"
        delta_html = (
            f"""<div class="kpi-trend {delta_class}">{delta_icon} {delta}</div>"""
        )

    style = f"border-left: 4px solid {color};" if color else ""

    html = f"""
    <div class="kpi-card" style="{style}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """
    with col:
        st.markdown(html, unsafe_allow_html=True)


def info_card(message: str, card_type: str = "info"):
    """Display a styled info/warning/success/error card"""
    colors = {
        "success": ("#ecfdf5", "#065f46", "#a7f3d0"),
        "warning": ("#fffbeb", "#92400e", "#fde68a"),
        "error": ("#fef2f2", "#991b1b", "#fecaca"),
        "info": ("#eff6ff", "#1e40af", "#bfdbfe"),
    }
    bg, text, border = colors.get(card_type, colors["info"])

    st.markdown(
        f"""
        <div style="
            background-color: {bg};
            border: 1px solid {border};
            border-radius: {BORDER_RADIUS};
            padding: 1rem 1.25rem;
            color: {text};
            font-size: 0.9rem;
        ">
            {message}
        </div>
        """,
        unsafe_allow_html=True,
    )


def styled_dataframe(df: pd.DataFrame, height: int = None, hide_index: bool = True):
    """Display a styled dataframe with custom formatting"""
    st.dataframe(df, use_container_width=True, hide_index=hide_index, height=height)


def stats_row(col1, col2, col3, col4):
    """Create a row of 4 stat cards"""
    cols = st.columns(4)
    return cols


def divider():
    """Insert a styled divider"""
    st.markdown(
        f"""
        <div class="enterprise-divider"></div>
        """,
        unsafe_allow_html=True,
    )


def page_title(title: str, subtitle: str = None):
    """Create a styled page title"""
    if subtitle:
        st.markdown(
            f"""
            <div style="margin-bottom: 2rem;">
                <h1 style="font-size: 2rem; font-weight: 700; color: {TEXT_PRIMARY}; margin-bottom: 0.25rem;">
                    {title}
                </h1>
                <p style="color: {TEXT_SECONDARY}; font-size: 1rem; margin: 0;">
                    {subtitle}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div style="margin-bottom: 2rem;">
                <h1 style="font-size: 2rem; font-weight: 700; color: {TEXT_PRIMARY};">
                    {title}
                </h1>
            </div>
            """,
            unsafe_allow_html=True,
        )


def category_badge(category: str):
    """Generate HTML for a category badge with color"""
    colors = {
        "Food & Dining": "#f59e0b",
        "Transport": "#3b82f6",
        "Shopping": "#ec4899",
        "Entertainment": "#8b5cf6",
        "Bank Transfer": "#06b6d4",
        "Transfer": "#06b6d4",
        "Bills & Utilities": "#ef4444",
        "Rent": "#8b5cf6",
        "Health": "#10b981",
        "Investment": "#3b82f6",
        "Uncategorized": "#94a3b8",
    }
    color = colors.get(category, "#94a3b8")

    st.markdown(
        f"""
        <span style="
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            background-color: {color}20;
            color: {color};
            border: 1px solid {color}40;
        ">
            {category}
        </span>
        """,
        unsafe_allow_html=True,
    )


def upload_zone():
    """Render a styled upload zone"""
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, {BG_CARD} 0%, #f1f5f9 100%);
            border: 2px dashed {ACCENT_COLOR};
            border-radius: 16px;
            padding: 3rem 2rem;
            text-align: center;
            transition: all 0.3s ease;
        ">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📁</div>
            <h3 style="color: {TEXT_PRIMARY}; margin-bottom: 0.5rem;">
                Upload Your Bank Statement
            </h3>
            <p style="color: {TEXT_SECONDARY}; font-size: 0.9rem;">
                Drag and drop or click to upload CSV or PDF files
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def summary_cards(stats: dict):
    """Display summary statistics in a grid"""
    cols = st.columns(len(stats))
    for i, (label, value) in enumerate(stats.items()):
        with cols[i]:
            st.metric(label=label, value=value)


def alert_banner(message: str, alert_type: str = "info"):
    """Display an alert banner at the top"""
    colors = {
        "success": ("#10b981", "#ecfdf5"),
        "warning": ("#f59e0b", "#fffbeb"),
        "error": ("#ef4444", "#fef2f2"),
        "info": ("#3b82f6", "#eff6ff"),
    }
    icon, bg = colors.get(alert_type, colors["info"])

    st.markdown(
        f"""
        <div style="
            background-color: {bg};
            border-left: 4px solid {icon};
            border-radius: 8px;
            padding: 1rem 1.25rem;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        ">
            <span style="font-size: 1.25rem;">{"✅" if alert_type == "success" else "⚠️" if alert_type == "warning" else "❌" if alert_type == "error" else "ℹ️"}</span>
            <span style="color: #1e293b; font-size: 0.9rem;">{message}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar(transaction_count: int = 0, show_stats: bool = True):
    """
    Render a clean, minimal sidebar brand and stats.
    Navigation is handled by st.navigation() in main.py.

    Args:
        transaction_count: Number of transactions to display
        show_stats: Whether to show quick stats
    """
    st.markdown(SIDEBAR_CSS, unsafe_allow_html=True)

    chart_svg = '<svg viewBox="0 0 24 24"><path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/></svg>'

    st.html(f"""
    <div class="sidebar-brand-card">
        <div class="sidebar-brand-inner">
            <div class="sidebar-brand-icon">
                {chart_svg}
            </div>
            <div class="sidebar-brand-text">
                <h1>Finance Audit</h1>
                <p>Intelligence Platform</p>
            </div>
        </div>
    </div>
    """)

    if show_stats and transaction_count > 0:
        doc_svg = '<svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>'
        st.html(f"""
        <div class="sidebar-divider-light"></div>
        <div class="sidebar-meta-light">
            <div class="sidebar-meta-item-light">
                {doc_svg}
                <span>{transaction_count:,} transactions</span>
            </div>
        </div>
        """)
