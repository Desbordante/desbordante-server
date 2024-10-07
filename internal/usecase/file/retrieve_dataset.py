from typing import Protocol
from uuid import UUID
from pydantic import BaseModel

from internal.dto.repository.file import DatasetFindSchema, DatasetResponseSchema
from internal.uow import DataStorageContext, UnitOfWork
from internal.usecase.file.exception import DatasetNotFoundException


class DatasetRepo(Protocol):
    def find(
        self, dataset_info: DatasetFindSchema, context: DataStorageContext
    ) -> DatasetResponseSchema | None: ...


class RetrieveDatasetUseCaseResult(BaseModel):
    id: UUID
    file_id: UUID
    separator: str
    header: list[int]


class RetrieveDataset:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
        dataset_repo: DatasetRepo,
    ):
        self.unit_of_work = unit_of_work
        self.dataset_repo = dataset_repo

    def __call__(self, *, dataset_id: UUID) -> RetrieveDatasetUseCaseResult:
        dataset_find_schema = DatasetFindSchema(
            id=dataset_id,
        )

        with self.unit_of_work as context:
            dataset = self.dataset_repo.find(dataset_find_schema, context)

            if not dataset:
                raise DatasetNotFoundException()

        return RetrieveDatasetUseCaseResult(
            id=dataset.id,
            file_id=dataset.file_id,
            separator=dataset.separator,
            header=dataset.header,
        )
