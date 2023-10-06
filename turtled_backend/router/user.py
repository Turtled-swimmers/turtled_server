from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from starlette import status

from turtled_backend.common.util.auth import CurrentUser
from turtled_backend.container import Container
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
from turtled_backend.service.user import UserService

router = APIRouter()


@cbv(router)
class UserRouter:
    @inject
    def __init__(self, user_service: UserService = Depends(Provide[Container.user_service])):
        self.user_service = user_service

    @router.post("/login/local", response_model=UserLoginResponse)
    async def login(self, req: UserLoginRequest):  # password를 이렇게 노출시키면 안될 것 같은데?? 그리고 추후 user 정보는 DI로 주입하는게 효율적일듯
        return await self.user_service.login(req)

    @router.post("/signup", status_code=status.HTTP_204_NO_CONTENT)
    async def signup(self, req: UserSignUpRequest):
        return await self.user_service.signup(req)

    @router.post("/profile", response_model=UserProfileResponse)
    async def find_profile(self):
        return await self.user_service.find_profile()

    @router.post("/profile/medal", response_model=UserProfileMedalResponse)
    async def find_profile_medal(self):
        return await self.user_service.find_profile_medal()

    @router.post("/register", response_model=UserDeviceResponse, status_code=201)
    async def register_device(self, subject: Optional[CurrentUser], user_device: UserDeviceRequest):
        return await self.user_service.register_device(subject, user_device)
