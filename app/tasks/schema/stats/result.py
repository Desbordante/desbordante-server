from app.tasks.schema.base_task_result import BaseTaskResult


class StatsTaskResult(BaseTaskResult):
    column_index: int
    type: str
    distinct: int | None
    is_categorical: bool | None
    count: int | None
    avg: str | None
    std: str | None
    skewness: str | None
    kurtosis: str | None
    min: str | None
    max: str | None
    sum: str | None
    quantile25: str | None
    quantile50: str | None
    quantile75: str | None
