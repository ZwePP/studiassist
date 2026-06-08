from functools import lru_cache

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()


class Settings(BaseSettings):
    app_name: str = "Stamford StudyAssist API"
    app_version: str = "2.0.0"

    ai_provider: str = Field(default="gemini", alias="AI_PROVIDER")

    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    gemini_api_key: str | None = Field(default=None, alias="GEMINI_API_KEY")
    anthropic_api_key: str | None = Field(default=None, alias="ANTHROPIC_API_KEY")

    openai_model: str = Field(default="gpt-4o-mini", alias="OPENAI_MODEL")
    gemini_model: str = Field(default="gemini-flash-lite-latest", alias="GEMINI_MODEL")
    anthropic_model: str = Field(default="claude-haiku-4-5", alias="ANTHROPIC_MODEL")

    max_ai_tokens: int = Field(default=1500, alias="MAX_AI_TOKENS")
    stream_ai_tokens: int = Field(default=800, alias="STREAM_AI_TOKENS")

    db_path: str = Field(default="db/ruvector.db", alias="DB_PATH")

    cors_origins: list[str] = [
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()