from typing import assert_never

from _app.domain.task.schemas.fd.task import FdTask
from _app.domain.task.schemas.fd.filter import FdFilter
from _app.domain.task.schemas.fd.sort import FdSorter

from _app.domain.task.schemas.pfd.task import PfdTask
from _app.domain.task.schemas.pfd.filter import PfdFilter
from _app.domain.task.schemas.pfd.sort import PfdSorter

from _app.domain.task.schemas.afd.task import AfdTask
from _app.domain.task.schemas.afd.filter import AfdFilter
from _app.domain.task.schemas.afd.sort import AfdSorter

from _app.domain.task.schemas.afd_verification.task import AfdVerificationTask
from _app.domain.task.schemas.afd_verification.filter import AfdVerificationFilter
from _app.domain.task.schemas.afd_verification.sort import AfdVerificationSorter

from _app.domain.task.schemas.dd.task import DdTask
from _app.domain.task.schemas.dd.filter import DdFilter
from _app.domain.task.schemas.dd.sort import DdSorter

from _app.domain.task.schemas.md.task import MdTask
from _app.domain.task.schemas.md.filter import MdFilter
from _app.domain.task.schemas.md.sort import MdSorter

from _app.domain.task.schemas.nar.task import NarTask
from _app.domain.task.schemas.nar.filter import NarFilter
from _app.domain.task.schemas.nar.sort import NarSorter

from _app.domain.task.schemas.adc.task import AdcTask
from _app.domain.task.schemas.adc.filter import AdcFilter
from _app.domain.task.schemas.adc.sort import AdcSorter

from _app.domain.task.schemas.ac.task import AcTask
from _app.domain.task.schemas.ac.filter import AcFilter
from _app.domain.task.schemas.ac.sort import AcSorter

from _app.domain.task.schemas.types import PrimitiveName


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
        case PrimitiveName.AFD_VERIFICATION:
            return AfdVerificationFilter()
        case PrimitiveName.NAR:
            return NarFilter()
        case PrimitiveName.ADC:
            return AdcFilter()
        case PrimitiveName.AC:
            return AcFilter()
    assert_never(primitive_name)


def match_sorter_by_primitive_name(primitive_name: PrimitiveName):
    match primitive_name:
        case PrimitiveName.FD:
            return FdSorter()
        case PrimitiveName.PFD:
            return PfdSorter()
        case PrimitiveName.AFD:
            return AfdSorter()
        case PrimitiveName.AFD_VERIFICATION:
            return AfdVerificationSorter()
        case PrimitiveName.DD:
            return DdSorter()
        case PrimitiveName.MD:
            return MdSorter()
        case PrimitiveName.NAR:
            return NarSorter()
        case PrimitiveName.AC:
            return AcSorter()
        case PrimitiveName.ADC:
            return AdcSorter()
    assert_never(primitive_name)
