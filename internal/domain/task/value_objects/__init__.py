from typing import Annotated, Union
from pydantic import Field

from internal.domain.task.value_objects.afd import AfdTaskConfig, AfdTaskResult
from internal.domain.task.value_objects.fd import FdTaskConfig, FdTaskResult

from internal.domain.task.value_objects.config import TaskConfig
from internal.domain.task.value_objects.result import TaskResult

from internal.domain.task.value_objects.primitive_name import PrimitiveName

from internal.domain.task.value_objects.task_status import TaskStatus
from internal.domain.task.value_objects.task_failure_reason import TaskFailureReason

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
