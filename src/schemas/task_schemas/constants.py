from src.schemas.task_schemas.ac.task_result import AcTaskResultFiltersSchema
from src.schemas.task_schemas.adc.task_result import AdcTaskResultFiltersSchema
from src.schemas.task_schemas.afd.task_result import AfdTaskResultFiltersSchema
from src.schemas.task_schemas.afd_verification.task_result import (
    AfdVerificationTaskResultFiltersSchema,
)
from src.schemas.task_schemas.ar.task_result import ArTaskResultFiltersSchema
from src.schemas.task_schemas.dd.task_result import DdTaskResultFiltersSchema
from src.schemas.task_schemas.fd.task_result import FdTaskResultFiltersSchema
from src.schemas.task_schemas.md.task_result import MdTaskResultFiltersSchema
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
}
