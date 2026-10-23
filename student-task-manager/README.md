# Student Task Manager

A small student task manager with a Streamlit interface, a Flask REST API, and
SQLite persistence.

## Project structure

```text
student-task-manager/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── streamlit_app.py
├── tests/
│   └── test_api.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Task fields

- `id`: unique integer assigned by the database
- `title`: required, non-empty task name
- `description`: additional details (defaults to an empty string)
- `priority`: `low`, `medium`, or `high` (defaults to `medium`)
- `status`: `pending`, `in_progress`, or `completed` (defaults to `pending`)
- `due_date`: optional date in `YYYY-MM-DD` format

## Set up and run

From this directory, create and activate a virtual environment, then install
the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Start the Streamlit app:

```powershell
python -m streamlit run app/streamlit_app.py
```

Streamlit opens the interface in your browser (usually at
`http://localhost:8501`). It supports creating, listing, updating, and
deleting tasks.

To start the Flask API instead:

```powershell
python -m app.main
```

The Flask API listens at `http://127.0.0.1:5000`. Both applications use the
same `tasks.db` file in this project directory, so run them against the same
database when you want them to share tasks. The database file is ignored by Git.
Set the `STUDENT_TASK_MANAGER_DB` environment variable before starting either
app to use a different SQLite database file.

## API

| Method | Endpoint | Result |
| --- | --- | --- |
| `GET` | `/api/tasks` | List tasks as `{"tasks": [...]}` |
| `POST` | `/api/tasks` | Create a task; returns `201` and the task |
| `GET` | `/api/tasks/<id>` | Read one task |
| `PATCH` | `/api/tasks/<id>` | Update only the supplied fields |
| `DELETE` | `/api/tasks/<id>` | Delete a task; returns `204` |

Example create request:

```json
{
  "title": "Complete DS assignment",
  "description": "Finish linked-list problems",
  "priority": "high",
  "status": "pending",
  "due_date": "2026-10-25"
}
```

Send JSON with `Content-Type: application/json`. Invalid data returns `400`
with a JSON error. A task that does not exist returns `404`.

## Run tests

```powershell
python -m unittest discover -s tests -v
```
