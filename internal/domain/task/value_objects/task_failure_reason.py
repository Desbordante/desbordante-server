from enum import StrEnum, auto


class TaskFailureReason(StrEnum):
    MEMORY_LIMIT_EXCEEDED = auto()
    TIME_LIMIT_EXCEEDED = auto()
    WORKER_KILLED_BY_SIGNAL = auto()
    OTHER = auto()
