import json
from typing import Annotated, Callable

from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from turtled_backend.common.error.exception import ErrorCode, NotFoundException
from turtled_backend.common.util.database import db
from turtled_backend.config.config import Config
from turtled_backend.container import Container
from turtled_backend.model.request.user import UserRequest
from turtled_backend.repository.user import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


def get_current_user_authorizer(*, required: bool = False) -> Callable:
    # Log-in user with a member ID or non-member order.
    return get_current_user if required else None


@inject
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_repository: UserRepository = Depends(Provide[Container.user_repository]),
):
    credentials_exception = NotFoundException(ErrorCode.NOT_ACCESSIBLE, "Could not validate credentials")
    try:
        with open(Config.SECRET_KEY_PATH, encoding="utf-8") as f:
            jwt_secret_key = json.load(f)

        payload = jwt.decode(token, jwt_secret_key["secret_key"], algorithms=[Config.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = await user_repository.find_by_email(db, email)
        if user is None:
            raise credentials_exception
        return UserRequest(
            id=user.id,
            username=user.username,
            email=user.email,
        )


CurrentUser = Annotated[UserRequest, Depends(get_current_user)]
