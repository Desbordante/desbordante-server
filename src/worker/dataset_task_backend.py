"""DatasetTaskBackend: DatabaseBackend with DatasetTask (JSONB result)."""

import json

from celery.backends.database import DatabaseBackend  # type: ignore[import-untyped]

from src.models.dataset_models import DatasetTask


class DatasetTaskBackend(DatabaseBackend):
    """DatabaseBackend using DatasetTask with JSONB result. Uses Celery's TaskSet."""

    task_cls = DatasetTask

    def _update_result(self, task, result, state, traceback=None, request=None):
        meta = self._get_result_meta(
            result=result,
            state=state,
            traceback=traceback,
            request=request,
            format_date=False,
            encode=True,
        )
        columns = [
            col.name
            for col in self.task_cls.__table__.columns
            if col.name not in {"id", "task_id", "created_at", "updated_at"}
        ]
        for column in columns:
            value = meta.get(column)
            if column == "result" and isinstance(value, str):
                try:
                    value = json.loads(value) if value else None
                except (json.JSONDecodeError, TypeError):
                    pass
            setattr(task, column, value)
