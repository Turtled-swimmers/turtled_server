
from pydantic import BaseModel

from fastapi import FastAPI, File, UploadFile

class MedalCheckRequest(BaseModel):
    medal_id: str
    device_token: str


class MedalChangeRequest(BaseModel):
    medal_id: str
