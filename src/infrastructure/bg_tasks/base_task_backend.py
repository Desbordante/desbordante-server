"""Base backend for Celery task result storage with extensible result processing."""

from contextlib import contextmanager
from typing import Any, Iterator, Sequence
from uuid import UUID

from celery import states
from celery.backends.base import BaseBackend
from celery.backends.database import (  # type: ignore[import-untyped]
    retry,
    session_cleanup,
)
from celery.backends.database.session import (  # type: ignore[import-untyped]
    SessionManager,
)
from celery.exceptions import SoftTimeLimitExceeded, TimeLimitExceeded, WorkerLostError
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from src.models.base_models import BaseTaskModel
from src.schemas.base_schemas import (
    TaskErrorSchema,
    TaskFailureReason,
    TaskStatus,
)

EXCEPTION_TO_FAILURE_REASON: dict[str, TaskFailureReason] = {
    TimeLimitExceeded.__name__: TaskFailureReason.TIME_LIMIT_EXCEEDED,
    SoftTimeLimitExceeded.__name__: TaskFailureReason.TIME_LIMIT_EXCEEDED,
    MemoryError.__name__: TaskFailureReason.MEMORY_LIMIT_EXCEEDED,
    WorkerLostError.__name__: TaskFailureReason.WORKER_LOST,
}


def _map_exception_to_failure_reason(exc_type: str) -> TaskFailureReason:
    """Map exception type name to TaskFailureReason."""
    return EXCEPTION_TO_FAILURE_REASON.get(exc_type, TaskFailureReason.OTHER)


def _build_error_schema(
    result: dict[str, Any], meta: dict[str, Any]
) -> TaskErrorSchema:
    """Build TaskErrorSchema from exception result dict."""
    exc_type = result["exc_type"]
    return TaskErrorSchema(
        reason=_map_exception_to_failure_reason(exc_type),
        exc_type=exc_type,
        exc_module=result["exc_module"],
        exc_message=result["exc_message"],
        traceback=meta.get("traceback"),
    )


class BaseTaskBackend[T: BaseTaskModel](BaseBackend):
    """
    Base backend for storing Celery task results in database.

    Subclasses must set task_cls and may override _process_success_result
    to add extra entities (e.g. profiling_deps) when task succeeds.
    """

    task_cls: type[T]

    def __init__(self, url: str, **kwargs) -> None:
        super().__init__(url=url, **kwargs)
        self.url = url
        self.session_manager = SessionManager()

    def _get_session(self) -> Session:
        _, session = self.session_manager.create_session(dburi=self.url)
        return session()

    @contextmanager
    def _session(self) -> Iterator[Session]:
        session = self._get_session()
        with session_cleanup(session):
            yield session

    def _process_result(
        self,
        task_id: str,
        result: Any,
        state: str,
        meta: dict[str, Any],
    ) -> tuple[Any, Sequence[Any]]:
        """
        Transform raw result for storage based on task state.

        Returns (result_to_store, extra_entities_to_add).
        Override _process_success_result for custom SUCCESS handling.
        """
        if state == states.STARTED:
            # Celery tries to store worker name and pid in the result, but we don't want to store it
            return None, []
        if state in states.EXCEPTION_STATES:
            error = _build_error_schema(result, meta)
            return error, []
        if state == states.SUCCESS:
            return self._process_success_result(task_id, result)
        return result, []

    def _process_success_result(
        self, task_id: str, result: Any
    ) -> tuple[Any, Sequence[Any]]:
        """
        Process result when task succeeds. Override to add extra entities.

        Default: store result as-is, no extra entities.
        Example override: extract items, create ProfilingDepModel records.
        """
        return result, []

    @retry
    def _store_result(
        self,
        task_id: str,
        result: Any,
        state: str,
        traceback: str | None = None,
        request: Any = None,
        **kwargs: Any,
    ) -> None:
        """Store return value and state of an executed task."""
        with self._session() as session:
            meta = self._get_result_meta(  # type: ignore[attr-defined]
                result=result,
                state=state,
                traceback=traceback,
                request=request,
                format_date=False,
            )

            result_to_store, extra_entities = self._process_result(
                task_id=task_id,
                result=meta["result"],
                state=state,
                meta=meta,
            )

            stmt = (
                update(self.task_cls)
                .where(self.task_cls.id == UUID(task_id))
                .values(
                    status=TaskStatus(meta["status"]),
                    result=result_to_store,
                    finished_at=meta["date_done"],
                )
            )

            session.execute(stmt)
            session.add_all(extra_entities)
            session.commit()

    @retry
    def _get_task_meta_for(self, task_id: str) -> dict[str, Any]:
        """Get task meta-data for a task by id."""
        with self._session() as session:
            task = session.scalars(
                select(self.task_cls).where(self.task_cls.id == UUID(task_id))
            ).one()

            meta = {
                "status": task.status.value,
                "result": task.result,
                "date_done": task.finished_at,
                "traceback": None,
                "children": [],
            }

            return self.meta_from_decoded(meta)  # type: ignore[attr-defined]
