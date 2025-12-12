"""Application settings for the Healthy Bite backend."""

import os


class Settings:
    """Basic application settings loaded from environment variables."""

    def __init__(self) -> None:
        self.APP_ENV: str = os.getenv("APP_ENV", "local")
        self.APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
        self.DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./healthybite.db")
        self.OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
        # OpenAI configuration (reserved for future real integration)
        self.OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.OPENAI_TIMEOUT: int = int(os.getenv("OPENAI_TIMEOUT", "30"))
        self.OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.3"))
        self.OPENAI_MAX_TOKENS: int = int(os.getenv("OPENAI_MAX_TOKENS", "512"))


settings = Settings()
