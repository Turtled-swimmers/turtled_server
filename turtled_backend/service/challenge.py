from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from turtled_backend.common.util import create_monthly_history
from turtled_backend.common.util.transaction import transactional
from turtled_backend.model.request.user import UserRequest
from turtled_backend.model.response.challenge import (
    CalendarEventResponse,
    ChallengeResponse,
    DateHistoryResponse,
)
from turtled_backend.repository.challenge import (
    CalenderRecordListRepository,
    MedalRepository,
    UserChallengeRepository,
)
from turtled_backend.repository.user import UserDeviceRepository
from turtled_backend.schema.challenge import CalenderRecordList, Medal


class ChallengeService:
    def __init__(
        self,
        medal_repository: MedalRepository,
        user_challenge_repository: UserChallengeRepository,
        user_device_repository: UserDeviceRepository,
        calendar_record_list_repository: CalenderRecordListRepository,
    ):
        self.medal_repository = medal_repository
        self.user_challenge_repository = user_challenge_repository
        self.user_device_repository = user_device_repository
        self.calendar_record_list_repository = calendar_record_list_repository

    @transactional(read_only=True)
    async def get_list(self, session: AsyncSession):
        medal_list = [  # test dataset
            Medal("1234", "test0.png", "나는야 성실한 성실 거북~!", "매일 매일 스트레칭한다!", "달성 조건: 1일 1스트레칭 연속 5회"),
            Medal("1235", "test1.png", "열심히 달리는 열심 거북", "작심삼일! 열심히 해봐야지!", "달성 조건: 3회 이상 스트레칭"),
            Medal("1236", "test2.png", "의지 넘치는 의지 거북", "한다면 한다~! 스트레칭 해보자고", "달성 조건: 10회 이상 스트레칭"),
        ]

        achievement_list = {"1234": True, "1235": False, "1236": False}
        return [ChallengeResponse.from_entity(medal, achievement_list[medal.id]) for medal in medal_list]

    @transactional(read_only=True)
    async def get_monthly_history(self, session: AsyncSession, subject: UserRequest, time_filter: str):
        date_field = await self.calendar_record_list_repository.find_by_user_and_month_and_year(
            session, subject.id, time_filter
        )

        if date_field is None:
            date_field = await create_monthly_history(time_filter)
            await self.calendar_record_list_repository.save(
                session, CalenderRecordList.of(month_and_year=time_filter, user_id=subject.id, date_field=date_field)
            )

        return [
            CalendarEventResponse(calendar_date=calendar_date, has_event=has_event)
            for calendar_date, has_event in date_field.items()
        ]

    @transactional(read_only=True)
    async def get_date_history(
        self, session: AsyncSession, subject: UserRequest, current_date: str
    ):  # TODO: authenticate
        date_selection1 = datetime.strptime(current_date + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        date_selection2 = datetime.strptime(current_date + " 01:00:00", "%Y-%m-%d %H:%M:%S")
        date_selection3 = datetime.strptime(current_date + " 02:00:00", "%Y-%m-%d %H:%M:%S")
        date_selection4 = datetime.strptime(current_date + " 03:00:00", "%Y-%m-%d %H:%M:%S")

        test_data = [
            {
                "timer_start_time": str(date_selection1.time()),
                "timer_end_time": str(date_selection2.time()),
                "repeat_cycle": 15,
                "count": 5,
            },
            {
                "timer_start_time": str(date_selection2.time()),
                "timer_end_time": str(date_selection3.time()),
                "repeat_cycle": 15,
                "count": 5,
            },
            {
                "timer_start_time": str(date_selection3.time()),
                "timer_end_time": str(date_selection4.time()),
                "repeat_cycle": 15,
                "count": 5,
            },
        ]

        return [DateHistoryResponse.from_entity(data) for data in test_data]
