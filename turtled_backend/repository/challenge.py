from datetime import date
from sqlalchemy import and_, desc, select, asc, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from turtled_backend.common.util.repository import Repository
from turtled_backend.schema.challenge import (
    CalenderRecordList,
    ChallengeRecord,
    Medal,
    UserChallenge,
    PredictRecord,
    ExerciseList
)


class MedalRepository(Repository[Medal]):
    async def find_all(self, session: AsyncSession):
        result = await session.execute(select(Medal))
        return result.scalars().all()

    async def find_by_order(self, session: AsyncSession, order: int):
        result = await session.execute(select(Medal).where((Medal.order == order)))
        return result.scalars().one_or_none()


class UserChallengeRepository(Repository[UserChallenge]):
    async def find_by_user_id(self, session: AsyncSession, user_id: str):
        result = await session.execute(
            select(UserChallenge).where((UserChallenge.user_id == user_id)).options(selectinload(UserChallenge.medal))
        )
        return result.scalars().all()


class CalenderRecordListRepository(Repository[CalenderRecordList]):
    async def find_by_user_and_month_and_year(self, session: AsyncSession, user_id: str, month_and_year: str):
        result = await session.execute(
            select(CalenderRecordList).where(
                and_(CalenderRecordList.user_id == user_id, CalenderRecordList.month_and_year == month_and_year)
            )
        )
        return result.scalars().one_or_none()


class ChallengeRecordRepository(Repository[ChallengeRecord]):
    async def find_recent_one_by_device_token(self, session: AsyncSession, device_id: str):
        result = await session.execute(
            select(ChallengeRecord)
            .where(ChallengeRecord.device_id == device_id)
            .order_by(desc(ChallengeRecord.start_time))
        )
        return result.scalars().first()

    async def find_by_date_and_user(self, session: AsyncSession, device_id: str, time_from: date, time_to: date):
        result = await session.execute(
            select(ChallengeRecord)
            .where(
                and_(
                    ChallengeRecord.device_id == device_id,
                    ChallengeRecord.end_time >= time_from,
                    ChallengeRecord.end_time < time_to,
                )
            )
            .order_by(asc(ChallengeRecord.start_time))
        )
        return result.scalars().all()

    async def find_all_by_device_id(self, session: AsyncSession, device_id: str):
        result = await session.execute(
            select(func.count('*')).select_from(ChallengeRecord)
            .where(
                    ChallengeRecord.device_id == device_id,
            )
        )
        return result.scalars().one_or_none()

class PredictRecordRepository(Repository[PredictRecord]):
    async def find_all_by_user(self, session: AsyncSession, user_id: str):
        result = await session.execute(
            select(PredictRecord)
            .where(and_(PredictRecord.user_id == user_id))
            .order_by(desc(PredictRecord.created_date))

        )
        return result.scalars().all()


class ExerciseListRepository(Repository[ExerciseList]):
    async def find_by_percentage(self, session: AsyncSession, percentage: int):
        result = await session.execute(
            select(ExerciseList)
            .where(and_(ExerciseList.percentage == percentage))
            .order_by(desc(ExerciseList.id))
        )
        return result.scalars().all()
