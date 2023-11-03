from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from turtled_backend.common.util import create_monthly_history
from turtled_backend.common.util.transaction import transactional
from turtled_backend.model.request.user import UserRequest
from turtled_backend.repository.user import UserRepository

from turtled_backend.model.response.challenge import (
    CalendarEventResponse,
    ChallengeResponse,
    DateHistoryResponse,
    MedalCheckResponse,
)
from turtled_backend.repository.challenge import (
    CalenderRecordListRepository,
    MedalRepository,
    UserChallengeRepository,
    ChallengeRecordRepository,
)
from turtled_backend.repository.user import UserDeviceRepository
from turtled_backend.schema.challenge import CalenderRecordList, UserChallenge
from turtled_backend.model.request.challenge import MedalCheckRequest, MedalChangeRequest
from turtled_backend.common.error.exception import ErrorCode, NotFoundException

class ChallengeService:
    def __init__(
        self,
        medal_repository: MedalRepository,
        user_challenge_repository: UserChallengeRepository,
        user_device_repository: UserDeviceRepository,
        calendar_record_list_repository: CalenderRecordListRepository,
        challenge_record_repository: ChallengeRecordRepository,
        user_repository: UserRepository,
    ):
        self.medal_repository = medal_repository
        self.user_challenge_repository = user_challenge_repository
        self.user_device_repository = user_device_repository
        self.calendar_record_list_repository = calendar_record_list_repository
        self.challenge_record_repository = challenge_record_repository
        self.user_repository = user_repository

    @transactional(read_only=True)
    async def get_list(self, session: AsyncSession, subject: UserRequest):
        challenge_list = await self.user_challenge_repository.find_by_user_id(session, subject.id)
        challenge_list.sort(key=lambda x: x.medal.order)
        return [ChallengeResponse.from_entity(record.medal, record.isAchieved) for record in challenge_list]

    @transactional()
    async def get_monthly_history(self, session: AsyncSession, subject: UserRequest, time_filter: str):
        calendar_record_list = await self.calendar_record_list_repository.find_by_user_and_month_and_year(
            session, subject.id, time_filter
        )

        if calendar_record_list is None:
            date_field = await create_monthly_history(time_filter)
            calendar_record_list = await self.calendar_record_list_repository.save(
                session, CalenderRecordList.of(month_and_year=time_filter, user_id=subject.id, date_field=date_field)
            )

        date_field = calendar_record_list.date_field

        return [
            CalendarEventResponse(calendar_date=calendar_date, has_event=has_event)
            for calendar_date, has_event in date_field.items()
        ]

    @transactional(read_only=True)
    async def get_date_history(self, session: AsyncSession, subject: UserRequest, current_date: str):
        time_from = datetime.strptime(current_date + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        time_to = time_from + timedelta(days=1)

        user_device_list = await self.user_device_repository.find_by_user_id(session, subject.id)

        challenge_record = []
        for user_device in user_device_list:
            challenge_record += await self.challenge_record_repository.find_by_date_and_user(
                session, user_device.id, time_from, time_to
            )

        return [DateHistoryResponse.from_entity(record) for record in challenge_record]

    # TODO: condition check implement as interface pattern
    @transactional()
    async def check_medal_achieved(self, session: AsyncSession, subject: UserRequest, req: MedalCheckRequest):
        user = await self.user_repository.find_by_id(session, subject.id)
        if user is None:
            raise NotFoundException(ErrorCode.DATA_DOES_NOT_EXIST, "User not found")

        medal = await self.medal_repository.find_by_id(session, req.medal_id)
        if medal is None:
            raise NotFoundException(ErrorCode.DATA_DOES_NOT_EXIST, "Medal not found")

        challenge_count = await self.challenge_record_repository.find_all_by_device_id(session, req.device_token)

        is_achieved = False
        if challenge_count > 0:
            user.update(medal_id=medal.id)
            is_achieved = True
            await self.user_challenge_repository.save(session, UserChallenge.of(
                user_id=subject.id,
                medal_id=medal.id,
                is_achieved=True))

        return MedalCheckResponse(is_achieved=is_achieved)


    @transactional()
    async def change_medal(self, session: AsyncSession, subject: UserRequest, req: MedalChangeRequest):
        user = await self.user_repository.find_by_id(session, subject.id)
        if user is None:
            raise NotFoundException(ErrorCode.DATA_DOES_NOT_EXIST, "User not found")

        medal = await self.medal_repository.find_by_id(session, req.medal_id)
        if medal is None:
            raise NotFoundException(ErrorCode.DATA_DOES_NOT_EXIST, "Medal not found")

        return user.update(medal_id=medal.id)
