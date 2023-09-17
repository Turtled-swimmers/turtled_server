from pydantic import BaseModel

from turtled_backend.schema.example import Example


class ExampleResponse(BaseModel):
    id: int
    name: str

    @classmethod
    def from_entity(cls, entity: Example):
        return cls(id=entity.id, name=entity.name)
