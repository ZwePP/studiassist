from fastapi import APIRouter, HTTPException

from schemas.quiz import QuizRequest
from services.ai_service import ai_error_to_http_exception, call_ai_full

from json import loads

from db.database import document_store



router = APIRouter(
    tags=["Quiz"],
)

@router.post("/quiz")
def generate_quiz(req: QuizRequest):
    if req.session_id and req.session_id in document_store:
        context = document_store[req.session_id]["full_text"][:4000]
        source = "lecture slides"
    else:
        context = ""
        source = f"{req.subject} at {req.level} level"

    system = """You are a quiz generator. Return ONLY a valid JSON array, no markdown, no explanation.
Each item must have: question (string), options (array of 4 strings), answer (one of the 4 strings exactly)."""

    user = f"""Generate {req.num_questions} multiple choice questions about {source}.
Level: {req.level}
{"Context:\n" + context if context else ""}

Return only JSON like: [{{"question":"...","options":["A","B","C","D"],"answer":"A"}}]"""

    try:
        raw = call_ai_full(system, user)
    except HTTPException:
        raise
    except Exception as e:
        raise ai_error_to_http_exception(e)
    raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        quiz = loads(raw)
        return {"quiz": quiz}
    except Exception:
        raise HTTPException(500, "Failed to parse quiz response from AI. Try again.")

