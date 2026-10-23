"""Application configuration loaded from environment variables."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class ConfigurationError(ValueError):
    """Raised when required application configuration is unavailable."""


@dataclass(frozen=True)
class Settings:
    """Store and validate application settings."""

    gemini_api_key: str
    gemini_model: str
    temperature: float


def load_settings() -> Settings:
    """Load settings and reject invalid configuration."""
    load_dotenv(PROJECT_ROOT / ".env")
    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    if not api_key:
        raise ConfigurationError(
            "GEMINI_API_KEY is missing. Create a .env file "
            "in the project root and add your Gemini API key."
        )

    model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()
    if not model:
        raise ConfigurationError("GEMINI_MODEL cannot be empty.")

    try:
        temperature = float(os.getenv("TEMPERATURE", "0.2"))
    except ValueError as exc:
        raise ConfigurationError("TEMPERATURE must be a number.") from exc

    if not 0.0 <= temperature <= 2.0:
        raise ConfigurationError("TEMPERATURE must be between 0.0 and 2.0.")

    return Settings(
        gemini_api_key=api_key,
        gemini_model=model,
        temperature=temperature,
    )
