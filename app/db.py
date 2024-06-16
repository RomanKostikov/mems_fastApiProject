import os
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker
from minio import Minio
from config import BUCKET_NAME, MINIO_URL, MINIO_KEY, MINIO_SECRET

# Создаем экземпляр MinIO-клиента
minio_client = Minio(
    MINIO_URL,
    access_key=MINIO_KEY,
    secret_key=MINIO_SECRET,
    secure=False
)

# Создаем подключение к базе данных SQLite3 с помощью SQLAlchemy
engine = create_engine('sqlite:///file.db')
metadata = MetaData()
file_ids_table = Table('file_ids', metadata,
                       Column('id', Integer, primary_key=True),
                       Column('object_name', String)
                       )
metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Получаем список объектов в bucket
objects = minio_client.list_objects(
    bucket_name=BUCKET_NAME,
    prefix='',
    recursive=True
)

# Сохраняем идентификаторы файлов в SQLite3 с использованием SQLAlchemy
for obj in objects:
    session.execute(file_ids_table.insert().values(object_name=obj.object_name))

# Сохраняем изменения в базе данных
session.commit()
