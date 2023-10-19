import json
import logging

import boto3
from turtled_backend.config.config import Config
from botocore.exceptions import ClientError

with open(Config.AWS_ACCESS_KEY_PATH, encoding="utf-8-sig") as f:
    aws_access_key = json.load(f)

AWS_ACCESS_KEY_ID = aws_access_key['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = aws_access_key['AWS_SECRET_ACCESS_KEY']
BUCKET_NAME = 'turtled-s3-bucket'
REGION_NAME = 'ap-northeast-2'


class S3Client:

    def __init__(self) -> None:
        self.s3_client = boto3.client(
            service_name='s3', region_name=REGION_NAME, aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

    async def s3_upload(self, filename: str, s2_path: str):
        # upload file to S3
        try:
            return self.s3_client.upload_file(filename, BUCKET_NAME, s2_path)
        except ClientError as e:
            logging.error(e)

    async def s3_download(self, s2_path: str):
        # download file to S3
        return f'https://{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/{s2_path}'


S3_CLIENT = S3Client()
