from src.schemas.base_schemas import BaseSchema


class FdModel(BaseSchema):
    lhs: list[str]
    rhs: list[str]


FdTaskResult = list[FdModel]
