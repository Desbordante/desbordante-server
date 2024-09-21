from __future__ import annotations
from pydantic import BaseModel
from typing import Any


class OptionalModel(BaseModel):
    """
    A base model class that automatically sets all fields, except those defined in
    `__non_optional_fields__`, to `None` by default. This allows for the creation
    of model where fields are optional unless explicitly marked as required.

    Attributes:
        __non_optional_fields__ (set): A set of field names that should remain
        non-optional. Fields listed here will not have `None` as their default value.
    """

    __non_optional_fields__ = set()

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        """
        Class-level initializer that ensures all fields except those specified
        in `__non_optional_fields__` are set to `None` by default. This method
        is called during the subclass initialization process.

        Args:
            **kwargs: Arbitrary keyword arguments passed to the superclass initializer.
        Exceptions:
            ValueError: If a field listed in `__non_optional_fields__` has a default value of `None`.
        """
        super().__pydantic_init_subclass__(**kwargs)

        for field_name, value in cls.model_fields.items():
            if field_name in cls.__non_optional_fields__:
                if value.default is None:
                    raise ValueError(
                        f"Field '{field_name}' is in __non_optional_fields__ but has a default value of None."
                    )
                continue
            value.default = None

        cls.model_rebuild(force=True)
