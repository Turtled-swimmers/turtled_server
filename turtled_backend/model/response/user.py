from typing import Dict, Optional, List

from pydantic import BaseModel

from turtled_backend.schema.user import User
from turtled_backend.config.config import Config


class UserLoginResponse(BaseModel):
    username: str
    token_type: str
    access_token: str

    @classmethod
    def from_entity(cls, entity: User):
        return cls(username=entity.email, token_type="Bearer", access_token="test_token")


class UserProfileResponse(BaseModel):
    username: str
    email: str
    update_version: str
    support_email: str

    @classmethod
    def from_entity(cls, entity: dict):
        return cls(
            username=entity["username"],
            email=entity["email"],
            update_version=entity["update_version"],
            support_email=Config.SUPPORT_EMAIL_ACCOUNT
        )


class UserProfileMedalResponse(BaseModel):
    title: str
    image: str

    @classmethod
    def from_entity(cls, title: str, image: str):
        return cls(
            title=title,
            image=image
        )


class UserDeviceResponse(BaseModel):
    id: int
    user_id: int
    token: str
    device_info: Optional[Dict]
