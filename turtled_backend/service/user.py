from sqlalchemy.ext.asyncio import AsyncSession

from turtled_backend.common.util.transaction import transactional
from turtled_backend.model.request.user import UserLoginRequest, UserSignUpRequest
from turtled_backend.model.response.user import UserLoginResponse
from turtled_backend.repository.user import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    @transactional(read_only=True)
    async def login(self, session: AsyncSession, req: UserLoginRequest):
        # example = await self.user_repository.save(session, UserLoginRequest(**req.dict()))
        # JWT token exchange
        return UserLoginResponse.from_entity(req)

    @transactional()
    async def signup(self, session: AsyncSession, req: UserSignUpRequest):
        # check user is newbie, and  signup user
        is_true = True
        if req.password != req.checked_password:
            is_true = False

        return await self.user_repository.test_return_status(session, is_true)
