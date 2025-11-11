from typing import Annotated

from fastapi import Depends

from src.api.dependencies import DatasetCrudDep, UserSessionDep
from src.schemas.dataset_schemas import DatasetQueryParamsSchema
from src.usecases.dataset.delete_dataset import DeleteDatasetUseCase
from src.usecases.dataset.get_dataset import GetDatasetUseCase
from src.usecases.dataset.get_datasets import GetDatasetsUseCase
from src.usecases.dataset.upload_dataset import UploadDatasetUseCase


async def get_upload_dataset_use_case(
    dataset_crud: DatasetCrudDep,
    user_session: UserSessionDep,
) -> UploadDatasetUseCase:
    return UploadDatasetUseCase(dataset_crud=dataset_crud, user=user_session)


UploadDatasetUseCaseDep = Annotated[
    UploadDatasetUseCase, Depends(get_upload_dataset_use_case)
]


async def get_get_datasets_use_case(
    dataset_crud: DatasetCrudDep,
    user_session: UserSessionDep,
) -> GetDatasetsUseCase:
    return GetDatasetsUseCase(dataset_crud=dataset_crud, user=user_session)


GetDatasetsUseCaseDep = Annotated[
    GetDatasetsUseCase, Depends(get_get_datasets_use_case)
]


async def get_get_dataset_use_case(
    dataset_crud: DatasetCrudDep,
    user_session: UserSessionDep,
) -> GetDatasetUseCase:
    return GetDatasetUseCase(dataset_crud=dataset_crud, user=user_session)


GetDatasetUseCaseDep = Annotated[GetDatasetUseCase, Depends(get_get_dataset_use_case)]


async def get_delete_dataset_use_case(
    dataset_crud: DatasetCrudDep,
    user_session: UserSessionDep,
) -> DeleteDatasetUseCase:
    return DeleteDatasetUseCase(dataset_crud=dataset_crud, user=user_session)


DeleteDatasetUseCaseDep = Annotated[
    DeleteDatasetUseCase, Depends(get_delete_dataset_use_case)
]


DatasetQueryParamsDep = Annotated[
    DatasetQueryParamsSchema,
    Depends(DatasetQueryParamsSchema),
]
