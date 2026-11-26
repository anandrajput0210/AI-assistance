"""Requirements brief: Student Task Management System

Scope note
----------
The prompt gives only the system name, not detailed scenario rules. The
requirements below define a minimal task CRUD scope. Items marked TBD or
proposed require stakeholder confirmation; authentication and unmentioned
features are not assumed.

Data model
----------
Task records use this JSON shape:

{
    "id": 1,
    "title": "Complete DS assignment",
    "description": "Finish linked-list problems",
    "priority": "high",
    "status": "pending",
    "due_date": "2026-10-25"
}

The server assigns a unique integer id. title is required and nonblank;
description and due_date may be empty or omitted. priority is low, medium,
or high (default: medium). status is pending, in_progress, or completed
(default: pending). A non-empty due_date uses YYYY-MM-DD. Field names are
normalized to description and priority.

Proposed REST API (design only; this script currently provides a CLI)
---------------------------------------------------------------------
Base path: /api/tasks

* GET /api/tasks -> 200 with {"tasks": [...]}.
* POST /api/tasks -> 201 with the created task; accepts title, description,
  priority, status, and due_date. id is assigned by the server.
* GET /api/tasks/{id} -> 200 with the task, or 404 if it does not exist.
* PATCH /api/tasks/{id} -> 200 with the updated task; only supplied fields
  change. Send null for description or due_date to clear an optional field.
* DELETE /api/tasks/{id} -> 204 on success, or 404 if it does not exist.

Invalid request data returns 400 with
{"error": {"code": "validation_error", "message": "A useful explanation"}}.
Unexpected storage failures return 500 with a generic error message; internal
paths and implementation details are not returned to clients.

Functional requirements
-----------------------
FR-001 (Create): The system shall allow a user to create a task with the
		minimum required fields agreed by stakeholders (currently TBD).
FR-002 (Read): The system shall display task details and a task list for the
		current system context; list scope and filtering rules are TBD.
FR-003 (Update): The system shall allow an existing task's supported fields
		to be changed and shall preserve fields not changed by the user.
FR-004 (Delete): The system shall allow a task to be deleted after the user
		identifies the task; confirmation and recovery behavior are TBD.
FR-005 (Validation): The system shall reject missing or invalid required
		values according to validation rules agreed by stakeholders.
FR-006 (Feedback): The system shall report whether each create, read, update,
		or delete operation succeeded and explain recoverable input errors.

Non-functional requirements (proposed; targets need agreement)
---------------------------------------------------------------
NFR-001 Usability: Task actions and validation feedback should be clear to
		the intended student users.
NFR-002 Data integrity: A successful update must not unintentionally alter
		unrelated task data; failed operations must not be reported as successful.
NFR-003 Performance: Agree response-time targets for expected task volumes
		and usage before implementation (TBD).
NFR-004 Reliability: Agree availability, backup, and recovery expectations
		based on the deployment environment (TBD).
NFR-005 Privacy/security: Agree data access, retention, and protection
		requirements based on the actual deployment and applicable policy. No
		login, roles, or authentication scheme is specified by this brief.

User stories
------------
US-001 As a student, I want to create a task so that I can record work I need
		to complete.
US-002 As a student, I want to view my available tasks so that I can review
		what has been recorded.
US-003 As a student, I want to view one task's details so that I can check
		its information.
US-004 As a student, I want to edit a task so that I can correct or update
		its information.
US-005 As a student, I want to delete a task I no longer need so that it is
		removed from the task list.
US-006 As a user, I want clear validation and operation feedback so that I
		can correct errors and understand whether an action succeeded.

Acceptance criteria for main CRUD operations
---------------------------------------------
Create (FR-001, FR-005, FR-006)
* Given valid values for all agreed required fields, when the user submits a
	new task, then one task is created and success is reported.
* Given a missing or invalid required value, when the user submits, then no
	task is created and the relevant validation error is reported.
* A newly created task can be found using the agreed read/list behavior.

Read (FR-002, FR-006)
* Given an existing task, when the user requests it by its identifier, then
	its stored details are displayed.
* Given no matching task, when the user requests an identifier, then a
	not-found result is reported without displaying another task as a match.
* When the user requests the task list, then the system returns tasks within
	the agreed list scope; empty-list behavior is clearly indicated.

Update (FR-003, FR-005, FR-006)
* Given an existing task and valid changes, when the user saves them, then
	the changes are persisted and success is reported.
* Fields not included in the change remain unchanged.
* Given invalid changes, then the update is rejected, the prior task data is
	preserved, and validation feedback is shown.
* Given a nonexistent task identifier, then no task is changed and a
	not-found result is reported.

Delete (FR-004, FR-006)
* Given an existing task, when the user confirms the agreed delete action,
	then the task is removed from subsequent reads and success is reported.
* Given a nonexistent task identifier, then no other task is removed and a
	not-found result is reported.
* If confirmation is required by the agreed design and the user cancels,
	then the task remains unchanged.

Edge cases to resolve or test
-----------------------------
* Empty, whitespace-only, overlong, malformed, or boundary-length field
	values; exact constraints are TBD.
* Duplicate task submissions, duplicate titles, and whether duplicates are
	permitted.
* Reading, updating, or deleting an unknown, already deleted, or malformed
	identifier.
* Updating with no changed fields, or with only some fields supplied.
* Concurrent edits/deletion of the same task and conflict behavior.
* Empty task list and unusually large task lists; pagination/sorting TBD.
* Storage failure during create, update, or delete, including whether an
	operation can be partially applied.
* Whether deletion is permanent or recoverable; no recovery feature is
	assumed.

Unanswered stakeholder questions
--------------------------------
1. What fields define a task (for example, title, description, due date, or
	 status), and which are required? These are examples, not assumed features.
2. Is the system single-user, shared, or multi-user? What defines task
	 ownership and list visibility?
3. Is authentication or authorization required? If so, what policy applies?
4. What platform, storage method, and deployment environment are intended?
5. What validation limits, duplicate rules, sorting, search, and filtering
	 are required?
6. Should deletion be permanent, confirmed, or recoverable?
7. What performance, availability, backup, privacy, and retention targets
	 must be met?
8. What should happen when two users or processes edit the same task?
"""

