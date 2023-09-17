import json
import traceback

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from turtled_backend.common.error.exception import (
    BadRequestException,
    ErrorCode,
    InternalServerException,
    NotFoundException,
    UnauthorizedException,
    UnprocessableEntityException,
)
from turtled_backend.config.log import logger


def add_http_exception_handler(app: FastAPI) -> None:
    @app.exception_handler(BadRequestException)
    async def bad_request_exception_handler(request: Request, exc: BadRequestException):
        logger.error(
            "[REQUEST] [%s] path: %s [RESPONSE] code: %d, message: %s",
            request.method,
            request.url.path,
            exc.code.value,
            exc.message,
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"code": exc.code.value, "message": exc.message}
        )

    @app.exception_handler(UnauthorizedException)
    async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
        logger.error(
            "[REQUEST] [%s] path: %s [RESPONSE] code: %d, message: %s",
            request.method,
            request.url.path,
            exc.code.value,
            exc.message,
        )
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED, content={"code": exc.code.value, "message": exc.message}
        )

    @app.exception_handler(NotFoundException)
    async def not_found_exception_handler(request: Request, exc: NotFoundException):
        logger.error(
            "[REQUEST] [%s] path: %s [RESPONSE] code: %d, message: %s",
            request.method,
            request.url.path,
            exc.code.value,
            exc.message,
        )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"code": exc.code.value, "message": exc.message}
        )

    @app.exception_handler(UnprocessableEntityException)
    async def unprocessable_entity_exception_handler(request: Request, exc: UnprocessableEntityException):
        logger.error(
            "[REQUEST] [%s] path: %s [RESPONSE] code: %d, message: %s",
            request.method,
            request.url.path,
            exc.code.value,
            exc.message,
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"code": exc.code.value, "message": exc.message}
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
        details = exc.errors()
        message = [{"loc": error["loc"], "message": error["msg"], "type": error["type"]} for error in details]
        logger.error(
            "[REQUEST] [%s] path: %s [RESPONSE] message: %s",
            request.method,
            request.url.path,
            ",".join([json.dumps(m) for m in message]),
        )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"code": ErrorCode.UNPROCESSABLE_ENTITY.value, "message": message},
        )

    @app.exception_handler(InternalServerException)
    async def internal_server_exception(request: Request, exc: InternalServerException):
        logger.error(
            "[REQUEST] [%s] path: %s [RESPONSE] code: %d, message: %s",
            request.method,
            request.url.path,
            exc.code.value,
            exc.message,
        )
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"code": exc.code.value, "message": exc.message}
        )

    @app.exception_handler(Exception)
    async def exception(request: Request, exc: Exception):
        logger.error(
            "[REQUEST] [%s] path: %s [RESPONSE] code: %d",
            request.method,
            request.url.path,
            ErrorCode.INTERNAL_SERVER_ERROR.value,
        )
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"code": ErrorCode.INTERNAL_SERVER_ERROR.value, "message": traceback.format_exception_only(exc)},
        )
