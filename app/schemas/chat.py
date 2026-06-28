from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    thread_id: str

class PipelineRequest(BaseModel):
    request: str
    max_iterations: Optional[int] = 3

class PipelineResponse(BaseModel):
    status: str
    language: str
    code: str
    tests: str
    attempts: int
    history: List[Dict[str, Any]]
    message: Optional[str] = None
