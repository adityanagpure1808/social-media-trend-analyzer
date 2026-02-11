from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_id: str
    report_id: str
    question: str

class ChatResponse(BaseModel):
    answer: str
    source: str
