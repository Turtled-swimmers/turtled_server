from pydantic import BaseModel


class UserLoginRequest(BaseModel):
    email: str
    password: str


class UserSignUpRequest(BaseModel):
    nickname: str
    email: str
    password: str
    checked_password: str
    device_token: str  # FCM device token
