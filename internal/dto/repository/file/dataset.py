from uuid import UUID

from internal.dto.repository.base_schema import BaseSchema, BaseCreateSchema, BaseUpdateSchema, \
    BaseResponseSchema, BaseFindSchema


class DatasetBaseSchema(BaseSchema):
    file_id: UUID
    separator: str
    header: list[int]
    is_built_in: bool = False


class DatasetCreateSchema(DatasetBaseSchema, BaseCreateSchema): ...


class DatasetUpdateSchema(DatasetBaseSchema, BaseUpdateSchema[UUID]): ...


class DatasetFindSchema(BaseFindSchema[UUID]): ...


class DatasetResponseSchema(DatasetBaseSchema, BaseResponseSchema[UUID]): ...
