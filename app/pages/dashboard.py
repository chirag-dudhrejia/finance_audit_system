import sys
import os
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import streamlit as st
import pandas as pd
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

st.markdown(
    """
<style>
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: white !important;
}
[data-testid="stSidebar"] a {
    color: rgba(255,255,255,0.7);
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    margin: 0.25rem 0;
    transition: all 0.2s ease;
}
[data-testid="stSidebar"] a:hover {
    background: rgba(255,255,255,0.1);
    color: white;
}
.page-header {
    background: linear-gradient(135deg, #1e3a5f 0%, #2d4a6f 100%);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
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
    margin-top: 1.5rem;
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
</style>
""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        """
    <div style="padding: 1rem 0; text-align: center;">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📊</div>
        <h1 style="font-size: 1.25rem; color: white; margin: 0;">Finance Audit</h1>
        <p style="font-size: 0.75rem; color: rgba(255,255,255,0.6); margin: 0.25rem 0 0 0;">Enterprise Edition</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown("### Navigation")

    st.page_link("main.py", label="📤 Upload Statement", icon="📤")
    st.page_link("pages/dashboard.py", label="📈 Dashboard", icon="📈")

    st.markdown("---")

    st.markdown("### Quick Stats")
    st.caption("View all analytics here")

DEMO_USER_ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, "demo-user"))

repo = TransactionRepo()
transactions = repo.get_transactions(DEMO_USER_ID)

txn_count = len(transactions)

