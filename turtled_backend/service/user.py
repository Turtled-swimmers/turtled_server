from sqlalchemy.ext.asyncio import AsyncSession

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
from turtled_backend.schema.user import UserDevice


class UserService:
    def __init__(self, user_repository: UserRepository, user_device_repository: UserDeviceRepository):
        self.user_repository = user_repository
        self.user_device_repository = user_device_repository

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
    async def register_device(self, session: AsyncSession, user_device: UserDeviceRequest):
        # register device token for FCM service
        saved_user_device = await self.user_device_repository.find_by_user_id_and_device_uuid(
            session, user_device.user_id, user_device.device_uuid
        )
        if saved_user_device is None:
            saved_user_device = await self.user_device_repository.save(
                session,
                UserDevice(
                    device_token=user_device.token, device_uuid=user_device.device_uuid, user_id=user_device.user_id
                ),
            )
        else:
            saved_user_device.update(user_device.token)

        return UserDeviceResponse.from_entity(saved_user_device)
