
from pydantic import BaseModel

from fastapi import FastAPI, File, UploadFile

class PredictRequest(BaseModel):
    surey_video: File()

