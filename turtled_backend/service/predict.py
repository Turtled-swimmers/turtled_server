from ulid import ULID
from fastapi import FastAPI, File, UploadFile, Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import FileResponse

from turtled_backend.common.util.transaction import transactional
from turtled_backend.common.util.s3 import S3_CLIENT
from turtled_backend.common.util.posture_package import run_prediction
from turtled_backend.model.response.predict import PredictResponse, PredictRecordResponse, PredictRecordDetailResponse
from turtled_backend.config.config import Config
from turtled_backend.common.error.exception import ErrorCode, NotFoundException
from turtled_backend.repository.challenge import PredictRecordRepository, ExerciseListRepository
from turtled_backend.schema.challenge import PredictRecord
from turtled_backend.repository.user import UserRepository
from turtled_backend.model.request.user import UserRequest
from turtled_backend.model.request.predict import PredictRecordDetailRequest


class PredictService:
    def __init__(
        self,
        predict_record_repository: PredictRecordRepository,
        user_repository: UserRepository,
        exercise_list_repository: ExerciseListRepository
    ):
        self.predict_record_repository = predict_record_repository
        self.user_repository = user_repository
        self.exercise_list_repository = exercise_list_repository

    @transactional()
    async def upload_file(self, session: AsyncSession, servey_video: UploadFile):
        IMAGE_PATH = Config.BASE_DIR + "/temp/"
        image_uid = str(ULID())
        input_filename = IMAGE_PATH + "input-" + image_uid + ".mp4"

        content = await servey_video.read()
        with open(input_filename, "wb") as fp:
            fp.write(content)

        try:
            max_neck_angle, targetFile = await run_prediction(image_uid)
            percentage = max_neck_angle / 90 * 100
        except Exception as e:
            raise NotFoundException(ErrorCode.ROW_ALREADY_EXIST, "사용자의 자세를 찾을 수 없습니다.")

        try:
            await S3_CLIENT.s3_upload(targetFile, f"temp/{image_uid}.jpg")
            target_image = await S3_CLIENT.s3_download(f"temp/{image_uid}.jpg")
        except Exception as e:
            raise NotFoundException(ErrorCode.ROW_ALREADY_EXIST, "S3 image upload failed.")

        return PredictResponse.of(percentage=percentage, image=target_image)

    @transactional()
    async def user_upload_file(self, session: AsyncSession, servey_video: UploadFile, subject: UserRequest):

        user = await self.user_repository.find_by_id(session, subject.id)
        if user is None:
            raise NotFoundException(ErrorCode.DATA_DOES_NOT_EXIST, "User not found")

        IMAGE_PATH = Config.BASE_DIR + "/temp/"
        image_uid = str(ULID())
        input_filename = IMAGE_PATH + "input-" + image_uid + ".mp4"

        content = await servey_video.read()
        with open(input_filename, "wb") as fp:
            fp.write(content)

        try:
            max_neck_angle, targetFile = await run_prediction(image_uid)
            percentage = max_neck_angle / 90 * 100
        except Exception as e:
            raise NotFoundException(ErrorCode.ROW_ALREADY_EXIST, "사용자의 자세를 찾을 수 없습니다.")

        try:
            await S3_CLIENT.s3_upload(targetFile, f"temp/{image_uid}.jpg")
            target_image = await S3_CLIENT.s3_download(f"temp/{image_uid}.jpg")
        except Exception as e:
            raise NotFoundException(ErrorCode.ROW_ALREADY_EXIST, "S3 image upload failed.")

        predict_record = await self.predict_record_repository.save(
            session,
            PredictRecord.of(
                nerd_neck_percentage=percentage,
                img_url=target_image,
                user_id=subject.id
            ),
        )

        return PredictResponse.of(percentage=percentage,
                                  image=target_image)

    @transactional(read_only=True)
    async def find_predict_history(self, session: AsyncSession, subject: UserRequest):

        user = await self.user_repository.find_by_id(session, subject.id)
        if user is None:
            raise NotFoundException(ErrorCode.DATA_DOES_NOT_EXIST, "User not found")

        predict_record_list = await self.predict_record_repository.find_all_by_user(
            session,
            user.id
        )

        return [PredictRecordResponse.from_entity(entity) for entity in predict_record_list]


    @transactional(read_only=True)
    async def find_predict_history_detail(self, session: AsyncSession, subject: UserRequest,
                                          req: PredictRecordDetailRequest):
        user = await self.user_repository.find_by_id(session, subject.id)
        if user is None:
            raise NotFoundException(ErrorCode.DATA_DOES_NOT_EXIST, "User not found")

        predict_record = await self.predict_record_repository.find_by_id(
            session,
            req.record_id
        )

        if predict_record is None:
            raise NotFoundException(ErrorCode.DATA_DOES_NOT_EXIST, "predict_record not found")

        if predict_record.nerd_neck_percentage > 44:
            exercise_image_list = await self.exercise_list_repository.find_by_percentage(session, 90)
        else:
            exercise_image_list = await self.exercise_list_repository.find_by_percentage(session, 20)

        exercise_images = [{"image": exercise.img_url, "description": exercise.description}
                           for exercise in exercise_image_list]
        print("LOG:", exercise_images)
        return PredictRecordDetailResponse.of(predict_record.nerd_neck_percentage, predict_record.img_url, exercise_images)