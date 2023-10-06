from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from turtled_backend.common.error.exception import ErrorCode, NotFoundException
from turtled_backend.common.util.auth import CurrentUser, pwd_context
from turtled_backend.common.util.transaction import transactional
from turtled_backend.model.request.user import (
    UserDeviceRequest,
    UserLoginRequest,
    UserSignUpRequest,
)
from turtled_backend.model.response.user import (
    UserDeviceResponse,
    UserLoginResponse,
    UserProfileMedalResponse,
    UserProfileResponse,
)
from turtled_backend.repository.user import UserDeviceRepository, UserRepository
from turtled_backend.schema.user import User, UserDevice


class UserService:
    def __init__(self, user_repository: UserRepository, user_device_repository: UserDeviceRepository):
        self.user_repository = user_repository
        self.user_device_repository = user_device_repository

    @transactional(read_only=True)
    async def login(self, session: AsyncSession, req: UserLoginRequest):
        user = self.user_repository.find_by_email(session, req.email)
        if user is None:
            raise NotFoundException(ErrorCode.DATA_DOES_NOT_EXIST, "User not found")

        return UserLoginResponse.from_entity(req)

    @transactional()
    async def signup(self, session: AsyncSession, req: UserSignUpRequest):
        user = self.user_repository.find_by_email(session, req.email)
        if user is not None:
            raise NotFoundException(ErrorCode.ROW_ALREADY_EXIST, "This user already exists")

        return await self.user_repository.save(
            session, User.of(req.username, req.email, pwd_context.hash(req.password))
        )

    @transactional(read_only=True)
    async def find_profile(self, session: AsyncSession):
        # find user profile information
        test_user_data = {"username": "Swimmers", "email": "turtled_test_user@gmail.com", "update_version": "0.0.1"}
        return UserProfileResponse.from_entity(test_user_data)

    @transactional(read_only=True)
    async def find_profile_medal(self, session: AsyncSession):
        # find user's latest gained medal information
        return UserProfileMedalResponse(title="성실 거북", image="s3://turtled-s3-bucket/medals/hello_turtle.png")

    @transactional()
    async def register_device(
        self, session: AsyncSession, subject: Optional[CurrentUser], user_device: UserDeviceRequest
    ):
        # register device token for FCM service
        user = None
        if subject is not None:
            if subject.id is not None:
                user = await self.user_repository.find_by_id(session, subject.id)

        # Verify to FCM server, that the device_token is real

        saved_user_device = await self.user_device_repository.find_by_device_token(session, user_device.token)
        if saved_user_device is None:
            saved_user_device = await self.user_device_repository.save(
                session,
                UserDevice.of(device_token=user_device.token, user_id=user.id if user else None),
            )
        else:
            saved_user_device.update(user_device.token, user_id=user.id if user else None)

        return UserDeviceResponse.from_entity(saved_user_device)
