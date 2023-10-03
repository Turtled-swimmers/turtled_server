from pydantic import BaseModel


class UserLoginRequest(BaseModel):
    email: str
    password: str


class UserSignUpRequest(BaseModel):
    username: str
    email: str
    password: str
    checked_password: str
    device_token: str  # FCM device token


class User(BaseModel):
    id: str
    username: str
    email: str


class UserDeviceRequest(BaseModel):
    user_id: str
    token: str
