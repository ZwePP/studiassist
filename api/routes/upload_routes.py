from hashlib import md5

from fastapi import UploadFile, HTTPException, File, APIRouter


from utils.document_utils import extract_text_from_pdf, chunk_text, extract_text_from_pptx
from services.rag_service import simple_embed
from db.database import document_store



router = APIRouter(
    tags=["Document Upload"],
)



@router.post(
    "/upload",
    summary="Upload lecture slides",
    description=(
        "Accepts one or more PDF/PPTX lecture slide files. "
        "The backend extracts text, splits the content into chunks, "
        "creates a session ID, and prepares the content for RAG-based quiz, summary, and AI chat features."
    ),
)

async def upload_pdf(files: list[UploadFile] = File(...)):
    if not files:
        raise HTTPException(400, "No files provided.")

    text_parts: list[str] = []
    file_names: list[str] = []
    raw_concat = b""

    for file in files:
        filename = file.filename.lower()
        if not (filename.endswith(".pdf") or filename.endswith(".pptx")):
            raise HTTPException(400, f"Unsupported file type: {file.filename}. Only PDF and PPTX are supported.")

        content = await file.read()
        raw_concat += content

        if filename.endswith(".pdf"):
            text = extract_text_from_pdf(content)
        else:
            text = extract_text_from_pptx(content)

        if not text.strip():
            raise HTTPException(400, f"Could not extract text from {file.filename}.")

        text_parts.append(f"=== {file.filename} ===\n{text}")
        file_names.append(file.filename)

    combined_text = "\n\n".join(text_parts)
    chunks = chunk_text(combined_text)
    session_id = md5(raw_concat).hexdigest()[:12]
    display_name = file_names[0] if len(file_names) == 1 else f"{len(file_names)} files"
    document_store[session_id] = {
        "filename": display_name,
        "files": file_names,
        "chunks": [{"text": c, "vec": simple_embed(c)} for c in chunks],
        "full_text": combined_text[:8000],
    }
    return {"session_id": session_id, "filename": display_name, "files": file_names, "chunks": len(chunks)}

