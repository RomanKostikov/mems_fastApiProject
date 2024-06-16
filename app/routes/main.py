# сервис с публичным API с бизнес-логикой
import io
import logging
import typing as t

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.exceptions import HTTPException
from starlette import status

from ..storage import MinioService
from . import serializers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
minio = MinioService.get_instance()

router = APIRouter()


@router.post("/images/")
async def upload_file(file: t.Optional[UploadFile] = File(None)) -> JSONResponse:
    if file is not None:
        try:
            image_id = await minio.put_object(file)
            return JSONResponse(content=serializers.UploadResponse(
                ID=image_id,
                message='Image Uploaded OK').model_dump(),
                status_code=status.HTTP_201_CREATED
            )

        except Exception:
            logger.exception('Occurred unhandled error while processing image')
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Failed to process given message with unhandled error',
            )

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='No file provided',
    )


@router.get("/images/{image_id}")
async def download(image_id: str):
    try:
        redirect_url = await minio.get_object(image_id)
        return RedirectResponse(url=redirect_url)
    except:
        return JSONResponse(status_code=404, content={"message": "Image not found"})


@router.delete("/images/{image_id}")
async def delete(image_id: str):
    try:
        await minio.remove_object(image_id)
    except:
        return JSONResponse(status_code=404, content={"message": "Image not found"})