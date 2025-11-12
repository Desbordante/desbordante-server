from typing import Any

from fastapi import APIRouter, File, Form, Request, UploadFile, status

from src.api.public.dependencies import UploadPublicDatasetUseCaseDep
from src.infrastructure.rate_limit.config import settings as rate_limit_settings
from src.infrastructure.rate_limit.limiter import limiter
from src.schemas.base_schemas import ApiErrorSchema
from src.schemas.dataset_schemas import OneOfUploadDatasetParams, PublicDatasetSchema

router = APIRouter()


class UploadFileAdapter:
    def __init__(self, upload_file: UploadFile):
        self.name = upload_file.filename or ""
        self.content_type = upload_file.content_type or ""
        self.data = upload_file.file
        self.size = upload_file.size or 0


@router.post(
    "/",
    response_model=PublicDatasetSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Upload public dataset",
    description="Upload public dataset (admin only)",
    tags=["public", "admin"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
        status.HTTP_403_FORBIDDEN: {"model": ApiErrorSchema},
        status.HTTP_409_CONFLICT: {"model": ApiErrorSchema},
        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE: {"model": ApiErrorSchema},
        status.HTTP_429_TOO_MANY_REQUESTS: {"model": ApiErrorSchema},
    },
)
@limiter.limit(rate_limit_settings.UPLOAD_RATE_LIMIT)
@limiter.limit(rate_limit_settings.UPLOAD_RATE_LIMIT_HOURLY)
async def upload_public_dataset(
    request: Request,
    upload_dataset: UploadPublicDatasetUseCaseDep,
    file: UploadFile = File(...),
    params: OneOfUploadDatasetParams = Form(...),
) -> Any:
    adapted_file = UploadFileAdapter(upload_file=file)

    return await upload_dataset(file=adapted_file, params=params, is_public=True)
