from fastapi import HTTPException, APIRouter


from db.database import document_store


from services.ai_service import call_ai_full, ai_error_to_http_exception



router = APIRouter(
    tags=["Document Upload"],
)





def summarize(session_id: str, subject: str = "", level: str = "Undergraduate"):
    if session_id not in document_store:
        raise HTTPException(404, "Session not found. Please upload a PDF first.")
    doc = document_store[session_id]

    system_prompt = f"""You are an academic study assistant. Summarize lecture slides clearly for a {level} student.
    Structure your summary as:
    1. 📌 Main Topics (bullet points)
    2. 🔑 Key Concepts (brief definitions)
    3. 💡 Important Takeaways"""

    user = f"Summarize this lecture content:\n\n{doc['full_text']}"
    try:
        summary = call_ai_full(system_prompt, user)
    except HTTPException:
        raise
    except Exception as e:
        raise ai_error_to_http_exception(e)
    return {"summary": summary, "filename": doc["filename"]}