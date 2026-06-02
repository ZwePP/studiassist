# 📚 AI Study Assistant

**Project Title:** AI Study Assistant for University Students  
**Objective:** Help students get instant, subject-specific answers to academic questions using AI.  
**Tools:** Python, Streamlit, FastAPI, Anthropic Claude API  
**AI Model:** Gemini 1.5 Flash (via Google Generative AI API)

---

## 🗂️ Project Structure

```
ai_study_assistant/
├── app.py            # Streamlit frontend
├── backend.py        # FastAPI backend
├── requirements.txt  # Dependencies
└── README.md
```

---

## ⚙️ Setup & Running Instructions

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/ai-study-assistant.git
cd ai-study-assistant
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your API key
```bash
# macOS/Linux
export GEMINI_API_KEY=your_key_here

# Windows (Command Prompt)
set GEMINI_API_KEY=your_key_here
```
Get a free API key at: https://aistudio.google.com/apikey

### 4. Start the FastAPI backend
```bash
uvicorn backend:app --reload
# Runs at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### 5. Start the Streamlit frontend (new terminal)
```bash
streamlit run app.py
# Opens at http://localhost:8501
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/subjects` | List available subjects |
| POST | `/ask` | Submit a question |

**POST `/ask` body:**
```json
{
  "subject": "Computer Science",
  "question": "What is recursion?",
  "level": "Undergraduate"
}
```

---

## ✨ Features
- Select subject + academic level
- Ask any academic question
- AI returns a structured, concise answer
- Question history shown in session
- Clean, minimal UI

---

## 👥 Team Members
- Member 1 — [Role]
- Member 2 — [Role]
- Member 3 — [Role]
