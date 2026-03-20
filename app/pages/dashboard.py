import sys
import os
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import streamlit as st
import pandas as pd
from data.repositories.transaction_repo import TransactionRepo
from services.insights import generate_insights

st.set_page_config(page_title="Dashboard", layout="wide")

st.title("Financial Dashboard")

DEMO_USER_ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, "demo-user"))

# Fetch transactions
repo = TransactionRepo()
transactions = repo.get_transactions(DEMO_USER_ID)

if not transactions:
    st.warning("No transactions found. Upload a bank statement first.")
    st.stop()

st.caption(f"{len(transactions)} transactions loaded")

# Generate insights
insights = generate_insights(transactions)

# ── Cash Flow ──────────────────────────────────────────
st.header("Cash Flow")
cf = insights["cashflow"]
col1, col2, col3, col4 = st.columns(4)
col1.metric("Income", f"Rs.{cf['income']:,.0f}")
col2.metric("Expenses", f"Rs.{cf['expenses']:,.0f}")
col3.metric("Net Savings", f"Rs.{cf['net_savings']:,.0f}")
col4.metric("Daily Burn", f"Rs.{cf['daily_burn']:,.0f}/day")

if cf["income"] > 0:
    st.progress(cf["savings_rate"] / 100, text=f"Savings Rate: {cf['savings_rate']}%")

# ── Category Breakdown ─────────────────────────────────
st.header("Spending by Category")
merch = insights["merchants"]
if merch["by_category"]:
    cat_df = pd.DataFrame(merch["by_category"])
    st.bar_chart(cat_df.set_index("category")["total_spend"])

    for cat in merch["by_category"]:
        st.caption(
            f"  {cat['category']}: Rs.{cat['total_spend']:,.0f} ({cat['txn_count']} txns)"
        )

# ── Top Merchants ──────────────────────────────────────
st.header("Top Merchants")
if merch["top_merchants"]:
    m_df = pd.DataFrame(merch["top_merchants"])
    st.dataframe(
        m_df.rename(
            columns={
                "name": "Merchant",
                "total_spend": "Total Spend (Rs.)",
                "txn_count": "Transactions",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

# ── Leakage Detection ──────────────────────────────────
st.header("Micro-Spending Leakage")
lk = insights["leakage"]
if lk["small_txn_count"] > 0:
    st.warning(
        f"You spent Rs.{lk['total_leaked']:,.0f} in {lk['small_txn_count']} "
        f"small transactions (< Rs.{lk['threshold']})"
    )
    with st.expander("Show small transactions"):
        lk_df = pd.DataFrame(lk["transactions"])
        st.dataframe(lk_df, use_container_width=True, hide_index=True)
else:
    st.success("No micro-spending leakage detected.")

# ── Recurring Payments ─────────────────────────────────
st.header("Recurring Payments")
rec = insights["recurring"]
if rec["count"] > 0:
    st.info(
        f"Detected {rec['count']} recurring payments totaling Rs.{rec['total_monthly_recurring']:,.0f}"
    )
    rec_df = pd.DataFrame(rec["recurring_payments"])
    st.dataframe(
        rec_df.rename(
            columns={
                "merchant": "Merchant",
                "amount": "Amount (Rs.)",
                "occurrences": "Times",
                "monthly_estimate": "Total (Rs.)",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )
else:
    st.caption("No recurring payments detected (need more data)")

# ── Behavior Patterns ──────────────────────────────────
st.header("Spending Behavior")
bh = insights["behavior"]

view = st.radio(
    "View by", ["Day of Week", "Month"], horizontal=True, key="behavior_view"
)

if view == "Day of Week":
    daily = bh["daily"]
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Weekday Avg", f"Rs.{daily['avg_weekday']:,.0f}")
    with col2:
        st.metric("Weekend Avg", f"Rs.{daily['avg_weekend']:,.0f}")
    with col3:
        st.metric("Peak Day", daily["peak_day"])

    if daily["weekend_multiplier"] > 0:
        st.caption(
            f"Weekend spending is {daily['weekend_multiplier']}x weekday average"
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
        st.metric("Avg Monthly Spend", f"Rs.{monthly['avg_monthly_spend']:,.0f}")
    with col2:
        delta_str = f"{monthly['trend_pct']:+.1f}%"
        st.metric(
            "Spending Trend",
            monthly["trend"].capitalize(),
            delta=delta_str if monthly["total_months"] >= 2 else None,
        )
    with col3:
        st.metric("Months Tracked", monthly["total_months"])

    # Highest and lowest months
    col1, col2 = st.columns(2)
    with col1:
        st.info(
            f"Highest: **{monthly['highest_month']['label']}** — "
            f"Rs.{monthly['highest_month']['spend']:,.0f}"
        )
    with col2:
        st.info(
            f"Lowest: **{monthly['lowest_month']['label']}** — "
            f"Rs.{monthly['lowest_month']['spend']:,.0f}"
        )

    # Month-over-month growth table
    if monthly["mom_growth"]:
        st.subheader("Month-over-Month Change")
        mom_df = pd.DataFrame(monthly["mom_growth"])
        mom_df["growth_display"] = mom_df["growth_pct"].apply(lambda x: f"{x:+.1f}%")
        mom_df["spend_display"] = mom_df["spend"].apply(lambda x: f"Rs.{x:,.0f}")
        st.dataframe(
            mom_df[["month", "prev_month", "spend_display", "growth_display"]].rename(
                columns={
                    "month": "Month",
                    "prev_month": "vs Previous",
                    "spend_display": "Spend",
                    "growth_display": "Change",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

    # Monthly chart
    if monthly["chart"]:
        chart_df = pd.DataFrame(
            {
                "Month": list(monthly["chart"].keys()),
                "Spend": list(monthly["chart"].values()),
            }
        )
        st.bar_chart(chart_df.set_index("Month")["Spend"])

# ── Raw Transactions ───────────────────────────────────
with st.expander("All Transactions"):
    txn_df = pd.DataFrame(transactions)
    display_cols = ["txn_date", "description", "amount", "category"]
    existing_cols = [c for c in display_cols if c in txn_df.columns]
    st.dataframe(txn_df[existing_cols], use_container_width=True, hide_index=True)
