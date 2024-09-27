from uuid import uuid4

import pandas as pd
import pytest
from pytest_mock import MockerFixture

from internal.uow import DataStorageContext
from internal.domain.task.value_objects import FdTaskConfig, PrimitiveName, FdTaskResult
from internal.domain.task.value_objects.fd import FdAlgoResult
from internal.domain.task.value_objects.fd.algo_config import AidConfig
from internal.usecase.task.profile_task import DatasetRepo, FileRepo, ProfileTask
from internal.usecase.file.exception import (
    DatasetNotFoundException as DatasetNotFoundUseCaseException,
)
from internal.usecase.file.exception import (
    FileMetadataNotFoundException as FileMetadataNotFoundUseCaseException,
)
from internal.dto.repository.file import (
    FileMetadataResponseSchema,
    DatasetResponseSchema,
    DatasetFindSchema,
    CSVFileFindSchema,
    DatasetNotFoundException,
    FileMetadataNotFoundException,
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
def file_repo_mock(mocker: MockerFixture):
    mock = mocker.Mock(spec=FileRepo)
    return mock


@pytest.fixture
def profile_task_use_case(
    unit_of_work_mock,
    dataset_repo_mock,
    file_repo_mock,
) -> ProfileTask:
    return ProfileTask(
        file_unit_of_work=unit_of_work_mock,
        dataset_unit_of_work=unit_of_work_mock,
        dataset_repo=dataset_repo_mock,
        file_repo=file_repo_mock,
    )


def test_profile_task_use_case_success(
    mocker: MockerFixture,
    profile_task_use_case,
    unit_of_work_mock,
    dataset_repo_mock,
    file_repo_mock,
) -> None:
    # Prepare data
    dataset_id = uuid4()
    file_id = uuid4()

    file_metadata_response = FileMetadataResponseSchema(
        id=file_id,
        file_name=uuid4(),
        original_file_name="name",
        mime_type="application/octet-stream",
    )

    dataset_response = DatasetResponseSchema(
        id=dataset_id,
        file_id=file_id,
        separator=",",
        header=[0],
    )

    cvs_file_read_response = pd.DataFrame(
        {"column1": [1, 2, 3], "column2": ["a", "b", "c"]}
    )

    aid_config = AidConfig(algo_name="aid")  # type: ignore
    task_config = FdTaskConfig(primitive_name=PrimitiveName.fd, config=aid_config)

    task_result = FdTaskResult(
        primitive_name=PrimitiveName.fd, result=FdAlgoResult(fds=[])
    )

    # Mocks
    dataset_repo_mock.find_with_file_metadata.return_value = (
        dataset_response,
        file_metadata_response,
    )
    file_repo_mock.find.return_value = cvs_file_read_response

    # Mock the execution of the task
    task_mock = mocker.Mock()
    task_mock.execute.return_value = task_result
    mocker.patch(
        "internal.usecase.task.profile_task.match_task_by_primitive_name",
        return_value=task_mock,
    )

    # Act
    result = profile_task_use_case(dataset_id=dataset_id, config=task_config)

    # Check result
    assert task_result == result

    # Check that all methods were called correctly
    dataset_repo_mock.find_with_file_metadata.assert_called_once_with(
        DatasetFindSchema(id=dataset_id),
        unit_of_work_mock.__enter__.return_value,
    )

    file_repo_mock.find.assert_called_once_with(
        CSVFileFindSchema(
            file_name=file_metadata_response.file_name,
            separator=dataset_response.separator,
            header=dataset_response.header,
        ),
        unit_of_work_mock.__enter__.return_value,
    )

    task_mock.execute.assert_called_once_with(
        table=cvs_file_read_response, task_config=task_config
    )

    # Check that UnitOfWork was entered and exited correctly
    assert unit_of_work_mock.__enter__.call_count == 2
    assert unit_of_work_mock.__exit__.call_count == 2


@pytest.mark.parametrize(
    "repo_exception, use_case_exception",
    [
        (DatasetNotFoundException, DatasetNotFoundUseCaseException),
        (FileMetadataNotFoundException, FileMetadataNotFoundUseCaseException),
    ],
)
def test_profile_task_use_case_dataset_not_found(
    profile_task_use_case,
    unit_of_work_mock,
    dataset_repo_mock,
    file_repo_mock,
    repo_exception,
    use_case_exception,
) -> None:
    # Prepare data
    dataset_id = uuid4()

    aid_config = AidConfig(algo_name="aid")  # type: ignore
    task_config = FdTaskConfig(primitive_name=PrimitiveName.fd, config=aid_config)

    # Mocks
    dataset_repo_mock.find_with_file_metadata.side_effect = repo_exception

    # Act and except error
    with pytest.raises(use_case_exception):
        profile_task_use_case(dataset_id=dataset_id, config=task_config)

    # Check that all methods were called correctly
    dataset_repo_mock.find_with_file_metadata.assert_called_once_with(
        DatasetFindSchema(id=dataset_id),
        unit_of_work_mock.__enter__.return_value,
    )

    assert not file_repo_mock.find.called

    # Check that UnitOfWork was entered and exited correctly
    assert unit_of_work_mock.__enter__.call_count == 2
    assert unit_of_work_mock.__exit__.call_count == 2
