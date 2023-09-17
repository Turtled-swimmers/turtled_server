from pydantic import BaseModel

from turtled_backend.schema.user import User


class UserLoginResponse(BaseModel):
    username: str
    token_type: str
    access_token: str

    @classmethod
    def from_entity(cls, entity: User):
        return cls(username=entity.email, token_type="Bearer", access_token="test_token")
