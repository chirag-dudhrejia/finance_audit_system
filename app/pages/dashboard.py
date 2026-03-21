import sys
import os
import uuid
import base64
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import streamlit as st
import pandas as pd
import plotly.express as px
from data.repositories.transaction_repo import TransactionRepo
from services.insights import generate_insights
from components.ui import apply_theme, render_sidebar

st.set_page_config(
    page_title="Finance Audit - Dashboard",
    page_icon="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%234f46e5' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M3 3v18h18'/%3E%3Cpath d='M18 17V9'/%3E%3Cpath d='M13 17V5'/%3E%3Cpath d='M8 17v-3'/%3E%3C/svg%3E",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()

DEMO_USER_ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, "demo-user"))


def svg_to_img(svg_str):
    """Convert raw SVG string to an <img> tag with base64 data URI."""
    w_match = re.search(r'width="(\d+)"', svg_str)
    h_match = re.search(r'height="(\d+)"', svg_str)
    w = w_match.group(1) if w_match else "18"
    h = h_match.group(1) if h_match else "18"
    svg_str = svg_str.replace('stroke="currentColor"', 'stroke="#ffffff"')
    svg_str = svg_str.replace('stroke-width="2"', 'stroke-width="2.5"')
    b64 = base64.b64encode(svg_str.encode("utf-8")).decode("utf-8")
    return f'<img src="data:image/svg+xml;base64,{b64}" width="{w}" height="{h}" style="display:inline-block;vertical-align:middle;">'


DASH_ICONS_RAW = {
    "chart": '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/></svg>',
    "wallet": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>',
    "income": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
    "expense": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><polyline points="19 12 12 19 5 12"/></svg>',
    "savings": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 5c-1.5 0-2.8 1.4-3 2-3.5-1.5-11-.3-11 5 0 1.8 0 3 2 4.5V20h4v-2h3v2h4v-4c1-.5 1.7-1 2-2h2v-4h-2c0-1-.5-1.5-1-2V5z"/><path d="M2 9v1c0 1.1.9 2 2 2h1"/><circle cx="16" cy="11" r="1"/></svg>',
    "clock": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    "trending_up": '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>',
    "trending_down": '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 18 13.5 8.5 8.5 13.5 1 6"/><polyline points="17 18 23 18 23 12"/></svg>',
    "trending_neutral": '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/></svg>',
    "check": '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
    "dollar": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
    "percent": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="5" x2="5" y2="19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/></svg>',
    "category": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>',
    "store": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
    "repeat": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="17 1 21 5 17 9"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><polyline points="7 23 3 19 7 15"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/></svg>',
    "alert": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    "tag": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg>',
    "file": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
    "calendar": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
    "bar_chart": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
    "pie_chart": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/></svg>',
    "refresh": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>',
    "link": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>',
    "settings": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
    "upload": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>',
    "arrow_right": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>',
    "bank": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="22" x2="21" y2="22"/><line x1="6" y1="18" x2="6" y2="11"/><line x1="10" y1="18" x2="10" y2="11"/><line x1="14" y1="18" x2="14" y2="11"/><line x1="18" y1="18" x2="18" y2="11"/><polygon points="12 2 20 7 4 7"/></svg>',
    "credit_card": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>',
    "zap": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
    "layers": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>',
    "target": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
    "info": '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
}

DASH_ICONS = {k: svg_to_img(v) for k, v in DASH_ICONS_RAW.items()}

repo = TransactionRepo()
transactions = repo.get_transactions(DEMO_USER_ID)

txn_count = len(transactions)

with st.sidebar:
    render_sidebar(
        current_page="dashboard", transaction_count=txn_count, show_stats=True
    )

