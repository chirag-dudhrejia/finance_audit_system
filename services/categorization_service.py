from ml.similarity_search import find_similar
from agents.categorizer_agent import categorize_llm

RULES = {
    "swiggy": "Food",
    "zomato": "Food",
    "uber": "Transport"
}

class CategorizationService:

    def categorize(self, description):
        desc = description.lower()

        # Rule-based
        for k, v in RULES.items():
            if k in desc:
                return v

        # Embedding similarity
        category = find_similar(desc)
        if category:
            return category

        # LLM fallback
        return categorize_llm(desc)