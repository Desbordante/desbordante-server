from typing import Annotated

from fastapi import Depends

from _app.dependencies.dependencies import SessionDep
from _app.domain.file.dataset.models import Dataset
from _app.domain.file.dataset.schemas import DatasetCreate
from _app.domain.file.dataset.service import DatasetService
from _app.repository.repository import BaseRepository


def get_dataset_service(session: SessionDep) -> DatasetService:
    return DatasetService(repository=BaseRepository(model=Dataset, session=session))


DatasetServiceDep = Annotated[DatasetService, Depends(get_dataset_service)]

CreateParamsDep = Annotated[DatasetCreate, Depends(DatasetCreate)]
