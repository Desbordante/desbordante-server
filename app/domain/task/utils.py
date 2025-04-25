from typing import assert_never

from app.domain.task.schemas.fd.task import FdTask
from app.domain.task.schemas.fd.filter import FdFilter
from app.domain.task.schemas.fd.sort import FdFSorter

from app.domain.task.schemas.pfd.task import PfdTask
from app.domain.task.schemas.pfd.filter import PfdFilter
from app.domain.task.schemas.pfd.sort import PfdFSorter

from app.domain.task.schemas.afd.task import AfdTask
from app.domain.task.schemas.afd.filter import AfdFilter
from app.domain.task.schemas.afd.sort import AfdFSorter

from app.domain.task.schemas.afd_verification.task import AfdVerificationTask

from app.domain.task.schemas.dd.task import DdTask
from app.domain.task.schemas.dd.filter import DdFilter
from app.domain.task.schemas.dd.sort import DdFSorter

from app.domain.task.schemas.md.task import MdTask
from app.domain.task.schemas.md.filter import MdFilter

from app.domain.task.schemas.nar.task import NarTask
from app.domain.task.schemas.nar.filter import NarFilter
from app.domain.task.schemas.nar.sort import NarSorter


from app.domain.task.schemas.adc.task import AdcTask

from app.domain.task.schemas.ac.task import AcTask

from app.domain.task.schemas.types import PrimitiveName


def match_task_by_primitive_name(primitive_name: PrimitiveName):
    match primitive_name:
        case PrimitiveName.FD:
            return FdTask()
        case PrimitiveName.PFD:
            return PfdTask()
        case PrimitiveName.AFD:
            return AfdTask()
        case PrimitiveName.AFD_VERIFICATION:
            return AfdVerificationTask()
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


def match_filter_by_primitive_name(primitive_name: PrimitiveName):
    match primitive_name:
        case PrimitiveName.DD:
            return DdFilter()
        case PrimitiveName.MD:
            return MdFilter()
        case PrimitiveName.PFD:
            return PfdFilter()
        case PrimitiveName.FD:
            return FdFilter()
        case PrimitiveName.AFD:
            return AfdFilter()
        case PrimitiveName.NAR:
            return NarFilter()
    assert_never(primitive_name)

def match_sorter_by_primitive_name(primitive_name: PrimitiveName):
    match primitive_name:
        case PrimitiveName.FD:
            return FdFSorter()
        case PrimitiveName.PFD:
            return PfdFSorter()      
        case PrimitiveName.AFD:
            return AfdFSorter()
        case PrimitiveName.DD:
            return DdFSorter()
        # case PrimitiveName.MD:
        #     return MdFilter()
        case PrimitiveName.NAR:
            return NarSorter()
    assert_never(primitive_name)
