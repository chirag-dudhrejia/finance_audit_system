from core.llm_provider import llm

CATEGORIES = [
    "Food & Dining",
    "Transport",
    "Shopping",
    "Bills & Utilities",
    "Entertainment",
    "Health",
    "Transfer",
    "Bank Transfer",
    "ATM Withdrawal",
    "Education",
    "Rent",
    "Salary",
    "Investment",
    "Insurance",
    "Subscriptions",
    "Uncategorized",
]


def categorizer(state):
    description = state.get("description", "")

    prompt = f"""Categorize this bank transaction into exactly ONE category.

Valid categories: {", ".join(CATEGORIES)}

Transaction: {description}

Reply with ONLY the category name, nothing else."""

    try:
        response = llm.generate_content(prompt, max_output_tokens=20)
        category = response.strip()
        # Validate it's a known category
        if category not in CATEGORIES:
            category = "Uncategorized"
    except Exception:
        category = "Uncategorized"

    return {**state, "category": category}


def categorize_llm(description):
    """Standalone LLM categorization for use by CategorizationService."""
    prompt = f"""Categorize this bank transaction into exactly ONE category.

Valid categories: {", ".join(CATEGORIES)}

Transaction: {description}

Reply with ONLY the category name, nothing else."""

    try:
        response = llm.generate_content(prompt, max_output_tokens=20)
        category = response.strip()
        if category not in CATEGORIES:
            return "Uncategorized"
        return category
    except Exception:
        return "Uncategorized"
