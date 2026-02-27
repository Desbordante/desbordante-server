import pytest

from src.domain.authorization.entities import Actor, Dataset, Task, User
from src.infrastructure.authorization.dataset_policy import DatasetPolicy
from src.infrastructure.authorization.task_policy import TaskPolicy
from src.infrastructure.authorization.user_policy import UserPolicy


@pytest.fixture
def anonymous_actor() -> Actor:
    return Actor(user_id=None, is_admin=False)


@pytest.fixture
def user_actor() -> Actor:
    return Actor(user_id=1, is_admin=False)


@pytest.fixture
def admin_actor() -> Actor:
    return Actor(user_id=2, is_admin=True)


@pytest.fixture
def dataset_policy() -> DatasetPolicy:
    return DatasetPolicy()


@pytest.fixture
def task_policy() -> TaskPolicy:
    return TaskPolicy()


@pytest.fixture
def user_policy() -> UserPolicy:
    return UserPolicy()


def make_dataset(*, owner_id: int, is_public: bool) -> Dataset:
    return Dataset(owner_id=owner_id, is_public=is_public)


def make_task(*, owner_id: int, is_public: bool) -> Task:
    return Task(owner_id=owner_id, is_public=is_public)


def make_user(*, id: int, is_admin: bool = False) -> User:
    return User(id=id, is_admin=is_admin)
