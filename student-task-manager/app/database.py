"""SQLite persistence for tasks."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from .models import Task


@contextmanager
def connect(database_path: str | Path) -> Iterator[sqlite3.Connection]:
	path = Path(database_path)
	path.parent.mkdir(parents=True, exist_ok=True)
	connection = sqlite3.connect(path)
	connection.row_factory = sqlite3.Row
	try:
		with connection:
			yield connection
	finally:
		connection.close()


def initialize_database(database_path: str | Path) -> None:
	with connect(database_path) as connection:
		connection.execute(
			"""
			CREATE TABLE IF NOT EXISTS tasks (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				title TEXT NOT NULL CHECK (length(trim(title)) > 0),
				description TEXT NOT NULL DEFAULT '',
				priority TEXT NOT NULL DEFAULT 'medium'
					CHECK (priority IN ('low', 'medium', 'high')),
				status TEXT NOT NULL DEFAULT 'pending'
					CHECK (status IN ('pending', 'in_progress', 'completed')),
				due_date TEXT
			)
			"""
		)


def _task_from_row(row: sqlite3.Row) -> Task:
	return Task(
		id=row["id"],
		title=row["title"],
		description=row["description"],
		priority=row["priority"],
		status=row["status"],
		due_date=row["due_date"],
	)


def list_tasks(database_path: str | Path) -> list[Task]:
	with connect(database_path) as connection:
		rows = connection.execute(
			"SELECT id, title, description, priority, status, due_date "
			"FROM tasks ORDER BY id"
		).fetchall()
	return [_task_from_row(row) for row in rows]


def get_task(database_path: str | Path, task_id: int) -> Task | None:
	with connect(database_path) as connection:
		row = connection.execute(
			"SELECT id, title, description, priority, status, due_date "
			"FROM tasks WHERE id = ?",
			(task_id,),
		).fetchone()
	return _task_from_row(row) if row is not None else None


def create_task(database_path: str | Path, values: dict[str, object]) -> Task:
	with connect(database_path) as connection:
		cursor = connection.execute(
			"INSERT INTO tasks (title, description, priority, status, due_date) "
			"VALUES (?, ?, ?, ?, ?)",
			(
				values["title"],
				values["description"],
				values["priority"],
				values["status"],
				values["due_date"],
			),
		)
		row = connection.execute(
			"SELECT id, title, description, priority, status, due_date "
			"FROM tasks WHERE id = ?",
			(cursor.lastrowid,),
		).fetchone()
	return _task_from_row(row)


def update_task(
	database_path: str | Path, task_id: int, values: dict[str, object]
) -> Task | None:
	if not values:
		return get_task(database_path, task_id)

	columns = ", ".join(f"{field} = ?" for field in values)
	parameters = [*values.values(), task_id]
	with connect(database_path) as connection:
		cursor = connection.execute(
			f"UPDATE tasks SET {columns} WHERE id = ?",
			parameters,
		)
		if cursor.rowcount == 0:
			return None
		row = connection.execute(
			"SELECT id, title, description, priority, status, due_date "
			"FROM tasks WHERE id = ?",
			(task_id,),
		).fetchone()
	return _task_from_row(row)


def delete_task(database_path: str | Path, task_id: int) -> bool:
	with connect(database_path) as connection:
		cursor = connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
	return cursor.rowcount > 0
