from app.domain.task.schema.fd import (
    TaneTask,
    TaneConfig,
    PyroConfig,
    PyroTask,
    FDAlgoResult,
)
from enum import StrEnum, auto


class TaskAlgoType(StrEnum):
    Pyro = auto()
    Tane = auto()


AFDAlgoResult = FDAlgoResult

__all__ = ["TaneTask", "TaneConfig", "PyroConfig", "PyroTask", "AFDAlgoResult"]
