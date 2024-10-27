from typing import Annotated, Union
from pydantic import Field

from internal.domain.task.value_objects.afd import AfdTaskConfig, AfdTaskResult
from internal.domain.task.value_objects.fd import FdTaskConfig, FdTaskResult
from internal.domain.task.value_objects.ac import AcTaskConfig, AcTaskResult
from internal.domain.task.value_objects.ind import IndTaskConfig, IndTaskResult
from internal.domain.task.value_objects.aind import AindTaskConfig, AindTaskResult
from internal.domain.task.value_objects.ar import ArTaskConfig, ArTaskResult

from internal.domain.task.value_objects.config import TaskConfig  # noqa: F401
from internal.domain.task.value_objects.result import TaskResult  # noqa: F401

from internal.domain.task.value_objects.primitive_name import (  # noqa: F401
    PrimitiveName,
)

from internal.domain.task.value_objects.task_status import TaskStatus  # noqa: F401
from internal.domain.task.value_objects.task_failure_reason import (  # noqa: F401
    TaskFailureReason,
)

from internal.domain.task.value_objects.incorrect_algo_exception import (  # noqa: F401
    IncorrectAlgorithmName,
)

OneOfTaskConfig = Annotated[
    Union[
        FdTaskConfig,
        AfdTaskConfig,
        AcTaskConfig,
        IndTaskConfig,
        AindTaskConfig,
        ArTaskConfig,
    ],
    Field(discriminator="primitive_name"),
]

OneOfTaskResult = Annotated[
    Union[
        FdTaskResult,
        AfdTaskResult,
        AcTaskResult,
        IndTaskResult,
        AindTaskResult,
        ArTaskResult,
    ],
    Field(discriminator="primitive_name"),
]