st.html(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    :root {
        --primary: #0f172a;
        --primary-light: #1e293b;
        --accent: #0891b2;
        --accent-light: #22d3ee;
        --success: #059669;
        --success-light: #34d399;
        --warning: #d97706;
        --warning-light: #fbbf24;
        --danger: #dc2626;
        --danger-light: #f87171;
        --purple: #7c3aed;
        --purple-light: #a78bfa;
        --bg: #f1f5f9;
        --card: #ffffff;
        --border: #e2e8f0;
        --text: #0f172a;
        --text-secondary: #64748b;
        --text-muted: #94a3b8;
    }
    
    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    
    .icon-wrapper svg {
        color: inherit;
        stroke: currentColor;
    }
    
    .enterprise-card {
        background: var(--card);
        border-radius: 16px;
        border: 1px solid var(--border);
        box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.1);
        transition: box-shadow 0.2s ease, transform 0.2s ease;
    }
    
    .enterprise-card:hover {
        box-shadow: 0 4px 6px rgba(0,0,0,0.05), 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .enterprise-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.375rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        gap: 0.375rem;
    }
    
    .enterprise-btn {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.875rem;
        font-weight: 500;
        border: none;
        cursor: pointer;
        transition: all 0.15s ease;
    }
    
    .enterprise-btn:hover {
        transform: translateY(-1px);
    }
    
    .metric-card {
        background: linear-gradient(135deg, var(--card) 0%, #f8fafc 100%);
        border-radius: 12px;
        padding: 1.25rem;
        border: 1px solid var(--border);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: radial-gradient(circle at top right, var(--accent-color, rgba(8,145,178,0.1)) 0%, transparent 70%);
        pointer-events: none;
    }
    
    .section-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--border);
        margin-bottom: 1rem;
    }
    
    .section-title {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .section-title-icon {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
    }
    
    .section-title-icon svg {
        width: 20px;
        height: 20px;
        color: white;
    }
    
    .section-title-text h3 {
        margin: 0;
        font-size: 1rem;
        font-weight: 600;
        color: var(--text);
    }
    
    .section-title-text p {
        margin: 0;
        font-size: 0.75rem;
        color: var(--text-muted);
    }
    
    .progress-bar {
        width: 100%;
        height: 8px;
        background: #e2e8f0;
        border-radius: 4px;
        overflow: hidden;
    }
    
    .progress-bar-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.5s ease;
    }
    
    .list-item {
        display: flex;
        align-items: center;
        padding: 0.75rem;
        background: #f8fafc;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        transition: all 0.15s ease;
    }
    
    .list-item:hover {
        background: #f1f5f9;
        transform: translateX(2px);
    }
    
    .scrollable {
        max-height: 320px;
        overflow-y: auto;
        scrollbar-width: thin;
        scrollbar-color: #cbd5e1 transparent;
    }
    .scrollable::-webkit-scrollbar { width: 6px; }
    .scrollable::-webkit-scrollbar-track { background: transparent; }
    .scrollable::-webkit-scrollbar-thumb { background-color: #cbd5e1; border-radius: 3px; }
    
    .circular-progress {
        position: relative;
        width: 100px;
        height: 100px;
    }
    
    .circular-progress svg {
        transform: rotate(-90deg);
    }
    
    .circular-progress-text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
    }
    
    .stMetric { background: transparent !important; }
    .stMetric > div { background: transparent !important; padding: 0 !important; }
    </style>
    """,
)

st.html(
    f"""
<div style="
    background: linear-gradient(135deg, #312e81 0%, #4f46e5 40%, #6366f1 100%);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.25rem;
    display: flex;
    align-items: center;
    gap: 1.25rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 12px 30px rgba(79,70,229,0.25);
">
    <div style="
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: 
            radial-gradient(ellipse at 20% 80%, rgba(99,102,241,0.4) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 20%, rgba(129,140,248,0.3) 0%, transparent 50%);
        pointer-events: none;
    "></div>
    
    <div style="
        width: 52px;
        height: 52px;
        background: rgba(255,255,255,0.2);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        border: 1px solid rgba(255,255,255,0.25);
        color: #ffffff;
    ">
        {DASH_ICONS["chart"]}
    </div>
    
    <div style="position: relative; z-index: 1; flex: 1;">
        <h1 style="
            margin: 0;
            font-size: 1.25rem;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: -0.01em;
        ">Financial Overview</h1>
        <p style="
            margin: 0.25rem 0 0 0;
            font-size: 0.8125rem;
            color: rgba(255,255,255,0.8);
        ">Transaction intelligence dashboard • {txn_count} transactions</p>
    </div>
</div>
""",
)

st.markdown("---")

insights = generate_insights(transactions)

cf = insights["cashflow"]

st.html(
    f"""
<div class="enterprise-card" style="padding: 1.5rem; margin-bottom: 1.5rem;">
    <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 1.25rem; border-bottom: 1px solid #e2e8f0; margin-bottom: 1.25rem;">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="width: 44px; height: 44px; background: linear-gradient(135deg, #0891b2 0%, #22d3ee 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(8,145,178,0.3); color: #ffffff;">
                {DASH_ICONS["wallet"]}
            </div>
            <div>
                <h2 style="margin: 0; font-size: 1.125rem; font-weight: 600; color: #0f172a;">Key Metrics</h2>
                <p style="margin: 2px 0 0 0; font-size: 0.75rem; color: #64748b;">Financial performance indicators</p>
            </div>
        </div>
        <div style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); padding: 0.5rem 1rem; border-radius: 9999px; display: flex; align-items: center; gap: 0.5rem; color: #059669;">
            {DASH_ICONS["check"]}
            <span style="font-size: 0.8125rem; font-weight: 600; color: #059669;">{len(transactions)} Records</span>
        </div>
    </div>
    
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;">
        <div class="metric-card" style="--accent-color: rgba(5,150,105,0.1); border: 1px solid #05966930;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 0.625rem;">
                    <div style="width: 36px; height: 36px; background: linear-gradient(135deg, #059669 0%, #047857 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(5,150,105,0.3); color: #ffffff;">
                        {DASH_ICONS["dollar"]}
                    </div>
                    <span style="font-size: 0.6875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #059669;">Income</span>
                </div>
                <div style="color: #059669;">{DASH_ICONS["trending_up"]}</div>
            </div>
            <div style="font-size: 1.625rem; font-weight: 700; color: #0f172a; margin-bottom: 0.25rem; font-feature-settings: 'tnum';">₹{cf["income"]:,.0f}</div>
            <div style="font-size: 0.75rem; color: #64748b;">Total credits</div>
        </div>
        
        <div class="metric-card" style="--accent-color: rgba(220,38,38,0.1); border: 1px solid #dc262630;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 0.625rem;">
                    <div style="width: 36px; height: 36px; background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(220,38,38,0.3); color: #ffffff;">
                        {DASH_ICONS["expense"]}
                    </div>
                    <span style="font-size: 0.6875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #dc2626;">Expenses</span>
                </div>
                <div style="color: #dc2626;">{DASH_ICONS["trending_down"]}</div>
            </div>
            <div style="font-size: 1.625rem; font-weight: 700; color: #0f172a; margin-bottom: 0.25rem; font-feature-settings: 'tnum';">₹{cf["expenses"]:,.0f}</div>
            <div style="font-size: 0.75rem; color: #64748b;">Total debits</div>
        </div>
        
        <div class="metric-card" style="--accent-color: rgba(8,145,178,0.1); border: 1px solid #0891b230;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 0.625rem;">
                    <div style="width: 36px; height: 36px; background: linear-gradient(135deg, #0891b2 0%, #0e7490 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(8,145,178,0.3); color: #ffffff;">
                        {DASH_ICONS["savings"]}
                    </div>
                    <span style="font-size: 0.6875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #0891b2;">Savings</span>
                </div>
                <div style="color: #0891b2;">{DASH_ICONS["zap"]}</div>
            </div>
            <div style="font-size: 1.625rem; font-weight: 700; color: #0f172a; margin-bottom: 0.25rem; font-feature-settings: 'tnum';">₹{cf["net_savings"]:,.0f}</div>
            <div style="font-size: 0.75rem; color: #64748b;">Net balance</div>
        </div>
        
        <div class="metric-card" style="--accent-color: rgba(124,58,237,0.1); border: 1px solid #7c3aed30;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 0.625rem;">
                    <div style="width: 36px; height: 36px; background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(124,58,237,0.3); color: #ffffff;">
                        {DASH_ICONS["clock"]}
                    </div>
                    <span style="font-size: 0.6875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #7c3aed;">Daily Burn</span>
                </div>
                <div style="color: #7c3aed;">{DASH_ICONS["clock"]}</div>
            </div>
            <div style="font-size: 1.625rem; font-weight: 700; color: #0f172a; margin-bottom: 0.25rem; font-feature-settings: 'tnum';">₹{cf["daily_burn"]:,.0f}</div>
            <div style="font-size: 0.75rem; color: #64748b;">Per day avg</div>
        </div>
    </div>
