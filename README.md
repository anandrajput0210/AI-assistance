# AI Assistance

A repository of Python learning exercises and independent software projects.
Each application is kept in its own directory so its dependencies, setup, and
documentation stay separate.

## Repository structure

```text
AI-assistance/
├── exercises/
│   └── python/                 # Standalone Python exercises and CLI practice
├── calculator/                 # HTML, CSS, and JavaScript calculator
├── cse-department-website/     # React + Vite + TypeScript website
├── question_answering_app/     # Streamlit + Gemini question-answering app
└── student-task-manager/       # Flask REST API + Streamlit UI + SQLite
```

## Python exercises

See [exercises/python/README.md](exercises/python/README.md) for descriptions
and run commands. These scripts are independent exercises, not one combined
Python application.

Example:

```powershell
python exercises/python/promptB.py
```

## Applications

### Calculator

A standalone browser application. Open `calculator/index.html` in a browser.
Its HTML, CSS, and JavaScript files are kept together in `calculator/`.

### BMSIT&M CSE Department Website

A React, Vite, TypeScript, and Tailwind CSS website concept.

```powershell
cd cse-department-website
npm install
npm run dev
```

See [cse-department-website/README.md](cse-department-website/README.md)
before publishing; the page content includes sample data that must be verified.

### AI Question & Answering System

A Streamlit application using Google's Gemini API. Setup, environment
configuration, and tests are documented in
[question_answering_app/README.md](question_answering_app/README.md).

### Student Task Manager

A task-management application with a Flask REST API, Streamlit interface, and
SQLite persistence. API routes and setup instructions are documented in
[student-task-manager/README.md](student-task-manager/README.md).

## Repository conventions

- Keep each independent application in its existing project directory.
- Keep standalone programming exercises under `exercises/python/`.
- Use each project's own dependency manifest and README.
- Do not commit virtual environments, dependency folders, build output,
  local databases, runtime data, or secret environment files.
