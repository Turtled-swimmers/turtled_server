from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

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


    @transactional(read_only=True)
    async def get_monthly_history(self, session: AsyncSession, current_user: CurrentUser, current_month: str):

        year, month = current_month.split('-')
        date_field = {}

        def get_dates_in_month(year: int, month: int):
            # Initialize the start date for the given month
            start_date = datetime(year, month, 1)

            # Calculate the number of days in the month
            next_month = start_date.replace(day=28) + timedelta(days=4)
            last_date = (next_month - timedelta(days=next_month.day)).day

            # Iterate through the month and yield dates in 'yyyy-mm-dd' format
            current_date = start_date
            while current_date.day <= last_date:
                yield current_date.strftime('%Y-%m-%d')
                current_date += timedelta(days=1)

        for date_str in get_dates_in_month(int(year), int(month)):
            if int(date_str.strftime('%d')) % 2:
                date_field[date_str] = False
            else: date_field[date_str] = False

        monthly_event_list = CalenderList(month_and_year=current_month, date_field=date_field)
        return [CalendarEventResponse.of()]
