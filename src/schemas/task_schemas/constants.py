from src.schemas.task_schemas.ac.task_result import AcTaskResultFiltersSchema
from src.schemas.task_schemas.afd.task_result import AfdTaskResultFiltersSchema
from src.schemas.task_schemas.fd.task_result import FdTaskResultFiltersSchema
from src.schemas.task_schemas.types import PrimitiveName

filters_schemas_map = {
    PrimitiveName.FD: FdTaskResultFiltersSchema,
    PrimitiveName.AFD: AfdTaskResultFiltersSchema,
    PrimitiveName.AC: AcTaskResultFiltersSchema,
}
