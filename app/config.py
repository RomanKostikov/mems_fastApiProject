from environs import Env

env = Env()
env.read_env()

BUCKET_NAME = env.str('BUCKET_NAME')
MINIO_URL = env.str('MINIO_URL')
MINIO_KEY = env.str('MINIO_KEY')
MINIO_SECRET = env.str('MINIO_SECRET')