from typing import assert_never

from _app.domain.task.schemas.fd.task import FdTask
from _app.domain.task.schemas.nar.task import NarTask
from _app.domain.task.schemas.types import PrimitiveName


def match_task_by_primitive_name(primitive_name: PrimitiveName):
    match primitive_name:
        case PrimitiveName.FD:
            return FdTask()
        case PrimitiveName.NAR:
            return NarTask()
    assert_never(primitive_name)
