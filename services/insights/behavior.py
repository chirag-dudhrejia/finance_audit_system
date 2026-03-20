"""Spending behavior patterns: daily (weekday/weekend) and monthly trends."""

from collections import defaultdict
from datetime import datetime

MONTH_NAMES = [
    "",
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]


def _parse_date(date_str: str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        return None


def compute_daily(transactions: list[dict]) -> dict:
    """Weekday vs weekend breakdown, daily chart by day-of-week."""
    day_names = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    weekday_spend = 0.0
    weekend_spend = 0.0
    weekday_count = 0
    weekend_count = 0
    daily_spend = defaultdict(float)

    for txn in transactions:
        amount = txn.get("amount")
        date_str = txn.get("txn_date")
        if amount is None or not date_str:
            continue
        amt = abs(float(amount))
        dt = _parse_date(date_str)
        if not dt:
            continue

        day_name = day_names[dt.weekday()]
        daily_spend[day_name] += amt

        if dt.weekday() < 5:
            weekday_spend += amt
            weekday_count += 1
        else:
            weekend_spend += amt
            weekend_count += 1

    avg_weekday = weekday_spend / weekday_count if weekday_count else 0
    avg_weekend = weekend_spend / weekend_count if weekend_count else 0
    peak_day = max(daily_spend, key=daily_spend.get) if daily_spend else "N/A"

    return {
        "avg_weekday": round(avg_weekday, 2),
        "avg_weekend": round(avg_weekend, 2),
        "weekend_multiplier": round(avg_weekend / avg_weekday, 1)
        if avg_weekday > 0
        else 0,
        "peak_day": peak_day,
        "chart": {day: round(daily_spend.get(day, 0), 2) for day in day_names},
    }


def compute_monthly(transactions: list[dict]) -> dict:
    """Monthly spending trends, growth, and month-over-month comparison."""
    # Group by "YYYY-MM"
    monthly_spend = defaultdict(float)
    monthly_count = defaultdict(int)
    monthly_income = defaultdict(float)

    for txn in transactions:
        amount = txn.get("amount")
        date_str = txn.get("txn_date")
        if amount is None or not date_str:
            continue

        dt = _parse_date(date_str)
        if not dt:
            continue

        month_key = dt.strftime("%Y-%m")
        amt = float(amount)
        monthly_spend[month_key] += abs(amt)
        monthly_count[month_key] += 1
        if amt > 0:
            monthly_income[month_key] += amt

    if not monthly_spend:
        return _empty_monthly()

    sorted_months = sorted(monthly_spend.keys())

    # Highest and lowest spending months
    highest_month = max(monthly_spend, key=monthly_spend.get)
    lowest_month = min(monthly_spend, key=monthly_spend.get)

    # Average monthly spend
    total_spend = sum(monthly_spend.values())
    avg_monthly = total_spend / len(sorted_months)

    # Month-over-month growth
    mom_growth = []
    for i in range(1, len(sorted_months)):
        prev = monthly_spend[sorted_months[i - 1]]
        curr = monthly_spend[sorted_months[i]]
        growth_pct = ((curr - prev) / prev * 100) if prev > 0 else 0
        mom_growth.append(
            {
                "month": sorted_months[i],
                "prev_month": sorted_months[i - 1],
                "growth_pct": round(growth_pct, 1),
                "spend": round(curr, 2),
            }
        )

    # Overall trend (first vs last month)
    if len(sorted_months) >= 2:
        first_spend = monthly_spend[sorted_months[0]]
        last_spend = monthly_spend[sorted_months[-1]]
        overall_change = (
            ((last_spend - first_spend) / first_spend * 100) if first_spend > 0 else 0
        )
        if overall_change > 10:
            trend = "increasing"
        elif overall_change < -10:
            trend = "decreasing"
        else:
            trend = "stable"
    else:
        trend = "insufficient data"
        overall_change = 0

    # Monthly savings
    monthly_net = {}
    for m in sorted_months:
        monthly_net[m] = round(monthly_income.get(m, 0) - monthly_spend[m], 2)

    # Chart data - label with month names
    chart = {}
    for m in sorted_months:
        _, month_num = m.split("-")
        label = f"{MONTH_NAMES[int(month_num)]} {m[:4]}"
        chart[label] = round(monthly_spend[m], 2)

    highest_label = (
        f"{MONTH_NAMES[int(highest_month.split('-')[1])]} {highest_month[:4]}"
    )
    lowest_label = f"{MONTH_NAMES[int(lowest_month.split('-')[1])]} {lowest_month[:4]}"

    return {
        "total_months": len(sorted_months),
        "avg_monthly_spend": round(avg_monthly, 2),
        "highest_month": {
            "label": highest_label,
            "spend": round(monthly_spend[highest_month], 2),
        },
        "lowest_month": {
            "label": lowest_label,
            "spend": round(monthly_spend[lowest_month], 2),
        },
        "trend": trend,
        "trend_pct": round(overall_change, 1),
        "mom_growth": mom_growth,
        "monthly_net": monthly_net,
        "chart": chart,
    }


def _empty_monthly():
    return {
        "total_months": 0,
        "avg_monthly_spend": 0,
        "highest_month": {"label": "N/A", "spend": 0},
        "lowest_month": {"label": "N/A", "spend": 0},
        "trend": "insufficient data",
        "trend_pct": 0,
        "mom_growth": [],
        "monthly_net": {},
        "chart": {},
    }


def compute(transactions: list[dict]) -> dict:
    """Compute both daily and monthly insights."""
    return {
        "daily": compute_daily(transactions),
        "monthly": compute_monthly(transactions),
    }
