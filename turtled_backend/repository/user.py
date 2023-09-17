import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from turtled_backend.common.util.repository import Repository
from turtled_backend.schema.user import User


async def test_return_200(is_true: bool):
    # coroutine that returns a value
    return 200 if is_true else 400


class UserRepository(Repository[User]):
    async def test_return_status(self, session: AsyncSession, is_true: bool):
        return await asyncio.create_task(test_return_200(is_true))
