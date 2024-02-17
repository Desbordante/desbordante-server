from app.domain.task.schema.specific_with_deps_result import SpecificTaskWithDepsResult


class TypoFDTaskResult(SpecificTaskWithDepsResult):
    pk_column_indices: list[int] | None
