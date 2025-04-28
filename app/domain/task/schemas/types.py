from enum import StrEnum, auto


class PrimitiveName(StrEnum):
    FD = auto()
    PFD = auto()
    FD_VERIFICATION = auto()
    AFD = auto()
    AFD_VERIFICATION = auto()
    DD = auto()
    MD = auto()
    MFD_VERIFICATION = auto()
    NAR = auto()
    ADC = auto()
    AC = auto()


class SortOrder(StrEnum):
    ASC = auto()
    DESC = auto()


class TaskStatus(StrEnum):
    CREATED = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
