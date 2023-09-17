from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from turtled_backend.model.request.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def fake_decode_token(token):
    return User(id="010101", username=token + "fakedecoded", email="testuser@example.com")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    current_user = fake_decode_token(token)
    return current_user


CurrentUser = Annotated[User, Depends(get_current_user)]
