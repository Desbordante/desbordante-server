from typing import assert_never

from app.domain.task.schemas.fd.task import FdTask
from app.domain.task.schemas.dd.task import DdTask
from app.domain.task.schemas.nar.task import NarTask
from app.domain.task.schemas.types import PrimitiveName


def match_task_by_primitive_name(primitive_name: PrimitiveName):
    match primitive_name:
        case PrimitiveName.FD:
            return FdTask()
        case PrimitiveName.NAR:
            return NarTask()
        case PrimitiveName.DD:
            return DdTask()
    assert_never(primitive_name)
