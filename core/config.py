import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    OPENROUTER_MODEL = os.getenv(
        "OPENROUTER_MODEL", "arcee-ai/trinity-large-preview:free"
    )

    CATEGORIZATION_LLM_ENABLED = (
        os.getenv("CATEGORIZATION_LLM_ENABLED", "true").lower() == "true"
    )


settings = Settings()
