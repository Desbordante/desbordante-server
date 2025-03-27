from enum import StrEnum, auto


class PrimitiveName(StrEnum):
    FD = auto()


class TaskStatus(StrEnum):
    CREATED = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
