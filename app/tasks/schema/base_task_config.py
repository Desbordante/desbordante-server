from enum import StrEnum, auto
from pydantic import BaseModel


class DBTaskPrimitiveType(StrEnum):
    AR = auto()
    CFD = auto()
    FD = auto()
    TypoFD = auto()
    TypoCluster = auto()
    SpecificTypoCluster = auto()
    Stats = auto()


class BaseTaskConfig(BaseModel):
    algorithm_name: str
    primitive_type: DBTaskPrimitiveType
