from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, date

from turtled_backend.common.util.auth import CurrentUser
from turtled_backend.common.util.transaction import transactional
from turtled_backend.model.response.challenge import ChallengeResponse, CalendarEventResponse
from turtled_backend.repository.challenge import (
    MedalRepository,
    UserChallengeRepository,
)
from turtled_backend.schema.challenge import Medal, CalenderList


class ChallengeService:
    def __init__(self, medal_repository: MedalRepository, user_challenge_repository: UserChallengeRepository):
        self.medal_repository = medal_repository
        self.user_challenge_repository = user_challenge_repository

    @transactional(read_only=True)
    async def get_list(self, session: AsyncSession, current_user: CurrentUser):
        medal_list = [
            Medal("1234", "test0.png", "나는야 성실한 성실 거북~!", "매일 매일 스트레칭한다!", "달성 조건: 1일 1스트레칭 연속 5회"),
            Medal("1235", "test1.png", "열심히 달리는 열심 거북", "작심삼일! 열심히 해봐야지!", "달성 조건: 3회 이상 스트레칭"),
            Medal("1236", "test2.png", "의지 넘치는 의지 거북", "한다면 한다~! 스트레칭 해보자고", "달성 조건: 10회 이상 스트레칭"),
        ]
        achievement_list = {"1234": True, "1235": False, "1236": False}
        return [ChallengeResponse.from_entity(medal, achievement_list[medal.id]) for medal in medal_list]

    def get_dates_in_month(self, year: int, month: int):
        # Initialize the start date for the given month
        start_date = datetime(year, month, 1)

        # Calculate the number of days in the month
        next_month = start_date.replace(day=28) + timedelta(days=4)
        last_day = (next_month - timedelta(days=next_month.day)).day

        return int(last_day)

    @transactional(read_only=True)
    async def get_monthly_history(self, session: AsyncSession, time_filter: str):  # TODO: authenticate

        year_filter, month_filter = (int(_filter) for _filter in time_filter.split('-'))
        date_field = {}

        first_date_of_month = date(year_filter, month_filter, 1)

        end_day_of_month = self.get_dates_in_month(int(year_filter), int(month_filter))
        end_date_of_month = date(year_filter, month_filter, end_day_of_month)

        # TODO: remove when test data is migrated to test db
        current_date = first_date_of_month
        for i in range(first_date_of_month.day, end_date_of_month.day+1):
            date_field[current_date.strftime('%Y-%m-%d')] = False if current_date.day % 2 else True
            current_date += timedelta(days=1)

        return [CalendarEventResponse(calendar_date=calendar_date, has_event=has_event)
                for calendar_date, has_event in date_field.items()]

