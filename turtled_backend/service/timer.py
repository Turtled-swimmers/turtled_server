import json
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from turtled_backend.common.error.exception import ErrorCode, NotFoundException
from turtled_backend.common.util.firebase import firebase_manager
from turtled_backend.common.util.transaction import transactional
from turtled_backend.model.request.timer import (
    MessageRequest,
    TimerEndRequest,
    TimerStartRequest,
)
from turtled_backend.model.response.timer import ErrorResponse, MessageResponse
from turtled_backend.repository.challenge import ChallengeRecordRepository
from turtled_backend.repository.user import UserDeviceRepository
from turtled_backend.schema.challenge import ChallengeRecord


class TimerService:
    def __init__(
        self, user_device_repository: UserDeviceRepository, challenge_record_repository: ChallengeRecordRepository
    ):
        self.user_device_repository = user_device_repository
        self.challenge_record_repository = challenge_record_repository

    @transactional()
    async def start_timer(self, session: AsyncSession, request: TimerStartRequest):
        user_device = await self.user_device_repository.find_by_device_token(session, request.device_token)

        if user_device is None:
            raise NotFoundException(ErrorCode.DATA_DOES_NOT_EXIST, "User's device token is not registered.")
        return await self.challenge_record_repository.save(
            session,
            ChallengeRecord.of(
                start_time=datetime.strptime(request.start_time, "%Y-%m-%d %H:%M:%S"),
                repeat_cycle=request.repeat_cycle,
                device_id=user_device.id,
            ),
        )

    @transactional()
    async def end_timer(self, session: AsyncSession, request: TimerEndRequest):
        user_device = await self.user_device_repository.find_by_device_token(session, request.device_token)

        if user_device is None:
            raise NotFoundException(ErrorCode.DATA_DOES_NOT_EXIST, "User's device token is not registered.")

        challenge_record = await self.challenge_record_repository.find_recent_one_by_device_token(
            session, user_device.id
        )

        if challenge_record is None:
            raise NotFoundException(ErrorCode.DATA_DOES_NOT_EXIST, "Timer has not been started.")

        challenge_record.update(challenge_record.count, datetime.strptime(request.end_time, "%Y-%m-%d %H:%M:%S"))

    @transactional(read_only=True)
    async def send_message(self, session: AsyncSession, message: MessageRequest):
        user_device = await self.user_device_repository.find_by_device_token(session, message.device_token)
        if user_device is None:
            raise NotFoundException(
                ErrorCode.DATA_DOES_NOT_EXIST, f"user id {message.user_id} don't have any registered device(s)"
            )

        batch_response = firebase_manager.send(
            message.message, message.notify.get("title"), message.notify.get("body"), [user_device.device_token]
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
