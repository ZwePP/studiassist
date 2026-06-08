from fastapi import APIRouter, HTTPException
from starlette.responses import PlainTextResponse

from schemas.questions import QuestionRequest
from services.ai_service import call_ai_full, ai_error_to_http_exception
from services.rag_service import retrieve_context

router = APIRouter(
    tags=["Document Upload"],
)

@router.post("/ask")
def ask_question(req: QuestionRequest):
    if not req.question.strip():
        raise HTTPException(400, "Question cannot be empty.")

    context = retrieve_context(req.session_id, req.question) if req.session_id else ""

    system = f"""You are a strict study assistant for {req.subject} at {req.level} level.
ONLY answer questions related to {req.subject}. Refuse anything off-topic.
If lecture context is provided, prioritize it in your answer.
Structure: direct answer → explanation → example."""

    user = (f"Lecture Context:\n{context}\n\n" if context else "") + \
           f"Subject: {req.subject} | Level: {req.level}\nQuestion: {req.question}"

    # Non-streaming: Gemini free-tier streaming can stall for ~90s before the first chunk,
    # which exceeds the frontend's request timeout. A single full response is more reliable.
    try:
        answer = call_ai_full(system, user)
    except HTTPException:
        raise
    except Exception as e:
        raise ai_error_to_http_exception(e)
    return PlainTextResponse(answer)