"""A small command-line student task manager.

Tasks are stored in ``tasks.json`` next to this script.
"""

import json
import os
from pathlib import Path
import tempfile
from datetime import datetime


DATA_FILE = Path(__file__).with_name("tasks.json")
PRIORITIES = ("low", "medium", "high")
STATUSES = ("pending", "in_progress", "completed")


class TaskStoreError(Exception):
	"""Raised when task data cannot be safely read or saved."""


def load_tasks():
	if not DATA_FILE.exists():
		return []
	try:
		with DATA_FILE.open("r", encoding="utf-8") as file:
			tasks = json.load(file)
		if not isinstance(tasks, list) or any(not isinstance(t, dict) for t in tasks):
			raise ValueError("the data must be a list of task records")
		return tasks
	except (OSError, json.JSONDecodeError, ValueError) as exc:
		raise TaskStoreError(f"Could not read {DATA_FILE.name}: {exc}") from exc


def save_tasks(tasks):
	"""Atomically replace the data file so a failed save does not truncate it."""
	temporary_path = None
	try:
		with tempfile.NamedTemporaryFile(
			"w", encoding="utf-8", dir=DATA_FILE.parent, delete=False
		) as file:
			temporary_path = Path(file.name)
			json.dump(tasks, file, ensure_ascii=False, indent=2)
			file.write("\n")
		os.replace(temporary_path, DATA_FILE)
	except (OSError, TypeError, ValueError) as exc:
		if temporary_path is not None:
			try:
				temporary_path.unlink(missing_ok=True)
			except OSError:
				pass
		raise TaskStoreError(f"Could not save tasks: {exc}") from exc


def find_task(tasks, task_id):
	return next((task for task in tasks if task.get("id") == task_id), None)


def prompt_nonempty(label, current=None):
	while True:
		suffix = f" [{current}]" if current else ""
		value = input(f"{label}{suffix}: ").strip()
		if not value and current is not None:
			return current
		if value:
			return value
		print(f"{label} is required.")


def list_tasks(tasks):
	if not tasks:
		print("No tasks found.")
		return
	print(f"{'ID':<6} {'PRIORITY':<10} {'STATUS':<12} {'DUE DATE':<12} TITLE")
	print("-" * 74)
	for task in tasks:
		print(
			f"{task.get('id', '?'):<6} "
			f"{task.get('priority', 'medium'):<10} "
			f"{task.get('status', '?'):<12} "
			f"{task.get('due_date') or '-':<12} "
			f"{task.get('title', '(untitled)')}"
		)


def show_task(task):
	print(f"\nID:          {task['id']}")
	print(f"Title:       {task['title']}")
	print(f"Description: {task.get('description') or '-'}")
	print(f"Priority:    {task.get('priority', 'medium')}")
	print(f"Due date:    {task.get('due_date') or '-'}")
	print(f"Status:      {task['status']}\n")


