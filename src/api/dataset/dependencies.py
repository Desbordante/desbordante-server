from typing import Annotated

from fastapi import Depends

from src.api.dependencies import DatasetCrudDep, DatasetPolicyDep
from src.usecases.dataset.delete_dataset import DeleteDatasetUseCase
from src.usecases.dataset.get_dataset import GetDatasetUseCase


async def get_get_dataset_use_case(
    dataset_crud: DatasetCrudDep,
    dataset_policy: DatasetPolicyDep,
) -> GetDatasetUseCase:
    return GetDatasetUseCase(dataset_crud=dataset_crud, dataset_policy=dataset_policy)


GetDatasetUseCaseDep = Annotated[GetDatasetUseCase, Depends(get_get_dataset_use_case)]


async def get_delete_dataset_use_case(
    dataset_crud: DatasetCrudDep,
) -> DeleteDatasetUseCase:
    return DeleteDatasetUseCase(dataset_crud=dataset_crud)


DeleteDatasetUseCaseDep = Annotated[
    DeleteDatasetUseCase, Depends(get_delete_dataset_use_case)
]
