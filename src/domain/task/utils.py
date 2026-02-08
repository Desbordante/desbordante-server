from typing import assert_never

from src.domain.task.primitives.afd import AfdTask
from src.domain.task.primitives.fd import FdTask
from src.schemas.task_schemas.types import PrimitiveName


def match_task_by_primitive_name(primitive_name: PrimitiveName):
    match primitive_name:
        case PrimitiveName.fd:
            return FdTask()
        case PrimitiveName.afd:
            return AfdTask()
    assert_never(primitive_name)
