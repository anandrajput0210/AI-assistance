"""Task model and request-data validation."""

from dataclasses import asdict, dataclass
from datetime import date


PRIORITIES = ("low", "medium", "high")
STATUSES = ("pending", "in_progress", "completed")
EDITABLE_FIELDS = {"title", "description", "priority", "status", "due_date"}


class ValidationError(ValueError):
	"""Raised when task input does not match the API contract."""


@dataclass(frozen=True)
class Task:
	id: int
	title: str
	description: str
	priority: str
	status: str
	due_date: str | None

	def to_dict(self) -> dict[str, int | str | None]:
		return asdict(self)


def validate_task_payload(payload: object, partial: bool = False) -> dict[str, object]:
	if not isinstance(payload, dict):
		raise ValidationError("The request body must be a JSON object.")

	unexpected_fields = set(payload) - EDITABLE_FIELDS
	if unexpected_fields:
		fields = ", ".join(sorted(unexpected_fields))
		raise ValidationError(f"Unsupported field(s): {fields}.")
	if partial and not payload:
		raise ValidationError("Provide at least one field to update.")
	if not partial and "title" not in payload:
		raise ValidationError("The title field is required.")

	values: dict[str, object] = {}
	if not partial:
		values.update(
			description="",
			priority="medium",
			status="pending",
			due_date=None,
		)

	if "title" in payload:
		title = payload["title"]
		if not isinstance(title, str) or not title.strip():
			raise ValidationError("Title must be a non-empty string.")
		values["title"] = title.strip()

	if "description" in payload:
		description = payload["description"]
		if description is None and partial:
			description = ""
		if not isinstance(description, str):
			raise ValidationError("Description must be a string or null.")
		values["description"] = description.strip()

	if "priority" in payload:
		priority = payload["priority"]
		if not isinstance(priority, str) or priority not in PRIORITIES:
			raise ValidationError(
				f"Priority must be one of: {', '.join(PRIORITIES)}."
			)
		values["priority"] = priority

	if "status" in payload:
		status = payload["status"]
		if not isinstance(status, str) or status not in STATUSES:
			raise ValidationError(f"Status must be one of: {', '.join(STATUSES)}.")
		values["status"] = status

	if "due_date" in payload:
		due_date = payload["due_date"]
		if due_date is None and partial:
			values["due_date"] = None
		elif not isinstance(due_date, str):
			raise ValidationError("Due date must be a YYYY-MM-DD string or null.")
		elif not due_date.strip():
			values["due_date"] = None
		else:
			try:
				parsed_date = date.fromisoformat(due_date)
			except ValueError as exc:
				raise ValidationError(
					"Due date must be a valid date in YYYY-MM-DD format."
				) from exc
			if parsed_date.isoformat() != due_date:
				raise ValidationError(
					"Due date must be a valid date in YYYY-MM-DD format."
				)
			values["due_date"] = due_date

	return values
