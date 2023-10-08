from typing import Optional

from pydantic import BaseModel

from turtled_backend.config.config import Config
from turtled_backend.schema.user import User, UserDevice


class UserLoginResponse(BaseModel):
    username: str
    token_type: str
    access_token: str

    @classmethod
    def of(cls, access_token: str, username: str):
        return cls(username=username, token_type="bearer", access_token=access_token)


class UserProfileResponse(BaseModel):
    username: str
    email: str
    support_email: str

    @classmethod
    def from_entity(cls, entity: User):
        return cls(
            username=entity.username,
            email=entity.email,
            support_email=Config.SUPPORT_EMAIL_ACCOUNT,
        )


class UserProfileMedalResponse(BaseModel):
    title: str
    image: str

    @classmethod
    def from_entity(cls, title: str, image: str):
        return cls(title=title, image=image)


class UserDeviceResponse(BaseModel):
    user_id: Optional[str]
    device_token: str

    @classmethod
    def from_entity(cls, entity: UserDevice):
        return cls(user_id=entity.user_id, device_token=entity.device_token)
