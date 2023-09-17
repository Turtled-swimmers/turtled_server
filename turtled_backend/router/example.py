from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from turtled_backend.container import Container
from turtled_backend.model.request.example import ExampleRequest
from turtled_backend.model.response.example import ExampleResponse
from turtled_backend.service.example import ExampleService

router = APIRouter()


@cbv(router)
class ExampleRouter:
    @inject
    def __init__(self, example_service: ExampleService = Depends(Provide[Container.example_service])):
        self.example_service = example_service

    @router.get("/{example_id}", response_model=ExampleResponse)
    async def get_name(self, example_id: int):
        return await self.example_service.find_by_id(example_id)

    @router.post("/", response_model=ExampleResponse)
    async def upload(self, req: ExampleRequest):
        return await self.example_service.save(req)
