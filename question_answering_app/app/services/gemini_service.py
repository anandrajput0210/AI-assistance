"""Gemini-backed answer generation."""

import logging
import re
from collections.abc import Sequence

from google import genai
from google.genai import errors, types

from app.config.settings import Settings
from app.prompts.qa_prompt import SYSTEM_PROMPT


logger = logging.getLogger(__name__)


class AnswerGenerationError(RuntimeError):
	"""Raised when an answer cannot be generated safely."""


class GeminiService:
	"""Encapsulate Gemini client setup and text-generation requests."""

	def __init__(self, settings: Settings, client: genai.Client | None = None) -> None:
		self._settings = settings
		self._client = client or genai.Client(api_key=settings.gemini_api_key)

	def generate_answer(self, messages: Sequence[dict[str, str]]) -> str:
		"""Generate an answer using the system prompt and chat history."""
		contents: list[types.Content] = []
		for message in messages:
			role = message.get("role")
			text = message.get("content")
			if role not in ("user", "assistant") or not isinstance(text, str):
				raise ValueError(
					"Conversation messages must contain a valid role and text."
				)
			contents.append(
				types.Content(
					role="model" if role == "assistant" else "user",
					parts=[types.Part(text=text)],
				)
			)

		if not contents:
			raise ValueError("At least one conversation message is required.")

		try:
			response = self._client.models.generate_content(
				model=self._settings.gemini_model,
				contents=contents,
				config=types.GenerateContentConfig(
					system_instruction=SYSTEM_PROMPT,
					temperature=self._settings.temperature,
					thinking_config=types.ThinkingConfig(
						thinking_level=types.ThinkingLevel.LOW,
					),
				),
			)
		except errors.APIError as exc:
			status = getattr(exc, "status", None)
			code = getattr(exc, "code", None)
			logger.error(
				"Gemini request failed (%s, HTTP %s, %s).",
				type(exc).__name__,
				code or "unknown",
				status or "unknown",
			)
			raise AnswerGenerationError(
				self._safe_error_message(exc)
			) from exc

		try:
			content = response.text
		except (AttributeError, ValueError):
			content = None
		if not isinstance(content, str) or not content.strip():
			raise AnswerGenerationError("Gemini returned an empty response.")
		logger.info("Gemini response generated successfully.")
		return content.strip()

	def _safe_error_message(self, error: errors.APIError) -> str:
		"""Return a useful provider diagnostic without exposing credentials."""
		status_code = getattr(error, "code", None)
		status = getattr(error, "status", None)
		provider_message = getattr(error, "message", None)
		if not isinstance(provider_message, str):
			provider_message = ""

		provider_message = provider_message.replace(
			self._settings.gemini_api_key,
			"[REDACTED]",
		)
		provider_message = re.sub(
			r"AIza[0-9A-Za-z_-]{20,}",
			"[REDACTED]",
			provider_message,
		)
		provider_message = " ".join(provider_message.split())[:300]

		if status_code == 400:
			summary = (
				"Gemini rejected the request. Check that GEMINI_MODEL is available "
				"for the Gemini API and that the request settings are supported."
			)
		elif status_code == 404:
			summary = (
				"Gemini could not find the requested model or API resource. Check "
				"GEMINI_MODEL and confirm the model is available to your API key."
			)
		elif status_code in (401, 403):
			summary = (
				"Gemini rejected the API credentials or access. Check GEMINI_API_KEY "
				"and the key's access to the Gemini API."
			)
		elif status_code == 429:
			summary = "Gemini quota or rate limit reached. Check your API quota and retry later."
		elif isinstance(status_code, int) and status_code >= 500:
			summary = "Gemini is temporarily unavailable. Try again later."
		else:
			summary = "Gemini could not generate an answer. Check your configuration and retry."

		details = []
		if status_code is not None:
			details.append(f"HTTP {status_code}")
		if isinstance(status, str) and status:
			details.append(status)
		if status_code in (400, 404) and provider_message:
			details.append(provider_message)

		return f"{summary} ({'; '.join(details)})." if details else summary
