"""Backend for profiling task result storage with profiling_deps."""

from typing import Any

from src.models.task_models import ProfilingDepModel, ProfilingTaskModel
from src.schemas.task_schemas.base_schemas import (
    OneOfTaskResultItemSchema,
    OneOfTaskResultSchema,
)
from src.schemas.task_schemas.primitives.base_schemas import PrimitiveResultSchema
from src.worker.base_task_backend import BaseTaskBackend


class ProfilingTaskBackend(BaseTaskBackend[ProfilingTaskModel]):
    task_cls = ProfilingTaskModel

    def _process_success_result(
        self,
        task_id: str,
        result: PrimitiveResultSchema[OneOfTaskResultSchema, OneOfTaskResultItemSchema],
    ) -> tuple[Any, list[ProfilingDepModel]]:
        """Extract profiling_deps from result.items and store aggregated result."""

        profiling_deps = [
            ProfilingDepModel(task_id=task_id, result=dep) for dep in result.items
        ]
        return result.result, profiling_deps
