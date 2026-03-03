from io import BytesIO
from uuid import uuid4

from unittest.mock import MagicMock

import pandas as pd
import pytest
from pytest_mock import MockerFixture

from src.crud.dataset_crud import DatasetCrud
from src.domain.task.value_objects import FdTaskConfig, FdTaskResult, PrimitiveName
from src.domain.task.value_objects.fd import FdAlgoResult
from src.domain.task.value_objects.fd.algo_config import AidConfig
from src.domain.task.value_objects.fd.algo_name import FdAlgoName
from src.exceptions import ResourceNotFoundException
from src.infrastructure.storage.client import S3Storage
from src.models.dataset_models import DatasetModel
from src.schemas.dataset_schemas import DatasetSeparator, TabularDatasetParams
from src.usecases.task.profile_task import ProfileTaskUseCase


@pytest.fixture
def dataset_crud_mock(mocker: MockerFixture):
    mock = mocker.Mock()
    mock.get_by = mocker.AsyncMock()
    return mock


@pytest.fixture
def storage_mock(mocker: MockerFixture):
    mock = mocker.Mock()
    mock.download = mocker.AsyncMock()
    return mock


@pytest.fixture
def profile_task_use_case(
    dataset_crud_mock: DatasetCrud,
    storage_mock: S3Storage,
) -> ProfileTaskUseCase:
    return ProfileTaskUseCase(
        dataset_crud=dataset_crud_mock,
        storage=storage_mock,
    )


pytestmark = pytest.mark.asyncio


async def test_profile_task_use_case_success(
    mocker: MockerFixture,
    profile_task_use_case: ProfileTaskUseCase,
    dataset_crud_mock: MagicMock,
    storage_mock: MagicMock,
) -> None:
    # Prepare data
    dataset_id = uuid4()
    csv_content = b"column1,column2\n1,a\n2,b\n3,c"
    expected_df = pd.read_csv(BytesIO(csv_content))

    dataset_params = TabularDatasetParams(
        has_header=True,
        separator=DatasetSeparator.COMMA,
    )
    dataset = mocker.Mock(spec=DatasetModel)
    dataset.path = "datasets/some-path.csv"
    dataset.params = dataset_params

    aid_config = AidConfig(
        algo_name=FdAlgoName.Aid,
        is_null_equal_null=True,
    )
    task_config = FdTaskConfig(primitive_name=PrimitiveName.fd, config=aid_config)

    task_result = FdTaskResult(
        primitive_name=PrimitiveName.fd, result=FdAlgoResult(fds=[])
    )

    # Mocks
    dataset_crud_mock.get_by.return_value = dataset
    storage_mock.download.return_value = csv_content

    task_mock = mocker.Mock()
    task_mock.execute.return_value = task_result
    mocker.patch(
        "src.usecases.task.profile_task.match_task_by_primitive_name",
        return_value=task_mock,
    )

    # Act
    result = await profile_task_use_case(dataset_id=dataset_id, config=task_config)

    # Assert
    assert task_result == result

    dataset_crud_mock.get_by.assert_awaited_once_with(id=dataset_id)
    storage_mock.download.assert_awaited_once_with(path=dataset.path)
    task_mock.execute.assert_called_once()
    call_kwargs = task_mock.execute.call_args.kwargs
    pd.testing.assert_frame_equal(call_kwargs["table"], expected_df)
    assert call_kwargs["task_config"] == task_config


async def test_profile_task_use_case_dataset_not_found(
    profile_task_use_case: ProfileTaskUseCase,
    dataset_crud_mock: MagicMock,
) -> None:
    dataset_id = uuid4()

    aid_config = AidConfig(
        algo_name=FdAlgoName.Aid,
        is_null_equal_null=True,
    )
    task_config = FdTaskConfig(primitive_name=PrimitiveName.fd, config=aid_config)

    dataset_crud_mock.get_by.side_effect = ResourceNotFoundException(
        "Dataset not found"
    )

    with pytest.raises(ResourceNotFoundException):
        await profile_task_use_case(dataset_id=dataset_id, config=task_config)

    dataset_crud_mock.get_by.assert_awaited_once_with(id=dataset_id)
