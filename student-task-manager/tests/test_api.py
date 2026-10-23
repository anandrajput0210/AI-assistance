"""Tests for the task-management REST API."""

import json
import tempfile
import unittest
from pathlib import Path

from app.main import create_app


class TaskApiTests(unittest.TestCase):
	def setUp(self):
		self.temporary_directory = tempfile.TemporaryDirectory()
		database_path = Path(self.temporary_directory.name) / "test_tasks.db"
		self.client = create_app(database_path).test_client()
		self.sample_task = {
			"title": "Complete DS assignment",
			"description": "Finish linked-list problems",
			"priority": "high",
			"status": "pending",
			"due_date": "2026-10-25",
		}

	def tearDown(self):
		self.temporary_directory.cleanup()

	def test_create_and_list_task(self):
		response = self.client.post("/api/tasks", json=self.sample_task)

		self.assertEqual(response.status_code, 201)
		created_task = response.get_json()
		self.assertEqual(created_task["id"], 1)
		self.assertEqual(created_task["title"], self.sample_task["title"])
		self.assertEqual(created_task["description"], self.sample_task["description"])
		self.assertEqual(created_task["priority"], "high")
		self.assertEqual(created_task["status"], "pending")
		self.assertEqual(created_task["due_date"], "2026-10-25")

		list_response = self.client.get("/api/tasks")
		self.assertEqual(list_response.status_code, 200)
		self.assertEqual(list_response.get_json()["tasks"], [created_task])

	def test_validation_rejects_invalid_priority_and_date(self):
		invalid_priority = {**self.sample_task, "priority": "urgent"}
		response = self.client.post("/api/tasks", json=invalid_priority)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json()["error"]["code"], "validation_error")

		invalid_date = {**self.sample_task, "due_date": "25-10-2026"}
		response = self.client.post("/api/tasks", json=invalid_date)
		self.assertEqual(response.status_code, 400)

	def test_patch_preserves_fields_not_sent(self):
		created = self.client.post("/api/tasks", json=self.sample_task).get_json()

		response = self.client.patch(
			f"/api/tasks/{created['id']}",
			json={"status": "completed"},
		)

		self.assertEqual(response.status_code, 200)
		updated_task = response.get_json()
		self.assertEqual(updated_task["status"], "completed")
		self.assertEqual(updated_task["title"], self.sample_task["title"])
		self.assertEqual(updated_task["priority"], self.sample_task["priority"])

	def test_get_and_delete_unknown_task_return_not_found(self):
		self.assertEqual(self.client.get("/api/tasks/999").status_code, 404)
		self.assertEqual(self.client.delete("/api/tasks/999").status_code, 404)

	def test_delete_existing_task(self):
		created = self.client.post("/api/tasks", json=self.sample_task).get_json()

		response = self.client.delete(f"/api/tasks/{created['id']}")

		self.assertEqual(response.status_code, 204)
		self.assertEqual(response.data, b"")
		self.assertEqual(self.client.get("/api/tasks").get_json()["tasks"], [])

	def test_malformed_json_returns_json_error(self):
		response = self.client.post(
			"/api/tasks",
			data="{",
			content_type="application/json",
		)

		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json()["error"]["code"], "invalid_json")


if __name__ == "__main__":
	unittest.main()
