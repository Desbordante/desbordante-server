from fastapi import Depends

from internal.infrastructure.data_storage.flat import FlatContextMaker
from internal.infrastructure.data_storage.relational.postgres.context import (
    get_postgres_context_maker,
    get_postgres_context_maker_without_pool,
)
from internal.repository.flat import FileRepository
from internal.repository.relational.file import (
    FileMetaDataRepository,
    DatasetRepository,
)
from internal.repository.relational.task import TaskRepository
from internal.uow import UnitOfWork


def get_unit_of_work(context_maker=Depends(get_postgres_context_maker)) -> UnitOfWork:

    return UnitOfWork(context_maker)


def get_unit_of_work_without_pool(
    context_maker=Depends(get_postgres_context_maker_without_pool),
) -> UnitOfWork:

    return UnitOfWork(context_maker)


def get_flat_unit_of_work(context_maker: FlatContextMaker = Depends()) -> UnitOfWork:

    return UnitOfWork(context_maker)


def get_file_repo() -> FileRepository:
    return FileRepository()


def get_file_metadata_repo() -> FileMetaDataRepository:
    return FileMetaDataRepository()


def get_dataset_repo() -> DatasetRepository:
    return DatasetRepository()


def get_task_repo() -> TaskRepository:
    return TaskRepository()
