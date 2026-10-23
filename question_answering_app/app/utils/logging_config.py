"""Application logging configuration."""

import logging


def configure_logging() -> None:
	"""Configure concise application logs without conversation or secret data."""
	logging.basicConfig(
		level=logging.INFO,
		format="%(asctime)s %(levelname)s %(name)s: %(message)s",
	)
