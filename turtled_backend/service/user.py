import json
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from turtled_backend.common.error.exception import ErrorCode, NotFoundException
from turtled_backend.common.util.transaction import transactional
from turtled_backend.common.util.s3 import S3_CLIENT
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
from turtled_backend.schema.challenge import UserChallenge
from turtled_backend.repository.challenge import MedalRepository, UserChallengeRepository


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        user_device_repository: UserDeviceRepository,
        medal_repository: MedalRepository,
        user_challenge_repository: UserChallengeRepository
    ):
        self.user_repository = user_repository
        self.user_device_repository = user_device_repository
        self.medal_repository = medal_repository
        self.user_challenge_repository = user_challenge_repository

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
        user = await self.user_repository.find_by_email(session, req.email)
        if user is not None:
            raise NotFoundException(ErrorCode.ROW_ALREADY_EXIST, "This user already exists")
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        user = await self.user_repository.save(
            session, User.of(req.username, req.email, pwd_context.hash(req.password))
        )

        medal_list = await self.medal_repository.find_all(session)
        user_medal_list = [UserChallenge.of(user_id=user.id, medal_id=medal.id) for medal in medal_list]
        return await self.user_challenge_repository.save_all(session, user_medal_list)

    @transactional(read_only=True)
    async def find_profile(self, session: AsyncSession, subject: UserRequest):
        # find user profile information
        user = await self.user_repository.find_by_id(session, subject.id)
        if user is None:
            raise NotFoundException(ErrorCode.DATA_DOES_NOT_EXIST, "User not found")

        return UserProfileResponse.from_entity(user)

    @transactional(read_only=True)
    async def find_profile_medal(self, session: AsyncSession, subject: UserRequest):
        # find user's latest gained medal information
        user = await self.user_repository.find_by_id(session, subject.id)
        if user is None:
            raise NotFoundException(ErrorCode.DATA_DOES_NOT_EXIST, "User not found")

        if user.medal_id is None:
            title = "헬로 거북"
            image = await S3_CLIENT.s3_download("medals/hello_turtle.png")
        else:
            medal = await self.medal_repository.find_by_id(session, user.medal_id)
            if medal is None:
                raise NotFoundException(ErrorCode.DATA_DOES_NOT_EXIST,"Medal not found")
            title = medal.image
            image = medal.title

        return UserProfileMedalResponse(title=title, image=image)

    @transactional()
    async def register_device_with_user(
        self, session: AsyncSession, subject: UserRequest, user_device: UserDeviceRequest
    ):
        user = await self.user_repository.find_by_id(session, subject.id)
        if user is None:
            raise NotFoundException(ErrorCode.ROW_ALREADY_EXIST, "No user exists")

        saved_user_device = await self.user_device_repository.find_by_device_token(session, user_device.token)
        if saved_user_device is None:
            saved_user_device = await self.user_device_repository.save(
                session,
                UserDevice.of(device_token=user_device.token, user_id=subject.id),
            )
        else:
            saved_user_device.update(user_device.token, user_id=subject.id)

        return UserDeviceResponse.from_entity(saved_user_device)

    @transactional()
    async def register_device(self, session: AsyncSession, user_device: UserDeviceRequest):
        saved_user_device = await self.user_device_repository.find_by_device_token(session, user_device.token)
        if saved_user_device is None:
            saved_user_device = await self.user_device_repository.save(
                session,
                UserDevice.of(device_token=user_device.token),
            )
        else:
            saved_user_device.update(user_device.token)

        return UserDeviceResponse.from_entity(saved_user_device)
