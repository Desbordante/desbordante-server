from src.schemas.task_schemas.constants import filters_schemas_map
from src.schemas.task_schemas.types import PrimitiveName


def get_filters_schema_by_primitive_name(primitive_name: PrimitiveName):
    if filters_schema := filters_schemas_map.get(primitive_name):
        return filters_schema
    raise ValueError(f"Filters schema for {primitive_name} primitive not found")
