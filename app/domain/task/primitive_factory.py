from enum import auto
from enum import StrEnum
from app.domain.task.task_factory import TaskFactory
from app.domain.task.fd import fd_factory
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

AnyTaskFactory: TypeAlias = TaskFactory


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
    def get_all(cls) -> Iterable[AnyTaskFactory]:
        return cls.primitives.values()

    @classmethod
    def get_names(cls) -> Iterable[PrimitiveName]:
        return cls.primitives.keys()


PrimitiveFactory.register(PrimitiveName.fd, fd_factory)
