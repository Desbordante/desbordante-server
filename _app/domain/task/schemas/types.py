from enum import StrEnum, auto


class PrimitiveName(StrEnum):
    FD = auto()
    DD = auto()
    MD = auto()
    NAR = auto()
    ADC = auto()
    AC = auto()


class TaskStatus(StrEnum):
    CREATED = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
