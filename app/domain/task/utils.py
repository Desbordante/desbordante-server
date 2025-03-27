from typing import assert_never

from app.domain.task.schemas.fd.task import FdTask
from app.domain.task.schemas.types import PrimitiveName


def match_task_by_primitive_name(primitive_name: PrimitiveName):
    match primitive_name:
        case PrimitiveName.FD:
            return FdTask()
    assert_never(primitive_name)
