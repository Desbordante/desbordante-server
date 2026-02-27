import pytest

from src.domain.authorization.entities import Actor
from src.infrastructure.authorization.dataset_policy import DatasetPolicy
from src.infrastructure.authorization.task_policy import TaskPolicy
from src.infrastructure.authorization.user_policy import UserPolicy

from tests.unit.infrastructure.authorization.constants import ADMIN_USER_ID, USER_ID


@pytest.fixture
def anonymous_actor() -> Actor:
    return Actor(user_id=None, is_admin=False)


@pytest.fixture
def user_actor() -> Actor:
    return Actor(user_id=USER_ID, is_admin=False)


@pytest.fixture
def admin_actor() -> Actor:
    return Actor(user_id=ADMIN_USER_ID, is_admin=True)


@pytest.fixture
def dataset_policy() -> DatasetPolicy:
    return DatasetPolicy()


@pytest.fixture
def task_policy() -> TaskPolicy:
    return TaskPolicy()


@pytest.fixture
def user_policy() -> UserPolicy:
    return UserPolicy()
