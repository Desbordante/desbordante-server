from enum import StrEnum, auto

from app.schemas.schemas import BaseSchema


class PrimitiveName(StrEnum):
    FD = auto()


class TaskStatus(StrEnum):
    CREATED = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()


class OneOfTaskConfig(BaseSchema):
    primitive_name: PrimitiveName


class OneOfTaskResult(BaseSchema):
    primitive_name: PrimitiveName


class TaskCreate(OneOfTaskConfig):
    pass
