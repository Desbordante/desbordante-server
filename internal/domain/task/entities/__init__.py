from typing import assert_never

from internal.domain.task.entities.fd import FdTask
from internal.domain.task.entities.afd import AfdTask
from internal.domain.task.entities.ac import AcTask
from internal.domain.task.value_objects import PrimitiveName


def match_task_by_primitive_name(primitive_name: PrimitiveName):
    """
    Returns an instance of a task based on the given primitive name.

    Args:
        primitive_name (PrimitiveName): The name of the task primitive.

    Returns:
        object: An instance of the corresponding task (e.g., `FdTask`, `AfdTask`).

    Raises:
        AssertionError: If `primitive_name` does not match known task types.
    """
    match primitive_name:
        case PrimitiveName.fd:
            return FdTask()
        case PrimitiveName.afd:
            return AfdTask()
        case PrimitiveName.ac:
            return AcTask()
    assert_never(primitive_name)
