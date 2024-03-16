from app.domain.task.primitive_factory import PrimitiveFactory, PrimitiveName
import pytest


@pytest.mark.parametrize(
    "primitive_name", [primitive_name.value for primitive_name in PrimitiveName]
)
def test_get_task_by_primitive_name(primitive_name: str):
    task_factory = PrimitiveFactory.get_by_name(primitive_name)
    for name in task_factory.enum_used_as_keys:
        task_factory.get_by_name(name.value)
