from typing import List, Dict
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from turtled_backend.schema.challenge import PredictRecord

class PredictResponse(BaseModel):
    percentage: int
    image: str
    @staticmethod
    def of(percentage: int, image: str):
        return PredictResponse(percentage=percentage, image=image)


class PredictRecordResponse(BaseModel):
    record_id: str
    created_date: str
    percentage: int
    img_url: str

    @classmethod
    def from_entity(cls, entity: PredictRecord):
        return cls(
            record_id=entity.id,
            created_date=entity.created_date,
            percentage=entity.nerd_neck_percentage,
            img_url=entity.img_url,
        )


class PredictRecordDetailResponse(BaseModel):
    percentage: int
    img_url: str
    exercise_img_list: Dict[str, str]

    @staticmethod
    def of(percentage: int, img_url: str, exercise_images: List[Dict[str, str]]):
        return PredictRecordDetailResponse(
            percentage=percentage,
            img_url=img_url,
            exercise_img_list={exercise_images["image"]: exercise_images["description"]
                               for exercise_images in exercise_images}
        )
