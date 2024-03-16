from enum import StrEnum
from app.domain.task.abstract_task import AnyTask
from typing import Iterable, Type

type AnyAlgoName = StrEnum


class TaskFactory[E: AnyAlgoName, T: AnyTask]:
    def __init__(self, enum_used_as_keys: Type[E], general_task_cls: Type[T]) -> None:
        self.tasks: dict[E, T] = {}
        self.enum_used_as_keys = enum_used_as_keys

        try:
            general_task_cls.result_model_cls
        except AttributeError:
            raise ValueError(
                "Attribute `result_model_cls` must be implemented in general class"
            )

        self.general_task_cls = general_task_cls

    def register_task(self, task_type: E):
        def decorator(task_cls: Type[AnyTask]):
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
        return self.tasks.values()

    def get_names(self) -> Iterable[E]:
        return self.tasks.keys()


type AnyTaskFactory = TaskFactory[AnyAlgoName, AnyTask]
