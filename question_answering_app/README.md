# AI Question & Answering System

A Streamlit chat application that answers questions using Google's Gemini API.
It supports follow-up questions within a session, configurable model and
temperature, and a resettable conversation.

## Features

- ChatGPT-style conversation using Streamlit chat components.
- Multi-turn context kept in Streamlit session state.
- Gemini model requests isolated in a service module.
- Configurable model and temperature.
- Low Gemini thinking level by default to reduce latency for everyday questions.
- Friendly configuration and provider error messages.
- No API calls for empty submissions.
- Unit tests use a mocked Gemini client; no API key is needed to test.

## Architecture

The UI (`app/main.py`) renders the chat and handles session state.
`app/services/gemini_service.py` calls the Gemini SDK; configuration, prompts,
and logging are maintained in separate modules. Conversation history is sent
with each stateless `generate_content` request. It is held only in the active
Streamlit session and is not stored in a database.

## Project structure

```text
question_answering_app/
├── app/
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── prompts/
│   │   ├── __init__.py
│   │   └── qa_prompt.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── gemini_service.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logging_config.py
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   └── test_gemini_service.py
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── run.sh
```

## Prerequisites

- Python 3.10 or newer.
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).
- Network access to the Gemini API for live questions.

## Set up

Run commands from the `question_answering_app` folder.

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS/Linux
source .venv/bin/activate
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Configure Gemini

Copy `.env.example` to `.env` (do not commit `.env`) and replace its placeholder
with your own API key:

```powershell
# Windows PowerShell
Copy-Item .env.example .env
```

```bash
# macOS/Linux
cp .env.example .env
```

```dotenv
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.8-flash
TEMPERATURE=0.2
```

The settings are:

- `GEMINI_API_KEY`: required secret. Never share it or add it to source control.
- `GEMINI_MODEL`: optional model name; defaults to `gemini-3.8-flash`.
- `TEMPERATURE`: optional generation temperature from `0.0` to `2.0`;
  defaults to `0.2`.

The app reads `.env` from the project root. If the key is missing, it displays
a configuration message and does not call the API.

## Run the application

From the project root:

```powershell
python -m streamlit run app/main.py
```

Streamlit prints a local URL, normally `http://localhost:8501`, and opens the
app in your browser. Use **Clear Conversation** in the sidebar to reset the
current chat. Stop the server with `Ctrl+C` in the terminal.

macOS/Linux helper:

```bash
./run.sh
```

## Run tests

Tests do not use a real key or contact Gemini:

```powershell
python -m pytest
```

## Example questions

- Explain recursion with a short example.
- What is the difference between a list and a tuple in Python?
- Give me a study plan for learning data structures.
- Follow-up: Can you explain the second step in more detail?

## Troubleshooting

- **Missing API key:** Copy `.env.example` to `.env` and set `GEMINI_API_KEY`.
- **Invalid key or model:** Check the key in Google AI Studio and confirm the
  configured model is available to your account.
- **Connection or quota error:** Check internet access and Gemini API quota.
  The UI shows a safe error; logs do not include the key or chat transcript.
- **Module not found:** Activate the virtual environment and reinstall with
  `python -m pip install -r requirements.txt`.
- **Streamlit command not found:** Start the app with
  `python -m streamlit run app/main.py`.

## Security considerations

- Keep `.env` private; it is ignored by Git.
- `.env.example` contains placeholders only.
- Never paste API keys into chat, screenshots, issue reports, or logs.
- Do not expose this app publicly without authentication, usage controls, and
  an appropriate privacy policy.
- Questions and answers are sent to Google's Gemini API for generation. Avoid
  entering sensitive personal or confidential data.

## Stop and deactivate

- Stop the running Streamlit process with `Ctrl+C` in its terminal.
- Deactivate the virtual environment with:

```powershell
deactivate
```

## Future enhancements

- Add user authentication and per-user conversation storage.
- Add response streaming and conversation export.
- Add rate limiting and usage monitoring for public deployments.
- Add configurable context limits for long conversations.
