import json

from sqlalchemy.ext.asyncio import AsyncSession

from turtled_backend.common.error.exception import ErrorCode, NotFoundException
from turtled_backend.common.util.firebase import firebase_manager
from turtled_backend.common.util.transaction import transactional
from turtled_backend.model.request.timer import MessageRequest
from turtled_backend.model.response.timer import ErrorResponse, MessageResponse
from turtled_backend.repository.user import UserDeviceRepository


class TimerService:
    def __init__(self, user_device_repository: UserDeviceRepository):
        self.user_device_repository = user_device_repository

    @transactional(read_only=True)
    async def send_message(self, session: AsyncSession, message: MessageRequest):
        tokens = await self.user_device_repository.find_by_user_id(session, message.user_id)
        if len(tokens) == 0:
            raise NotFoundException(
                ErrorCode.DATA_DOES_NOT_EXIST, f"user id {message.user_id} don't have any registered device(s)"
            )

        batch_response = firebase_manager.send(
            message.message, message.notify.get("title"), message.notify.get("body"), tokens
        )
        errors_lst = []
        for v in batch_response.responses:
            if v.exception:
                error = {}
                cause_resp = v.exception.__dict__.get("_cause").__dict__
                cause_dict = json.loads(cause_resp.get("content").decode("utf-8"))
                # Preparing custom error response list
                error["status"] = cause_dict.get("error").get("status", None)
                error["code"] = cause_dict.get("error").get("code", None)
                error["error_code"] = cause_dict.get("error").get("details")[0].get("errorCode", None)
                error["cause"] = cause_dict.get("error").get("message", None)
                errors_lst.append(error)

        return MessageResponse(
            success_count=batch_response.success_count,
            message=f"sent message to {batch_response.success_count} device(s)",
            error=ErrorResponse(count=batch_response.failure_count, errors=errors_lst),
        )
