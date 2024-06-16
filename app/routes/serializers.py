from pydantic import BaseModel
from tricky.typing import String


class UploadResponse(BaseModel):
    ID: String
    message: String