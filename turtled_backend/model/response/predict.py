from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

class PredictResponse(BaseModel):
    percentage: int
    @staticmethod
    def of(percentage: int):
        return PredictResponse(percentage=percentage)
