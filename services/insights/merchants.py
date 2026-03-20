"""Merchant-level insights: top merchants, frequency, spend per merchant."""

from collections import defaultdict


def _extract_merchant(description: str) -> str:
    """Extract merchant/person name from UPI description."""
    if description.upper().startswith("UPI/"):
        parts = description.split("/")
        if len(parts) >= 2:
            return parts[1].strip()
    return description.strip()


def compute(transactions: list[dict]) -> dict:
    merchant_spend = defaultdict(float)
    merchant_count = defaultdict(int)

    for txn in transactions:
        amount = txn.get("amount")
        desc = txn.get("description", "")
        if amount is None:
            continue
        amount = abs(float(amount))
        merchant = _extract_merchant(desc)
        merchant_spend[merchant] += amount
        merchant_count[merchant] += 1

    # Sort by total spend descending
    top_merchants = sorted(
        [
            {
                "name": name,
                "total_spend": round(spend, 2),
                "txn_count": merchant_count[name],
            }
            for name, spend in merchant_spend.items()
        ],
        key=lambda x: x["total_spend"],
        reverse=True,
    )

    # Category breakdown
    category_spend = defaultdict(float)
    category_count = defaultdict(int)
    for txn in transactions:
        amount = txn.get("amount")
        cat = txn.get("category", "Uncategorized")
        if amount is None:
            continue
        category_spend[cat] += abs(float(amount))
        category_count[cat] += 1

    by_category = sorted(
        [
            {
                "category": cat,
                "total_spend": round(s, 2),
                "txn_count": category_count[cat],
            }
            for cat, s in category_spend.items()
        ],
        key=lambda x: x["total_spend"],
        reverse=True,
    )

    return {
        "top_merchants": top_merchants[:10],
        "by_category": by_category,
        "unique_merchants": len(merchant_spend),
    }
