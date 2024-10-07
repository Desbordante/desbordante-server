from typing import Annotated, Union
from pydantic import Field

from internal.domain.task.value_objects.afd import AfdTaskConfig, AfdTaskResult
from internal.domain.task.value_objects.fd import FdTaskConfig, FdTaskResult

from internal.domain.task.value_objects.config import TaskConfig  # noqa: F401
from internal.domain.task.value_objects.result import TaskResult  # noqa: F401

from internal.domain.task.value_objects.primitive_name import (  # noqa: F401
    PrimitiveName,
)

from internal.domain.task.value_objects.task_status import TaskStatus  # noqa: F401
from internal.domain.task.value_objects.task_failure_reason import (  # noqa: F401
    TaskFailureReason,
)

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
