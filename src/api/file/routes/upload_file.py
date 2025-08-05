from typing import Any

from fastapi import APIRouter, File, UploadFile, status

from src.api.file.dependencies import UploadFileUseCaseDep
from src.schemas.base_schemas import ApiErrorSchema
from src.schemas.file_schemas import FileSchema

router = APIRouter()


class UploadFileAdapter:
    def __init__(self, upload_file: UploadFile):
        self.name = upload_file.filename or ""
        self.content_type = upload_file.content_type or ""
        self.data = upload_file.file
        self.size = upload_file.size or 0


@router.post(
    "/",
    response_model=FileSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Upload file",
    description="Upload file to server",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
        status.HTTP_429_TOO_MANY_REQUESTS: {"model": ApiErrorSchema},
    },
)
async def upload_file(
    upload_file: UploadFileUseCaseDep,
    file: UploadFile = File(...),
) -> Any:
    adapted_file = UploadFileAdapter(upload_file=file)

    return await upload_file(file=adapted_file)
