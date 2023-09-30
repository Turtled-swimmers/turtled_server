import asyncio
from typing import Dict, Optional

from sqlalchemy import String, and_, select
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
    async def find_by_user_id_and_device_info(self, session: AsyncSession, user_id: str, device_info: Optional[Dict]):
        result = await session.execute(
            select(UserDevice).where(
                and_(
                    UserDevice.user_id == user_id,
                    UserDevice.device_info["device_type"].cast(String) == device_info["device_type"],
                    UserDevice.device_info["ip"].cast(String) == device_info["ip"],
                )
            )
        )
        return result.scalars().one_or_none()
