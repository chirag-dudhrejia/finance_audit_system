from enum import Enum
from typing import Optional
from google import genai


class LLMProvider(str, Enum):
    GEMINI = "gemini"
    OPENROUTER = "openrouter"


class LLMProviderManager:
    def __init__(self):
        self._gemini_client = None
        self._openrouter_client = None

    def _get_gemini_client(self):
        if self._gemini_client is None:
            from core.config import settings

            self._gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
        return self._gemini_client

    def _get_openrouter_client(self):
        if self._openrouter_client is None:
            from openai import OpenAI
            from core.config import settings

            self._openrouter_client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=settings.OPENROUTER_API_KEY,
                timeout=120.0,
            )
        return self._openrouter_client

    def generate_content(
        self,
        prompt: str,
        provider: Optional[LLMProvider] = None,
        model: Optional[str] = None,
        max_output_tokens: int = 2048,
        temperature: float = 0,
        reasoning: bool = False,
    ) -> str:
        from core.config import settings

        if provider is None:
            provider = LLMProvider(settings.LLM_PROVIDER)

        if provider == LLMProvider.GEMINI:
            return self._generate_gemini(
                prompt=prompt,
                model=model or settings.GEMINI_MODEL,
                max_output_tokens=max_output_tokens,
                temperature=temperature,
            )
        elif provider == LLMProvider.OPENROUTER:
            return self._generate_openrouter(
                prompt=prompt,
                model=model or settings.OPENROUTER_MODEL,
                temperature=temperature,
                reasoning=reasoning,
                max_output_tokens=max_output_tokens,
            )
        else:
            raise ValueError(f"Unknown provider: {provider}")

    def _generate_gemini(
        self,
        prompt: str,
        model: str,
        max_output_tokens: int,
        temperature: float,
    ) -> str:
        client = self._get_gemini_client()
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                max_output_tokens=max_output_tokens,
                temperature=temperature,
            ),
        )
        return response.text or ""

    def _generate_openrouter(
        self,
        prompt: str,
        model: str,
        temperature: float,
        reasoning: bool = False,
        max_output_tokens: int = 2048,
    ) -> str:
        client = self._get_openrouter_client()

        extra_body = {}
        if reasoning:
            extra_body["reasoning"] = {"enabled": True}

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_output_tokens,
            extra_body=extra_body if extra_body else None,
        )

        return response.choices[0].message.content or ""


llm = LLMProviderManager()
