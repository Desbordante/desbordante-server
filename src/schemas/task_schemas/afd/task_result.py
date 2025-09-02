from src.schemas.base_schemas import BaseSchema


class AfdModel(BaseSchema):
    lhs: list[str]
    rhs: list[str]


AfdTaskResult = list[AfdModel]
