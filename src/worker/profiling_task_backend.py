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
from sqlalchemy import update
from sqlalchemy.orm import Session

from src.models.task_models import ProfilingDepModel, ProfilingTaskModel
from src.schemas.base_schemas import (
    TaskErrorSchema,
    TaskFailureReason,
    TaskStatus,
)


class ProfilingTaskBackend(BaseBackend):
    task_cls = ProfilingTaskModel

    def __init__(self, url: str, **kwargs):
        super().__init__(url=url, **kwargs)

        self.url = url
        self.session_manager = SessionManager()

    def _get_session(self) -> Session:
        _, session = self.session_manager.create_session(dburi=self.url)
        return session()

    @retry
    def _store_result(
        self,
        task_id: str,
        result,
        state: str,
        traceback: str | None = None,
        request=None,
        **kwargs,
    ) -> None:
        """Store return value and state of an executed task."""
        session = self._get_session()

        with session_cleanup(session):
            meta = self._get_result_meta(  # type: ignore[attr-defined]
                result=result,
                state=state,
                traceback=traceback,
                request=request,
                format_date=False,
            )

            result = meta["result"]
            profiling_deps = []

            if state == states.STARTED:
                result = None  # Celery tries to store worker name and pid in the result, but we don't want to store it
            elif state in states.EXCEPTION_STATES:
                exc_type = result["exc_type"]

                reason = TaskFailureReason.OTHER
                if exc_type in [
                    TimeLimitExceeded.__name__,
                    SoftTimeLimitExceeded.__name__,
                ]:
                    reason = TaskFailureReason.TIME_LIMIT_EXCEEDED
                elif exc_type == MemoryError.__name__:
                    reason = TaskFailureReason.MEMORY_LIMIT_EXCEEDED
                elif exc_type == WorkerLostError.__name__:
                    reason = TaskFailureReason.WORKER_LOST

                result = TaskErrorSchema(
                    reason=reason,
                    exc_type=exc_type,
                    exc_module=result["exc_module"],
                    exc_message=result["exc_message"],
                    traceback=meta["traceback"],
                )
            elif state == states.SUCCESS:
                profiling_deps = [
                    ProfilingDepModel(
                        task_id=task_id,
                        result=dep,
                    )
                    for dep in result.items
                ]
                result = result.result

            stmt = (
                update(self.task_cls)
                .where(self.task_cls.id == UUID(task_id))
                .values(
                    status=TaskStatus(meta["status"]),
                    result=result,
                    finished_at=meta["date_done"],
                )
            )

            session.execute(stmt)

            session.add_all(profiling_deps)

            session.commit()

    @retry
    def _get_task_meta_for(self, task_id: str):
        """Get task meta-data for a task by id."""
        session = self._get_session()

        with session_cleanup(session):
            task = (
                session.query(self.task_cls)
                .filter(self.task_cls.id == UUID(task_id))
                .one()
            )

            meta = {
                "status": task.status.value,
                "result": task.result,
                "date_done": task.finished_at,
                "traceback": None,
                "children": [],
            }

            return self.meta_from_decoded(meta)  # type: ignore[attr-defined]
