import os
import glob

from minio import Minio

# Файл ждя загрузки мемов(используя S3-совместимое хранилище (н-р, MinIO).)
MINIO_ENDPOINT = 'minio:9000'
MINIO_ACCESS_KEY = 'minioadmin'
MINIO_SECRET_KEY = 'minioadmin'
MINIO_PORT = '9000'
MINIO_BUCKET_NAME = 'Roman777'

storage = Minio(MINIO_ENDPOINT, access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY)


class Storage:
    def __init__(self):
        self.bucket_name = MINIO_BUCKET_NAME

    def upload_file(self, file_path):
        with open(file_path, 'rb') as file:
            filename = os.path.basename(file_path)
            storage.put_object(
                self.bucket_name,
                filename,
                file,
                length=os.path.getsize(file_path)
            )

    def upload_collection(self, directory):
        files = glob.glob(os.path.join(directory, '*.jpg'), recursive=True) + glob.glob(
            os.path.join(directory, '*.jpeg'), recursive=True)
        for file_path in files:
            self.upload_file(file_path)

    def get_file_url(self, filename):
        return f'http://{MINIO_ENDPOINT}:{MINIO_PORT}/{self.bucket_name}/{filename}'


# Пример использования
directory = './'
Storage().upload_collection(directory)

# # Получение URL-адреса файла
# filename = 'example.jpg'
# file_url = Storage().get_file_url(filename)
# print(file_url)
