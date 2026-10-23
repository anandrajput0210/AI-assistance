"""Streamlit user interface for the student task manager."""

import sqlite3
import os
from datetime import date
from pathlib import Path

import streamlit as st

from app import database
from app.models import PRIORITIES, STATUSES, ValidationError, validate_task_payload


DATABASE_PATH = Path(
	os.environ.get(
		"STUDENT_TASK_MANAGER_DB",
		Path(__file__).resolve().parent.parent / "tasks.db",
	)
)
database.initialize_database(DATABASE_PATH)

st.set_page_config(page_title="Student Task Manager", page_icon="📝", layout="wide")
st.title("Student Task Manager")
st.caption("Create, review, update, and delete your tasks.")

try:
	tasks = database.list_tasks(DATABASE_PATH)
except sqlite3.Error as error:
	st.error(f"Could not load tasks from the database: {error}")
	st.stop()

st.subheader("Your tasks")
if tasks:
	st.dataframe(
		[
			{
				"ID": task.id,
				"Title": task.title,
				"Description": task.description,
				"Priority": task.priority,
				"Status": task.status,
				"Due date": task.due_date or "",
			}
			for task in tasks
		],
		hide_index=True,
		use_container_width=True,
	)
else:
	st.info("No tasks yet. Add your first task below.")

st.divider()
st.subheader("Add a task")
with st.form("create_task_form", clear_on_submit=True):
	title = st.text_input("Task name *")
	description = st.text_area("Additional details")
	priority = st.selectbox("Priority", PRIORITIES, index=1)
	status = st.selectbox("Status", STATUSES)
	due_date = st.date_input("Target date (optional)", value=None)
	create_submitted = st.form_submit_button("Create task", type="primary")

if create_submitted:
	payload = {
		"title": title,
		"description": description,
		"priority": priority,
		"status": status,
		"due_date": due_date.isoformat() if isinstance(due_date, date) else None,
	}
	try:
		values = validate_task_payload(payload)
		database.create_task(DATABASE_PATH, values)
	except ValidationError as error:
		st.error(str(error))
	except sqlite3.Error as error:
		st.error(f"Could not save the task: {error}")
	else:
		st.success("Task created.")
		st.rerun()

if tasks:
	st.divider()
	st.subheader("Update or delete a task")
	task_by_id = {task.id: task for task in tasks}
	task_id = st.selectbox(
		"Choose a task",
		options=list(task_by_id),
		format_func=lambda selected_id: (
			f"{selected_id}: {task_by_id[selected_id].title}"
		),
	)
	selected_task = task_by_id[task_id]

	update_column, delete_column = st.columns(2)
	with update_column:
		st.markdown("#### Edit task")
		with st.form("update_task_form"):
			updated_title = st.text_input("Task name", value=selected_task.title)
			updated_description = st.text_area(
				"Additional details",
				value=selected_task.description,
			)
			updated_priority = st.selectbox(
				"Priority",
				PRIORITIES,
				index=PRIORITIES.index(selected_task.priority),
				key="updated_priority",
			)
			updated_status = st.selectbox(
				"Status",
				STATUSES,
				index=STATUSES.index(selected_task.status),
				key="updated_status",
			)
			updated_due_date = st.text_input(
				"Target date (YYYY-MM-DD; leave blank to clear)",
				value=selected_task.due_date or "",
			)
			update_submitted = st.form_submit_button("Save changes")

		if update_submitted:
			payload = {
				"title": updated_title,
				"description": updated_description,
				"priority": updated_priority,
				"status": updated_status,
				"due_date": updated_due_date or None,
			}
			try:
				values = validate_task_payload(payload, partial=True)
				updated_task = database.update_task(
					DATABASE_PATH,
					task_id,
					values,
				)
				if updated_task is None:
					st.error("That task no longer exists. Refresh the page.")
				else:
					st.success("Task updated.")
					st.rerun()
			except ValidationError as error:
				st.error(str(error))
			except sqlite3.Error as error:
				st.error(f"Could not update the task: {error}")

	with delete_column:
		st.markdown("#### Delete task")
		with st.form("delete_task_form"):
			st.write(f"Selected task: **{selected_task.title}**")
			confirmed = st.checkbox("I confirm that I want to delete this task.")
			delete_submitted = st.form_submit_button("Delete task")

		if delete_submitted:
			if not confirmed:
				st.warning("Confirm deletion before continuing.")
			else:
				try:
					deleted = database.delete_task(DATABASE_PATH, task_id)
				except sqlite3.Error as error:
					st.error(f"Could not delete the task: {error}")
				else:
					if deleted:
						st.success("Task deleted.")
						st.rerun()
					else:
						st.error("That task no longer exists. Refresh the page.")
