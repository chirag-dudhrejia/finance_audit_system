"""
Reusable enterprise-grade UI components for Finance Audit System
"""

import streamlit as st
import pandas as pd
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


def sidebar_logo(title: str = "Finance Audit", subtitle: str = "Enterprise"):
    """Add a styled logo to the sidebar"""
    st.sidebar.markdown(
        f"""
        <div style="padding: 1rem 0; margin-bottom: 1rem;">
            <h2 style="color: white; font-size: 1.5rem; font-weight: 700; margin: 0;">
                {title}
            </h2>
            <p style="color: rgba(255,255,255,0.6); font-size: 0.75rem; margin: 0.25rem 0 0 0;">
                {subtitle}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sidebar_nav(items: list):
    """Create styled navigation links in sidebar"""
    for item in items:
        st.sidebar.markdown(
            f"""
            <a href="/{item["path"]}" style="
                display: block;
                padding: 0.75rem 1rem;
                color: rgba(255,255,255,0.7);
                text-decoration: none;
                border-radius: 8px;
                margin: 0.25rem 0;
                transition: all 0.2s ease;
            ">
                {item["icon"]} {item["label"]}
            </a>
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
