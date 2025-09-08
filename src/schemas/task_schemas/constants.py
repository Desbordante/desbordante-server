from src.schemas.task_schemas.primitives.ac.task_result import AcTaskResultFiltersSchema
from src.schemas.task_schemas.primitives.adc.task_result import (
    AdcTaskResultFiltersSchema,
)
from src.schemas.task_schemas.primitives.afd.task_result import (
    AfdTaskResultFiltersSchema,
)
from src.schemas.task_schemas.primitives.afd_verification.task_result import (
    AfdVerificationTaskResultFiltersSchema,
)
from src.schemas.task_schemas.primitives.ar.task_result import ArTaskResultFiltersSchema
from src.schemas.task_schemas.primitives.dd.task_result import DdTaskResultFiltersSchema
from src.schemas.task_schemas.primitives.fd.task_result import FdTaskResultFiltersSchema
from src.schemas.task_schemas.primitives.md.task_result import MdTaskResultFiltersSchema
from src.schemas.task_schemas.primitives.mfd_verification.task_result import (
    MfdVerificationTaskResultFiltersSchema,
)
from src.schemas.task_schemas.primitives.nar.task_result import (
    NarTaskResultFiltersSchema,
)
from src.schemas.task_schemas.primitives.pfd.task_result import (
    PfdTaskResultFiltersSchema,
)
from src.schemas.task_schemas.types import PrimitiveName

filters_schemas_map = {
    PrimitiveName.FD: FdTaskResultFiltersSchema,
    PrimitiveName.AFD: AfdTaskResultFiltersSchema,
    PrimitiveName.AC: AcTaskResultFiltersSchema,
    PrimitiveName.ADC: AdcTaskResultFiltersSchema,
    PrimitiveName.AFD_VERIFICATION: AfdVerificationTaskResultFiltersSchema,
    PrimitiveName.AR: ArTaskResultFiltersSchema,
    PrimitiveName.DD: DdTaskResultFiltersSchema,
    PrimitiveName.MD: MdTaskResultFiltersSchema,
    PrimitiveName.MFD_VERIFICATION: MfdVerificationTaskResultFiltersSchema,
    PrimitiveName.NAR: NarTaskResultFiltersSchema,
    PrimitiveName.PFD: PfdTaskResultFiltersSchema,
}
