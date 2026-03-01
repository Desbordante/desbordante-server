from io import BytesIO
from typing import Protocol
from uuid import UUID

import pandas as pd

from src.domain.task.entities import match_task_by_primitive_name
from src.domain.task.value_objects import OneOfTaskConfig, OneOfTaskResult
from src.models.dataset_models import DatasetModel
from src.schemas.dataset_schemas import TabularDatasetParams


class DatasetCrud(Protocol):
    async def get_by(self, *, id: UUID) -> DatasetModel: ...


class Storage(Protocol):
    async def download(self, *, path: str) -> bytes: ...


class ProfileTaskUseCase:
    def __init__(
        self,
        *,
        dataset_crud: DatasetCrud,
        storage: Storage,
    ):
        self._dataset_crud = dataset_crud
        self._storage = storage

    async def __call__(
        self, *, dataset_id: UUID, config: OneOfTaskConfig
    ) -> OneOfTaskResult:
        dataset = await self._dataset_crud.get_by(id=dataset_id)

        params = TabularDatasetParams.model_validate(dataset.params)

        bytes = await self._storage.download(path=dataset.path)

        df = pd.read_csv(
            BytesIO(bytes),
            sep=params.separator,
            header=0 if params.has_header else None,
        )

        task = match_task_by_primitive_name(primitive_name=config.primitive_name)
        result = task.execute(table=df, task_config=config)  # type: ignore
        return result
