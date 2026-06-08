from pydantic import BaseModel



class QuestionRequest(BaseModel):
    subject: str
    question: str
    level: str = "Undergraduate"
    session_id: str = ""


