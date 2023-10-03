import asyncio
from typing import Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from turtled_backend.common.util.repository import Repository
from turtled_backend.schema.user import User, UserDevice


async def test_return_200(is_true: bool):
    # coroutine that returns a value
    return 200 if is_true else 400


class UserRepository(Repository[User]):
    async def test_return_status(self, session: AsyncSession, is_true: bool):
        return await asyncio.create_task(test_return_200(is_true))


class UserDeviceRepository(Repository[UserDevice]):
    async def find_by_device_token(self, session: AsyncSession, device_token: str):
        result = await session.execute(select(UserDevice).where(UserDevice.device_token == device_token))
        return result.scalars().one_or_none()

    async def find_by_user_id(self, session: AsyncSession, user_id: str):
        result = await session.execute(select(UserDevice.device_token).where(UserDevice.user_id == user_id))
        return result.scalars().all()

    async def find_by_user_id_and_device_token(self, session: AsyncSession, user_id: Optional[str], device_token: str):
        result = await session.execute(
            select(UserDevice).where(
                and_(
                    UserDevice.user_id == user_id,
                    UserDevice.device_token == device_token,
                )
            )
        )
        return result.scalars().one_or_none()
