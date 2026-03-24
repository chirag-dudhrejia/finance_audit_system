import time
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


def _parse_batch_response(response: str, count: int) -> list[str]:
    """Parse numbered batch response into a list of categories.

    Expected format:
        1: Food & Dining
        2: Transport
        ...
    """
    categories = ["Uncategorized"] * count
    for line in response.strip().splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        try:
            parts = line.split(":", 1)
            idx = int(parts[0].strip()) - 1
            cat = parts[1].strip()
            if 0 <= idx < count:
                categories[idx] = cat if cat in CATEGORIES else "Uncategorized"
        except (ValueError, IndexError):
            continue
    return categories


def categorize_batch_llm(descriptions: list[str]) -> list[str]:
    """Categorize multiple transactions in a single LLM call.

    Args:
        descriptions: List of transaction descriptions.

    Returns:
        List of category strings, same order as input.
    """
    if not descriptions:
        return []

    numbered = "\n".join(f"{i + 1}. {desc}" for i, desc in enumerate(descriptions))

    prompt = f"""
You are a financial transaction categorization engine.

Your task is to assign EXACTLY ONE category to EACH transaction.

---------------------
STRICT RULES (MANDATORY)
---------------------
1. You MUST use ONLY the categories from the provided list.
2. DO NOT create new categories.
3. DO NOT modify category names.
4. Output MUST strictly follow the required format.
5. Output MUST contain EXACTLY {len(descriptions)} lines.
6. Each line MUST correspond to the transaction number.
7. DO NOT include explanations, notes, or extra text.
8. If unsure, choose the closest matching category.
9. If no category fits, use: Uncategorized

---------------------
VALID CATEGORIES
---------------------
{", ".join(CATEGORIES)}

---------------------
TRANSACTIONS
---------------------
{numbered}

---------------------
OUTPUT FORMAT (STRICT)
---------------------
1: <category>
2: <category>
3: <category>
...

ONLY return the numbered list. NO extra text.
"""

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = llm.generate_content(prompt, max_output_tokens=2000)
            categories = _parse_batch_response(response, len(descriptions))
            return categories
        except Exception as e:
            if attempt < max_retries - 1:
                wait = 2**attempt
                print(
                    f"[CATEGORIZER] Batch LLM attempt {attempt + 1} failed: {e}. Retrying in {wait}s..."
                )
                time.sleep(wait)
            else:
                print(
                    f"[CATEGORIZER] Batch LLM failed after {max_retries} attempts: {e}. Falling back to individual calls."
                )
                return [_categorize_single_with_retry(desc) for desc in descriptions]

    return ["Uncategorized"] * len(descriptions)


def _categorize_single_with_retry(description: str) -> str:
    """Categorize a single transaction with retry on failure."""
    for attempt in range(2):
        try:
            return categorize_llm(description)
        except Exception:
            if attempt < 1:
                time.sleep(1)
    return "Uncategorized"
