"""Recurring transaction detection: same amount + same merchant + periodic interval."""

from collections import defaultdict


def _extract_merchant(description: str) -> str:
    if description.upper().startswith("UPI/"):
        parts = description.split("/")
        if len(parts) >= 2:
            return parts[1].strip()
    return description.strip()


def compute(transactions: list[dict]) -> dict:
    # Group by (merchant, rounded_amount)
    patterns = defaultdict(list)

    for txn in transactions:
        amount = txn.get("amount")
        if amount is None:
            continue
        amt = round(abs(float(amount)), 0)
        merchant = _extract_merchant(txn.get("description", ""))
        key = (merchant, amt)
        patterns[key].append(txn.get("txn_date", ""))

    # Recurring = same (merchant, amount) appears 2+ times
    recurring = []
    for (merchant, amount), dates in patterns.items():
        if len(dates) >= 2:
            recurring.append(
                {
                    "merchant": merchant,
                    "amount": amount,
                    "occurrences": len(dates),
                    "dates": sorted(dates),
                    "monthly_estimate": amount * len(dates),
                }
            )

    recurring.sort(key=lambda x: x["monthly_estimate"], reverse=True)

    total_monthly = sum(r["monthly_estimate"] for r in recurring)

    return {
        "recurring_payments": recurring,
        "total_monthly_recurring": round(total_monthly, 2),
        "count": len(recurring),
    }
