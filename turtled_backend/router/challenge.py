from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from turtled_backend.common.util.auth import CurrentUser
from turtled_backend.container import Container
from turtled_backend.model.response.challenge import (
    CalendarEventResponse,
    ChallengeResponse,
    DateHistoryResponse,
)
from turtled_backend.service.challenge import ChallengeService

router = APIRouter()


@cbv(router)
class ChallengeRouter:
    @inject
    def __init__(self, challenge_service: ChallengeService = Depends(Provide[Container.challenge_service])):
        self.challenge_service = challenge_service

    @router.get("/list", response_model=List[ChallengeResponse])
    async def find_challenge_list(self):
        return await self.challenge_service.get_list()

    @router.get("/history/{time_filter}", response_model=List[CalendarEventResponse])
    async def find_monthly_history(self, subject: CurrentUser, time_filter: str):
        return await self.challenge_service.get_monthly_history(subject, time_filter)

    @router.get("/history/detail/{current_date}", response_model=List[DateHistoryResponse])
    async def find_date_history(self, subject: CurrentUser, current_date: str):
        return await self.challenge_service.get_date_history(current_date)
