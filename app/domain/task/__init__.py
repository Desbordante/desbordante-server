from app.domain.task.afd import AfdTask, AfdTaskConfig, AfdTaskResult
from app.domain.task.fd import FdTaskConfig, FdTaskResult
from typing import Annotated, Union, assert_never
from pydantic import Field
from app.domain.task.fd import FdTask
from app.domain.task.primitive_name import PrimitiveName


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


def match_task_by_primitive_name(primitive_name: PrimitiveName):
    match primitive_name:
        case PrimitiveName.fd:
            return FdTask()
        case PrimitiveName.afd:
            return AfdTask()
    assert_never(primitive_name)
