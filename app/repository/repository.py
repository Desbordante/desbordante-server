from typing import Any, Generic, TypeVar
from uuid import UUID

from sqlalchemy import exc
from sqlmodel import Session, select

from app.exceptions.exceptions import (
    ResourceAlreadyExistsException,
    ResourceNotFoundException,
)
from app.models import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    """
    Generic base repository for CRUD operations.

    Attributes:
        model: The SQLModel model class
        session: Session for database operations
    """

    def __init__(self, model: type[ModelType], session: Session):
        self.model = model
        self._session = session

    def create(self, obj_in: ModelType) -> ModelType:
        """
        Create a new database record.

        Args:
            obj_in: Model instance to create

        Returns:
            Created model instance

        Raises:
            ResourceAlreadyExistsException: If record already exists
        """
        try:
            self._session.add(obj_in)
            self._session.commit()
            self._session.refresh(obj_in)
            return obj_in
        except exc.IntegrityError:
            self._session.rollback()
            raise ResourceAlreadyExistsException(
                f"{self.model.__name__} already exists"
            )

    def update(
        self, *, obj_current: ModelType, obj_new: dict[str, Any] | ModelType
    ) -> ModelType:
        """
        Update an existing record.

        Args:
            obj_current: Existing model instance to update
            obj_new: New data as dict or model instance

        Returns:
            Updated model instance
        """
        update_data = (
            obj_new
            if isinstance(obj_new, dict)
            else obj_new.model_dump(exclude_unset=True)
        )

        obj_current.sqlmodel_update(update_data)
        self._session.add(obj_current)
        self._session.commit()
        self._session.refresh(obj_current)
        return obj_current

    def get_by_id(self, id: int | UUID) -> ModelType:
        """
        Get a record by its ID.

        Args:
            id: Record ID (can be integer or UUID)

        Returns:
            Found model instance

        Raises:
            ResourceNotFoundException: When record with given ID is not found
        """
        statement = select(self.model).where(self.model.id == id)
        obj = self._session.exec(statement).first()
        if not obj:
            raise ResourceNotFoundException(
                f"{self.model.__name__} with id {id} not found"
            )
        return obj

    def get_by(self, *, field: str, value: Any) -> ModelType:
        """
        Get a record by any field value.

        Args:
            field: Model field name to filter by
            value: Value to search for

        Returns:
            Found model instance

        Raises:
            ValueError: When field doesn't exist in model
            ResourceNotFoundException: When record is not found
        """
        if not hasattr(self.model, field):
            raise ValueError(
                f"Field '{field}' does not exist in model {self.model.__name__}"
            )

        statement = select(self.model).where(getattr(self.model, field) == value)
        obj = self._session.exec(statement).first()
        if not obj:
            raise ResourceNotFoundException(
                f"{self.model.__name__} with {field} {value} not found"
            )
        return obj

    def delete(self, *, id: int | UUID) -> ModelType:
        """
        Delete a record by ID.

        Args:
            id: Record ID to delete

        Returns:
            Deleted model instance

        Raises:
            ResourceNotFoundException: When record with given ID is not found
        """
        obj = self.get_by_id(id)
        self._session.delete(obj)
        self._session.commit()
        return obj
