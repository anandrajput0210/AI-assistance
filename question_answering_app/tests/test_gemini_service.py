"""Tests for Gemini answer generation without network access."""

from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest
from google.genai import errors

from app.config.settings import Settings
from app.services.gemini_service import AnswerGenerationError, GeminiService


@pytest.fixture
def settings():
	return Settings(
		gemini_api_key="test-key",
		gemini_model="gemini-test-model",
		temperature=0.4,
	)


def test_service_initializes_gemini_client(settings):
	with patch("app.services.gemini_service.genai.Client") as client_factory:
		service = GeminiService(settings)

	client_factory.assert_called_once_with(api_key="test-key")
	assert isinstance(service, GeminiService)


def test_generate_answer_maps_history_and_returns_text(settings):
	client = Mock()
	client.models.generate_content.return_value = SimpleNamespace(
		text="  Here is the answer.  "
	)
	service = GeminiService(settings, client=client)

	answer = service.generate_answer(
		[
			{"role": "user", "content": "What is a linked list?"},
			{"role": "assistant", "content": "A sequence of nodes."},
			{"role": "user", "content": "What is its first node called?"},
		]
	)

	assert answer == "Here is the answer."
	call = client.models.generate_content.call_args
	assert call.kwargs["model"] == "gemini-test-model"
	assert [content.role for content in call.kwargs["contents"]] == [
		"user",
		"model",
		"user",
	]
	assert call.kwargs["contents"][2].parts[0].text == (
		"What is its first node called?"
	)
	assert call.kwargs["config"].temperature == 0.4
	assert (
		call.kwargs["config"].thinking_config.thinking_level
		== "LOW"
	)


def test_provider_error_is_replaced_with_safe_message(settings):
	client = Mock()
	client.models.generate_content.side_effect = errors.APIError(
		500,
		{"message": "sensitive provider response"},
	)
	service = GeminiService(settings, client=client)

	with pytest.raises(AnswerGenerationError) as error:
		service.generate_answer([{"role": "user", "content": "Hello"}])

	assert "sensitive provider response" not in str(error.value)
	assert "Gemini is temporarily unavailable" in str(error.value)


def test_bad_request_shows_sanitized_provider_diagnostic(settings):
	client = Mock()
	client.models.generate_content.side_effect = errors.APIError(
		400,
		{
			"error": {
				"status": "INVALID_ARGUMENT",
				"message": "Invalid request with key test-key.",
			}
		},
	)
	service = GeminiService(settings, client=client)

	with pytest.raises(AnswerGenerationError) as error:
		service.generate_answer([{"role": "user", "content": "Hello"}])

	assert "HTTP 400" in str(error.value)
	assert "INVALID_ARGUMENT" in str(error.value)
	assert "Invalid request" in str(error.value)
	assert "test-key" not in str(error.value)


def test_not_found_shows_sanitized_model_diagnostic(settings):
	client = Mock()
	client.models.generate_content.side_effect = errors.APIError(
		404,
		{
			"error": {
				"status": "NOT_FOUND",
				"message": "models/gemini-test-model was not found for test-key",
			}
		},
	)
	service = GeminiService(settings, client=client)

	with pytest.raises(AnswerGenerationError) as error:
		service.generate_answer([{"role": "user", "content": "Hello"}])

	assert "HTTP 404" in str(error.value)
	assert "NOT_FOUND" in str(error.value)
	assert "models/gemini-test-model was not found" in str(error.value)
	assert "test-key" not in str(error.value)


def test_empty_or_malformed_conversation_is_rejected(settings):
	service = GeminiService(settings, client=Mock())

	with pytest.raises(ValueError, match="At least one"):
		service.generate_answer([])
	with pytest.raises(ValueError, match="valid role and text"):
		service.generate_answer([{"role": "system", "content": "bad role"}])
