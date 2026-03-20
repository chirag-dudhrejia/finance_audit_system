"""Cash Flow Intelligence: income, expenses, savings, daily burn rate."""


def compute(transactions: list[dict]) -> dict:
    income = 0.0
    expenses = 0.0

    for txn in transactions:
        amount = txn.get("amount")
        if amount is None:
            continue
        amount = float(amount)
        if amount > 0:
            income += amount
        else:
            expenses += abs(amount)

    savings = income - expenses

    # Daily burn rate
    dates = set()
    for txn in transactions:
        d = txn.get("txn_date")
        if d:
            dates.add(d)
    num_days = max(len(dates), 1)

    daily_burn = expenses / num_days

    # Savings rate
    savings_rate = (savings / income * 100) if income > 0 else 0

    return {
        "income": round(income, 2),
        "expenses": round(expenses, 2),
        "net_savings": round(savings, 2),
        "savings_rate": round(savings_rate, 1),
        "daily_burn": round(daily_burn, 2),
        "num_days": num_days,
    }
