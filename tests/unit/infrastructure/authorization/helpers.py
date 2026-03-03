"""Helper functions for authorization policy tests."""

from src.domain.authorization.entities import Dataset, Task, User


def make_dataset(*, owner_id: int, is_public: bool) -> Dataset:
    return Dataset(owner_id=owner_id, is_public=is_public)


def make_task(*, owner_id: int, is_public: bool) -> Task:
    return Task(owner_id=owner_id, is_public=is_public)


def make_user(*, id: int, is_admin: bool = False) -> User:
    return User(id=id, is_admin=is_admin)