</div>
""",
)

progress_pct = min(cf["savings_rate"], 100)
savings_color = (
    "#059669"
    if cf["savings_rate"] > 20
    else "#d97706"
    if cf["savings_rate"] > 0
    else "#dc2626"
)
savings_status = (
    "Excellent"
    if cf["savings_rate"] > 20
    else "Needs Attention"
    if cf["savings_rate"] > 0
    else "Critical"
)
savings_message = (
    "Your savings rate is impressive"
    if cf["savings_rate"] > 20
    else "Consider reducing expenses"
    if cf["savings_rate"] > 0
    else "Expenses exceed income"
)

st.html(
    f"""
<div class="enterprise-card" style="padding: 1rem; margin-bottom: 1.5rem;">
    <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
        <div style="width: 36px; height: 36px; background: linear-gradient(135deg, {savings_color} 0%, {savings_color}dd 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; color: #ffffff;">
            {DASH_ICONS["dollar"]}
        </div>
        <div>
            <div style="font-size: 0.9375rem; font-weight: 600; color: #0f172a;">Savings Rate</div>
            <div style="font-size: 0.75rem; color: #64748b; margin-top: 1px;">{savings_message}</div>
        </div>
    </div>
    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.75rem;">
        <div style="flex: 1; background: #e2e8f0; border-radius: 8px; height: 28px; overflow: hidden;">
            <div style="width: {progress_pct}%; background: linear-gradient(90deg, {savings_color}, {savings_color}cc); height: 100%; border-radius: 8px;"></div>
        </div>
        <span style="font-size: 1.125rem; font-weight: 700; color: {savings_color}; flex-shrink: 0;">{cf["savings_rate"]}%</span>
    </div>
    <div style="display: flex; align-items: center; gap: 0.5rem;">
        <div style="color: {savings_color};">{DASH_ICONS["check"]}</div>
        <span style="font-size: 0.8125rem; font-weight: 500; color: {savings_color};">Status: {savings_status}</span>
    </div>
