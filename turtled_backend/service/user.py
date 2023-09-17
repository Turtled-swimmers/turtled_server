from sqlalchemy.ext.asyncio import AsyncSession

from turtled_backend.common.error.exception import ErrorCode, NotFoundException
from turtled_backend.common.util.transaction import transactional
from turtled_backend.model.request.user import UserLoginRequest
from turtled_backend.model.response.user import UserLoginResponse
from turtled_backend.repository.user import UserRepository
from turtled_backend.schema.user import UserLoginInfo


class UserService:
    def __init__(self,
                 user_repository: UserRepository):
        self.user_repository = user_repository

    @transactional(read_only=True)
    async def login(self, session: AsyncSession, req: UserLoginRequest):
        # example = await self.user_repository.save(session, UserLoginRequest(**req.dict()))
        # JWT 생성
        return UserLoginResponse.from_entity(req)
