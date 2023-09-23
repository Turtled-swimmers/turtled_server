from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from turtled_backend.common.util.auth import CurrentUser
from turtled_backend.container import Container
from turtled_backend.model.response.challenge import ChallengeResponse, CalendarEventResponse
from turtled_backend.service.challenge import ChallengeService

router = APIRouter()


@cbv(router)
class ExampleRouter:
    @inject
    def __init__(self, challenge_service: ChallengeService = Depends(Provide[Container.challenge_service])):
        self.challenge_service = challenge_service

    @router.get("/list", response_model=List[ChallengeResponse])
    async def find_challenge_list(self,
                                  current_user: CurrentUser):
        return await self.challenge_service.get_list(current_user)

    @router.get("/history/{time_filter}", response_model=List[CalendarEventResponse])
    async def find_challenge_history(self,
                                     time_filter: str):
        return await self.challenge_service.get_monthly_history(time_filter)
