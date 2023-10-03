from typing import Dict

from pydantic import BaseModel


class MessageRequest(BaseModel):
    message: str
    notify: Dict
    device_token: str


class TimerStartRequest(BaseModel):
    device_token: str
    repeat_cycle: int
    start_time: str


class TimerEndRequest(BaseModel):
    device_token: str
    end_time: str
