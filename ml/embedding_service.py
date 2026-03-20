from google import genai
from core.config import settings


def get_embedding(text):
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    result = client.models.embed_content(
        model="models/embedding-001",
        contents=text,
    )
    return result.embeddings[0].values
