from typing import Dict

from pydantic import BaseModel


class Notify:
    def __init__(self, title: str, body: str):
        self.title = title
        self.body = body


class MessageRequest(BaseModel):
    message: str
    notify: Dict[str, str] = {"title": "", "body": ""}
    device_token: str


class TimerStartRequest(BaseModel):
    device_token: str
    repeat_cycle: int
    start_time: str


class TimerEndRequest(BaseModel):
    device_token: str
    end_time: str
