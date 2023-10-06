from typing import Annotated, Callable, Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from turtled_backend.model.request.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def fake_decode_token(token):
    return User(id="010101", username=token + "fakedecoded", email="testuser@example.com")


def fake_hash_password(password: str):
    return "fakehashed" + password


def get_current_user_authorizer(*, required: bool = False) -> Callable:
    return get_current_user if required else get_current_user_optional


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    current_user = fake_decode_token(token)
    return current_user


async def get_current_user_optional(token: Annotated[str, Depends(oauth2_scheme)]) -> Optional[User]:
    # Log-in user with a member ID or non-member order.
    if token:
        return await get_current_user(token)
    return None


CurrentUser = Annotated[User, Depends(get_current_user_authorizer)]
