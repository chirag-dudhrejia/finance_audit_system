from agents.categorizer_agent import categorize_batch_llm

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
        """Categorize a transaction using rules first.

        Returns the matched category or "PENDING_LLM" if no rule matched.
        LLM fallback is deferred to batch processing via categorize_batch().
        """
        if not description:
            return "Uncategorized"

        desc = description.lower()

        # Rule-based matching on full description
        for keyword, category in RULES.items():
            if keyword in desc:
                return category

        # No rule matched — defer LLM to batch
        return "PENDING_LLM"

    def categorize_batch(self, descriptions: list[str]) -> list[str]:
        """Batch-categorize transactions using LLM.

        Chunks the input into groups of 15 and sends each chunk
        to the LLM in a single call. Failed chunks are retried
        with exponential backoff.

        Args:
            descriptions: List of transaction descriptions that didn't match rules.

        Returns:
            List of category strings, same order as input.
        """
        if not descriptions:
            return []

        # Pre-process: extract UPI names where applicable
        processed = []
        for desc in descriptions:
            d = desc.lower().strip() if desc else ""
            if d.startswith("upi/"):
                name = _extract_name_from_upi(desc)
                processed.append(name if name else desc)
            else:
                processed.append(desc)

        # Chunk and categorize
        chunk_size = 30
        all_results = []
        for i in range(0, len(processed), chunk_size):
            chunk = processed[i : i + chunk_size]
            results = categorize_batch_llm(chunk)
            all_results.extend(results)

        return all_results
