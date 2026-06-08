from collections.abc import Generator

from fastapi import HTTPException

from config.ai_client import get_ai_client
from config.config import settings


PROVIDER = settings.ai_provider.lower()
ai_client = get_ai_client()


def ai_error_to_http_exception(exc: Exception) -> HTTPException:
    """Translate provider exceptions into a clean HTTPException for the frontend."""
    msg = str(exc)
    code = getattr(exc, "code", None)

    if code == 429 or "ResourceExhausted" in type(exc).__name__ or "429" in msg:
        return HTTPException(
            status_code=429,
            detail="AI quota exceeded for today. Try a different provider or wait for the daily quota to reset.",
        )

    if code == 404 or "NotFound" in type(exc).__name__:
        return HTTPException(
            status_code=502,
            detail=f"AI model not found: {msg.splitlines()[0]}",
        )

    return HTTPException(
        status_code=502,
        detail=f"AI request failed: {type(exc).__name__}: {msg.splitlines()[0][:200]}",
    )


def call_ai_full(system: str, user: str) -> str:
    try:
        if PROVIDER == "openai":
            response = ai_client.chat.completions.create(
                model=settings.openai_model,
                max_tokens=settings.max_ai_tokens,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            )

            return response.choices[0].message.content or ""

        if PROVIDER == "gemini":
            model = ai_client.GenerativeModel(
                model_name=settings.gemini_model,
                system_instruction=system,
            )

            response = model.generate_content(user)
            return response.text or ""

        if PROVIDER == "anthropic":
            response = ai_client.messages.create(
                model=settings.anthropic_model,
                max_tokens=settings.max_ai_tokens,
                system=system,
                messages=[
                    {"role": "user", "content": user},
                ],
            )

            return response.content[0].text or ""

        raise RuntimeError(f"Unsupported AI provider: {PROVIDER}")

    except HTTPException:
        raise
    except Exception as exc:
        raise ai_error_to_http_exception(exc)


def stream_ai(system: str, user: str) -> Generator[str, None, None]:
    try:
        if PROVIDER == "openai":
            with ai_client.chat.completions.create(
                model=settings.openai_model,
                max_tokens=settings.stream_ai_tokens,
                stream=True,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            ) as stream:
                for chunk in stream:
                    text = chunk.choices[0].delta.content
                    if text:
                        yield text
            return

        if PROVIDER == "gemini":
            model = ai_client.GenerativeModel(
                model_name=settings.gemini_model,
                system_instruction=system,
            )

            for chunk in model.generate_content(user, stream=True):
                if chunk.text:
                    yield chunk.text
            return

        if PROVIDER == "anthropic":
            with ai_client.messages.stream(
                model=settings.anthropic_model,
                max_tokens=settings.stream_ai_tokens,
                system=system,
                messages=[
                    {"role": "user", "content": user},
                ],
            ) as stream:
                for text in stream.text_stream:
                    yield text
            return

        raise RuntimeError(f"Unsupported AI provider: {PROVIDER}")

    except HTTPException:
        raise
    except Exception as exc:
        raise ai_error_to_http_exception(exc)