from typing import Annotated

from fastapi import Depends

from src.api.dependencies import DatasetCrudDep
from src.usecases.dataset.get_public_datasets import GetPublicDatasetsUseCase


async def get_get_public_datasets_use_case(
    dataset_crud: DatasetCrudDep,
) -> GetPublicDatasetsUseCase:
    return GetPublicDatasetsUseCase(dataset_crud=dataset_crud)


GetPublicDatasetsUseCaseDep = Annotated[
    GetPublicDatasetsUseCase, Depends(get_get_public_datasets_use_case)
]