</div>
""",
)

st.markdown("---")

merch = insights["merchants"]

color_map = {
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

lk = insights["leakage"]
rec = insights["recurring"]

cat_col, merch_col = st.columns(2)

with cat_col:
    cat_parts = []
    if merch["by_category"]:
        sorted_cats = sorted(
            merch["by_category"], key=lambda x: x["total_spend"], reverse=True
        )
        max_spend = max(c["total_spend"] for c in sorted_cats)
        for cat in sorted_cats:
            pct = (cat["total_spend"] / max_spend) * 100
            color = color_map.get(cat["category"], "#64748b")
            cat_parts.append(f"""
            <div class="list-item">
                <div style="flex: 1; min-width: 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.375rem;">
                        <span style="font-size: 0.8125rem; color: #0f172a; font-weight: 500; max-width: 100px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{cat["category"]}</span>
                        <span style="font-size: 0.8125rem; font-weight: 600; color: #0f172a; font-feature-settings: 'tnum';">₹{cat["total_spend"]:,.0f}</span>
                    </div>
                    <div class="progress-bar" style="height: 6px;">
                        <div class="progress-bar-fill" style="width: {pct}%; background: linear-gradient(90deg, {color}, {color}cc);"></div>
                    </div>
                    <div style="font-size: 0.6875rem; color: #94a3b8; margin-top: 0.25rem;">{cat["txn_count"]} transactions</div>
                </div>
            </div>""")
    else:
        cat_parts.append(
            "<p style='color: #64748b; text-align: center; padding: 2rem;'>No categories found</p>"
        )

    st.html(
        f"""
    <div class="enterprise-card" style="padding: 1.25rem; overflow: hidden;">
        <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 1rem; border-bottom: 1px solid #e2e8f0; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <div style="width: 36px; height: 36px; background: linear-gradient(135deg, #0891b2 0%, #22d3ee 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #ffffff;">
                    {DASH_ICONS["pie_chart"]}
                </div>
                <span style="font-size: 0.9375rem; font-weight: 600; color: #0f172a;">Spending by Category</span>
            </div>
            <span style="background: #ecfdf5; color: #059669; padding: 0.25rem 0.625rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600;">{len(merch["by_category"])}</span>
        </div>
        <div class="scrollable">
            {"".join(cat_parts)}
        </div>
    </div>
    """,
    )

with merch_col:
    if merch["top_merchants"]:
        merch_items = ""
        for i, m in enumerate(merch["top_merchants"][:8], 1):
            badge_colors = {
                1: ("#d97706", "#fef3c7"),
                2: ("#64748b", "#f1f5f9"),
                3: ("#b45309", "#fef3c7"),
            }
            bgc, bgc2 = badge_colors.get(i, ("#64748b", "#f8fafc"))
            merch_items += f"""
            <div class="list-item" style="padding: 0.625rem;">
                <div style="width: 28px; height: 28px; background: linear-gradient(135deg, {bgc}, {bgc}dd); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: white; flex-shrink: 0; box-shadow: 0 2px 4px {bgc}40;">{i}</div>
                <div style="flex: 1; min-width: 0; margin-left: 0.75rem;">
                    <div style="font-size: 0.8125rem; font-weight: 600; color: #0f172a; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{m["name"]}</div>
                    <div style="font-size: 0.6875rem; color: #94a3b8;">{m["txn_count"]} transactions</div>
                </div>
                <div style="font-size: 0.875rem; font-weight: 600; color: #0f172a; flex-shrink: 0; font-feature-settings: 'tnum';">₹{m["total_spend"]:,.0f}</div>
            </div>"""
    else:
        merch_items = "<p style='color: #64748b; text-align: center; padding: 2rem;'>No merchant data</p>"

    st.html(
        f"""
    <div class="enterprise-card" style="padding: 1.25rem; overflow: hidden;">
        <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 1rem; border-bottom: 1px solid #e2e8f0; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <div style="width: 36px; height: 36px; background: linear-gradient(135deg, #d97706 0%, #b45309 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #ffffff;">
                    {DASH_ICONS["store"]}
                </div>
                <span style="font-size: 0.9375rem; font-weight: 600; color: #0f172a;">Top Merchants</span>
            </div>
            <span style="background: #fef3c7; color: #d97706; padding: 0.25rem 0.625rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600;">{len(merch["top_merchants"]) if merch["top_merchants"] else 0}</span>
        </div>
        <div class="scrollable">
            {merch_items}
        </div>
    </div>
    """,
    )

st.markdown("---")

lk_col, rec_col = st.columns(2)

lk_color = "#dc2626" if lk["small_txn_count"] > 0 else "#059669"
lk_bg = "#fef2f2" if lk["small_txn_count"] > 0 else "#ecfdf5"

with lk_col:
    lk_html = f"""
    <div class="enterprise-card" style="padding: 1.25rem; overflow: hidden;">
        <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 1rem; border-bottom: 1px solid #e2e8f0; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <div style="width: 36px; height: 36px; background: linear-gradient(135deg, {lk_color} 0%, {lk_color}dd 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px {lk_color}30; color: #ffffff;">
                    {DASH_ICONS["alert"]}
                </div>
                <span style="font-size: 0.9375rem; font-weight: 600; color: #0f172a;">Micro Leakage</span>
            </div>
            <span style="background: {lk_bg}; color: {lk_color}; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; display: flex; align-items: center; gap: 0.375rem;">
                <span style="color: {lk_color};">{DASH_ICONS["check"] if lk["small_txn_count"] == 0 else DASH_ICONS["info"]}</span>
                {"Clear" if lk["small_txn_count"] == 0 else "Found"}
            </span>
        </div>
    """

    if lk["small_txn_count"] > 0:
        lk_html += f"""
        <div style="background: {lk_bg}; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; border: 1px solid {lk_color}20;">
            <div style="display: flex; align-items: center; gap: 0.625rem; margin-bottom: 0.5rem;">
                <div style="color: {lk_color};">{DASH_ICONS["info"]}</div>
                <span style="font-size: 0.8125rem; font-weight: 600; color: {lk_color};">Potential Leakage Detected</span>
            </div>
            <p style="font-size: 0.8125rem; color: #64748b; margin: 0; line-height: 1.5;">
                <strong style="color: #0f172a;">₹{lk["total_leaked"]:,.0f}</strong> in <strong style="color: #0f172a;">{lk["small_txn_count"]}</strong> small transactions (under ₹{lk["threshold"]})
            </p>
        </div>
        """
    else:
        lk_html += f"""
        <div style="background: {lk_bg}; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; text-align: center; border: 1px solid {lk_color}20;">
            <div style="color: {lk_color}; margin-bottom: 0.5rem;">{DASH_ICONS["check"]}</div>
            <div style="font-size: 0.875rem; font-weight: 600; color: {lk_color};">No Leakage Detected</div>
            <div style="font-size: 0.75rem; color: #64748b; margin-top: 0.25rem;">Your spending is well-managed</div>
        </div>
        """

    lk_html += "</div>"
    st.html(lk_html)

    if lk["small_txn_count"] > 0:
        transactions_data = lk["transactions"] or []
        lk_df = pd.DataFrame(transactions_data)
        display_cols = [
            c
            for c in ["txn_date", "date", "description", "amount"]
            if c in lk_df.columns
        ]
        with st.expander(
            f"📄 View {lk['small_txn_count']} Records",
            expanded=False,
        ):
            if display_cols:
                st.dataframe(
                    lk_df[display_cols], use_container_width=True, hide_index=True
                )
            else:
                st.dataframe(lk_df, use_container_width=True, hide_index=True)

with rec_col:
    rec_html = f"""
    <div class="enterprise-card" style="padding: 1.25rem; overflow: hidden;">
        <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 1rem; border-bottom: 1px solid #e2e8f0; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <div style="width: 36px; height: 36px; background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(124,58,237,0.3); color: #ffffff;">
                    {DASH_ICONS["repeat"]}
                </div>
                <span style="font-size: 0.9375rem; font-weight: 600; color: #0f172a;">Recurring Payments</span>
            </div>
            <span style="background: #f5f3ff; color: #7c3aed; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600;">{rec["count"]} Sources</span>
        </div>
    """

    if rec["count"] > 0:
        rec_html += f"""
        <div style="background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%); border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem; position: relative; overflow: hidden;">
            <div style="position: absolute; top: -20px; right: -20px; width: 80px; height: 80px; background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);"></div>
            <div style="position: relative; z-index: 1;">
                <div style="font-size: 0.6875rem; color: rgba(255,255,255,0.7); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.25rem;">Monthly Estimate</div>
                <div style="font-size: 1.75rem; font-weight: 700; color: white; font-feature-settings: 'tnum';">₹{rec["total_monthly_recurring"]:,.0f}</div>
            </div>
        </div>
    </div>
    """
        st.html(rec_html)
        rec_df = pd.DataFrame(rec["recurring_payments"])
        with st.expander(
            f"💳 View {rec['count']} Payments",
            expanded=False,
        ):
            display_df = rec_df.rename(
                columns={
                    "merchant": "Merchant",
                    "monthly_estimate": "Monthly Amount",
                    "occurrences": "Times",
                }
            )
            st.dataframe(
                display_df[["Merchant", "Monthly Amount", "Times"]],
                use_container_width=True,
                hide_index=True,
            )
    else:
        rec_html += f"""
        <div style="background: #f8fafc; border-radius: 12px; padding: 2rem; text-align: center; border: 1px dashed #e2e8f0;">
            <div style="color: #94a3b8; margin-bottom: 0.75rem;">{DASH_ICONS["calendar"]}</div>
            <div style="font-size: 0.875rem; color: #64748b;">No recurring payments detected</div>
            <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 0.25rem;">Need more transaction history</div>
        </div>
    </div>
    """
        st.html(rec_html)

bh = insights["behavior"]

st.html(
    f"""
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
    <div style="display: flex; align-items: center; gap: 0.75rem;">
        <div style="width: 36px; height: 36px; background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #ffffff;">
            {DASH_ICONS["bar_chart"]}
        </div>
        <div>
            <div style="font-size: 0.9375rem; font-weight: 600; color: #0f172a;">Spending Behavior</div>
            <div style="font-size: 0.75rem; color: #64748b; margin-top: 1px;">Analyze your spending patterns</div>
        </div>
    </div>
