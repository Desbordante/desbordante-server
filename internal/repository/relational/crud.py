from typing import Type

from sqlalchemy import select

from internal.infrastructure.data_storage.relational.model import ORMBaseModel
from internal.dto.repository.base_schema import (
    BaseCreateSchema,
    BaseUpdateSchema,
    BaseFindSchema,
    BaseResponseSchema,
)
from internal.infrastructure.data_storage import Context


class CRUD[
    ORMModel: ORMBaseModel,
    CreateSchema: BaseCreateSchema,
    UpdateSchema: BaseUpdateSchema,
    FindSchema: BaseFindSchema,
    ResponseSchema: BaseResponseSchema,
]:

    def __init__(
        self, orm_model: Type[ORMModel], response_schema: Type[ResponseSchema]
    ) -> None:

        self._orm_model: Type[ORMModel] = orm_model
        self._response_schema: Type[ResponseSchema] = response_schema

    def create(self, create_schema: CreateSchema, context: Context) -> ResponseSchema:
        create_schema_dict = create_schema.model_dump()
        db_model_instance = self._orm_model(**create_schema_dict)
        context.add(db_model_instance)
        context.flush()
        return self._response_schema.model_validate(db_model_instance)

    def _find(self, find_schema: FindSchema, context: Context) -> ORMModel | None:
        find_schema_dict = find_schema.model_dump()
        stmt = select(self._orm_model).filter_by(**find_schema_dict)
        db_model_instance = context.execute(stmt).scalars().one_or_none()
        return db_model_instance

    def find(self, find_schema: FindSchema, context: Context) -> ResponseSchema | None:
        db_model_instance = self._find(find_schema, context)
        response = (
            self._response_schema.model_validate(db_model_instance)
            if db_model_instance
            else None
        )
        return response

    def find_or_create(
        self,
        find_schema: FindSchema,
        create_schema: CreateSchema,
        context: Context,
    ) -> ResponseSchema:

        db_model_instance = self._find(find_schema, context)
        if not db_model_instance:
            db_model_instance = self.create(create_schema, context)
        return self._response_schema.model_validate(db_model_instance)

    def update(
        self,
        find_schema: FindSchema,
        update_schema: UpdateSchema,
        fields_to_update_if_none: set[str] | None,
        context: Context,
    ) -> ResponseSchema:

        db_model_instance = self._find(find_schema, context)
        update_schema_dict = update_schema.model_dump()
        fields_to_update_if_none = (
            fields_to_update_if_none if fields_to_update_if_none else set()
        )

        for key, value in update_schema_dict.items():
            if value is not None or key in fields_to_update_if_none:
                setattr(db_model_instance, key, value)

        context.add(db_model_instance)
        context.flush()

        return self._response_schema.model_validate(db_model_instance)

    def delete(
        self, find_schema: FindSchema, context: Context
    ) -> ResponseSchema | None:
        db_model_instance = self._find(find_schema, context)
        if not db_model_instance:
            return None
        context.delete(db_model_instance)
        context.flush()
        return self._response_schema.model_validate(db_model_instance)
