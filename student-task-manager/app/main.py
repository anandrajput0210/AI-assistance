"""Flask REST API for the student task manager."""

import sqlite3
from pathlib import Path

from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest

from . import database
from .models import ValidationError, validate_task_payload


def create_app(database_path: str | Path | None = None) -> Flask:
	app = Flask(__name__)
	app.config["DATABASE_PATH"] = str(
		database_path or Path(__file__).resolve().parent.parent / "tasks.db"
	)
	database.initialize_database(app.config["DATABASE_PATH"])

	@app.errorhandler(ValidationError)
	def handle_validation_error(error: ValidationError):
		return jsonify(
			error={"code": "validation_error", "message": str(error)}
		), 400

	@app.errorhandler(BadRequest)
	def handle_bad_request(_error: BadRequest):
		return jsonify(
			error={
				"code": "invalid_json",
				"message": "Request body must contain valid JSON.",
			}
		), 400

	@app.errorhandler(sqlite3.Error)
	def handle_database_error(error: sqlite3.Error):
		app.logger.exception("Task database operation failed: %s", error)
		return jsonify(
			error={
				"code": "storage_error",
				"message": "The task could not be processed because of a storage error.",
			}
		), 500

	@app.errorhandler(404)
	def handle_not_found(_error):
		return jsonify(
			error={"code": "not_found", "message": "The requested resource was not found."}
		), 404

	def read_json_body():
		if not request.is_json:
			raise ValidationError("Content-Type must be application/json.")
		return request.get_json()

	@app.get("/api/tasks")
	def list_task_route():
		tasks = database.list_tasks(app.config["DATABASE_PATH"])
		return jsonify(tasks=[task.to_dict() for task in tasks])

	@app.post("/api/tasks")
	def create_task_route():
		values = validate_task_payload(read_json_body())
		task = database.create_task(app.config["DATABASE_PATH"], values)
		return jsonify(task.to_dict()), 201

	@app.get("/api/tasks/<int:task_id>")
	def get_task_route(task_id: int):
		task = database.get_task(app.config["DATABASE_PATH"], task_id)
		if task is None:
			return jsonify(
				error={"code": "not_found", "message": "Task was not found."}
			), 404
		return jsonify(task.to_dict())

	@app.patch("/api/tasks/<int:task_id>")
	def update_task_route(task_id: int):
		values = validate_task_payload(read_json_body(), partial=True)
		task = database.update_task(app.config["DATABASE_PATH"], task_id, values)
		if task is None:
			return jsonify(
				error={"code": "not_found", "message": "Task was not found."}
			), 404
		return jsonify(task.to_dict())

	@app.delete("/api/tasks/<int:task_id>")
	def delete_task_route(task_id: int):
		deleted = database.delete_task(app.config["DATABASE_PATH"], task_id)
		if not deleted:
			return jsonify(
				error={"code": "not_found", "message": "Task was not found."}
			), 404
		return "", 204

	return app


if __name__ == "__main__":
	create_app().run(debug=True)
