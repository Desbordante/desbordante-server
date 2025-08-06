from typing import Annotated

from fastapi import Depends

from src.api.dependencies import DatasetCrudDep, VerifiedUserDep
from src.usecases.dataset.upload_dataset import UploadDatasetUseCase


def get_upload_dataset_use_case(
    dataset_crud: DatasetCrudDep,
    user: VerifiedUserDep,
) -> UploadDatasetUseCase:
    return UploadDatasetUseCase(dataset_crud=dataset_crud, user=user)


UploadDatasetUseCaseDep = Annotated[
    UploadDatasetUseCase, Depends(get_upload_dataset_use_case)
]


# def get_get_datasets_use_case(
#     dataset_crud: DatasetCrudDep,
#     user: AuthorizedUserDep,
# ) -> GetDatasetsUseCase:
#     return GetDatasetsUseCase(dataset_crud=dataset_crud, user=user)


# GetDatasetsUseCaseDep = Annotated[
#     GetDatasetsUseCase, Depends(get_get_datasets_use_case)
# ]
