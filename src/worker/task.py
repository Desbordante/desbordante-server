import asyncio
from typing import Any
from uuid import UUID

from billiard.einfo import ExceptionInfo
from celery import Task

from src.crud.base_crud import BaseCrud
from src.db.session import scoped_session
from src.models.base_models import BaseModel
from src.schemas.base_schemas import TaskErrorSchema, TaskStatus

loop = asyncio.get_event_loop()


class DatabaseTaskBase[ModelType: BaseModel, IdType: int | UUID](Task):  # type: ignore
    """
    Base class for Celery tasks with automatic status management.

    Required attributes:
    - crud_class: CRUD class for DB operations

    Usage: @app.task(bind=True, base=DatabaseTaskBase)
    Entity access: self.entity (pre-loaded)
    """

    abstract = True

    crud_class: type[BaseCrud[ModelType, IdType]]
    status_field: str = "status"
    result_field: str = "result"
    entity: ModelType

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        id = args[0]
        self.entity = self._update_object(
            id, **{self.status_field: TaskStatus.Processing}
        )
        return self.run(*args, **kwargs)  # type: ignore

    def on_success(
        self, retval: Any, task_id: str, args: tuple[Any, ...], kwargs: dict[str, Any]
    ) -> None:
        id = args[0]

        self._update_object(
            id,
            **{
                self.status_field: TaskStatus.Success,
                self.result_field: self.create_result_object(id, retval),
            },
        )

    def on_failure(
        self,
        exc: Exception,
        task_id: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        einfo: ExceptionInfo,
    ) -> None:
        id = args[0]

        self._update_object(
            id,
            **{
                self.status_field: TaskStatus.Failed,
                self.result_field: self.create_error_object(id, exc),
            },
        )

    def create_result_object(self, id: IdType, retval: Any) -> Any:
        return retval

    def create_error_object(self, id: IdType, exc: Exception) -> Any:
        return TaskErrorSchema(error=str(exc))

    def _update_object(self, id: IdType, **kwargs: Any) -> ModelType:
        return loop.run_until_complete(self._update_object_async(id, **kwargs))

    async def _update_object_async(self, id: IdType, **kwargs: Any) -> ModelType:
        async with scoped_session() as session:
            crud = self.crud_class(session=session)
            entity = await crud.get_by(id=id)
            return await crud.update(entity=entity, **kwargs)
        raise RuntimeError("Failed to get database session")
