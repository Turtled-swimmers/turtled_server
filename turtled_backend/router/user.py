from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from turtled_backend.container import Container
from turtled_backend.model.request.user import UserLoginRequest, UserSignUpRequest
from turtled_backend.model.response.user import UserLoginResponse
from turtled_backend.service.user import UserService

router = APIRouter()


@cbv(router)
class ExampleRouter:
    @inject
    def __init__(self, user_service: UserService = Depends(Provide[Container.user_service])):
        self.user_service = user_service

    @router.post("/login/local", response_model=UserLoginResponse)
    async def login(self, req: UserLoginRequest):  # password를 이렇게 노출시키면 안될 것 같은데?? 그리고 추후 user 정보는 DI로 주입하는게 효율적일듯
        return await self.user_service.login(req)

    @router.post("/signup")
    async def signup(self, req: UserSignUpRequest):
        return await self.user_service.signup(req)
