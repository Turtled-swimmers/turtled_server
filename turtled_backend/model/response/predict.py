from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

class PredictResponse(BaseModel):
    percentage: int
    image: str
    @staticmethod
    def of(percentage: int, image: str):
        return PredictResponse(percentage=percentage, image=image)
