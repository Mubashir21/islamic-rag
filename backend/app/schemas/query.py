from pydantic import BaseModel
from typing import Optional


class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None