from src.domain.task.primitives.ac import AcPrimitive
from src.domain.task.primitives.afd import AfdPrimitive
from src.domain.task.primitives.fd import FdPrimitive
from src.schemas.task_schemas.types import PrimitiveName

primitives_map = {
    PrimitiveName.FD: FdPrimitive,
    PrimitiveName.AFD: AfdPrimitive,
    PrimitiveName.AC: AcPrimitive,
}
