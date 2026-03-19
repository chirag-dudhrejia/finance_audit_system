from core.llm_provider import llm


def categorizer(state):
    description = state.get("description")

    prompt = f"""
Categorize this transaction:
{description}
"""

    response = llm.generate_content(prompt)
    return {**state, "category": response.strip()}
