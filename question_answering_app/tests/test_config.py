"""Tests for application configuration."""

import pytest

from app.config.settings import ConfigurationError, load_settings


@pytest.fixture(autouse=True)
def prevent_local_dotenv_loading(monkeypatch):
	monkeypatch.setattr(
		"app.config.settings.load_dotenv",
		lambda *_args, **_kwargs: False,
	)


def test_load_settings_from_environment(monkeypatch):
	monkeypatch.setenv("GEMINI_API_KEY", "test-key")
	monkeypatch.setenv("GEMINI_MODEL", "gemini-test-model")
	monkeypatch.setenv("TEMPERATURE", "0.7")

	settings = load_settings()

	assert settings.gemini_api_key == "test-key"
	assert settings.gemini_model == "gemini-test-model"
	assert settings.temperature == 0.7


def test_load_settings_uses_non_secret_defaults(monkeypatch):
	monkeypatch.setenv("GEMINI_API_KEY", "test-key")
	monkeypatch.delenv("GEMINI_MODEL", raising=False)
	monkeypatch.delenv("TEMPERATURE", raising=False)

	settings = load_settings()

	assert settings.gemini_model == "gemini-3.8-flash"
	assert settings.temperature == 0.2


def test_missing_api_key_has_safe_configuration_message(monkeypatch):
	monkeypatch.delenv("GEMINI_API_KEY", raising=False)

	with pytest.raises(ConfigurationError, match="Create a .env file"):
		load_settings()


@pytest.mark.parametrize("temperature", ["not-a-number", "-0.1", "2.1"])
def test_invalid_temperature_is_rejected(monkeypatch, temperature):
	monkeypatch.setenv("GEMINI_API_KEY", "test-key")
	monkeypatch.setenv("TEMPERATURE", temperature)

	with pytest.raises(ConfigurationError):
		load_settings()
