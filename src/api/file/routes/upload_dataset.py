from typing import Annotated, Any

from fastapi import APIRouter, File, Query, UploadFile, status

from src.api.file.dependencies import UploadDatasetUseCaseDep
from src.schemas.base_schemas import ApiErrorSchema
from src.schemas.file_schemas import (
    DatasetSchema,
    FileType,
    UploadTabularDatasetSchema,
)

router = APIRouter()


class UploadFileAdapter:
    type = FileType.Dataset

    def __init__(self, upload_file: UploadFile):
        self.name = upload_file.filename or ""
        self.content_type = upload_file.content_type or ""
        self._upload_file = upload_file
        self.data = upload_file.file
        self.size = upload_file.size or 0

    async def read(self, chunk_size: int) -> bytes:
        return await self._upload_file.read(chunk_size)


@router.post(
    "/datasets",
    response_model=DatasetSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Upload dataset",
    description="Upload dataset to server",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
        status.HTTP_403_FORBIDDEN: {"model": ApiErrorSchema},
    },
)
async def upload_dataset(
    upload_dataset: UploadDatasetUseCaseDep,
    data: Annotated[UploadTabularDatasetSchema, Query()],
    file: UploadFile = File(...),
) -> Any:
    adapted_file = UploadFileAdapter(file)

    dataset = await upload_dataset(file=adapted_file, data=data)

    return dataset
