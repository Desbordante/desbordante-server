from app.domain.task.schema.base_result import BaseTaskResult


class TypoClusterTaskResult(BaseTaskResult):
    typo_clusters: str | None
    suspicious_indices: list[int] | None
    clusters_count: int | None
