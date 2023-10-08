from sqlalchemy import and_, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from turtled_backend.common.util.repository import Repository
from turtled_backend.schema.challenge import (
    CalenderRecordList,
    ChallengeRecord,
    Medal,
    UserChallenge,
)


class MedalRepository(Repository[Medal]):
    ...


class UserChallengeRepository(Repository[UserChallenge]):
    ...


class CalenderRecordListRepository(Repository[CalenderRecordList]):
    async def find_by_user_and_month_and_year(self, session: AsyncSession, user_id: str, month_and_year: str):
        user = await session.execute(
            select(CalenderRecordList).where(
                and_(CalenderRecordList.user_id == user_id, CalenderRecordList.month_and_year == month_and_year)
            )
        )
        return user.scalars().one_or_none()


class ChallengeRecordRepository(Repository[ChallengeRecord]):
    async def find_recent_one_by_device_token(self, session: AsyncSession, device_id: str):
        result = await session.execute(
            select(ChallengeRecord)
            .where(ChallengeRecord.device_id == device_id)
            .order_by(desc(ChallengeRecord.start_time))
        )
        return result.scalars().first()
