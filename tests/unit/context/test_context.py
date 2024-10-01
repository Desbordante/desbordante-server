import pytest
from pytest_mock import MockerFixture
from internal.infrastructure.data_storage.flat import (
    FlatAddModel,
    FlatDeleteModel,
    FlatContext,
)
from internal.infrastructure.data_storage.relational import (
    RelationalAddModel,
    RelationalDeleteModel,
    RelationalContextType,
)
from internal.infrastructure.data_storage import (
    Context,
)


@pytest.fixture
def mock_postgres_context(mocker: MockerFixture):
    mock_context = mocker.Mock(spec=RelationalContextType)
    mock_context.commit = mocker.Mock()
    mock_context.rollback = mocker.Mock()
    mock_context.close = mocker.Mock()
    mock_context.flush = mocker.Mock()
    mock_context.add = mocker.Mock()
    mock_context.delete = mocker.Mock()
    mock_context.execute = mocker.Mock()
    return mock_context


@pytest.fixture
def mock_flat_context(mocker: MockerFixture):
    mock_context = mocker.Mock(spec=FlatContext)
    mock_context.commit = mocker.Mock()
    mock_context.rollback = mocker.Mock()
    mock_context.close = mocker.Mock()
    mock_context.flush = mocker.Mock()
    mock_context.add = mocker.Mock()
    mock_context.delete = mocker.Mock()
    mock_context.async_flush = mocker.AsyncMock()
    return mock_context


@pytest.fixture
def context(mock_postgres_context, mock_flat_context):
    return Context(mock_postgres_context, mock_flat_context)


def test_context_commit(context, mock_postgres_context, mock_flat_context):
    context.commit()
    mock_postgres_context.commit.assert_called_once()
    mock_flat_context.commit.assert_called_once()


def test_context_rollback(context, mock_postgres_context, mock_flat_context):
    context.rollback()
    mock_postgres_context.rollback.assert_called_once()
    mock_flat_context.rollback.assert_called_once()


def test_context_close(context, mock_postgres_context, mock_flat_context):
    context.close()
    mock_postgres_context.close.assert_called_once()
    mock_flat_context.close.assert_called_once()


def test_context_flush(context, mock_postgres_context, mock_flat_context):
    context.flush()
    mock_postgres_context.flush.assert_called_once()
    mock_flat_context.flush.assert_called_once()


@pytest.mark.asyncio
async def test_context_async_flush(
    mocker: MockerFixture, context, mock_postgres_context, mock_flat_context
):
    mock_flat_context.async_flush = mocker.AsyncMock()
    await context.async_flush()
    mock_postgres_context.flush.assert_called_once()
    mock_flat_context.async_flush.assert_called_once()
    mock_flat_context.flush.assert_not_called()


def test_context_add_relational_model(
    context, mock_postgres_context, mock_flat_context
):
    relational_model = RelationalAddModel()
    context.add(relational_model)
    mock_postgres_context.add.assert_called_once_with(relational_model)
    mock_flat_context.add.assert_not_called()


def test_context_add_flat_model(
    mocker: MockerFixture, context, mock_postgres_context, mock_flat_context
):
    flat_model = FlatAddModel(file=mocker.Mock(), file_name="test_file.txt")
    context.add(flat_model)
    mock_flat_context.add.assert_called_once_with(flat_model)
    mock_postgres_context.add.assert_not_called()


def test_context_delete_relational_model(
    context, mock_postgres_context, mock_flat_context
):
    relational_model = RelationalDeleteModel()
    context.delete(relational_model)
    mock_postgres_context.delete.assert_called_once_with(relational_model)
    mock_flat_context.delete.assert_not_called()


def test_context_delete_flat_model(context, mock_postgres_context, mock_flat_context):
    flat_model = FlatDeleteModel(file_name="test_file.txt")
    context.delete(flat_model)
    mock_flat_context.delete.assert_called_once_with(flat_model)
    mock_postgres_context.add.assert_not_called()


def test_context_execute(context, mock_postgres_context, mock_flat_context):
    query = "SELECT * FROM users"
    context.execute(query)
    mock_postgres_context.execute.assert_called_once_with(query)
    mock_postgres_context.add.assert_not_called()
