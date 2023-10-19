from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from turtled_backend.common.util.auth import CurrentUser
from turtled_backend.container import Container
from turtled_backend.model.response.predict import PredictResponse
from turtled_backend.service.predict import PredictService
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

router = APIRouter()


@cbv(router)
class PredictRouter:
    @inject
    def __init__(self, predict_service: PredictService = Depends(Provide[Container.predict_service])):
        self.predict_service = predict_service

    @router.post("/upload", response_model = PredictResponse) # , response_class=FileResponse
    async def upload_file(self, servey_video: UploadFile):
        return await self.predict_service.upload_file(servey_video)
