from typing import Any

from fastapi import APIRouter, File, Form, UploadFile, status

from src.api.user.dependencies import UploadMyDatasetUseCaseDep
from src.schemas.base_schemas import ApiErrorSchema
from src.schemas.dataset_schemas import OneOfUploadDatasetParams, PrivateDatasetSchema

router = APIRouter()


class UploadFileAdapter:
    def __init__(self, upload_file: UploadFile):
        self.name = upload_file.filename or ""
        self.content_type = upload_file.content_type or ""
        self.data = upload_file.file
        self.size = upload_file.size or 0


@router.post(
    "/me/datasets/",
    response_model=PrivateDatasetSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Upload my private dataset",
    description="Upload private dataset for current user",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
        status.HTTP_409_CONFLICT: {"model": ApiErrorSchema},
        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE: {"model": ApiErrorSchema},
        status.HTTP_429_TOO_MANY_REQUESTS: {"model": ApiErrorSchema},
    },
)
async def upload_my_dataset(
    upload_dataset: UploadMyDatasetUseCaseDep,
    file: UploadFile = File(...),
    params: OneOfUploadDatasetParams = Form(...),
) -> Any:
    adapted_file = UploadFileAdapter(upload_file=file)

    return await upload_dataset(file=adapted_file, params=params, is_public=False)
