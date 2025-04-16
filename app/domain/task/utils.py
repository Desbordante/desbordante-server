from typing import assert_never

from app.domain.task.schemas.fd.task import FdTask
from app.domain.task.schemas.dd.task import DdTask
from app.domain.task.schemas.md.task import MdTask
from app.domain.task.schemas.nar.task import NarTask
from app.domain.task.schemas.adc.task import AdcTask
from app.domain.task.schemas.ac.task import AcTask
from app.domain.task.schemas.types import PrimitiveName


def match_task_by_primitive_name(primitive_name: PrimitiveName):
    match primitive_name:
        case PrimitiveName.FD:
            return FdTask()
        case PrimitiveName.NAR:
            return NarTask()
        case PrimitiveName.DD:
            return DdTask()
        case PrimitiveName.MD:
            return MdTask()
        case PrimitiveName.ADC:
            return AdcTask()
        case PrimitiveName.AC:
            return AcTask()
    assert_never(primitive_name)
