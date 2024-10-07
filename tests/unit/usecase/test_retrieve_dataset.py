from uuid import uuid4

import pytest
from pytest_mock import MockerFixture

from internal.dto.repository.file import DatasetResponseSchema, DatasetFindSchema
from internal.uow import DataStorageContext
from internal.usecase.file.exception import DatasetNotFoundException
from internal.usecase.file.retrieve_dataset import (
    DatasetRepo,
    RetrieveDataset,
    RetrieveDatasetUseCaseResult,
)


@pytest.fixture
def unit_of_work_mock(mocker: MockerFixture):
    mock = mocker.MagicMock()
    mock.__enter__.return_value = mocker.Mock(
        return_value=mocker.Mock(), spec=DataStorageContext
    )
    mock.__exit__.return_value = None

    def exit_side_effect(exc_type, exc_value, traceback) -> bool:
        if exc_type:
            raise exc_value
        return False

    mock.__exit__.side_effect = exit_side_effect
    return mock


@pytest.fixture
def dataset_repo_mock(mocker: MockerFixture):
    mock = mocker.Mock(spec=DatasetRepo)
    return mock


@pytest.fixture
def retrieve_dataset_use_case(unit_of_work_mock, dataset_repo_mock):
    return RetrieveDataset(
        unit_of_work=unit_of_work_mock, dataset_repo=dataset_repo_mock
    )


def test_retrieve_dataset_use_case_success(
    unit_of_work_mock,
    dataset_repo_mock,
    retrieve_dataset_use_case,
):
    # Prepare data
    dataset_id = uuid4()
    file_id = uuid4()

    dataset_repo_mock.find.return_value = DatasetResponseSchema(
        id=dataset_id, file_id=file_id, separator="?", header=[1, 2, 3, 4, 5]
    )

    # Act
    result = retrieve_dataset_use_case(dataset_id=dataset_id)

    # Check result
    assert result == RetrieveDatasetUseCaseResult(
        id=dataset_id, file_id=file_id, separator="?", header=[1, 2, 3, 4, 5]
    )

    # Check that repositories' find method work correctly
    dataset_repo_mock.find.assert_called_once_with(
        DatasetFindSchema(id=dataset_id), unit_of_work_mock.__enter__.return_value
    )

    # Check that UnitOfWork was entered and exited correctly
    unit_of_work_mock.__enter__.assert_called_once()
    unit_of_work_mock.__exit__.assert_called_once()


def test_retrieve_dataset_use_case_not_found(
    unit_of_work_mock,
    retrieve_dataset_use_case,
    dataset_repo_mock,
):
    # Prepare data
    dataset_id = uuid4()

    # Mocks repository operations
    dataset_repo_mock.find.return_value = None

    # Act and except error
    with pytest.raises(DatasetNotFoundException):
        retrieve_dataset_use_case(dataset_id=dataset_id)

    # Check that repositories' find method work correctly
    dataset_repo_mock.find.assert_called_once_with(
        DatasetFindSchema(id=dataset_id), unit_of_work_mock.__enter__.return_value
    )

    # Check that UnitOfWork was entered and exited correctly
    unit_of_work_mock.__enter__.assert_called_once()
    unit_of_work_mock.__exit__.assert_called_once()
