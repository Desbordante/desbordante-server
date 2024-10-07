import datetime

from pydantic import BaseModel, ConfigDict

from internal.domain.common import OptionalModel


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BaseCreateSchema(BaseSchema): ...


class BaseFindSchema[T](BaseSchema):
    id: T


class BaseUpdateSchema(BaseSchema, OptionalModel):
    __non_optional_fields__ = {
        "id",
    }


class BaseResponseSchema[T](BaseSchema):
    id: T

    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None
