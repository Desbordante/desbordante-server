from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )

    def serializable_dict(self):
        """Return a dict which contains only serializable fields."""
        default_dict = self.model_dump()

        return jsonable_encoder(default_dict)


class ApiErrorSchema(BaseSchema):
    detail: str
