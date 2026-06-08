# 📚 Stamford StudyAssist

> **AI-Powered Learning Assistant for Stamford International University Students**

Stamford StudyAssist is an intelligent learning platform that helps students study more efficiently using AI. By combining lecture uploads, Retrieval-Augmented Generation (RAG), quiz generation, and summarization, students can interact with their course materials in a smarter and more engaging way.

---

## 🎯 Project Objective

The goal of Stamford StudyAssist is to improve the learning experience by allowing students to:

* Upload lecture slides and study materials
* Ask AI questions about their courses
* Generate quizzes from lecture content
* Summarize lengthy lectures into concise notes
* Track learning progress and performance
* Receive context-aware answers grounded in their own materials

---

## ✨ Core Features

### 📄 Lecture Upload & Processing

Upload study materials in:

* PDF (`.pdf`)
* PowerPoint (`.pptx`)

The system automatically:

* Extracts text
* Processes lecture content
* Splits content into searchable chunks
* Prepares data for RAG retrieval

---

### 🤖 AI Study Assistant

Ask questions such as:

> "What is recursion?"

> "Explain Porter's Five Forces."

> "What were the key concepts in Chapter 4?"

The AI retrieves relevant lecture content and generates contextual answers.

---

### 🔍 Retrieval-Augmented Generation (RAG)

Instead of relying solely on the AI model's knowledge, the system:

1. Retrieves relevant lecture content
2. Uses the retrieved information as context
3. Generates more accurate and lecture-specific responses

This significantly reduces hallucinations and improves answer quality.

---

### 📝 AI Quiz Generation

Generate multiple-choice quizzes directly from:

* Uploaded lecture slides
* Course content
* Selected subjects

Perfect for:

* Exam preparation
* Self-assessment
* Knowledge reinforcement

---

### 📚 Lecture Summarization

Convert lengthy lectures into concise study notes including:

* Key concepts
* Main topics
* Important definitions
* Exam-relevant takeaways

---

### 📊 Learning Analytics

Track student performance through:

* Quiz scores
* Session history
* Subject performance
* Learning trends
* Weak areas for improvement

---

## 🏗️ System Architecture

```text
Frontend (Streamlit)
        │
        ▼
Backend API (FastAPI)
        │
        ▼
 AI Service Layer
        │
        ▼
  RAG Retrieval
        │
        ▼
 Lecture Database
        │
        ▼
OpenAI / Gemini / Claude
```

---

## 🛠️ Technology Stack

| Category            | Technology             |
| ------------------- | ---------------------- |
| Frontend            | Streamlit              |
| Backend             | FastAPI                |
| Language            | Python                 |
| Database            | SQLite                 |
| AI Providers        | Gemini, OpenAI, Claude |
| Document Processing | PyPDF, Python-PPTX     |
| Configuration       | Pydantic Settings      |
| API Documentation   | Swagger UI             |

---

## 📂 Project Structure

```text
studyassist/
│
├── .env
├── .env.example
├── .gitignore
├── main.py
├── requirements.txt
├── README.md
│
├── .streamlit/
│   └── config.toml
│
├── api/
│   ├── router.py
│   └── routes/
│       ├── question_routes.py
│       ├── quiz_routes.py
│       ├── subjects_routes.py
│       ├── summarize_routes.py
│       └── upload_routes.py
│
├── config/
│   ├── ai_client.py
│   ├── config.py
│   └── constants.py
│
├── db/
│   └── database.py
│
├── frontend/
│   └── streamlist_app.py
│
├── schemas/
│   ├── questions.py
│   └── quiz.py
│
├── services/
│   ├── ai_service.py
│   └── rag_service.py
│
└── utils/
    └── document_utils.py
```

---

## ⚙️ Environment Setup

Create a `.env` file in the project root:

```env
AI_PROVIDER=gemini

GEMINI_API_KEY=your_api_key

OPENAI_API_KEY=
ANTHROPIC_API_KEY=

OPENAI_MODEL=gpt-4o-mini
GEMINI_MODEL=gemini-flash-lite-latest
ANTHROPIC_MODEL=claude-haiku-4-5

MAX_AI_TOKENS=1500
STREAM_AI_TOKENS=800

DB_PATH=db/ruvector.db
```

---

## 🚀 Installation

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Backend

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Backend URL:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

---

## ▶️ Running the Frontend

Launch Streamlit:

```bash
streamlit run frontend/streamlist_app.py
```

Frontend URL:

```text
http://localhost:8501
```

---

## 🔌 Available API Endpoints

| Method | Endpoint         | Description                   |
| ------ | ---------------- | ----------------------------- |
| GET    | `/`              | API health check              |
| GET    | `/docs`          | Interactive API documentation |
| GET    | `/api/subjects`  | Retrieve available subjects   |
| POST   | `/api/upload`    | Upload lecture slides         |
| POST   | `/api/ask`       | Ask AI-powered questions      |
| POST   | `/api/quiz`      | Generate quizzes              |
| POST   | `/api/summarize` | Generate lecture summaries    |

---

## 🧠 Supported AI Providers

The application supports multiple AI providers through environment configuration.

### Google Gemini

```env
AI_PROVIDER=gemini
```

### OpenAI

```env
AI_PROVIDER=openai
```

### Anthropic Claude

```env
AI_PROVIDER=anthropic
```

Switching providers requires **no code changes**.

---

## 👥 Team Members

* Member 1
* Member 2
* Member 3

---

## 📌 Version

**Version 2.0**

Built for the **AI-Driven Web Application Final Project** at **Stamford International University**.
