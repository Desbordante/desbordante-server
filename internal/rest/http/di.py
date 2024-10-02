from fastapi import Depends

from internal.infrastructure.data_storage import (
    get_context_maker,
    get_context_maker_without_pool,
)
from internal.repository.flat import FileRepository
from internal.repository.relational.file import (
    FileMetadataRepository,
    DatasetRepository,
)
from internal.repository.relational.task import TaskRepository
from internal.uow import UnitOfWork


def get_unit_of_work(context_maker=Depends(get_context_maker)) -> UnitOfWork:
    return UnitOfWork(context_maker)


def get_unit_of_work_without_pool(
    context_maker=Depends(get_context_maker_without_pool),
) -> UnitOfWork:
    return UnitOfWork(context_maker)


def get_file_repo() -> FileRepository:
    return FileRepository()


def get_file_metadata_repo() -> FileMetadataRepository:
    return FileMetadataRepository()


def get_dataset_repo() -> DatasetRepository:
    return DatasetRepository()


def get_task_repo() -> TaskRepository:
    return TaskRepository()
