from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv
from starlette import status

from turtled_backend.common.util.auth import CurrentUser
from turtled_backend.container import Container
from turtled_backend.model.request.user import UserDeviceRequest, UserSignUpRequest
from turtled_backend.model.response.user import (
    UserDeviceResponse,
    UserLoginResponse,
    UserProfileMedalResponse,
    UserProfileResponse,
)
from turtled_backend.service.user import UserService

router = APIRouter()


@cbv(router)
class UserRouter:
    @inject
    def __init__(self, user_service: UserService = Depends(Provide[Container.user_service])):
        self.user_service = user_service

    @router.post("/login/local", response_model=UserLoginResponse)
    async def login(self, form_data: OAuth2PasswordRequestForm = Depends()):
        return await self.user_service.login(form_data)

    @router.post("/signup", status_code=status.HTTP_204_NO_CONTENT)
    async def signup(self, req: UserSignUpRequest):
        return await self.user_service.signup(req)

    @router.post("/profile", response_model=UserProfileResponse)
    async def find_profile(self, subject: CurrentUser):
        return await self.user_service.find_profile()

    @router.post("/profile/medal", response_model=UserProfileMedalResponse)
    async def find_profile_medal(self, subject: CurrentUser):
        return await self.user_service.find_profile_medal()

    @router.post("/register", response_model=UserDeviceResponse, status_code=201)
    async def register_device(self, subject: CurrentUser, user_device: UserDeviceRequest):
        return await self.user_service.register_device_with_user(subject, user_device)
