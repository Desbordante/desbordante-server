from typing import Annotated

from fastapi import Depends

from src.api.dependencies import DatasetCrudDep
from src.usecases.dataset.delete_dataset import DeleteDatasetUseCase
from src.usecases.dataset.get_dataset import GetDatasetUseCase


async def get_get_dataset_use_case(
    dataset_crud: DatasetCrudDep,
) -> GetDatasetUseCase:
    return GetDatasetUseCase(dataset_crud=dataset_crud)


GetDatasetUseCaseDep = Annotated[GetDatasetUseCase, Depends(get_get_dataset_use_case)]


async def get_delete_dataset_use_case(
    dataset_crud: DatasetCrudDep,
) -> DeleteDatasetUseCase:
    return DeleteDatasetUseCase(dataset_crud=dataset_crud)


DeleteDatasetUseCaseDep = Annotated[
    DeleteDatasetUseCase, Depends(get_delete_dataset_use_case)
]