</div>
"""
)

view = st.segmented_control(
    "View spending by",
    ["Day of Week", "Month"],
    default="Day of Week",
    key="behavior_view",
    label_visibility="collapsed",
)

if view == "Day of Week":
    daily = bh["daily"]

    st.html(
        f"""
    <div class="enterprise-card" style="padding: 1.5rem; margin-bottom: 1.5rem;">
        <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 1.25rem; border-bottom: 1px solid #e2e8f0; margin-bottom: 1.25rem;">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="width: 44px; height: 44px; background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(124,58,237,0.3);">
                    {DASH_ICONS["calendar"]}
                </div>
                <div>
                    <h2 style="margin: 0; font-size: 1.125rem; font-weight: 600; color: #0f172a;">Spending Behavior</h2>
                    <p style="margin: 2px 0 0 0; font-size: 0.75rem; color: #64748b;">Day of Week Analysis</p>
                </div>
            </div>
            <div style="background: #f5f3ff; padding: 0.5rem 1rem; border-radius: 9999px; display: flex; align-items: center; gap: 0.5rem;">
                {DASH_ICONS["calendar"]}
                <span style="font-size: 0.8125rem; font-weight: 600; color: #7c3aed;">Day of Week</span>
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
            <div class="metric-card" style="--accent-color: rgba(5,150,105,0.1); border: 1px solid #05966930;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.875rem;">
                    <div style="display: flex; align-items: center; gap: 0.625rem;">
                        <div style="width: 36px; height: 36px; background: linear-gradient(135deg, #059669 0%, #047857 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(5,150,105,0.3);">
                            {DASH_ICONS["bank"]}
                        </div>
                        <span style="font-size: 0.6875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #059669;">Weekday Avg</span>
                    </div>
                </div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #0f172a; margin-bottom: 0.25rem; font-feature-settings: 'tnum';">₹{daily["avg_weekday"]:,.0f}</div>
                <div style="font-size: 0.75rem; color: #64748b;">Mon - Fri average</div>
            </div>
            
            <div class="metric-card" style="--accent-color: rgba(217,119,6,0.1); border: 1px solid #d9770630;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.875rem;">
                    <div style="display: flex; align-items: center; gap: 0.625rem;">
                        <div style="width: 36px; height: 36px; background: linear-gradient(135deg, #d97706 0%, #b45309 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(217,119,6,0.3);">
                            {DASH_ICONS["calendar"]}
                        </div>
                        <span style="font-size: 0.6875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #d97706;">Weekend Avg</span>
                    </div>
                </div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #0f172a; margin-bottom: 0.25rem; font-feature-settings: 'tnum';">₹{daily["avg_weekend"]:,.0f}</div>
                <div style="font-size: 0.75rem; color: #64748b;">Sat - Sun average</div>
            </div>
            
            <div class="metric-card" style="--accent-color: rgba(8,145,178,0.1); border: 1px solid #0891b230;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.875rem;">
                    <div style="display: flex; align-items: center; gap: 0.625rem;">
                        <div style="width: 36px; height: 36px; background: linear-gradient(135deg, #0891b2 0%, #0e7490 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(8,145,178,0.3);">
                            {DASH_ICONS["zap"]}
                        </div>
                        <span style="font-size: 0.6875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #0891b2;">Peak Day</span>
                    </div>
                </div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #0f172a; margin-bottom: 0.25rem;">{daily["peak_day"]}</div>
                <div style="font-size: 0.75rem; color: #64748b;">Highest spending</div>
            </div>
        </div>
    """,
    )

    if daily["weekend_multiplier"] > 0:
        multiplier = daily["weekend_multiplier"]
        is_high = multiplier > 1.2
        alert_color = "#dc2626" if is_high else "#059669"
        alert_bg = "#fef2f2" if is_high else "#ecfdf5"
        alert_border = "#fecaca" if is_high else "#a7f3d0"
        alert_text_color = "#991b1b" if is_high else "#065f46"
        msg = (
            "This is significantly higher than weekdays."
            if is_high
            else "Your weekend spending is well-controlled."
        )

        st.html(
            f"""
        <div style="background: {alert_bg}; border: 1px solid {alert_border}; border-radius: 12px; padding: 1rem; margin-top: 1rem; display: flex; align-items: center; gap: 1rem;">
            <div style="width: 40px; height: 40px; background: linear-gradient(135deg, {alert_color}15 0%, {alert_color}08 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                <div style="color: {alert_color};">{DASH_ICONS["alert"] if is_high else DASH_ICONS["check"]}</div>
            </div>
            <div>
                <div style="font-size: 0.875rem; font-weight: 600; color: {alert_text_color};">
                    Weekend spending is <strong>{multiplier}x</strong> your weekday average
                </div>
                <div style="font-size: 0.75rem; color: {alert_color}cc; margin-top: 0.25rem;">{msg}</div>
            </div>
        </div>
        """,
        )

    if any(v > 0 for v in daily["chart"].values()):
        chart_df = pd.DataFrame(
            {"Day": list(daily["chart"].keys()), "Spend": list(daily["chart"].values())}
        )
        colors = [
            "#10b981"
            if d in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            else "#f59e0b"
            for d in chart_df["Day"]
        ]
        fig = px.bar(
            chart_df,
            x="Day",
            y="Spend",
            color=colors,
            text_auto=True,
        )
        fig.update_layout(
            margin=dict(l=10, r=10, t=20, b=50),
            yaxis=dict(
                title=None,
                tickprefix="₹",
                tickformat=",.0f",
                rangemode="tozero",
                automargin=True,
            ),
            xaxis=dict(title=None, tickangle=0),
            showlegend=False,
            height=320,
            plot_bgcolor="white",
            paper_bgcolor="white",
        )
        fig.update_traces(textposition="outside", texttemplate="₹%{y:,.0f}")
        st.plotly_chart(fig, use_container_width=True)

else:
    monthly = bh["monthly"]
    trend_color = (
        "#059669"
        if monthly["trend"] == "increasing"
        else "#dc2626"
        if monthly["trend"] == "decreasing"
        else "#64748b"
    )
    trend_bg = f"linear-gradient(180deg, {trend_color}08 0%, #ffffff 100%)"

    st.html(
        f"""
    <div class="enterprise-card" style="padding: 1.5rem; margin-bottom: 1.5rem;">
        <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 1.25rem; border-bottom: 1px solid #e2e8f0; margin-bottom: 1.25rem;">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="width: 44px; height: 44px; background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(124,58,237,0.3);">
                    {DASH_ICONS["calendar"]}
                </div>
                <div>
                    <h2 style="margin: 0; font-size: 1.125rem; font-weight: 600; color: #0f172a;">Spending Behavior</h2>
                    <p style="margin: 2px 0 0 0; font-size: 0.75rem; color: #64748b;">Monthly Analysis</p>
                </div>
            </div>
            <div style="background: #f5f3ff; padding: 0.5rem 1rem; border-radius: 9999px; display: flex; align-items: center; gap: 0.5rem;">
                {DASH_ICONS["calendar"]}
                <span style="font-size: 0.8125rem; font-weight: 600; color: #7c3aed;">Month</span>
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
            <div class="metric-card" style="--accent-color: rgba(8,145,178,0.1); border: 1px solid #0891b230;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.875rem;">
                    <div style="display: flex; align-items: center; gap: 0.625rem;">
                        <div style="width: 36px; height: 36px; background: linear-gradient(135deg, #0891b2 0%, #0e7490 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(8,145,178,0.3);">
                            {DASH_ICONS["dollar"]}
                        </div>
                        <span style="font-size: 0.6875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #0891b2;">Avg Monthly</span>
                    </div>
                </div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #0f172a; margin-bottom: 0.25rem; font-feature-settings: 'tnum';">₹{monthly["avg_monthly_spend"]:,.0f}</div>
                <div style="font-size: 0.75rem; color: #64748b;">Average spend</div>
            </div>
            
            <div class="metric-card" style="--accent-color: {trend_color}10; border: 1px solid {trend_color}30;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.875rem;">
                    <div style="display: flex; align-items: center; gap: 0.625rem;">
                        <div style="width: 36px; height: 36px; background: linear-gradient(135deg, {trend_color} 0%, {trend_color}dd 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px {trend_color}30;">
                            {DASH_ICONS["trending_up"] if monthly["trend"] == "increasing" else DASH_ICONS["trending_down"] if monthly["trend"] == "decreasing" else DASH_ICONS["trending_neutral"]}
                        </div>
                        <span style="font-size: 0.6875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: {trend_color};">Trend</span>
                    </div>
                </div>
                <div style="font-size: 1.5rem; font-weight: 700; color: {trend_color}; text-transform: capitalize; margin-bottom: 0.25rem;">{monthly["trend"]}</div>
                <div style="font-size: 0.75rem; color: #64748b;">{"+" if monthly["trend_pct"] > 0 else ""}{monthly["trend_pct"]:.1f}% change</div>
            </div>
            
            <div class="metric-card" style="--accent-color: rgba(100,116,139,0.1); border: 1px solid #64748b30;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.875rem;">
                    <div style="display: flex; align-items: center; gap: 0.625rem;">
                        <div style="width: 36px; height: 36px; background: linear-gradient(135deg, #64748b 0%, #475569 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(100,116,139,0.3);">
                            {DASH_ICONS["calendar"]}
                        </div>
                        <span style="font-size: 0.6875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b;">Months</span>
                    </div>
                </div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #0f172a; margin-bottom: 0.25rem;">{monthly["total_months"]}</div>
                <div style="font-size: 0.75rem; color: #64748b;">Tracked</div>
            </div>
        </div>
    """,
    )

    if monthly["highest_month"]["spend"] > 0 or monthly["lowest_month"]["spend"] > 0:
        st.html(
            f"""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
            <div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-radius: 12px; padding: 1rem; display: flex; align-items: center; gap: 1rem; border: 1px solid #fcd34d;">
                <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #d97706 0%, #b45309 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(217,119,6,0.3); flex-shrink: 0;">
                    {DASH_ICONS["trending_up"]}
                </div>
                <div>
                    <div style="font-size: 0.6875rem; font-weight: 600; text-transform: uppercase; color: #92400e; letter-spacing: 0.03em;">Highest Month</div>
                    <div style="font-size: 0.9375rem; font-weight: 700; color: #991b1b;">{monthly["highest_month"]["label"]}</div>
                    <div style="font-size: 0.8125rem; color: #b45309; font-feature-settings: 'tnum';">₹{monthly["highest_month"]["spend"]:,.0f}</div>
                </div>
            </div>
            <div style="background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); border-radius: 12px; padding: 1rem; display: flex; align-items: center; gap: 1rem; border: 1px solid #6ee7b7;">
                <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #059669 0%, #047857 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(5,150,105,0.3); flex-shrink: 0;">
                    {DASH_ICONS["trending_down"]}
                </div>
                <div>
                    <div style="font-size: 0.6875rem; font-weight: 600; text-transform: uppercase; color: #065f46; letter-spacing: 0.03em;">Lowest Month</div>
                    <div style="font-size: 0.9375rem; font-weight: 700; color: #047857;">{monthly["lowest_month"]["label"]}</div>
                    <div style="font-size: 0.8125rem; color: #059669; font-feature-settings: 'tnum';">₹{monthly["lowest_month"]["spend"]:,.0f}</div>
                </div>
            </div>
        </div>
        """,
        )

    if monthly["mom_growth"]:
        st.html(
            """
        <h4 style="margin: 1.25rem 0 1rem 0; font-size: 0.9375rem; font-weight: 600; color: #0f172a;">Month-over-Month Growth</h4>
        """,
        )

        mom_df = pd.DataFrame(monthly["mom_growth"])
        mom_df["growth_display"] = mom_df["growth_pct"].apply(
            lambda x: (
                f'<span style="display: inline-flex; align-items: center; gap: 0.25rem; color: {"#059669" if x >= 0 else "#dc2626"}; font-weight: 600;">{DASH_ICONS["trending_up"] if x >= 0 else DASH_ICONS["trending_down"]}{"+" if x >= 0 else ""}{x:.1f}%</span>'
            )
        )

        table_html = """
        <div style="background: #f8fafc; border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0;">
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr style="background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);">
                        <th style="padding: 0.75rem 1rem; text-align: left; font-size: 0.6875rem; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em;">Month</th>
                        <th style="padding: 0.75rem 1rem; text-align: left; font-size: 0.6875rem; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em;">Previous</th>
                        <th style="padding: 0.75rem 1rem; text-align: left; font-size: 0.6875rem; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em;">Spend</th>
                        <th style="padding: 0.75rem 1rem; text-align: left; font-size: 0.6875rem; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em;">Change</th>
                    </tr>
                </thead>
                <tbody>
        """
        for _, row in mom_df.iterrows():
            table_html += f"""
                    <tr style="border-top: 1px solid #e2e8f0;">
                        <td style="padding: 0.75rem 1rem; font-size: 0.8125rem; color: #0f172a; font-weight: 500;">{row["month"]}</td>
                        <td style="padding: 0.75rem 1rem; font-size: 0.8125rem; color: #64748b;">{row["prev_month"]}</td>
                        <td style="padding: 0.75rem 1rem; font-size: 0.8125rem; color: #0f172a; font-weight: 600; font-feature-settings: 'tnum';">₹{row["spend"]:,.0f}</td>
                        <td style="padding: 0.75rem 1rem; font-size: 0.8125rem;">{row["growth_display"]}</td>
                    </tr>
            """
        table_html += """
                </tbody>
            </table>
        </div>
        """
        st.html(table_html)

    if monthly["chart"]:
        chart_df = pd.DataFrame(
            {
                "Month": list(monthly["chart"].keys()),
                "Spend": list(monthly["chart"].values()),
            }
        )
        fig = px.bar(
            chart_df,
            x="Month",
            y="Spend",
            text_auto=True,
            color_discrete_sequence=["#8b5cf6"],
        )
        fig.update_layout(
            margin=dict(l=10, r=10, t=20, b=50),
            yaxis=dict(
                title=None,
                tickprefix="₹",
                tickformat=",.0f",
                rangemode="tozero",
                automargin=True,
            ),
            xaxis=dict(title=None, tickangle=0),
            showlegend=False,
            height=320,
            plot_bgcolor="white",
            paper_bgcolor="white",
        )
        fig.update_traces(textposition="outside", texttemplate="₹%{y:,.0f}")
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.html(
    """
<div class="enterprise-card" style="padding: 1.25rem; margin-bottom: 1rem;">
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <div style="width: 36px; height: 36px; background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center;">
                {DASH_ICONS["file"]}
            </div>
            <span style="font-size: 0.9375rem; font-weight: 600; color: #0f172a;">All Transactions</span>
            <span style="background: #f1f5f9; color: #64748b; padding: 0.25rem 0.625rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600;">{len(transactions)}</span>
        </div>
    </div>
</div>
""",
)

txn_df = pd.DataFrame(transactions)
display_cols = ["txn_date", "description", "amount", "category"]
existing_cols = [c for c in display_cols if c in txn_df.columns]
st.dataframe(txn_df[existing_cols], use_container_width=True, hide_index=True)

st.html(
    f"""
<div style="text-align: center; padding: 2rem 0; color: #94a3b8; font-size: 0.8125rem;">
    <div style="display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
        {DASH_ICONS["layers"]}
        <span>Finance Audit Dashboard</span>
        <span style="color: #cbd5e1;">•</span>
        <span>Powered by AI</span>
    </div>
</div>
""",
)
