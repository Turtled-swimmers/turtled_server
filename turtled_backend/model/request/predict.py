
from pydantic import BaseModel

from fastapi import FastAPI, File, UploadFile

class PredictRecordDetailRequest(BaseModel):
    record_id: str

