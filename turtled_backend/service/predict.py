from sqlalchemy.ext.asyncio import AsyncSession

from turtled_backend.common.util.transaction import transactional
from turtled_backend.model.response.predict import PredictResponse

class PredictService:
    def __init__(
        self,
        # user_challenge_repository: UserChallengeRepository,
    ):
        pass
    # self.medal_repository = medal_repository

    @transactional()
    async def upload_file(self, session: AsyncSession):
        return PredictResponse.of("12", "12")
