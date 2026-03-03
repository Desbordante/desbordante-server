from typing import Any

from fastapi import APIRouter, File, Form, Request, UploadFile, status

from src.api.dependencies import AuthenticatedActorDep
from src.api.user.dependencies import (
    CheckContentTypeUseCaseDep,
    UploadMyDatasetUseCaseDep,
)
from src.infrastructure.rate_limit.config import settings as rate_limit_settings
from src.infrastructure.rate_limit.limiter import limiter
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
    "/me/datasets/",
    response_model=DatasetSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Upload my dataset",
    description="Upload dataset to current user's account",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
        status.HTTP_409_CONFLICT: {"model": ApiErrorSchema},
        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE: {"model": ApiErrorSchema},
        status.HTTP_429_TOO_MANY_REQUESTS: {"model": ApiErrorSchema},
    },
)
@limiter.limit(rate_limit_settings.UPLOAD_RATE_LIMIT)
@limiter.limit(rate_limit_settings.UPLOAD_RATE_LIMIT_HOURLY)
async def upload_my_dataset(
    request: Request,
    upload_dataset: UploadMyDatasetUseCaseDep,
    check_content_type: CheckContentTypeUseCaseDep,
    actor: AuthenticatedActorDep,
    file: UploadFile = File(...),
    is_public: bool = Form(default=False),
    params: OneOfUploadDatasetParams = Form(...),
) -> Any:
    adapted_file = UploadFileAdapter(upload_file=file)

    check_content_type(file=adapted_file)

    return await upload_dataset(
        actor=actor, file=adapted_file, params=params, is_public=is_public
    )
