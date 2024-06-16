import os
import uuid
from fastapi import UploadFile
from miniopy_async import Minio
from app.config import MINIO_KEY, MINIO_URL, MINIO_SECRET, BUCKET_NAME


class MinioService:
    __instance = None

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = MinioService()
        return cls.__instance

    def __init__(self):
        self.minio_url = MINIO_URL
        self.minio_access_key = MINIO_KEY
        self.minio_secret_key = MINIO_SECRET
        self.bucket_name = BUCKET_NAME
        self.minio_client = Minio(
            self.minio_url,
            access_key=self.minio_access_key,
            secret_key=self.minio_secret_key,
            secure=False
        )

    async def put_object(self, file: UploadFile) -> str:
        bucket_name = self.bucket_name

        if not self.minio_client.bucket_exists(bucket_name):
            self.minio_client.make_bucket(bucket_name)

        file_id = str(uuid.uuid4())
        file_name = file_id + ".jpg"

        with file.file as file_data:
            await self.minio_client.put_object(
                bucket_name=bucket_name,
                object_name=file_name,
                data=file_data,
                length=os.fstat(file_data.fileno()).st_size,
                content_type="image/jpeg"
            )

        return file_id

    async def remove_object(self, file_name: str) -> None:
        await self.minio_client.remove_object(
            bucket_name=self.bucket_name,
            object_name=file_name + ".jpg",
        )

    async def get_object(self, file_name: str):

        image_url = await self.minio_client.presigned_get_object(bucket_name=self.bucket_name,
                                                                 object_name=file_name + ".jpg")
        return image_url