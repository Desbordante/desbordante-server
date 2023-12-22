from app.tasks.schema.specific_with_deps_result import SpecificTaskWithDepsResult


class FDTaskResult(SpecificTaskWithDepsResult):
    pk_column_indices: list[int] | None
    without_patterns: str | None
