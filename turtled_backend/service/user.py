import json
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from turtled_backend.common.error.exception import ErrorCode, NotFoundException
from turtled_backend.common.util.transaction import transactional
from turtled_backend.config.config import Config
from turtled_backend.model.request.user import (
    UserDeviceRequest,
    UserRequest,
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
    async def login(self, session: AsyncSession, form_data: OAuth2PasswordRequestForm):
        with open(Config.SECRET_KEY_PATH, encoding="utf-8") as f:
            jwt_secret_key = json.load(f)

        # check user and password
        user = await self.user_repository.find_by_email(session, form_data.username)
        if user is None:
            raise NotFoundException(ErrorCode.DATA_DOES_NOT_EXIST, "User not found")

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        if not user or not pwd_context.verify(form_data.password, user.password):
            raise NotFoundException(ErrorCode.NOT_ACCESSIBLE, "Incorrect username or password")

        # make access token
        data = {"sub": user.email, "exp": datetime.utcnow() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)}
        access_token = jwt.encode(data, jwt_secret_key["secret_key"], algorithm=Config.ALGORITHM)

        return UserLoginResponse.of(access_token=access_token, username=user.username)

    @transactional()
    async def signup(self, session: AsyncSession, req: UserSignUpRequest):
        user = self.user_repository.find_by_email(session, req.email)
        if user is not None:
            raise NotFoundException(ErrorCode.ROW_ALREADY_EXIST, "This user already exists")

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
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
    async def register_device_with_user(
        self, session: AsyncSession, subject: UserRequest, user_device: UserDeviceRequest
    ):
        user = await self.user_repository.find_by_id(session, subject.id)
        if user is not None:
            raise NotFoundException(ErrorCode.ROW_ALREADY_EXIST, "This user already exists")

        saved_user_device = await self.user_device_repository.find_by_device_token(session, user_device.token)
        if saved_user_device is None:
            saved_user_device = await self.user_device_repository.save(
                session,
                UserDevice.of(device_token=user_device.token, user_id=subject.id),
            )
        else:
            saved_user_device.update(user_device.token, user_id=subject.id)

        return UserDeviceResponse.from_entity(saved_user_device)
