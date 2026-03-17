from uuid import UUID

from celery.backends.base import BaseBackend
from celery.backends.database import (  # type: ignore[import-untyped]
    retry,
    session_cleanup,
)
from celery.backends.database.session import (  # type: ignore[import-untyped]
    SessionManager,
)
from sqlalchemy import update
from sqlalchemy.orm import Session

from src.models.dataset_models import PreprocessingTaskModel
from src.schemas.base_schemas import CeleryTaskStatus


class PreprocessingTaskBackend(BaseBackend):
    task_cls = PreprocessingTaskModel

    def __init__(self, url: str, **kwargs):
        # The `url` argument was added later and is used by
        # the app to set backend by url (celery.app.backends.by_url)
        super().__init__(url=url, **kwargs)

        self.url = url
        self.session_manager = SessionManager()

    def _get_session(self) -> Session:
        engine, session = self.session_manager.create_session(dburi=self.url)
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

            stmt = (
                update(self.task_cls)
                .where(self.task_cls.id == UUID(task_id))
                .values(
                    status=CeleryTaskStatus(meta["status"]),
                    result=meta["result"],
                    finished_at=meta["date_done"],
                )
            )

            session.execute(stmt)

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
