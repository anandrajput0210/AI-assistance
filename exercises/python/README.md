# Python Exercises

These scripts are separate learning exercises. They do not share an application
runtime or require third-party packages.

## Programs

| File | Purpose |
| --- | --- |
| `avgmarks.py` | Defines `calculate_average(marks)`, validates marks, and includes normal, boundary, and invalid-input assertions. |
| `promptA.py` | Collects one student's subject marks and displays the total, average, and pass/fail result. |
| `promptB.py` | Collects marks for five students, validates the range, assigns letter grades, and prints a formatted report. |
| `student.py` | Collects five student names and marks, assigns grades, and displays a results table. |
| `swap.py` | Currently checks whether a number is prime. The earlier number-swapping example remains commented out. |
| `testing.py` | Demonstrates numeric input validation and mark-category selection. |
| `student-task.py` | A JSON-backed command-line task manager prototype with create, read, update, and delete actions. Its REST API section is a proposed contract in the docstring; this script does not run a Flask API. |

## Requirements

- Python 3
- No third-party packages are required for these scripts.

## Run an exercise

Run commands from the repository root. For example:

```powershell
python exercises/python/promptB.py
python exercises/python/avgmarks.py
python exercises/python/student-task.py
```

The task-manager script creates `tasks.json` in this directory when tasks are
saved. That runtime data file is local and is excluded from Git.
