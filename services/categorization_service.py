from agents.categorizer_agent import categorize_llm

RULES = {
    # Food & Dining
    "swiggy": "Food & Dining",
    "zomato": "Food & Dining",
    "zepto": "Food & Dining",
    "blinkit": "Food & Dining",
    "bigbasket": "Food & Dining",
    "dominos": "Food & Dining",
    "mcdonald": "Food & Dining",
    "kfc": "Food & Dining",
    "starbucks": "Food & Dining",
    "cafe": "Food & Dining",
    "restaurant": "Food & Dining",
    # Transport
    "uber": "Transport",
    "ola": "Transport",
    "rapido": "Transport",
    "metro": "Transport",
    "irctc": "Transport",
    "fuel": "Transport",
    "petrol": "Transport",
    "diesel": "Transport",
    # Shopping
    "amazon": "Shopping",
    "flipkart": "Shopping",
    "myntra": "Shopping",
    "ajio": "Shopping",
    "nykaa": "Shopping",
    "meesho": "Shopping",
    # Bills & Utilities
    "electricity": "Bills & Utilities",
    "water": "Bills & Utilities",
    "gas": "Bills & Utilities",
    "broadband": "Bills & Utilities",
    "jio": "Bills & Utilities",
    "airtel": "Bills & Utilities",
    "vi ": "Bills & Utilities",
    "recharge": "Bills & Utilities",
    "mobile": "Bills & Utilities",
    # Entertainment
    "netflix": "Entertainment",
    "hotstar": "Entertainment",
    "prime video": "Entertainment",
    "spotify": "Entertainment",
    "youtube": "Entertainment",
    "bookmyshow": "Entertainment",
    "gaming": "Entertainment",
    # Health
    "pharmacy": "Health",
    "apollo": "Health",
    "hospital": "Health",
    "clinic": "Health",
    "doctor": "Health",
    "medicine": "Health",
    "1mg": "Health",
    "pharmeasy": "Health",
    # Bank transfers
    "neft": "Bank Transfer",
    "imps": "Bank Transfer",
    "rtgs": "Bank Transfer",
    # ATM
    "atm": "ATM Withdrawal",
    "cash withdrawal": "ATM Withdrawal",
}


def _extract_name_from_upi(description: str) -> str:
    """Extract the name from a UPI description.

    Format: UPI/NAME/UPI_ID_or_QR/...
    """
    desc = description.strip()
    if desc.upper().startswith("UPI/"):
        parts = desc.split("/")
        if len(parts) >= 2:
            return parts[1].strip()
    return ""


class CategorizationService:
    def categorize(self, description: str) -> str:
        """Categorize a transaction using rules first, LLM as fallback."""
        if not description:
            return "Uncategorized"

        desc = description.lower()

        # Rule-based matching on full description
        for keyword, category in RULES.items():
            if keyword in desc:
                return category

        # UPI transaction - send extracted name to LLM
        if desc.startswith("upi/"):
            name = _extract_name_from_upi(description)
            if name:
                try:
                    return categorize_llm(name)
                except Exception:
                    return "Uncategorized"
            return "Uncategorized"

        # LLM fallback for non-UPI transactions
        try:
            return categorize_llm(description)
        except Exception:
            return "Uncategorized"
