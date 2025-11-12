from typing import Annotated

from fastapi import Depends

from src.api.dependencies import AdminSessionDep, DatasetCrudDep
from src.usecases.dataset.get_public_datasets import GetPublicDatasetsUseCase
from src.usecases.dataset.upload_dataset import UploadDatasetUseCase


async def get_get_public_datasets_use_case(
    dataset_crud: DatasetCrudDep,
) -> GetPublicDatasetsUseCase:
    return GetPublicDatasetsUseCase(dataset_crud=dataset_crud)


GetPublicDatasetsUseCaseDep = Annotated[
    GetPublicDatasetsUseCase, Depends(get_get_public_datasets_use_case)
]


async def get_upload_public_dataset_use_case(
    dataset_crud: DatasetCrudDep,
    admin_session: AdminSessionDep,
) -> UploadDatasetUseCase:
    return UploadDatasetUseCase(dataset_crud=dataset_crud, user=admin_session)


UploadPublicDatasetUseCaseDep = Annotated[
    UploadDatasetUseCase, Depends(get_upload_public_dataset_use_case)
]
