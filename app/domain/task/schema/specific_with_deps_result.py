from app.domain.task.schema.base_result import BaseTaskResult


class SpecificTaskWithDepsResult(BaseTaskResult):
    deps: str | None
    deps_amount: int | None
