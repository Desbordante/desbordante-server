from app.tasks.schema.base_task_result import BaseTaskResult


class SpecificTaskWithDepsResult(BaseTaskResult):
    deps: str | None
    deps_amount: int | None
