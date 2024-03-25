from __future__ import annotations
from pydantic import BaseModel
from typing import Any


class OptionalModel(BaseModel):
    __non_optional_fields__ = set()

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)

        for field in cls.model_fields.values():
            if field in cls.__non_optional_fields__:
                continue
            field.default = None

        cls.model_rebuild(force=True)
