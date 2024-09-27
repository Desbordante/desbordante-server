from typing import Protocol
from uuid import UUID

from internal.domain.task.entities import match_task_by_primitive_name
from internal.domain.task.value_objects import OneOfTaskResult, OneOfTaskConfig
from internal.dto.repository.file import (
    DatasetFindSchema,
    DatasetResponseSchema,
    FileMetadataResponseSchema,
)
from internal.dto.repository.file import CSVFileFindSchema, CSVFileResponseSchema
from internal.dto.repository.file import (
    DatasetNotFoundException,
    FileMetadataNotFoundException,
)
from internal.usecase.file.exception import (
    DatasetNotFoundException as DatasetNotFoundUseCaseException,
)
from internal.usecase.file.exception import (
    FileMetadataNotFoundException as FileMetadataNotFoundUseCaseException,
)
from internal.uow import UnitOfWork, DataStorageContext


class DatasetRepo(Protocol):

    def find_with_file_metadata(
        self, dataset_info: DatasetFindSchema, context: DataStorageContext
    ) -> tuple[DatasetResponseSchema, FileMetadataResponseSchema]: ...


class FileRepo(Protocol):

    def find(
        self, file_info: CSVFileFindSchema, context: DataStorageContext
    ) -> CSVFileResponseSchema: ...


class ProfileTask:

    def __init__(
        self,
        # It is assumed that the two repositories will be associated with different repositories.
        # In order to support different repositories, different UoW will be needed.
        # If both of your repositories are linked to the same repository, use only one of the UoW.
        file_unit_of_work: UnitOfWork,
        dataset_unit_of_work: UnitOfWork,
        file_repo: FileRepo,
        dataset_repo: DatasetRepo,
    ):
        self.file_unit_of_work = file_unit_of_work
        self.dataset_unit_of_work = dataset_unit_of_work
        self.file_repo = file_repo
        self.dataset_repo = dataset_repo

    def __call__(self, *, dataset_id: UUID, config: OneOfTaskConfig) -> OneOfTaskResult:

        with self.file_unit_of_work as file_context:
            with self.dataset_unit_of_work as dataset_context:
                try:
                    dataset, file_metadata = self.dataset_repo.find_with_file_metadata(
                        DatasetFindSchema(id=dataset_id), dataset_context
                    )

                    df = self.file_repo.find(
                        CSVFileFindSchema(
                            file_name=file_metadata.file_name,
                            separator=dataset.separator,
                            header=dataset.header,
                        ),
                        file_context,
                    )
                except DatasetNotFoundException:
                    raise DatasetNotFoundUseCaseException()
                except FileMetadataNotFoundException:
                    raise FileMetadataNotFoundUseCaseException()

        task = match_task_by_primitive_name(primitive_name=config.primitive_name)
        result = task.execute(table=df, task_config=config)  # type: ignore
        return result
