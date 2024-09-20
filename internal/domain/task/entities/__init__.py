from typing import assert_never

from internal.domain.task.entities.fd import FdTask
from internal.domain.task.entities.afd import AfdTask
from internal.domain.task.value_objects import PrimitiveName


def match_task_by_primitive_name(primitive_name: PrimitiveName):
    match primitive_name:
        case PrimitiveName.fd:
            return FdTask()
        case PrimitiveName.afd:
            return AfdTask()
    assert_never(primitive_name)
