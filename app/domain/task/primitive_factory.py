from enum import StrEnum, auto
from app.domain.task.task_factory import TaskFactory, E, T

from typing import Iterable, TypeVar, TypeAlias


class PrimitiveName(StrEnum):
    fd = auto()
    # afd = auto()
    # ar = auto()
    # ac = auto()
    # fd_verification = auto()
    # mfd_verification = auto()
    # statistics = auto()
    # ucc = auto()
    # ucc_verification = auto()


F = TypeVar("F", bound=TaskFactory)

AnyTaskFactory: TypeAlias = TaskFactory[E, T]


class PrimitiveFactory:
    primitives: dict[PrimitiveName, AnyTaskFactory] = {}

    @classmethod
    def register(cls, name: PrimitiveName, factory: F) -> F:
        cls.primitives[name] = factory
        return factory

    @classmethod
    def get_by_name(cls, name: PrimitiveName) -> AnyTaskFactory:
        factory = cls.primitives.get(name, None)
        if not factory:
            raise ValueError(
                f"Can't find task factory by provided primitive name: {name}. Do you forgot to register it in PrimitiveFactory?"
            )
        return factory

    @classmethod
    def get_all(self) -> Iterable[AnyTaskFactory]:
        return list(self.primitives.values())
