from pydantic import BaseModel
from typing import Optional

class PromptCreate(BaseModel):
    prompt: str
    llm: str
    started: Optional[int] = None  # Unix epoch, set by backend if not provided

class PromptOut(BaseModel):
    id: int
    prompt: str
    response: Optional[str]
    llm: str
    started: int
    completed: Optional[int]
    timestamp: str
