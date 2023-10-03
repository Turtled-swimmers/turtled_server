from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from turtled_backend.common.util.repository import Repository
from turtled_backend.schema.challenge import ChallengeRecord, Medal, UserChallenge


class MedalRepository(Repository[Medal]):
    ...


class UserChallengeRepository(Repository[UserChallenge]):
    ...


class ChallengeRecordRepository(Repository[ChallengeRecord]):
    async def find_recent_one_by_device_token(self, session: AsyncSession, device_id: str):
        result = await session.execute(
            select(ChallengeRecord)
            .where(ChallengeRecord.device_id == device_id)
            .order_by(desc(ChallengeRecord.start_time))
        )
        return result.first()
