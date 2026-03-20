"""Micro-spending leakage detection: many small transactions that add up."""

LEAKAGE_THRESHOLD = 200  # transactions below this are "micro"


def compute(transactions: list[dict]) -> dict:
    small_txns = []
    for txn in transactions:
        amount = txn.get("amount")
        if amount is None:
            continue
        amt = abs(float(amount))
        if 0 < amt < LEAKAGE_THRESHOLD:
            small_txns.append(
                {
                    "description": txn.get("description", ""),
                    "amount": round(amt, 2),
                    "date": txn.get("txn_date", ""),
                    "category": txn.get("category", "Uncategorized"),
                }
            )

    total_leaked = sum(t["amount"] for t in small_txns)

    return {
        "small_txn_count": len(small_txns),
        "total_leaked": round(total_leaked, 2),
        "threshold": LEAKAGE_THRESHOLD,
        "transactions": sorted(small_txns, key=lambda x: x["amount"], reverse=True),
    }
