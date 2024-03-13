from enum import StrEnum
from app.domain.task.abstract_task import AbstractTask
from typing import Generic, TypeVar, Iterable, Type

E = TypeVar("E", bound=StrEnum)
T = TypeVar("T", bound=AbstractTask)


class TaskFactory(Generic[E, T]):
    def __init__(self, key_enum: type[StrEnum]) -> None:
        self.tasks: dict[E, T] = {}
        self.key_enum = key_enum

    def register_task(self, task_type: E):
        def decorator(task_cls):
            self.tasks[task_type] = task_cls
            return task_cls

        return decorator

    def get_by_name(self, name: E) -> T:
        task = self.tasks.get(name, None)
        if not task:
            raise ValueError(
                f"Can't find task by provided algorithm name: {name}. Do you forgot to register it in TaskFactory?"
            )
        return task

    def get_all(self) -> Iterable[T]:
        return list(self.tasks.values())
