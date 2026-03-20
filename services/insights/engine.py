"""Insight engine: combines all insight modules into a single report."""

from services.insights import cashflow, merchants, leakage, recurring, behavior


def generate_insights(transactions: list[dict]) -> dict:
    """Generate a complete insight report from transactions."""
    if not transactions:
        return {"error": "No transactions found"}

    return {
        "cashflow": cashflow.compute(transactions),
        "merchants": merchants.compute(transactions),
        "leakage": leakage.compute(transactions),
        "recurring": recurring.compute(transactions),
        "behavior": behavior.compute(transactions),
    }
