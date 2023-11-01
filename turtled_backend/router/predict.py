from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from turtled_backend.common.util.auth import CurrentUser
from turtled_backend.container import Container
from turtled_backend.model.response.predict import PredictResponse, PredictRecordResponse, PredictRecordDetailResponse
from turtled_backend.model.request.predict import PredictRecordDetailRequest
from turtled_backend.service.predict import PredictService
from fastapi import FastAPI, File, UploadFile

router = APIRouter()


@cbv(router)
class PredictRouter:
    @inject
    def __init__(self, predict_service: PredictService = Depends(Provide[Container.predict_service])):
        self.predict_service = predict_service

    @router.post("/upload", response_model = PredictResponse)  # , response_class=FileResponse
    async def upload_file(self, servey_video: UploadFile):
        return await self.predict_service.upload_file(servey_video)

    @router.post("/user_upload", response_model = PredictResponse)  # , response_class=FileResponse
    async def user_upload_file(self, subject: CurrentUser, servey_video: UploadFile):
        return await self.predict_service.user_upload_file(servey_video, subject)

    @router.get("/predict_history", response_model=List[PredictRecordResponse])  # , response_class=FileResponse
    async def find_predict_history(self, subject: CurrentUser):
        return await self.predict_service.find_predict_history(subject)

    @router.post("/predict_history_detail", response_model=PredictRecordDetailResponse)  # , response_class=FileResponse
    async def find_predict_history_detail(self, subject: CurrentUser, req: PredictRecordDetailRequest):
        return await self.predict_service.find_predict_history_detail(subject, req)
