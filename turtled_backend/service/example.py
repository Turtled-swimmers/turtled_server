from sqlalchemy.ext.asyncio import AsyncSession

from turtled_backend.common.error.exception import ErrorCode, NotFoundException
from turtled_backend.common.util.transaction import transactional
from turtled_backend.model.request.example import ExampleRequest
from turtled_backend.model.response.example import ExampleResponse
from turtled_backend.repository.example import ExampleRepository
from turtled_backend.schema.example import Example


class ExampleService:
    def __init__(self,
                 example_repository: ExampleRepository):
        self.example_repository = example_repository

    @transactional(read_only=True)
    async def find_by_id(self, session: AsyncSession, example_id: int):
        example = await self.example_repository.find_by_id(session, example_id)
        if example is None:
            raise NotFoundException(
                ErrorCode.DATA_DOES_NOT_EXIST,
                "Not found example"
            )

        return ExampleResponse.from_entity(example)

    @transactional()
    async def save(self, session: AsyncSession, req: ExampleRequest):
        example = await self.example_repository.save(session, Example(**req.dict()))

        return ExampleResponse.from_entity(example)
