from src.domain.task.primitives.constants import primitives_map
from src.schemas.task_schemas.types import PrimitiveName


def get_primitive_class_by_name(primitive_name: PrimitiveName):
    if primitive_class := primitives_map.get(primitive_name):
        return primitive_class
    raise ValueError(f"Primitive {primitive_name} not found")
