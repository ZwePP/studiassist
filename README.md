# 📚 AI Study Assistant

A small FastAPI + Streamlit project that provides a subject-focused study assistant powered by configurable AI providers (OpenAI, Google Gemini, or Anthropic Claude).

**Quick summary:**
- Backend: `backend.py` (FastAPI) — exposes `/`, `/subjects`, `/ask`
- Frontend: `app.py` (Streamlit) — simple UI for asking questions
- AI providers supported: OpenAI, Gemini (Google), Anthropic

---

## ⚙️ Requirements
- Python 3.10+ recommended
- Virtual environment (optional but recommended)

Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Environment / Configuration
The app reads keys and settings from environment variables. You can place them in a `.env` file at the project root (the project loads it via `python-dotenv`).

Required variables:

- `AI_PROVIDER` — one of `openai`, `gemini`, or `anthropic` (controls which client `backend.py` uses)
- `OPENAI_API_KEY` — if `AI_PROVIDER=openai`
- `GEMINI_API_KEY` — if `AI_PROVIDER=gemini`
- `ANTHROPIC_API_KEY` — if `AI_PROVIDER=anthropic`

Example `.env` (do NOT commit your real keys):

```
AI_PROVIDER=openai
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
ANTHROPIC_API_KEY=...
```

---

## Run (local development)
1. Activate your virtualenv (if used):

```bash
source .venv/bin/activate
```

2. Start the backend (FastAPI):

```bash
uvicorn backend:app --reload --port 8000
```

3. In a new terminal, start the Streamlit frontend:

```bash
streamlit run app.py
```

The frontend expects the backend at `http://localhost:8000` by default.

---

## API
- `GET /` — health check
- `GET /subjects` — returns available subjects
- `POST /ask` — ask a question (JSON body: `subject`, `question`, `level`)

Example curl (non-streaming verification):

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"subject":"Computer Science","question":"What is recursion?","level":"Undergraduate"}'
```

Notes: the backend streams responses from the provider; the frontend collects that stream and shows a composed answer.

---

## Switching providers
Change `AI_PROVIDER` in your environment or `.env` to switch between `openai`, `gemini`, and `anthropic`. `backend.py` contains the provider-specific client setup and streaming helpers.

---

## Troubleshooting
- If the frontend shows "Backend is not running", start the backend and ensure it's reachable at `http://localhost:8000`.
- Verify your environment variable names and keys.
- Check `requirements.txt` for compatible package versions if you encounter import errors.

---

## License & Notes
This project is an educational sample. Keep API keys secret and avoid committing them to version control.
