import asyncio

import nest_asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from turtled_backend.common.error.handler import add_http_exception_handler
from turtled_backend.common.util.database import db
from turtled_backend.config.config import Config
from turtled_backend.container import Container
from turtled_backend.router import challenge, example, index, user

nest_asyncio.apply()


def create_app() -> FastAPI:
    _app = FastAPI()

    """ Define Container """
    container = Container()
    _app.container = container

    """ Define Routers """
    api_version = "v1"
    api_prefix = "/api/" + api_version

    _app.include_router(index.router)
    _app.include_router(example.router, prefix=api_prefix + "/examples")
    _app.include_router(user.router, prefix=api_prefix + "/users")
    _app.include_router(challenge.router, prefix=api_prefix + "/challenges")

    """ Define Middleware """
    _app.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
    )
    _app.add_middleware(SessionMiddleware, secret_key=Config.SESSION_SECRET_KEY)

    add_http_exception_handler(_app)

    return _app


app = create_app()


@app.on_event("startup")
async def startup():
    """Initialize Database"""
    asyncio.run(db.create_database())


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
