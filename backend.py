"""
AI Study Assistant - FastAPI Backend
Supports OpenAI, Gemini, or Anthropic with streaming responses.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Study Assistant API")

# ── Provider setup ────────────────────────────────────────────────────────────
PROVIDER = os.getenv("AI_PROVIDER", "").lower()

if PROVIDER == "openai":
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

elif PROVIDER == "gemini":
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    client = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction="You are a helpful university-level study assistant. Answer clearly and concisely. Give a direct answer, key concept explanation if needed, and one example if helpful."
    )

elif PROVIDER == "anthropic":
    import anthropic
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

else:
    raise RuntimeError("AI_PROVIDER not set. Add AI_PROVIDER=openai|gemini|anthropic to your .env")

SYSTEM_PROMPT = """You are a strict university-level study assistant.
You ONLY answer questions related to the subject and level provided by the user.
If the question is off-topic or unrelated to the given subject, respond with:
"I can only answer questions related to {subject}. Please ask a relevant question."

Rules:
- Stay strictly within the given subject and academic level
- Adjust complexity to match the level (High School / Undergraduate / Graduate)
- Structure your response: direct answer → concept explanation → example
- Refuse any question outside the subject scope
- Be concise and clear in your explanations
- 200-300 words max per answer"""

SUBJECTS = ["Mathematics", "Physics", "Chemistry", "Biology",
            "Computer Science", "Business", "Economics", "Literature"]


class QuestionRequest(BaseModel):
    subject: str
    question: str
    level: str = "Undergraduate"


@app.get("/")
def root():
    return {"status": "running", "provider": PROVIDER, "service": "AI Study Assistant API"}


@app.get("/subjects")
def get_subjects():
    return {"subjects": SUBJECTS}


def stream_openai(prompt: str):
    with client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=600,
        stream=True,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    ) as stream:
        for chunk in stream:
            text = chunk.choices[0].delta.content
            if text:
                yield text


def stream_gemini(prompt: str):
    response = client.generate_content(prompt, stream=True)
    for chunk in response:
        if chunk.text:
            yield chunk.text


def stream_anthropic(prompt: str):
    with client.messages.stream(
        model="claude-haiku-4-5",
        max_tokens=600,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            yield text


@app.post("/ask")
def ask_question(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    if request.subject not in SUBJECTS:
        raise HTTPException(status_code=400, detail=f"Subject must be one of: {SUBJECTS}")

    prompt = f"""Subject: {request.subject}
Level: {request.level}

You must only answer questions about {request.subject} at {request.level} level.
If the question below is not related to {request.subject}, refuse to answer it.

Question: {request.question}"""

    streamers = {
        "openai": stream_openai,
        "gemini": stream_gemini,
        "anthropic": stream_anthropic,
    }

    try:
        return StreamingResponse(streamers[PROVIDER](prompt), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI error: {str(e)}")