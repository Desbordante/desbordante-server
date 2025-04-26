from fastapi import APIRouter, File, UploadFile, status

from _app.domain.auth.dependencies import AuthorizedUserDep
from _app.domain.file.dataset.models import DatasetPublic
from _app.domain.file.schemas import FileType
from _app.schemas import HTTPApiError

from ..dependencies import StorageClientDep
from .dependencies import CreateParamsDep, DatasetServiceDep

router = APIRouter()


@router.post(
    "/",
    response_model=DatasetPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a dataset",
    description="Upload a dataset to the server. The dataset will be associated with the current user.",
    responses={status.HTTP_403_FORBIDDEN: {"model": HTTPApiError}},
)
def upload_dataset(
    user: AuthorizedUserDep,
    dataset_service: DatasetServiceDep,
    storage_client: StorageClientDep,
    params: CreateParamsDep,
    file: UploadFile = File(),
) -> DatasetPublic:
    path = storage_client.upload_file(
        file=file, type=FileType.Dataset, owner_id=user.id
    )

    file.file.seek(0)

    return dataset_service.create_dataset(
        params=params, file=file, owner_id=user.id, path=path
    )
