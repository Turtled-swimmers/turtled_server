from typing import Dict

from pydantic import BaseModel


class MessageRequest(BaseModel):
    user_id: str
    message: str
    notify: Dict
