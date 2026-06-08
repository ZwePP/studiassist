from config.config import settings


def get_ai_client():
    provider = settings.ai_provider.lower()

    if provider == "openai":
        from openai import OpenAI

        return OpenAI(
            api_key=settings.openai_api_key
        )

    elif provider == "gemini":
        import google.generativeai as genai

        genai.configure(
            api_key=settings.gemini_api_key
        )

        return genai

    elif provider == "anthropic":
        import anthropic

        return anthropic.Anthropic(
            api_key=settings.anthropic_api_key
        )

    raise RuntimeError(
        f"Unsupported provider: {provider}"
    )
