from typing import Dict

from pydantic import BaseModel, Field


class MessageRequest(BaseModel):
    user_id: str
    message: str
    notify: Dict
