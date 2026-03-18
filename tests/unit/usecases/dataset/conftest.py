from io import BytesIO
from types import SimpleNamespace
from uuid import uuid4

import pytest
from pytest_mock import MockerFixture

from src.schemas.base_schemas import TaskStatus
from src.schemas.dataset_schemas import (
    DatasetSeparator,
    DatasetType,
    UploadTabularDatasetParams,
)
from src.usecases.dataset.upload_dataset import UploadDatasetUseCase

from tests.unit.usecases.dataset.constants import (
    FAKE_FILE_NAME,
    FAKE_FILE_SIZE,
    FAKE_USER_ID,
    STORAGE_LIMIT,
)


@pytest.fixture
def actor(mocker: MockerFixture):
    mock = mocker.Mock()
    mock.user_id = FAKE_USER_ID
    mock.is_admin = False
    return mock


@pytest.fixture
def file(mocker: MockerFixture):
    mock = mocker.Mock()
    mock.name = FAKE_FILE_NAME
    mock.size = FAKE_FILE_SIZE
    mock.data = BytesIO(b"col1,col2\n1,2\n3,4")
    mock.content_type = "text/csv"
    return mock


@pytest.fixture
def upload_params() -> UploadTabularDatasetParams:
    return UploadTabularDatasetParams(
        type=DatasetType.TABULAR,
        has_header=True,
        separator=DatasetSeparator.COMMA,
    )


@pytest.fixture
def dataset_crud_mock(mocker: MockerFixture, created_dataset):
    mock = mocker.Mock()
    mock.create_with_storage_check = mocker.AsyncMock(return_value=created_dataset)
    mock.update = mocker.AsyncMock()
    mock.delete = mocker.AsyncMock()
    return mock


@pytest.fixture
def storage_mock(mocker: MockerFixture):
    mock = mocker.Mock()
    mock.upload = mocker.AsyncMock()
    return mock


@pytest.fixture
def dataset_policy_mock(mocker: MockerFixture):
    mock = mocker.Mock()
    mock.can_create = mocker.Mock(return_value=True)
    return mock


@pytest.fixture
def settings_mock(mocker: MockerFixture):
    mock = mocker.Mock()
    mock.STORAGE_LIMIT = STORAGE_LIMIT
    return mock


@pytest.fixture
def preprocess_dataset_runner_mock(mocker: MockerFixture):
    mock = mocker.Mock()
    mock.run = mocker.Mock()
    return mock


@pytest.fixture
def user_stats_empty(mocker: MockerFixture):
    stats = mocker.Mock()
    stats.total_size = 0
    stats.total_count = 0
    return stats


@pytest.fixture
def created_dataset(upload_params: UploadTabularDatasetParams):
    preprocessing_id = uuid4()
    preprocessing = SimpleNamespace(
        status=TaskStatus.PENDING,
        result=None,
        id=preprocessing_id,
    )
    return SimpleNamespace(
        id=uuid4(),
        type=DatasetType.TABULAR,
        params=upload_params.model_dump(exclude={"type"}),
        path=f"{FAKE_USER_ID}/{uuid4()}",
        preprocessing=preprocessing,
    )


@pytest.fixture
def upload_dataset_use_case(
    dataset_crud_mock,
    storage_mock,
    dataset_policy_mock,
    settings_mock,
    preprocess_dataset_runner_mock,
) -> UploadDatasetUseCase:
    return UploadDatasetUseCase(
        dataset_crud=dataset_crud_mock,
        storage=storage_mock,
        dataset_policy=dataset_policy_mock,
        settings=settings_mock,
        preprocess_dataset_runner=preprocess_dataset_runner_mock,
    )
