from typing import Dict

from pydantic import BaseModel


class MessageRequest(BaseModel):
    user_id: str
    message: str
    notify: Dict
    device_uuid: str


class TimerRequest(BaseModel):
    repeat_period: str
    timer_start_time: str
