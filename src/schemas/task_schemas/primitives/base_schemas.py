from src.schemas.base_schemas import BaseSchema


class BaseTaskResultSchema(BaseSchema):
    total_count: int


class PrimitiveResultSchema[R: BaseSchema, I: BaseSchema](BaseSchema):
    result: R
    items: list[I]
