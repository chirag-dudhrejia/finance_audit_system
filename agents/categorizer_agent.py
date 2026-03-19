import google.generativeai as genai
from core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

def categorizer(state):
    description = state.get("description")
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
    Categorize this transaction:
    {description}
    """

    res = model.generate_content(prompt)
    category = res.text.strip()
    return {**state, "category": category}