def create_task(tasks):
	title = prompt_nonempty("Title")
	description = input("Description (optional): ").strip()
	print("Priorities: " + ", ".join(PRIORITIES))
	priority = input("Priority [medium]: ").strip() or "medium"
	if priority not in PRIORITIES:
		print("Invalid priority. Task was not created.")
		return
	due_date = input("Due date (optional, YYYY-MM-DD): ").strip()
	if due_date:
		try:
			datetime.strptime(due_date, "%Y-%m-%d")
		except ValueError:
			print("Invalid due date. Use YYYY-MM-DD. Task was not created.")
			return
	print("Statuses: " + ", ".join(STATUSES))
	status = input("Status [pending]: ").strip() or STATUSES[0]
	if status not in STATUSES:
		print("Invalid status. Task was not created.")
		return
	next_id = max((int(t.get("id", 0)) for t in tasks if str(t.get("id", "0")).isdigit()), default=0) + 1
	task = {
		"id": next_id,
		"title": title,
		"description": description,
		"priority": priority,
		"due_date": due_date,
		"status": status,
	}
	updated_tasks = [*tasks, task]
	save_tasks(updated_tasks)
	tasks.append(task)
	print(f"Task {next_id} created.")


def get_task_id():
	raw = input("Task ID: ").strip()
	if not raw.isdigit():
		print("Please enter a valid numeric task ID.")
		return None
	return int(raw)


def view_task(tasks):
	task_id = get_task_id()
	if task_id is None:
		return
	task = find_task(tasks, task_id)
	if task is None:
		print("Task not found.")
	else:
		show_task(task)


def update_task(tasks):
	task_id = get_task_id()
	if task_id is None:
		return
	task = find_task(tasks, task_id)
	if task is None:
		print("Task not found.")
		return
	print("Press Enter to keep a value unchanged.")
	updated = dict(task)
	updated["title"] = prompt_nonempty("Title", task["title"])
	updated["description"] = input(
		f"Description [{task.get('description', '')}]: "
	).strip() or task.get("description", "")
	print("Priorities: " + ", ".join(PRIORITIES))
	priority = input(f"Priority [{task.get('priority', 'medium')}]: ").strip()
	if priority:
		if priority not in PRIORITIES:
			print("Invalid priority. Task was not updated.")
			return
		updated["priority"] = priority
	due_date = input(
		f"Due date [{task.get('due_date', '')}] (YYYY-MM-DD): "
	).strip()
	if due_date:
		try:
			datetime.strptime(due_date, "%Y-%m-%d")
		except ValueError:
			print("Invalid due date. Task was not updated.")
			return
		updated["due_date"] = due_date
	print("Statuses: " + ", ".join(STATUSES))
	status = input(f"Status [{task['status']}]: ").strip()
	if status:
		if status not in STATUSES:
			print("Invalid status. Task was not updated.")
			return
		updated["status"] = status
	index = tasks.index(task)
	updated_tasks = list(tasks)
	updated_tasks[index] = updated
	save_tasks(updated_tasks)
	tasks[index] = updated
	print(f"Task {task_id} updated.")


def delete_task(tasks):
	task_id = get_task_id()
	if task_id is None:
		return
	task = find_task(tasks, task_id)
	if task is None:
		print("Task not found.")
		return
	show_task(task)
	if input("Delete this task? [y/N]: ").strip().lower() != "y":
		print("Deletion cancelled.")
		return
	remaining = [item for item in tasks if item.get("id") != task_id]
	save_tasks(remaining)
	tasks[:] = remaining
	print(f"Task {task_id} deleted.")


def main():
	print("Student Task Manager")
	try:
		tasks = load_tasks()
		while True:
			print(
				"\n1. List tasks\n2. View task\n3. Create task\n"
				"4. Update task\n5. Delete task\n0. Exit"
			)
			choice = input("Choose an action: ").strip()
			try:
				if choice == "1":
					list_tasks(tasks)
				elif choice == "2":
					view_task(tasks)
				elif choice == "3":
					create_task(tasks)
				elif choice == "4":
					update_task(tasks)
				elif choice == "5":
					delete_task(tasks)
				elif choice == "0":
					print("Goodbye.")
					return
				else:
					print("Choose one of the listed options.")
			except TaskStoreError as exc:
				print(exc)
	except (TaskStoreError, KeyboardInterrupt) as exc:
		if isinstance(exc, KeyboardInterrupt):
			print("\nExiting.")
		else:
			print(exc)


if __name__ == "__main__":
	main()
