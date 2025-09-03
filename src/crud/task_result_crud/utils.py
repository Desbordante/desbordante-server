from src.crud.task_result_crud.constants import query_helpers_map
from src.schemas.task_schemas.types import PrimitiveName


def get_query_helper_by_primitive_name(primitive_name: PrimitiveName):
    if query_helper := query_helpers_map.get(primitive_name):
        return query_helper()
    raise ValueError(f"Query helper for {primitive_name} primitive not found")
