from typing import Annotated

from fastapi import Depends

from src.api.dependencies import AuthorizedUserDep, DatasetCrudDep, VerifiedUserDep
from src.usecases.dataset.get_dataset import GetDatasetUseCase
from src.usecases.dataset.get_datasets import GetDatasetsUseCase
from src.usecases.dataset.upload_dataset import UploadDatasetUseCase


def get_upload_dataset_use_case(
    dataset_crud: DatasetCrudDep,
    user: VerifiedUserDep,
) -> UploadDatasetUseCase:
    return UploadDatasetUseCase(dataset_crud=dataset_crud, user=user)


UploadDatasetUseCaseDep = Annotated[
    UploadDatasetUseCase, Depends(get_upload_dataset_use_case)
]


def get_get_datasets_use_case(
    dataset_crud: DatasetCrudDep,
    user: AuthorizedUserDep,
) -> GetDatasetsUseCase:
    return GetDatasetsUseCase(dataset_crud=dataset_crud, user=user)


GetDatasetsUseCaseDep = Annotated[
    GetDatasetsUseCase, Depends(get_get_datasets_use_case)
]


def get_get_dataset_use_case(
    dataset_crud: DatasetCrudDep,
    user: AuthorizedUserDep,
) -> GetDatasetUseCase:
    return GetDatasetUseCase(dataset_crud=dataset_crud, user=user)


GetDatasetUseCaseDep = Annotated[GetDatasetUseCase, Depends(get_get_dataset_use_case)]
