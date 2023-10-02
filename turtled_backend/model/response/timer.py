from typing import Dict, List, Optional

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    count: int = 0
    errors: Optional[List[Dict]]


class MessageResponse(BaseModel):
    success_count: int
    message: str
    error: ErrorResponse
