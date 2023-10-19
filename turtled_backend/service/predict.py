from sqlalchemy.ext.asyncio import AsyncSession

from turtled_backend.common.util.transaction import transactional


class PredictService:
    def __init__(
        self,
        # user_challenge_repository: UserChallengeRepository,
    ):
        pass
    # self.medal_repository = medal_repository

    # @transactional()
    # async def upload_file(self, session: AsyncSession):
    #     return [] # [ChallengeResponse.from_entity(record.medal, record.isAchieved) for record in challenge_list]
