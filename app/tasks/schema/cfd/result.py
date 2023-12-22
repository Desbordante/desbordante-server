from app.tasks.schema.specific_with_deps_result import SpecificTaskWithDepsResult


class CFDTaskResult(SpecificTaskWithDepsResult):
    pk_column_indices: list[int] | None
    with_patterns: str | None
    without_patterns: str | None
    value_dictionary: dict[int, int] | None
