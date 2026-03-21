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

SIDEBAR_ICONS = {
    "upload": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>',
    "dashboard": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="9"/><rect x="14" y="3" width="7" height="5"/><rect x="14" y="12" width="7" height="9"/><rect x="3" y="16" width="7" height="5"/></svg>',
    "chart": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/></svg>',
    "transactions": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><line x1="10" y1="9" x2="8" y2="9"/></svg>',
    "analytics": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/></svg>',
    "search": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>',
    "settings": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
    "check": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
    "wallet": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12V7H5a2 2 0 0 1 0-4h14v4"/><path d="M3 5v14a2 2 0 0 0 2 2h16v-5"/><circle cx="18" cy="12" r="2"/></svg>',
    "trending": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>',
    "shield": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    "sparkle": '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>',
}

SIDEBAR_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #f1f5f9;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}
.sidebar-modern {
    padding: 0.75rem;
}
.sidebar-brand {
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    border-radius: 16px;
    padding: 1.25rem 1rem;
    margin-bottom: 1.25rem;
    border: 1px solid #e2e8f0;
    box-shadow: 0 2px 8px rgba(15,23,42,0.04);
    position: relative;
    overflow: hidden;
}
.sidebar-brand::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
}
.sidebar-brand-content {
    display: flex;
    align-items: center;
    gap: 0.875rem;
    padding-top: 0.25rem;
}
.sidebar-brand-icon {
    width: 44px;
    height: 44px;
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    box-shadow: 0 4px 12px rgba(79,70,229,0.3);
    position: relative;
}
.sidebar-brand-icon::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 12px;
    background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, transparent 50%);
}
.sidebar-brand-icon svg {
    color: #ffffff;
    position: relative;
    z-index: 1;
}
.sidebar-brand-text h1 {
    font-size: 1rem;
    font-weight: 700;
    color: #0f172a;
    margin: 0 0 0.125rem 0;
    letter-spacing: -0.02em;
}
.sidebar-brand-text p {
    font-size: 0.6875rem;
    color: #64748b;
    margin: 0;
    font-weight: 500;
}
.sidebar-section {
    margin-bottom: 1rem;
}
.sidebar-section-label {
    font-size: 0.625rem;
    font-weight: 700;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 0 0 0.625rem 0.875rem;
}
.sidebar-nav-item {
    display: flex;
    align-items: center;
    gap: 0.875rem;
    padding: 0.875rem 1rem;
    border-radius: 12px;
    color: #64748b;
    text-decoration: none;
    font-size: 0.875rem;
    font-weight: 500;
    transition: all 0.2s ease;
    margin: 0.125rem 0;
    position: relative;
    border: 1px solid transparent;
}
.sidebar-nav-item:hover {
    background: #f8fafc;
    color: #0f172a;
    border-color: #e2e8f0;
}
.sidebar-nav-item:hover svg {
    color: #4f46e5;
}
.sidebar-nav-item.active {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    color: #ffffff;
    border-color: transparent;
    box-shadow: 0 4px 16px rgba(79,70,229,0.35);
}
.sidebar-nav-item.active svg {
    color: #ffffff;
}
.sidebar-nav-icon {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: all 0.2s ease;
}
.sidebar-nav-item:not(.active):hover .sidebar-nav-icon {
    background: rgba(79,70,229,0.08);
}
.sidebar-nav-item.active .sidebar-nav-icon {
    background: rgba(255,255,255,0.2);
}
.sidebar-nav-item svg {
    flex-shrink: 0;
    transition: color 0.2s ease;
}
.sidebar-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, #f1f5f9 20%, #f1f5f9 80%, transparent 100%);
    margin: 1.25rem 0.75rem;
}
.sidebar-stats-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border-radius: 16px;
    padding: 1.125rem;
    border: 1px solid #e2e8f0;
    box-shadow: 0 2px 8px rgba(15,23,42,0.03);
}
.sidebar-stat-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.5rem;
    border-radius: 10px;
    margin-bottom: 0.375rem;
    transition: all 0.2s ease;
}
.sidebar-stat-row:last-child {
    margin-bottom: 0;
}
.sidebar-stat-row:hover {
    background: #f1f5f9;
}
.sidebar-stat-icon {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.sidebar-stat-icon.green {
    background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
}
.sidebar-stat-icon.green svg {
    color: #059669;
}
.sidebar-stat-icon.cyan {
    background: linear-gradient(135deg, #eef2ff 0%, #ede9fe 100%);
}
.sidebar-stat-icon.cyan svg {
    color: #7c3aed;
}
.sidebar-stat-icon.purple {
    background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%);
}
.sidebar-stat-icon.purple svg {
    color: #7c3aed;
}
.sidebar-stat-content {
    flex: 1;
    min-width: 0;
}
.sidebar-stat-label {
    font-size: 0.6875rem;
    color: #64748b;
    margin-bottom: 0.125rem;
}
.sidebar-stat-value {
    font-size: 0.9375rem;
    font-weight: 700;
    color: #0f172a;
}
.sidebar-stat-badge {
    font-size: 0.625rem;
    font-weight: 600;
    padding: 0.125rem 0.5rem;
    border-radius: 9999px;
    background: #d1fae5;
    color: #059669;
}
.sidebar-footer {
    margin-top: auto;
    padding: 1rem;
    text-align: center;
}
.sidebar-footer p {
    font-size: 0.6875rem;
    color: #94a3b8;
    margin: 0;
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


def render_sidebar(
    current_page: str = "main", transaction_count: int = 0, show_stats: bool = True
):
    """
    Render a unified, modern sidebar across all pages.

    Args:
        current_page: The current page identifier ('main' or 'dashboard')
        transaction_count: Number of transactions to display
        show_stats: Whether to show quick stats section
    """
    st.markdown(SIDEBAR_CSS, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-modern">', unsafe_allow_html=True)

    st.markdown(
        f"""
    <div class="sidebar-brand">
        <div class="sidebar-brand-content">
            <div class="sidebar-brand-icon">
                {SIDEBAR_ICONS["chart"]}
            </div>
            <div class="sidebar-brand-text">
                <h1>Finance Audit</h1>
                <p>Enterprise Edition</p>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown(
        '<p class="sidebar-section-label">Main Menu</p>', unsafe_allow_html=True
    )

    is_upload_active = "active" if current_page == "main" else ""
    is_dashboard_active = "active" if current_page == "dashboard" else ""

    st.markdown(
        f"""
    <a href="/" class="sidebar-nav-item {is_upload_active}">
        <div class="sidebar-nav-icon">{SIDEBAR_ICONS["upload"]}</div>
        <span>Upload Statement</span>
    </a>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
    <a href="/dashboard" class="sidebar-nav-item {is_dashboard_active}" onclick="window.location.href='/dashboard'">
        <div class="sidebar-nav-icon">{SIDEBAR_ICONS["dashboard"]}</div>
        <span>Dashboard</span>
    </a>
    """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sidebar-section-label">Quick Links</p>', unsafe_allow_html=True
    )

    st.markdown(
        f"""
    <a href="#" class="sidebar-nav-item">
        <div class="sidebar-nav-icon">{SIDEBAR_ICONS["analytics"]}</div>
        <span>View Analytics</span>
    </a>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
    <a href="#" class="sidebar-nav-item">
        <div class="sidebar-nav-icon">{SIDEBAR_ICONS["search"]}</div>
        <span>Search Transactions</span>
    </a>
    """,
        unsafe_allow_html=True,
    )

    if show_stats:
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        st.markdown(
            '<p class="sidebar-section-label">Quick Stats</p>', unsafe_allow_html=True
        )

        st.markdown(
            f"""
        <div class="sidebar-stats-card">
            <div class="sidebar-stat-row">
                <div class="sidebar-stat-icon cyan">
                    {SIDEBAR_ICONS["transactions"]}
                </div>
                <div class="sidebar-stat-content">
                    <div class="sidebar-stat-label">Total Transactions</div>
                    <div class="sidebar-stat-value">{transaction_count:,}</div>
                </div>
            </div>
            <div class="sidebar-stat-row">
                <div class="sidebar-stat-icon green">
                    {SIDEBAR_ICONS["shield"]}
                </div>
                <div class="sidebar-stat-content">
                    <div class="sidebar-stat-label">System Status</div>
                    <div class="sidebar-stat-value">Active</div>
                </div>
                <span class="sidebar-stat-badge">{SIDEBAR_ICONS["check"]}</span>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
