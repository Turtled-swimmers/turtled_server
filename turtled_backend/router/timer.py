from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from starlette import status

from turtled_backend.container import Container
from turtled_backend.model.request.timer import (
    MessageRequest,
    TimerEndRequest,
    TimerStartRequest,
)
from turtled_backend.model.response.timer import MessageResponse
from turtled_backend.service.timer import TimerService

router = APIRouter()


@cbv(router)
class TimerRouter:
    @inject
    def __init__(self, timer_service: TimerService = Depends(Provide[Container.timer_service])):
        self.timer_service = timer_service

    @router.post("/alarm", status_code=status.HTTP_204_NO_CONTENT)
    async def timer_start(self, request: TimerStartRequest):
        return await self.timer_service.start_timer(request)

    @router.post("/done", status_code=status.HTTP_204_NO_CONTENT)
    async def timer_done(self, request: TimerEndRequest):
        return await self.timer_service.end_timer(request)

    @router.post("/message")
    async def send_message(self, message: MessageRequest):
        return await self.timer_service.send_message(message)
