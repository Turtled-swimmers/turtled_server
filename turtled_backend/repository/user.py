from typing import Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from turtled_backend.common.util.repository import Repository
from turtled_backend.schema.user import User, UserDevice


class UserRepository(Repository[User]):
    async def find_by_email(self, session: AsyncSession, email: str):
        result = await session.execute(select(User).where(User.email == email))
        return result.scalars().one_or_none()


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
