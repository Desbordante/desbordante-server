from __future__ import annotations
import pydantic
import typing


class OptionalFields[Model: pydantic.BaseModel]:
    """Generate a new class with all attributes (not-recursively) optionals.

    Example:
        class Item(BaseModel):
            name: str
            description: str
            price: float
            tax: float


        @app.post("/items", response_model=Item)
        async def post_item(item: OptionalFields[Item]):
            ...
    """

    def __new__(
        cls,
        *args: object,
        **kwargs: object,
    ) -> OptionalFields[Model]:
        """Cannot instantiate.

        Raises:
            TypeError: Direct instantiation not allowed.
        """
        raise TypeError("Cannot instantiate abstract OptionalFields class.")

    def __init_subclass__(
        cls,
        *args: object,
        **kwargs: object,
    ) -> typing.NoReturn:
        """Cannot subclass.

        Raises:
           TypeError: Subclassing not allowed.
        """
        raise TypeError("Cannot subclass {}.OptionalFields".format(cls.__module__))

    def __class_getitem__(
        cls,
        wrapped_class: type[Model],
    ) -> type[Model]:
        """Convert model to a partial model with all fields being optionals."""

        return pydantic.create_model(  # type: ignore[no-any-return, call-overload]
            f"{wrapped_class.__name__}WithOptionalFields",
            __base__=wrapped_class,
            __module__=wrapped_class.__module__,
            **{
                name: (info.annotation, None)  # type: ignore[assignment, valid-type]
                for name, info in wrapped_class.model_fields.items()
            },
        )
