from enum import StrEnum, auto
from typing import Annotated, Union
from pydantic import Field

from internal.domain.task.value_objects.afd import AfdTaskConfig, AfdTaskResult
from internal.domain.task.value_objects.fd import FdTaskConfig, FdTaskResult

from internal.domain.task.value_objects.config import TaskConfig
from internal.domain.task.value_objects.result import TaskResult

from internal.domain.task.value_objects.primitive_name import PrimitiveName

class TaskStatus(StrEnum):
    FAILED = auto()
    CREATED = auto()
    RUNNING = auto()
    COMPLETED = auto()


class TaskFailureReason(StrEnum):
    MEMORY_LIMIT_EXCEEDED = auto()
    TIME_LIMIT_EXCEEDED = auto()
    WORKER_KILLED_BY_SIGNAL = auto()
    OTHER = auto()


OneOfTaskConfig = Annotated[
    Union[
        FdTaskConfig,
        AfdTaskConfig,
    ],
    Field(discriminator="primitive_name"),
]

OneOfTaskResult = Annotated[
    Union[
        FdTaskResult,
        AfdTaskResult,
    ],
    Field(discriminator="primitive_name"),
]
