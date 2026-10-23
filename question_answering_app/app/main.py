"""Streamlit question-and-answer interface."""

import logging

import streamlit as st

from app.config.settings import ConfigurationError, Settings, load_settings
from app.services.gemini_service import AnswerGenerationError, GeminiService
from app.utils.logging_config import configure_logging


logger = logging.getLogger(__name__)


def render_sidebar(settings: Settings | None) -> None:
	"""Render model information and conversation controls."""
	with st.sidebar:
		st.subheader("Settings")
		if settings is not None:
			st.caption(f"Model: `{settings.gemini_model}`")
			st.caption(f"Temperature: `{settings.temperature}`")
		else:
			st.caption("Model settings are unavailable until configuration is fixed.")

		if st.button("Clear Conversation", use_container_width=True):
			st.session_state.messages = []
			st.rerun()


def render_conversation(messages: list[dict[str, str]]) -> None:
	"""Display saved user and assistant messages in chat bubbles."""
	for message in messages:
		with st.chat_message(message["role"]):
			st.markdown(message["content"])


def main() -> None:
	"""Run the Streamlit chat application."""
	configure_logging()
	st.set_page_config(
		page_title="AI Question & Answering System",
		page_icon="💬",
	)
	st.title("AI Question & Answering System")
	st.write(
		"Ask a question and get an answer from a Google Gemini model. "
		"Continue the conversation with follow-up questions."
	)

	if "messages" not in st.session_state:
		st.session_state.messages = []

	try:
		settings = load_settings()
	except ConfigurationError as exc:
		settings = None
		logger.warning("Application configuration is incomplete.")
		st.error(str(exc))

	render_sidebar(settings)
	render_conversation(st.session_state.messages)

	if settings is None:
		st.info("Add GEMINI_API_KEY to your project-root .env file, then restart.")
		st.stop()

	prompt = st.chat_input("Ask a question")
	if prompt is None:
		return
	if not prompt.strip():
		st.warning("Enter a question before submitting.")
		return

	user_message = {"role": "user", "content": prompt.strip()}
	with st.chat_message("user"):
		st.markdown(user_message["content"])

	try:
		service = GeminiService(settings)
		with st.chat_message("assistant"):
			with st.spinner("Thinking..."):
				answer = service.generate_answer(
					[*st.session_state.messages, user_message]
				)
			st.markdown(answer)
	except AnswerGenerationError as exc:
		logger.warning("Gemini answer generation failed.")
		st.error(str(exc))
	except Exception as exc:
		logger.error("Unexpected application error (%s).", type(exc).__name__)
		st.error("An unexpected error occurred. Please try again.")
	else:
		st.session_state.messages.extend(
			[user_message, {"role": "assistant", "content": answer}]
		)


if __name__ == "__main__":
	main()
