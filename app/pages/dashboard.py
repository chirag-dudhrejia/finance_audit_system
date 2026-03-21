import sys
import os
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import streamlit as st
import pandas as pd
import plotly.express as px
from data.repositories.transaction_repo import TransactionRepo
from services.insights import generate_insights
from components.ui import apply_theme

st.set_page_config(
    page_title="Finance Audit - Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()

DEMO_USER_ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, "demo-user"))

repo = TransactionRepo()
transactions = repo.get_transactions(DEMO_USER_ID)

txn_count = len(transactions)

with st.sidebar:
    st.image(
        "app/assets/Gemini_Generated_Image_ri1spbri1spbri1s-removebg-preview.png",
        width=250,
    )
    st.markdown(
        """
        <div class="sidebar-brand">
            <h4>Finance Audit</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p class="sidebar-section-title">Navigation</p>', unsafe_allow_html=True
    )
    st.page_link("main.py", label="📤 Upload Statement")
    st.page_link("pages/dashboard.py", label="📈 Dashboard")

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    st.markdown('<p class="sidebar-section-title">Overview</p>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="sidebar-stats">
            <div class="stat-row">
                <span class="stat-label">📊 Transactions</span>
                <span class="stat-value">{txn_count}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">🎯 Status</span>
                <span class="stat-value" style="color: #10b981;">Active</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <style>
    .page-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d4a6f 100%);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 1rem;
        color: white;
    }
    .page-header h1 {
        color: white !important;
        font-size: 1.75rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
    }
    .page-header p {
        color: rgba(255,255,255,0.8);
        font-size: 0.95rem;
        margin: 0;
    }
    .page-header .stats {
        display: flex;
        gap: 2rem;
        margin-top: 1rem;
    }
    .page-header .stat {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .page-header .stat-value {
        font-size: 1.25rem;
        font-weight: 700;
    }
    .page-header .stat-label {
        font-size: 0.8rem;
        color: rgba(255,255,255,0.7);
    }
    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #e2e8f0;
        position: relative;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
    }
    .kpi-card.income::before { background: #10b981; }
    .kpi-card.expenses::before { background: #ef4444; }
    .kpi-card.savings::before { background: #3b82f6; }
    .kpi-card.neutral::before { background: #64748b; }
    .kpi-label {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
        margin-bottom: 0.5rem;
    }
    .kpi-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #1e293b;
    }
    .kpi-subtitle {
        font-size: 0.8rem;
        color: #94a3b8;
        margin-top: 0.25rem;
    }
    .nav-btn {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        background: #f1f5f9;
        border: none;
        border-radius: 8px;
        font-size: 0.85rem;
        color: #475569;
    }
    .nav-btn.primary {
        background: #1e3a5f;
        color: white;
    }
    .scrollable {
        max-height: 350px;
        overflow-y: auto;
        scrollbar-width: thin;
        scrollbar-color: #cbd5e1 transparent;
    }
    .scrollable::-webkit-scrollbar {
        width: 6px;
    }
    .scrollable::-webkit-scrollbar-track {
        background: transparent;
    }
    .scrollable::-webkit-scrollbar-thumb {
        background-color: #cbd5e1;
        border-radius: 3px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.html(f"""
<div style="background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 50%, #7c3aed 100%); border-radius: 20px; padding: 2.5rem; margin-bottom: 0.2rem; position: relative; overflow: hidden; box-shadow: 0 8px 32px rgba(37, 99, 235, 0.25);">
    <div style="position: absolute; top: -50px; right: -50px; width: 200px; height: 200px; background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);"></div>
    <div style="position: absolute; bottom: -80px; left: -40px; width: 250px; height: 250px; background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);"></div>
    
    <div style="position: relative; z-index: 1;">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1.5rem;">
            <div>
                <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.75rem;">
                    <div style="width: 56px; height: 56px; background: rgba(255,255,255,0.2); border-radius: 16px; display: flex; align-items: center; justify-content: center; backdrop-filter: blur(10px);">
                        <span style="font-size: 1.75rem;">📈</span>
                    </div>
                    <div>
                        <h1 style="margin: 0; font-size: 1.75rem; font-weight: 800; color: white;">Financial Dashboard</h1>
                        <p style="margin: 0; font-size: 0.9rem; color: rgba(255,255,255,0.8);">Comprehensive analysis of your transactions</p>
                    </div>
                </div>
            </div>
            
            <div style="display: flex; gap: 1rem;">
                <div style="background: rgba(255,255,255,0.15); backdrop-filter: blur(10px); border-radius: 16px; padding: 1rem 1.5rem; text-align: center; border: 1px solid rgba(255,255,255,0.2);">
                    <div style="font-size: 1.75rem; font-weight: 800; color: white;">{txn_count}</div>
                    <div style="font-size: 0.75rem; color: rgba(255,255,255,0.8); text-transform: uppercase; letter-spacing: 0.05em;">Transactions</div>
                </div>
                <div style="background: rgba(255,255,255,0.15); backdrop-filter: blur(10px); border-radius: 16px; padding: 1rem 1.5rem; text-align: center; border: 1px solid rgba(255,255,255,0.2);">
                    <div style="font-size: 1.75rem; font-weight: 800; color: #34d399;">✓</div>
                    <div style="font-size: 0.75rem; color: rgba(255,255,255,0.8); text-transform: uppercase; letter-spacing: 0.05em;">Active</div>
                </div>
            </div>
        </div>
    </div>
</div>
""")

if not transactions:
    st.markdown(
        """
    <div style="text-align: center; padding: 4rem 2rem; background: white; border-radius: 16px; border: 1px solid #e2e8f0;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">📂</div>
        <h2 style="color: #1e293b; margin-bottom: 0.5rem;">No Transactions Found</h2>
        <p style="color: #64748b; margin-bottom: 1.5rem;">
            Upload a bank statement to get started with financial insights
        </p>
        <a href="/" class="nav-btn primary" style="text-decoration: none;">
            ← Upload Statement
        </a>
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.stop()

st.html(f"""
<div style="display: flex; align-items: center; justify-content: space-between; background: white; border-radius: 12px; padding: 1rem 1.5rem; margin-bottom: 0.2rem; box-shadow: 0 2px 8px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
    <div style="display: flex; align-items: center; gap: 0.75rem;">
        <span style="font-size: 0.75rem; color: #94a3b8;">Showing</span>
        <span style="background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%); color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">{len(transactions)}</span>
        <span style="font-size: 0.75rem; color: #94a3b8;">transactions</span>
    </div>
    <a href="/" style="text-decoration: none;">
        <button style="background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.5rem 1rem; font-size: 0.8rem; color: #475569; cursor: pointer; display: flex; align-items: center; gap: 0.5rem; transition: all 0.2s;">
            <span>↑</span> Upload New
        </button>
    </a>
</div>
""")

insights = generate_insights(transactions)

st.markdown("---")

cf = insights["cashflow"]

st.html(f"""
<div style="background: white; border-radius: 20px; border: 1px solid #e2e8f0; padding: 2rem; margin-bottom: 1.5rem; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);">
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.75rem;">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%); border-radius: 14px; display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 1.5rem;">📊</span>
            </div>
            <div>
                <h2 style="margin: 0; font-size: 1.25rem; font-weight: 700; color: #1e293b;">Financial Overview</h2>
                <p style="margin: 0; font-size: 0.8rem; color: #94a3b8;">Your financial snapshot at a glance</p>
            </div>
        </div>
        <div style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); padding: 0.75rem 1.25rem; border-radius: 50px; display: flex; align-items: center; gap: 0.5rem;">
            <span style="font-size: 1.25rem;">✅</span>
            <span style="font-size: 0.85rem; font-weight: 600; color: #059669;">{len(transactions)} Transactions</span>
        </div>
    </div>
    
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;">
        <div style="background: linear-gradient(180deg, #ecfdf5 0%, #ffffff 100%); border-radius: 16px; padding: 1.5rem; border: 1px solid #d1fae5; position: relative; overflow: hidden;">
            <div style="position: absolute; top: 0; right: 0; width: 80px; height: 80px; background: radial-gradient(circle, rgba(16, 185, 129, 0.1) 0%, transparent 70%);"></div>
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
                <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #10b981 0%, #059669 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 1.25rem;">💰</span>
                </div>
                <span style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #10b981;">Income</span>
            </div>
            <div style="font-size: 1.75rem; font-weight: 800; color: #065f46; margin-bottom: 0.25rem;">₹{cf["income"]:,.0f}</div>
            <div style="font-size: 0.75rem; color: #6b7280;">Total credits received</div>
        </div>
        
        <div style="background: linear-gradient(180deg, #fef2f2 0%, #ffffff 100%); border-radius: 16px; padding: 1.5rem; border: 1px solid #fecaca; position: relative; overflow: hidden;">
            <div style="position: absolute; top: 0; right: 0; width: 80px; height: 80px; background: radial-gradient(circle, rgba(239, 68, 68, 0.1) 0%, transparent 70%);"></div>
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
                <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 1.25rem;">💸</span>
                </div>
                <span style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #ef4444;">Expenses</span>
            </div>
            <div style="font-size: 1.75rem; font-weight: 800; color: #991b1b; margin-bottom: 0.25rem;">₹{cf["expenses"]:,.0f}</div>
            <div style="font-size: 0.75rem; color: #6b7280;">Total debits made</div>
        </div>
        
        <div style="background: linear-gradient(180deg, #eff6ff 0%, #ffffff 100%); border-radius: 16px; padding: 1.5rem; border: 1px solid #bfdbfe; position: relative; overflow: hidden;">
            <div style="position: absolute; top: 0; right: 0; width: 80px; height: 80px; background: radial-gradient(circle, rgba(59, 130, 246, 0.1) 0%, transparent 70%);"></div>
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
                <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 1.25rem;">🏦</span>
                </div>
                <span style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #3b82f6;">Savings</span>
            </div>
            <div style="font-size: 1.75rem; font-weight: 800; color: #1e40af; margin-bottom: 0.25rem;">₹{cf["net_savings"]:,.0f}</div>
            <div style="font-size: 0.75rem; color: #6b7280;">Income minus expenses</div>
        </div>
        
        <div style="background: linear-gradient(180deg, #f5f3ff 0%, #ffffff 100%); border-radius: 16px; padding: 1.5rem; border: 1px solid #ddd6fe; position: relative; overflow: hidden;">
            <div style="position: absolute; top: 0; right: 0; width: 80px; height: 80px; background: radial-gradient(circle, rgba(139, 92, 246, 0.1) 0%, transparent 70%);"></div>
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
                <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 1.25rem;">🔥</span>
                </div>
                <span style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #8b5cf6;">Daily Burn</span>
            </div>
            <div style="font-size: 1.75rem; font-weight: 800; color: #6d28d9; margin-bottom: 0.25rem;">₹{cf["daily_burn"]:,.0f}</div>
            <div style="font-size: 0.75rem; color: #6b7280;">Average per day</div>
        </div>
    </div>
</div>
""")

progress_pct = min(cf["savings_rate"], 100)
savings_color = (
    "#10b981"
    if cf["savings_rate"] > 20
    else "#f59e0b"
    if cf["savings_rate"] > 0
    else "#ef4444"
)
savings_icon = (
    "🎉" if cf["savings_rate"] > 20 else "💡" if cf["savings_rate"] > 0 else "⚠️"
)
savings_text = (
    "Excellent! You're saving well"
    if cf["savings_rate"] > 20
    else "Room for improvement"
    if cf["savings_rate"] > 0
    else "Spending exceeds income"
)

st.html(f"""
<div style="background: white; border-radius: 20px; border: 1px solid #e2e8f0; padding: 2rem; margin-bottom: 1.5rem; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);">
    <div style="display: grid; grid-template-columns: 1fr 200px; gap: 2rem; align-items: center;">
        <div>
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.25rem;">
                <div style="width: 44px; height: 44px; background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 1.25rem;">💰</span>
                </div>
                <div>
                    <h3 style="margin: 0; font-size: 1.1rem; font-weight: 700; color: #1e293b;">Savings Rate</h3>
                    <p style="margin: 0; font-size: 0.8rem; color: #94a3b8;">Your savings progress</p>
                </div>
            </div>
            <div style="margin-bottom: 0.75rem;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="font-size: 0.85rem; color: #64748b;">Progress</span>
                    <span style="font-size: 0.85rem; font-weight: 700; color: {savings_color};">{cf["savings_rate"]}%</span>
                </div>
                <div style="background: #f1f5f9; border-radius: 10px; height: 12px; overflow: hidden;">
                    <div style="width: {progress_pct}%; background: linear-gradient(90deg, {savings_color}, #fbbf24); height: 100%; border-radius: 10px; transition: width 0.5s ease;"></div>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1rem;">{savings_icon}</span>
                <span style="font-size: 0.85rem; color: #64748b;">{savings_text}</span>
            </div>
        </div>
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 1.5rem; background: linear-gradient(135deg, {savings_color}10 0%, {savings_color}05 100%); border-radius: 16px; border: 2px solid {savings_color}30;">
            <div style="position: relative; width: 100px; height: 100px;">
                <svg viewBox="0 0 100 100" style="transform: rotate(-90deg);">
                    <circle cx="50" cy="50" r="42" fill="none" stroke="#f1f5f9" stroke-width="10"/>
                    <circle cx="50" cy="50" r="42" fill="none" stroke="{savings_color}" stroke-width="10" stroke-dasharray="{"{264}" if progress_pct >= 100 else str(int(264 * progress_pct / 100))} 264" stroke-linecap="round"/>
                </svg>
                <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center;">
                    <div style="font-size: 1.5rem; font-weight: 800; color: {savings_color};">{cf["savings_rate"]}%</div>
                </div>
            </div>
            <div style="margin-top: 0.5rem; font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;">Saved</div>
        </div>
    </div>
</div>
""")

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
    cat_html = f"""
    <div style="background: white; border-radius: 16px; border: 1px solid #e2e8f0; padding: 1.25rem; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); overflow: hidden;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <div style="width: 36px; height: 36px; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 1.1rem;">📊</span>
                </div>
                <span style="font-size: 1rem; font-weight: 700; color: #1e293b;">Spending by Category</span>
            </div>
            <span style="background: #dbeafe; color: #2563eb; padding: 0.3rem 0.75rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600;">{len(merch["by_category"])}</span>
        </div>
        <div style="max-height: 280px; overflow-y: auto;">
    """

    if merch["by_category"]:
        sorted_cats = sorted(
            merch["by_category"], key=lambda x: x["total_spend"], reverse=True
        )
        max_spend = max(c["total_spend"] for c in sorted_cats)

        for cat in sorted_cats:
            pct = (cat["total_spend"] / max_spend) * 100
            color = color_map.get(cat["category"], "#64748b")
            cat_html += f"""
            <div style="background: #f8fafc; border-radius: 8px; padding: 0.75rem; margin-bottom: 0.5rem; overflow: hidden;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                    <span style="font-size: 0.8rem; color: #475569; font-weight: 500; max-width: 120px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{cat["category"]}</span>
                    <span style="font-size: 0.85rem; font-weight: 700; color: #1e293b;">₹{cat["total_spend"]:,.0f}</span>
                </div>
                <div style="background: #e2e8f0; border-radius: 4px; height: 6px; overflow: hidden;">
                    <div style="width: {pct}%; background: {color}; height: 100%;"></div>
                </div>
                <div style="font-size: 0.65rem; color: #94a3b8; margin-top: 0.25rem;">{cat["txn_count"]} txns</div>
            </div>
            """
    else:
        cat_html += "<p style='color: #64748b; text-align: center; padding: 1rem;'>No categories found</p>"

    cat_html += "</div></div>"
    st.html(cat_html)

with merch_col:
    merch_html = f"""
    <div style="background: white; border-radius: 16px; border: 1px solid #e2e8f0; padding: 1.25rem; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); overflow: hidden;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <div style="width: 36px; height: 36px; background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 1.1rem;">🏆</span>
                </div>
                <span style="font-size: 1rem; font-weight: 700; color: #1e293b;">Top Merchants</span>
            </div>
            <span style="background: #fef3c7; color: #d97706; padding: 0.3rem 0.75rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600;">{len(merch["top_merchants"]) if merch["top_merchants"] else 0}</span>
        </div>
        <div style="max-height: 280px; overflow-y: auto;">
    """

    if merch["top_merchants"]:
        for i, m in enumerate(merch["top_merchants"][:8], 1):
            badge_colors = {
                1: ("#f59e0b", "#fef3c7"),
                2: ("#94a3b8", "#f1f5f9"),
                3: ("#cd7f32", "#fef3c7"),
            }
            bgc, bgc2 = badge_colors.get(i, ("#64748b", "#f8fafc"))
            merch_html += f"""
            <div style="display: flex; align-items: center; gap: 0.75rem; padding: 0.6rem; background: {bgc2}; border-radius: 8px; margin-bottom: 0.4rem; overflow: hidden;">
                <div style="width: 24px; height: 24px; background: {bgc}; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.7rem; font-weight: 700; color: white; flex-shrink: 0;">{i}</div>
                <div style="flex: 1; min-width: 0; overflow: hidden;">
                    <div style="font-size: 0.8rem; font-weight: 600; color: #1e293b; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{m["name"]}</div>
                    <div style="font-size: 0.65rem; color: #94a3b8;">{m["txn_count"]} txns</div>
                </div>
                <div style="font-size: 0.85rem; font-weight: 700; color: #1e293b; flex-shrink: 0;">₹{m["total_spend"]:,.0f}</div>
            </div>
            """
    else:
        merch_html += "<p style='color: #94a3b8; text-align: center; padding: 1rem;'>No merchant data</p>"

    merch_html += "</div></div>"
    st.html(merch_html)

st.markdown("---")

lk_col, rec_col = st.columns(2)

lk_color = "#ef4444" if lk["small_txn_count"] > 0 else "#10b981"
lk_bg = "#fef2f2" if lk["small_txn_count"] > 0 else "#ecfdf5"
lk_icon = "⚠️" if lk["small_txn_count"] > 0 else "✅"

with lk_col:
    lk_html = f"""
    <div style="background: white; border-radius: 16px; border: 1px solid #e2e8f0; padding: 1.25rem; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); overflow: hidden;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <div style="width: 36px; height: 36px; background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 1.1rem;">⚠️</span>
                </div>
                <span style="font-size: 1rem; font-weight: 700; color: #1e293b;">Leakage</span>
            </div>
            <span style="background: {lk_bg}; color: {lk_color}; padding: 0.3rem 0.75rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600;">{lk_icon} {"Found" if lk["small_txn_count"] > 0 else "Clear"}</span>
        </div>
    """

    if lk["small_txn_count"] > 0:
        lk_html += f"""
        <div style="background: #fffbeb; border-radius: 12px; padding: 1rem; margin-bottom: 0.75rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem;">
                <span style="font-size: 1.5rem;">{lk_icon}</span>
                <span style="font-size: 0.85rem; font-weight: 600; color: #92400e;">Leakage Detected</span>
            </div>
            <p style="font-size: 0.75rem; color: #64748b; margin: 0; line-height: 1.4;">
                ₹{lk["total_leaked"]:,.0f} in {lk["small_txn_count"]} txns (under ₹{lk["threshold"]})
            </p>
        </div>
        """
    else:
        lk_html += """
        <div style="background: #ecfdf5; border-radius: 12px; padding: 1rem; margin-bottom: 0.75rem; text-align: center;">
            <span style="font-size: 2rem;">✅</span>
            <div style="font-size: 0.85rem; font-weight: 600; color: #065f46; margin-top: 0.5rem;">No Leakage</div>
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
        with st.expander(f"📋 View {lk['small_txn_count']} Records", expanded=False):
            if display_cols:
                st.dataframe(
                    lk_df[display_cols], use_container_width=True, hide_index=True
                )
            else:
                st.dataframe(lk_df, use_container_width=True, hide_index=True)

with rec_col:
    rec_html = f"""
    <div style="background: white; border-radius: 16px; border: 1px solid #e2e8f0; padding: 1.25rem; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); overflow: hidden;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <div style="width: 36px; height: 36px; background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 1.1rem;">🔄</span>
                </div>
                <span style="font-size: 1rem; font-weight: 700; color: #1e293b;">Recurring</span>
            </div>
            <span style="background: #f5f3ff; color: #7c3aed; padding: 0.3rem 0.75rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600;">{rec["count"]} Sources</span>
        </div>
    """

    if rec["count"] > 0:
        rec_html += f"""
        <div style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); border-radius: 12px; padding: 1rem; text-align: center;">
            <div style="font-size: 0.65rem; color: rgba(255,255,255,0.8); text-transform: uppercase; margin-bottom: 0.25rem;">Monthly</div>
            <div style="font-size: 1.5rem; font-weight: 800; color: white;">₹{rec["total_monthly_recurring"]:,.0f}</div>
        </div>
    </div>
    """
        st.html(rec_html)
        rec_df = pd.DataFrame(rec["recurring_payments"])
        with st.expander(f"💳 View {rec['count']} Payments", expanded=False):
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
        rec_html += """
        <div style="background: #f8fafc; border-radius: 12px; padding: 1.5rem; text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📭</div>
            <div style="font-size: 0.8rem; color: #94a3b8;">No recurring detected</div>
        </div>
    </div>
    """
        st.html(rec_html)

st.markdown("---")

bh = insights["behavior"]

view = st.radio(
    "View spending by",
    ["📅 Day of Week", "📆 Month"],
    horizontal=True,
    index=0,
    key="behavior_view",
)

st.markdown("---")

if view == "📅 Day of Week":
    daily = bh["daily"]

    st.html(f"""
    <div style="background: white; border-radius: 20px; border: 1px solid #e2e8f0; padding: 2rem; margin-bottom: 1.5rem; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.75rem;">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); border-radius: 14px; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 1.5rem;">📈</span>
                </div>
                <div>
                    <h2 style="margin: 0; font-size: 1.25rem; font-weight: 700; color: #1e293b;">Spending Behavior</h2>
                    <p style="margin: 0; font-size: 0.8rem; color: #94a3b8;">Day of Week Analysis</p>
                </div>
            </div>
            <div style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); padding: 0.6rem 1.25rem; border-radius: 50px; display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 0.85rem;">📅</span>
                <span style="font-size: 0.85rem; font-weight: 600; color: #2563eb;">Day of Week</span>
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
            <div style="background: linear-gradient(180deg, #ecfdf5 0%, #ffffff 100%); border-radius: 16px; padding: 1.5rem; border: 1px solid #d1fae5; position: relative; overflow: hidden;">
                <div style="position: absolute; top: 0; right: 0; width: 80px; height: 80px; background: radial-gradient(circle, rgba(16, 185, 129, 0.1) 0%, transparent 70%);"></div>
                <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
                    <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #10b981 0%, #059669 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                        <span style="font-size: 1.25rem;">💼</span>
                    </div>
                    <span style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #10b981;">Weekday Avg</span>
                </div>
                <div style="font-size: 1.75rem; font-weight: 800; color: #065f46; margin-bottom: 0.25rem;">₹{daily["avg_weekday"]:,.0f}</div>
                <div style="font-size: 0.75rem; color: #6b7280;">Mon - Fri average</div>
            </div>
            
            <div style="background: linear-gradient(180deg, #fffbeb 0%, #ffffff 100%); border-radius: 16px; padding: 1.5rem; border: 1px solid #fde68a; position: relative; overflow: hidden;">
                <div style="position: absolute; top: 0; right: 0; width: 80px; height: 80px; background: radial-gradient(circle, rgba(245, 158, 11, 0.1) 0%, transparent 70%);"></div>
                <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
                    <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                        <span style="font-size: 1.25rem;">🌴</span>
                    </div>
                    <span style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #f59e0b;">Weekend Avg</span>
                </div>
                <div style="font-size: 1.75rem; font-weight: 800; color: #92400e; margin-bottom: 0.25rem;">₹{daily["avg_weekend"]:,.0f}</div>
                <div style="font-size: 0.75rem; color: #6b7280;">Sat - Sun average</div>
            </div>
            
            <div style="background: linear-gradient(180deg, #eff6ff 0%, #ffffff 100%); border-radius: 16px; padding: 1.5rem; border: 1px solid #bfdbfe; position: relative; overflow: hidden;">
                <div style="position: absolute; top: 0; right: 0; width: 80px; height: 80px; background: radial-gradient(circle, rgba(59, 130, 246, 0.1) 0%, transparent 70%);"></div>
                <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
                    <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                        <span style="font-size: 1.25rem;">📅</span>
                    </div>
                    <span style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #3b82f6;">Peak Day</span>
                </div>
                <div style="font-size: 1.75rem; font-weight: 800; color: #1e40af; margin-bottom: 0.25rem;">{daily["peak_day"]}</div>
                <div style="font-size: 0.75rem; color: #6b7280;">Highest spending</div>
            </div>
        </div>
    """)

    if daily["weekend_multiplier"] > 0:
        multiplier = daily["weekend_multiplier"]
        is_high = multiplier > 1.2
        alert_color = "#ef4444" if is_high else "#10b981"
        alert_bg = "#fef2f2" if is_high else "#f0fdf4"
        alert_border = "#fca5a5" if is_high else "#86efac"
        alert_icon = "⚠️" if is_high else "✅"
        alert_text_color = "#991b1b" if is_high else "#065f46"
        msg = (
            "This is significantly higher than weekdays."
            if is_high
            else "Your weekend spending is well-controlled."
        )

        st.html(f"""
        <div style="background: {alert_bg}; border: 1px solid {alert_border}; border-radius: 12px; padding: 1.25rem; margin-top: 1.25rem; display: flex; align-items: center; gap: 1rem;">
            <div style="width: 44px; height: 44px; background: linear-gradient(135deg, {alert_color}20 0%, {alert_color}10 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 1.25rem;">{alert_icon}</span>
            </div>
            <div>
                <div style="font-size: 0.95rem; font-weight: 600; color: {alert_text_color};">
                    Weekend spending is <strong>{multiplier}x</strong> your weekday average
                </div>
                <div style="font-size: 0.8rem; color: {alert_color}99; margin-top: 0.25rem;">{msg}</div>
            </div>
        </div>
        """)

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
    trend_icon = (
        "📈"
        if monthly["trend"] == "increasing"
        else "📉"
        if monthly["trend"] == "decreasing"
        else "➡️"
    )
    trend_color = (
        "#10b981"
        if monthly["trend"] == "increasing"
        else "#ef4444"
        if monthly["trend"] == "decreasing"
        else "#64748b"
    )
    trend_bg = f"linear-gradient(180deg, {trend_color}15 0%, #ffffff 100%)"

    st.html(f"""
    <div style="background: white; border-radius: 20px; border: 1px solid #e2e8f0; padding: 2rem; margin-bottom: 1.5rem; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.75rem;">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); border-radius: 14px; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 1.5rem;">📈</span>
                </div>
                <div>
                    <h2 style="margin: 0; font-size: 1.25rem; font-weight: 700; color: #1e293b;">Spending Behavior</h2>
                    <p style="margin: 0; font-size: 0.8rem; color: #94a3b8;">Monthly Analysis</p>
                </div>
            </div>
            <div style="background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%); padding: 0.6rem 1.25rem; border-radius: 50px; display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 0.85rem;">📆</span>
                <span style="font-size: 0.85rem; font-weight: 600; color: #7c3aed;">Month</span>
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
            <div style="background: linear-gradient(180deg, #eff6ff 0%, #ffffff 100%); border-radius: 16px; padding: 1.5rem; border: 1px solid #bfdbfe; position: relative; overflow: hidden;">
                <div style="position: absolute; top: 0; right: 0; width: 80px; height: 80px; background: radial-gradient(circle, rgba(59, 130, 246, 0.1) 0%, transparent 70%);"></div>
                <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
                    <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                        <span style="font-size: 1.25rem;">💰</span>
                    </div>
                    <span style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #3b82f6;">Avg Monthly</span>
                </div>
                <div style="font-size: 1.75rem; font-weight: 800; color: #1e40af; margin-bottom: 0.25rem;">₹{monthly["avg_monthly_spend"]:,.0f}</div>
                <div style="font-size: 0.75rem; color: #6b7280;">Average spend</div>
            </div>
            
            <div style="background: linear-gradient(180deg, {trend_color}15 0%, #ffffff 100%); border-radius: 16px; padding: 1.5rem; border: 1px solid {trend_color}40; position: relative; overflow: hidden;">
                <div style="position: absolute; top: 0; right: 0; width: 80px; height: 80px; background: radial-gradient(circle, rgba({trend_color}, 0.1) 0%, transparent 70%);"></div>
                <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
                    <div style="width: 40px; height: 40px; background: linear-gradient(135deg, {trend_color} 0%, {trend_color}cc 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                        <span style="font-size: 1.25rem;">{trend_icon}</span>
                    </div>
                    <span style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: {trend_color};">Trend</span>
                </div>
                <div style="font-size: 1.75rem; font-weight: 800; color: {trend_color}; text-transform: capitalize; margin-bottom: 0.25rem;">{monthly["trend"]}</div>
                <div style="font-size: 0.75rem; color: #6b7280;">{"+" if monthly["trend_pct"] > 0 else ""}{monthly["trend_pct"]:.1f}% change</div>
            </div>
            
            <div style="background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%); border-radius: 16px; padding: 1.5rem; border: 1px solid #e2e8f0; position: relative; overflow: hidden;">
                <div style="position: absolute; top: 0; right: 0; width: 80px; height: 80px; background: radial-gradient(circle, rgba(100, 116, 139, 0.1) 0%, transparent 70%);"></div>
                <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
                    <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #64748b 0%, #475569 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                        <span style="font-size: 1.25rem;">📆</span>
                    </div>
                    <span style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b;">Months</span>
                </div>
                <div style="font-size: 1.75rem; font-weight: 800; color: #475569; margin-bottom: 0.25rem;">{monthly["total_months"]}</div>
                <div style="font-size: 0.75rem; color: #6b7280;">Tracked</div>
            </div>
        </div>
    """)

    if monthly["highest_month"]["spend"] > 0 or monthly["lowest_month"]["spend"] > 0:
        st.html(f"""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1.25rem;">
            <div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-radius: 12px; padding: 1.25rem; display: flex; align-items: center; gap: 1rem; border: 1px solid #fcd34d;">
                <div style="width: 44px; height: 44px; background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 1.25rem;">📈</span>
                </div>
                <div>
                    <div style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; color: #92400e;">Highest Month</div>
                    <div style="font-size: 1rem; font-weight: 700; color: #991b1b;">{monthly["highest_month"]["label"]}</div>
                    <div style="font-size: 0.85rem; color: #b45309;">₹{monthly["highest_month"]["spend"]:,.0f}</div>
                </div>
            </div>
            <div style="background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); border-radius: 12px; padding: 1.25rem; display: flex; align-items: center; gap: 1rem; border: 1px solid #6ee7b7;">
                <div style="width: 44px; height: 44px; background: linear-gradient(135deg, #10b981 0%, #059669 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 1.25rem;">📉</span>
                </div>
                <div>
                    <div style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; color: #065f46;">Lowest Month</div>
                    <div style="font-size: 1rem; font-weight: 700; color: #047857;">{monthly["lowest_month"]["label"]}</div>
                    <div style="font-size: 0.85rem; color: #059669;">₹{monthly["lowest_month"]["spend"]:,.0f}</div>
                </div>
            </div>
        </div>
        """)

    if monthly["mom_growth"]:
        st.html("""
        <h4 style="margin: 1.5rem 0 1rem 0; font-size: 0.95rem; font-weight: 600; color: #475569;">Month-over-Month Growth</h4>
        """)

        mom_df = pd.DataFrame(monthly["mom_growth"])
        mom_df["growth_display"] = mom_df["growth_pct"].apply(
            lambda x: (
                f'<span style="color: {"#10b981" if x >= 0 else "#ef4444"}; font-weight: 600;">{"+" if x >= 0 else ""}{x:.1f}%</span>'
            )
        )

        table_html = """
        <div style="background: #f8fafc; border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0;">
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr style="background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);">
                        <th style="padding: 0.85rem 1rem; text-align: left; font-size: 0.7rem; font-weight: 600; color: #64748b; text-transform: uppercase;">Month</th>
                        <th style="padding: 0.85rem 1rem; text-align: left; font-size: 0.7rem; font-weight: 600; color: #64748b; text-transform: uppercase;">Previous</th>
                        <th style="padding: 0.85rem 1rem; text-align: left; font-size: 0.7rem; font-weight: 600; color: #64748b; text-transform: uppercase;">Spend</th>
                        <th style="padding: 0.85rem 1rem; text-align: left; font-size: 0.7rem; font-weight: 600; color: #64748b; text-transform: uppercase;">Change</th>
                    </tr>
                </thead>
                <tbody>
        """
        for _, row in mom_df.iterrows():
            table_html += f"""
                    <tr style="border-top: 1px solid #e2e8f0;">
                        <td style="padding: 0.85rem 1rem; font-size: 0.85rem; color: #1e293b;">{row["month"]}</td>
                        <td style="padding: 0.85rem 1rem; font-size: 0.85rem; color: #64748b;">{row["prev_month"]}</td>
                        <td style="padding: 0.85rem 1rem; font-size: 0.85rem; color: #1e293b; font-weight: 600;">₹{row["spend"]:,.0f}</td>
                        <td style="padding: 0.85rem 1rem; font-size: 0.85rem;">{row["growth_display"]}</td>
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

with st.expander("📋 View All Transactions"):
    txn_df = pd.DataFrame(transactions)
    display_cols = ["txn_date", "description", "amount", "category"]
    existing_cols = [c for c in display_cols if c in txn_df.columns]
    st.dataframe(txn_df[existing_cols], use_container_width=True, hide_index=True)

st.markdown(
    """
<div style="text-align: center; padding: 2rem 0; color: #94a3b8; font-size: 0.85rem;">
    <p style="margin: 0;">Finance Audit Dashboard • Powered by AI</p>
</div>
""",
    unsafe_allow_html=True,
)
