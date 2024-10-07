from enum import StrEnum, auto


class TaskStatus(StrEnum):
    FAILED = auto()
    CREATED = auto()
    RUNNING = auto()
    COMPLETED = auto()
