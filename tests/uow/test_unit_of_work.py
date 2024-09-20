import pytest
from pytest_mock import MockerFixture

from internal.uow import DataStorageContext, UnitOfWork
from internal.uow.uow import DataStorageContextMaker


@pytest.fixture
def context_mock(mocker: MockerFixture) -> DataStorageContext:
    return mocker.Mock(spec=DataStorageContext)


@pytest.fixture
def context_maker_mock(
    mocker: MockerFixture, context_mock: DataStorageContext
) -> DataStorageContextMaker:
    return mocker.Mock(spec=DataStorageContextMaker, return_value=context_mock)


def test_unit_of_work_commit_on_success(
    context_maker_mock: DataStorageContextMaker, context_mock: DataStorageContext
) -> None:
    uow = UnitOfWork(context_maker_mock)

    with uow as context:
        assert isinstance(context, DataStorageContext)
        pass

    context_mock.commit.assert_called_once()
    context_mock.rollback.assert_not_called()
    context_mock.close.assert_called_once()


def test_unit_of_work_rollback_on_failure(
    context_maker_mock: DataStorageContextMaker, context_mock: DataStorageContext
) -> None:
    uow = UnitOfWork(context_maker_mock)

    with pytest.raises(ValueError):
        with uow as context:
            assert isinstance(context, DataStorageContext)
            raise ValueError("Test error")

    context_mock.commit.assert_not_called()
    context_mock.rollback.assert_called_once()
    context_mock.close.assert_called_once()
