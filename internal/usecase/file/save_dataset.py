from typing import Protocol
from uuid import UUID

from internal.dto.repository.file import DatasetCreateSchema, DatasetResponseSchema
from internal.uow import DataStorageContext, UnitOfWork


class DatasetRepo(Protocol):

    def create(self, dataset_info: DatasetCreateSchema, context: DataStorageContext) -> DatasetResponseSchema: ...


class SaveDataset:

    def __init__(self, unit_of_work: UnitOfWork, dataset_repo: DatasetRepo):
        self.unit_of_work = unit_of_work
        self.dataset_repo = dataset_repo

    def __call__(
            self,
            *,
            file_id: UUID,
            separator: str,
            header: list[int],
    ) -> UUID:

        dataset_create_schema = DatasetCreateSchema(
            file_id=file_id,
            separator=separator,
            header=header
        )

        with self.unit_of_work as context:
            result = self.dataset_repo.create(dataset_create_schema, context)

        return result.id
