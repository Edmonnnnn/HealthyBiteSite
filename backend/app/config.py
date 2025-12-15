"""Application settings for the Healthy Bite backend."""

import os
from pathlib import Path


class Settings:
    """Basic application settings loaded from environment variables."""

    @staticmethod
    def _load_dotenv_if_present() -> None:
        """Lightweight .env loader without external deps."""
        env_path = os.getenv("HB_ENV_FILE")
        if not env_path:
            env_path = Path(__file__).resolve().parent.parent / ".env"
        try:
            path_obj = Path(env_path)
            if not path_obj.is_file():
                return
            for line in path_obj.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip()
                if key and key not in os.environ:
                    os.environ[key] = value
        except Exception:
            # fail silently; env vars can still be provided by the shell
            pass

    def __init__(self) -> None:
        # load .env once before reading values
        self._load_dotenv_if_present()
        self.APP_ENV: str = os.getenv("APP_ENV", "dev").lower()
        if self.APP_ENV not in {"dev", "prod"}:
            self.APP_ENV = "dev"
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
        self.ENABLE_DOCS: bool = self._parse_bool(os.getenv("ENABLE_DOCS"), True)
        self.APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
        self.DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./healthybite.db")
        self.AI_PROVIDER: str = os.getenv("AI_PROVIDER", "mock")
        self.OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
        self.OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        self.OPENAI_TIMEOUT_S: int = int(os.getenv("OPENAI_TIMEOUT_S") or os.getenv("OPENAI_TIMEOUT", "20"))
        self.OPENAI_BASE_URL: str | None = os.getenv("OPENAI_BASE_URL")
        # Kept for compatibility / potential tuning (not required by the new integration)
        self.OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.3"))
        self.OPENAI_MAX_TOKENS: int = int(os.getenv("OPENAI_MAX_TOKENS", "512"))
        self.DB_AUTO_CREATE: bool = self._parse_bool(os.getenv("DB_AUTO_CREATE"), False)
        cors_origins_raw = os.getenv("CORS_ALLOW_ORIGINS", "http://127.0.0.1:8080")
        self.CORS_ALLOW_ORIGINS: list[str] = self._parse_list(cors_origins_raw)
        self.CORS_ALLOW_CREDENTIALS: bool = self._parse_bool(os.getenv("CORS_ALLOW_CREDENTIALS"), False)
        self.CORS_ALLOW_METHODS: list[str] = self._parse_list(
            os.getenv("CORS_ALLOW_METHODS", "GET,POST,PUT,DELETE,OPTIONS")
        )
        self.CORS_ALLOW_HEADERS: list[str] = self._parse_list(os.getenv("CORS_ALLOW_HEADERS", "*"))

    @staticmethod
    def _parse_bool(value: str | None, default: bool) -> bool:
        if value is None:
            return default
        return value.strip().lower() in {"1", "true", "yes", "on"}

    @staticmethod
    def _parse_list(value: str | None) -> list[str]:
        if not value:
            return []
        return [item.strip() for item in value.split(",") if item.strip()]


settings = Settings()
