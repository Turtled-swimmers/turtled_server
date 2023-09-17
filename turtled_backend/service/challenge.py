from sqlalchemy.ext.asyncio import AsyncSession

from turtled_backend.common.util.auth import CurrentUser
from turtled_backend.common.util.transaction import transactional
from turtled_backend.model.response.challenge import ChallengeResponse
from turtled_backend.repository.challenge import (
    MedalRepository,
    UserChallengeRepository,
)
from turtled_backend.schema.challenge import Medal


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
