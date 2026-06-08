from pydantic import BaseModel

class QuizRequest(BaseModel):
    session_id: str
    subject: str
    level: str = "Undergraduate"
    num_questions: int = 5


class QuizAnswer(BaseModel):
    session_id: str
    question: str
    selected: str
    correct: str
    subject: str