st.markdown(
    f"""
<div class="page-header">
    <h1>📈 Financial Dashboard</h1>
    <p>Comprehensive analysis of your financial transactions</p>
    <div class="stats">
        <div class="stat">
            <span class="stat-value">📊</span>
            <span class="stat-label">Transactions</span>
        </div>
        <div class="stat">
            <span class="stat-value">{txn_count}</span>
            <span class="stat-label">Loaded</span>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

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

st.markdown(
    f"""
<div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
    <span style="font-size: 0.875rem; color: #64748b;">
        Showing <strong>{len(transactions)}</strong> transactions
    </span>
    <a href="/" style="text-decoration: none;">
        <button class="nav-btn">← Upload New</button>
    </a>
</div>
""",
    unsafe_allow_html=True,
)

insights = generate_insights(transactions)

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

cf = insights["cashflow"]

with col1:
    st.markdown(
        f"""
    <div class="kpi-card income">
        <div class="kpi-label">Total Income</div>
        <div class="kpi-value">₹{cf["income"]:,.0f}</div>
        <div class="kpi-subtitle">Credits received</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
    <div class="kpi-card expenses">
        <div class="kpi-label">Total Expenses</div>
        <div class="kpi-value">₹{cf["expenses"]:,.0f}</div>
        <div class="kpi-subtitle">Debits made</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
    <div class="kpi-card savings">
        <div class="kpi-label">Net Savings</div>
        <div class="kpi-value">₹{cf["net_savings"]:,.0f}</div>
        <div class="kpi-subtitle">Income minus expenses</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        f"""
    <div class="kpi-card neutral">
        <div class="kpi-label">Daily Burn Rate</div>
        <div class="kpi-value">₹{cf["daily_burn"]:,.0f}</div>
        <div class="kpi-subtitle">Per day average</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown("---")

progress_pct = min(cf["savings_rate"], 100)
savings_msg = (
    "Excellent!"
    if cf["savings_rate"] > 20
    else "Consider saving more"
    if cf["savings_rate"] > 0
    else "You're spending more than you earn"
)

savings_html = f"""
<div style="background: white; border-radius: 16px; border: 1px solid #e2e8f0; padding: 1.75rem; margin-bottom: 1.5rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
    <h3 style="margin: 0 0 1.5rem 0; font-size: 1.15rem; font-weight: 700; color: #1e293b; display: flex; align-items: center; gap: 0.75rem; padding-bottom: 1rem; border-bottom: 1px solid #e2e8f0;">
        💰 Savings Rate
    </h3>
    <div style="background: #f1f5f9; border-radius: 8px; height: 12px; overflow: hidden; margin-top: 1rem;">
        <div style="width: {progress_pct}%; background: linear-gradient(90deg, #3b82f6, #10b981); height: 100%; border-radius: 8px; display: flex; align-items: center; justify-content: flex-end; padding-right: 0.5rem; font-size: 0.7rem; font-weight: 600; color: white;">
            {cf["savings_rate"]}%
        </div>
    </div>
    <p style="margin-top: 1rem; font-size: 0.875rem; color: #64748b;">
        {cf["savings_rate"]}% of your income is being saved. {savings_msg}
    </p>
</div>
"""
st.html(savings_html)

st.markdown("---")

col1, col2 = st.columns([2, 1])

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

with col1:
    cat_html = """
    <div style="background: white; border-radius: 16px; border: 1px solid #e2e8f0; padding: 1.75rem; margin-bottom: 1.5rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
        <h3 style="margin: 0 0 1.5rem 0; font-size: 1.15rem; font-weight: 700; color: #1e293b; display: flex; align-items: center; gap: 0.75rem; padding-bottom: 1rem; border-bottom: 1px solid #e2e8f0;">
            📊 Spending by Category
        </h3>
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
            <div style="background: #f8fafc; border-radius: 10px; padding: 1rem; margin: 0.75rem 0; display: flex; align-items: center; gap: 1rem;">
                <div style="width: 150px; font-size: 0.95rem; color: #475569; font-weight: 500;">{cat["category"]}</div>
                <div style="flex: 1;">
                    <div style="background: #e2e8f0; border-radius: 6px; height: 32px; overflow: hidden;">
                        <div style="width: {pct}%; background: {color}; height: 100%; border-radius: 6px; display: flex; align-items: center; padding-left: 1rem; font-size: 0.8rem; font-weight: 600; color: white;">
                            {cat["txn_count"]} txns
                        </div>
                    </div>
                </div>
                <div style="width: 110px; text-align: right; font-size: 1rem; color: #1e293b; font-weight: 700;">₹{cat["total_spend"]:,.0f}</div>
            </div>
            """
    else:
        cat_html += """
        <p style="color: #64748b; text-align: center; padding: 2rem;">No categorized transactions found</p>
        """

    cat_html += "</div>"
    st.html(cat_html)

with col2:
    merch_html = """
    <div style="background: white; border-radius: 16px; border: 1px solid #e2e8f0; padding: 1.75rem; margin-bottom: 1.5rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
        <h3 style="margin: 0 0 1.5rem 0; font-size: 1.15rem; font-weight: 700; color: #1e293b; display: flex; align-items: center; gap: 0.75rem; padding-bottom: 1rem; border-bottom: 1px solid #e2e8f0;">
            🏆 Top Merchants
        </h3>
    """

    if merch["top_merchants"]:
        for i, m in enumerate(merch["top_merchants"][:5], 1):
            badge_color = (
                "#f59e0b"
                if i == 1
                else "#94a3b8"
                if i == 2
                else "#cd7f32"
                if i == 3
                else "#64748b"
            )
            merch_html += f"""
            <div style="display: flex; align-items: center; gap: 1rem; padding: 0.85rem 0; border-bottom: 1px solid #f1f5f9;">
                <div style="width: 32px; height: 32px; border-radius: 50%; background: {badge_color}; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.9rem; color: white;">{i}</div>
                <div style="flex: 1;">
                    <div style="font-weight: 600; font-size: 0.95rem; color: #1e293b;">{m["name"]}</div>
                    <div style="font-size: 0.8rem; color: #94a3b8;">{m["txn_count"]} transactions</div>
                </div>
                <div style="font-weight: 700; font-size: 1rem; color: #1e293b;">₹{m["total_spend"]:,.0f}</div>
            </div>
            """
    else:
        merch_html += """
        <p style="color: #94a3b8; text-align: center; padding: 2rem;">No merchant data available</p>
        """

    merch_html += "</div>"
    st.html(merch_html)

st.markdown("---")

col1, col2 = st.columns(2)

lk = insights["leakage"]

with col1:
    lk_html = f"""
    <div style="background: white; border-radius: 16px; border: 1px solid #e2e8f0; padding: 1.75rem; margin-bottom: 1.5rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
        <h3 style="margin: 0 0 1.5rem 0; font-size: 1.15rem; font-weight: 700; color: #1e293b; display: flex; align-items: center; gap: 0.75rem; padding-bottom: 1rem; border-bottom: 1px solid #e2e8f0;">
            ⚠️ Micro-Spending Leakage
        </h3>
    """

    if lk["small_txn_count"] > 0:
        lk_html += f"""
        <div style="background: #fffbeb; border: 1px solid #fde68a; border-radius: 12px; padding: 1.25rem; margin: 1rem 0;">
            <h4 style="margin: 0 0 0.5rem 0; font-size: 0.95rem; font-weight: 600; color: #92400e;">💸 Potential Leakage Detected</h4>
            <p style="margin: 0; font-size: 0.875rem; color: #64748b;">
                You spent <strong>₹{lk["total_leaked"]:,.0f}</strong> in <strong>{lk["small_txn_count"]}</strong> small 
                transactions (under ₹{lk["threshold"]}). These frequent small purchases can add up quickly.
            </p>
        </div>
        """
    else:
        lk_html += """
        <div style="background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 12px; padding: 1.25rem; margin: 1rem 0;">
            <h4 style="margin: 0 0 0.5rem 0; font-size: 0.95rem; font-weight: 600; color: #065f46;">✅ No Leakage Detected</h4>
            <p style="margin: 0; font-size: 0.875rem; color: #64748b;">Your spending appears well-managed with no significant micro-spending leakage.</p>
        </div>
        """

    lk_html += "</div>"
    st.html(lk_html)

    if lk["small_txn_count"] > 0:
        with st.expander("View Small Transactions"):
            lk_df = pd.DataFrame(lk["transactions"])
            st.dataframe(lk_df, use_container_width=True, hide_index=True)

rec = insights["recurring"]

with col2:
    rec_html = """
    <div style="background: white; border-radius: 16px; border: 1px solid #e2e8f0; padding: 1.75rem; margin-bottom: 1.5rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
        <h3 style="margin: 0 0 1.5rem 0; font-size: 1.15rem; font-weight: 700; color: #1e293b; display: flex; align-items: center; gap: 0.75rem; padding-bottom: 1rem; border-bottom: 1px solid #e2e8f0;">
            🔄 Recurring Payments
        </h3>
    """

    if rec["count"] > 0:
        rec_html += f"""
        <div style="background: #eff6ff; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem;">
            <div style="font-size: 0.75rem; text-transform: uppercase; color: #3b82f6; font-weight: 600; margin-bottom: 0.5rem;">
                Estimated Monthly Recurring
            </div>
            <div style="font-size: 1.75rem; font-weight: 700; color: #1e40af;">
                ₹{rec["total_monthly_recurring"]:,.0f}
            </div>
            <div style="font-size: 0.85rem; color: #64748b; margin-top: 0.25rem;">
                From {rec["count"]} recurring payment sources
            </div>
        </div>
        """

        rec_df = pd.DataFrame(rec["recurring_payments"])
        display_df = rec_df.rename(
            columns={
                "merchant": "Merchant",
                "amount": "Amount",
                "occurrences": "Times",
                "monthly_estimate": "Monthly Total",
            }
        )
        rec_html += "</div>"
        st.html(rec_html)
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        rec_html += """
        <p style="color: #94a3b8; text-align: center; padding: 2rem;">No recurring payments detected (need more data)</p>
        </div>
    """
    st.html(rec_html)

st.markdown("---")

bh = insights["behavior"]

behavior_html = f"""
<div style="background: white; border-radius: 16px; border: 1px solid #e2e8f0; padding: 1.75rem; margin-bottom: 1.5rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
    <h3 style="margin: 0 0 1.5rem 0; font-size: 1.15rem; font-weight: 700; color: #1e293b; display: flex; align-items: center; gap: 0.75rem; padding-bottom: 1rem; border-bottom: 1px solid #e2e8f0;">
        📈 Spending Behavior
    </h3>
"""
st.html(behavior_html)

view = st.radio(
    "View spending by",
    ["Day of Week", "Month"],
    horizontal=True,
    key="behavior_view",
)

if view == "Day of Week":
    daily = bh["daily"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
        <div style="background: white; border-radius: 12px; padding: 1.5rem; border: 1px solid #e2e8f0; position: relative; overflow: hidden; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);">
            <div style="position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: #10b981;"></div>
            <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; margin-bottom: 0.5rem;">Weekday Average</div>
            <div style="font-size: 1.75rem; font-weight: 700; color: #1e293b;">₹{daily["avg_weekday"]:,.0f}</div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 0.25rem;">Mon - Fri average</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div style="background: white; border-radius: 12px; padding: 1.5rem; border: 1px solid #e2e8f0; position: relative; overflow: hidden; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);">
            <div style="position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: #f59e0b;"></div>
            <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; margin-bottom: 0.5rem;">Weekend Average</div>
            <div style="font-size: 1.75rem; font-weight: 700; color: #1e293b;">₹{daily["avg_weekend"]:,.0f}</div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 0.25rem;">Sat - Sun average</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
        <div style="background: white; border-radius: 12px; padding: 1.5rem; border: 1px solid #e2e8f0; position: relative; overflow: hidden; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);">
            <div style="position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: #3b82f6;"></div>
            <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; margin-bottom: 0.5rem;">Peak Spending Day</div>
            <div style="font-size: 1.75rem; font-weight: 700; color: #1e293b;">{daily["peak_day"]}</div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 0.25rem;">Highest spending day</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    if daily["weekend_multiplier"] > 0:
        multiplier = daily["weekend_multiplier"]
        is_high = multiplier > 1.2
        alert_bg = "#fffbeb" if is_high else "#ecfdf5"
        alert_border = "#fde68a" if is_high else "#a7f3d0"
        alert_color = "#92400e" if is_high else "#065f46"
        msg = (
            "This is significantly higher than weekdays."
            if is_high
            else "Your weekend spending is well-controlled."
        )
        st.markdown(
            f"""
        <div style="background: {alert_bg}; border: 1px solid {alert_border}; border-radius: 12px; padding: 1.25rem; margin-top: 1rem;">
            <h4 style="margin: 0 0 0.5rem 0; font-size: 0.95rem; font-weight: 600; color: {alert_color};">📊 Weekend Spending Analysis</h4>
            <p style="margin: 0; font-size: 0.875rem; color: #64748b;">
                Your weekend spending is <strong>{multiplier}x</strong> your weekday average.
                {msg}
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    if any(v > 0 for v in daily["chart"].values()):
        chart_df = pd.DataFrame(
            {"Day": list(daily["chart"].keys()), "Spend": list(daily["chart"].values())}
        )
        st.bar_chart(chart_df.set_index("Day")["Spend"])

else:
    monthly = bh["monthly"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
        <div style="background: white; border-radius: 12px; padding: 1.5rem; border: 1px solid #e2e8f0; position: relative; overflow: hidden; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);">
            <div style="position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: #3b82f6;"></div>
            <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; margin-bottom: 0.5rem;">Avg Monthly Spend</div>
            <div style="font-size: 1.75rem; font-weight: 700; color: #1e293b;">₹{monthly["avg_monthly_spend"]:,.0f}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        trend_color = (
            "#10b981"
            if monthly["trend"] == "increasing"
            else "#ef4444"
            if monthly["trend"] == "decreasing"
            else "#64748b"
        )
        st.markdown(
            f"""
        <div style="background: white; border-radius: 12px; padding: 1.5rem; border: 1px solid #e2e8f0; position: relative; overflow: hidden; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);">
            <div style="position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: {trend_color};"></div>
            <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; margin-bottom: 0.5rem;">Spending Trend</div>
            <div style="font-size: 1.75rem; font-weight: 700; color: #1e293b;">{monthly["trend"].capitalize()}</div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 0.25rem;">{"+" if monthly["trend_pct"] > 0 else ""}{monthly["trend_pct"]:.1f}% change</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
        <div style="background: white; border-radius: 12px; padding: 1.5rem; border: 1px solid #e2e8f0; position: relative; overflow: hidden; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);">
            <div style="position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: #64748b;"></div>
            <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; margin-bottom: 0.5rem;">Months Tracked</div>
            <div style="font-size: 1.75rem; font-weight: 700; color: #1e293b;">{monthly["total_months"]}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    if monthly["highest_month"]["spend"] > 0 or monthly["lowest_month"]["spend"] > 0:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                f"""
            <div style="background: #fffbeb; border: 1px solid #fde68a; border-radius: 12px; padding: 1.25rem; margin-top: 1rem;">
                <h4 style="margin: 0 0 0.5rem 0; font-size: 0.95rem; font-weight: 600; color: #92400e;">📈 Highest Month</h4>
                <p style="margin: 0; font-size: 0.875rem; color: #64748b;">
                    <strong>{monthly["highest_month"]["label"]}</strong> with 
                    <strong>₹{monthly["highest_month"]["spend"]:,.0f}</strong> in spending
                </p>
            </div>
            """,
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f"""
            <div style="background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 12px; padding: 1.25rem; margin-top: 1rem;">
                <h4 style="margin: 0 0 0.5rem 0; font-size: 0.95rem; font-weight: 600; color: #065f46;">📉 Lowest Month</h4>
                <p style="margin: 0; font-size: 0.875rem; color: #64748b;">
                    <strong>{monthly["lowest_month"]["label"]}</strong> with 
                    <strong>₹{monthly["lowest_month"]["spend"]:,.0f}</strong> in spending
                </p>
            </div>
            """,
                unsafe_allow_html=True,
            )

    if monthly["mom_growth"]:
        st.markdown(
            """
        <h4 style="margin-top: 1.5rem; margin-bottom: 1rem; color: #1e293b; font-size: 1rem; font-weight: 600;">
            Month-over-Month Growth
        </h4>
        """,
            unsafe_allow_html=True,
        )

        mom_df = pd.DataFrame(monthly["mom_growth"])
        mom_df["growth_display"] = mom_df["growth_pct"].apply(
            lambda x: (
                f'<span style="color: {"#10b981" if x >= 0 else "#ef4444"};">{"+" if x >= 0 else ""}{x:.1f}%</span>'
            )
        )
        mom_df["spend_display"] = mom_df["spend"].apply(lambda x: f"₹{x:,.0f}")

        table_html = """
        <table style="width: 100%; border-collapse: collapse; margin-top: 1rem; background: #f8fafc; border-radius: 8px; overflow: hidden;">
            <thead>
                <tr style="background: #e2e8f0;">
                    <th style="padding: 1rem; text-align: left; font-size: 0.75rem; font-weight: 600; color: #475569; text-transform: uppercase;">Month</th>
                    <th style="padding: 1rem; text-align: left; font-size: 0.75rem; font-weight: 600; color: #475569; text-transform: uppercase;">Previous</th>
                    <th style="padding: 1rem; text-align: left; font-size: 0.75rem; font-weight: 600; color: #475569; text-transform: uppercase;">Spend</th>
                    <th style="padding: 1rem; text-align: left; font-size: 0.75rem; font-weight: 600; color: #475569; text-transform: uppercase;">Change</th>
                </tr>
            </thead>
            <tbody>
        """

        for _, row in mom_df.iterrows():
            table_html += f"""
                <tr style="border-bottom: 1px solid #e2e8f0;">
                    <td style="padding: 1rem; font-size: 0.9rem; color: #1e293b;">{row["month"]}</td>
                    <td style="padding: 1rem; font-size: 0.9rem; color: #1e293b;">{row["prev_month"]}</td>
                    <td style="padding: 1rem; font-size: 0.9rem; color: #1e293b;">{row["spend_display"]}</td>
                    <td style="padding: 1rem; font-size: 0.9rem;">{row["growth_display"]}</td>
                </tr>
            """

        table_html += "</tbody></table>"

        st.markdown(table_html, unsafe_allow_html=True)

    if monthly["chart"]:
        chart_df = pd.DataFrame(
            {
                "Month": list(monthly["chart"].keys()),
                "Spend": list(monthly["chart"].values()),
            }
        )
        st.bar_chart(chart_df.set_index("Month")["Spend"])

st.html("</div>")

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
