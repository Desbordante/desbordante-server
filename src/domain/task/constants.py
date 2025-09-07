from src.domain.task.primitives.ac import AcPrimitive
from src.domain.task.primitives.adc import AdcPrimitive
from src.domain.task.primitives.afd import AfdPrimitive
from src.domain.task.primitives.afd_verification import AfdVerificationPrimitive
from src.domain.task.primitives.ar import ArPrimitive
from src.domain.task.primitives.dd import DdPrimitive
from src.domain.task.primitives.fd import FdPrimitive
from src.domain.task.primitives.md import MdPrimitive
from src.domain.task.primitives.mfd_verification import MfdVerificationPrimitive
from src.domain.task.primitives.nar import NarPrimitive
from src.domain.task.primitives.pfd import PfdPrimitive
from src.schemas.task_schemas.types import PrimitiveName

primitives_map = {
    PrimitiveName.FD: FdPrimitive,
    PrimitiveName.AFD: AfdPrimitive,
    PrimitiveName.AC: AcPrimitive,
    PrimitiveName.ADC: AdcPrimitive,
    PrimitiveName.AFD_VERIFICATION: AfdVerificationPrimitive,
    PrimitiveName.AR: ArPrimitive,
    PrimitiveName.DD: DdPrimitive,
    PrimitiveName.MD: MdPrimitive,
    PrimitiveName.MFD_VERIFICATION: MfdVerificationPrimitive,
    PrimitiveName.NAR: NarPrimitive,
    PrimitiveName.PFD: PfdPrimitive,
}
