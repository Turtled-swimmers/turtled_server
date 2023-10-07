from pydantic import BaseModel, EmailStr, validator


class UserSignUpRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    checked_password: str

    @validator("username", "password", "checked_password", "email")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("None value is not allowed")
        return v

    @validator("checked_password")
    def passwords_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Password check failed")
        return v


class UserRequest(BaseModel):
    id: str
    username: str
    email: str


class UserDeviceRequest(BaseModel):
    token: str
