from enum import StrEnum, auto


class TaskStatus(StrEnum):
    PENDING = auto()
    PROCESSING = auto()
    SUCCESS = auto()
    FAILED = auto()
