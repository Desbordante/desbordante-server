from typing import Any

from fastapi import APIRouter, File, Form, UploadFile, status

from src.api.dataset.dependencies import UploadDatasetUseCaseDep
from src.schemas.base_schemas import ApiErrorSchema
from src.schemas.dataset_schemas import DatasetSchema, OneOfUploadDatasetParams

router = APIRouter()


class UploadFileAdapter:
    def __init__(self, upload_file: UploadFile):
        self.name = upload_file.filename or ""
        self.content_type = upload_file.content_type or ""
        self.data = upload_file.file
        self.size = upload_file.size or 0


@router.post(
    "/",
    response_model=DatasetSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Upload dataset",
    description="Upload dataset to server",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
        status.HTTP_403_FORBIDDEN: {"model": ApiErrorSchema},
        status.HTTP_429_TOO_MANY_REQUESTS: {"model": ApiErrorSchema},
    },
)
async def upload_dataset(
    upload_dataset: UploadDatasetUseCaseDep,
    file: UploadFile = File(...),
    params: OneOfUploadDatasetParams = Form(...),
) -> Any:
    adapted_file = UploadFileAdapter(upload_file=file)

    return await upload_dataset(file=adapted_file, params=params)
