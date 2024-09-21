from fastapi import Depends

from internal.rest.http.di import (
    get_unit_of_work,
    get_file_repo,
    get_file_metadata_repo,
    get_dataset_repo,
)
from internal.uow import UnitOfWork
from internal.usecase.file import SaveFile, SaveDataset, CheckContentType
from internal.usecase.file.retrieve_dataset import RetrieveDataset
from internal.usecase.file.save_dataset import DatasetRepo as SaveDatasetRepo
from internal.usecase.file.retrieve_dataset import DatasetRepo as RetrieveDatasetRepo
from internal.usecase.file.save_file import FileRepo, FileMetadataRepo


def get_save_file_use_case(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    file_repo: FileRepo = Depends(get_file_repo),
    file_metadata_repo: FileMetadataRepo = Depends(get_file_metadata_repo),
) -> SaveFile:
    return SaveFile(
        unit_of_work=unit_of_work,
        file_repo=file_repo,
        file_metadata_repo=file_metadata_repo,
    )


def get_save_dataset_use_case(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    dataset_repo: SaveDatasetRepo = Depends(get_dataset_repo),
) -> SaveDataset:
    return SaveDataset(
        unit_of_work=unit_of_work,
        dataset_repo=dataset_repo,
    )


def get_check_content_type_use_case() -> CheckContentType:
    return CheckContentType()


def get_retrieve_dataset_use_case(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    dataset_repo: RetrieveDatasetRepo = Depends(get_dataset_repo),
) -> RetrieveDataset:
    return RetrieveDataset(
        unit_of_work=unit_of_work,
        dataset_repo=dataset_repo,
    )
