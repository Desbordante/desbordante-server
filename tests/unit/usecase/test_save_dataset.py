from uuid import uuid4

import pytest
from pytest_mock import MockerFixture

from internal.dto.repository.file import DatasetResponseSchema, DatasetCreateSchema
from internal.uow import DataStorageContext
from internal.usecase.file.save_dataset import DatasetRepo, SaveDataset


@pytest.fixture
def unit_of_work_mock(mocker: MockerFixture):
    mock = mocker.MagicMock()
    mock.__enter__.return_value = mocker.Mock(
        return_value=mocker.Mock(), spec=DataStorageContext
    )
    mock.__exit__.return_value = mocker.Mock(return_value=None)
    return mock


@pytest.fixture
def dataset_repo_mock(mocker: MockerFixture):
    mock = mocker.Mock(spec=DatasetRepo)
    return mock


@pytest.fixture
def save_dataset(unit_of_work_mock, dataset_repo_mock):
    return SaveDataset(unit_of_work=unit_of_work_mock, dataset_repo=dataset_repo_mock)


def test_save_dataset(
    save_dataset,
    unit_of_work_mock,
    dataset_repo_mock,
) -> None:
    # Prepare data
    file_id = uuid4()
    dataset_id = uuid4()
    separator = "?"
    header = [1, 2, 3]

    dataset_repo_mock.create.return_value = DatasetResponseSchema(
        id=dataset_id, file_id=file_id, separator=separator, header=header
    )

    # Act
    result_id = save_dataset(file_id=file_id, separator=separator, header=header)

    # Check that the create method was called with the correct arguments
    dataset_repo_mock.create.assert_called_once_with(
        DatasetCreateSchema(file_id=file_id, separator=separator, header=header),
        unit_of_work_mock.__enter__.return_value,
    )

    # Check that UnitOfWork was entered and exited correctly
    unit_of_work_mock.__enter__.assert_called_once()
    unit_of_work_mock.__exit__.assert_called_once()

    # Verify that the result of the use case matches the expected dataset_id
    assert result_id == dataset_id
