from ulid import ULID
from fastapi import FastAPI, File, UploadFile, Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import FileResponse

from turtled_backend.common.util.transaction import transactional
from turtled_backend.common.util.s3 import S3_CLIENT
from turtled_backend.common.util.posture_package import run_prediction
from turtled_backend.model.response.predict import PredictResponse
from turtled_backend.config.config import Config

class PredictService:
    def __init__(
        self,
        # user_challenge_repository: UserChallengeRepository,
    ):
        pass
    # self.medal_repository = medal_repository

    @transactional()
    async def upload_file(self, session: AsyncSession, servey_video: UploadFile):
        IMAGE_PATH = Config.BASE_DIR + "/temp/"
        image_uid = str(ULID())
        input_filename = IMAGE_PATH + "input-" + image_uid + ".mp4"

        content = await servey_video.read()
        with open(input_filename, "wb") as fp:
            fp.write(content)


        max_neck_angle, targetFile = await run_prediction(image_uid)
        percentage = max_neck_angle / 90 * 100


        try:
            await S3_CLIENT.s3_upload(targetFile, f"temp/{image_uid}.jpg")
            target_image = await S3_CLIENT.s3_download(f"temp/{image_uid}.jpg")
        except Exception as e:
            print(e)

        # with open(targetFile, "rb") as video:
        #     data = video.read()
        #     headers = {
        #         'Percentage': f'{percentage}',
        #     }
        return PredictResponse.of(percentage=percentage, image=target_image)  # percentage # targetFile #output_filename # Response(data, status_code=206, headers=headers, media_type="video/mp4")
