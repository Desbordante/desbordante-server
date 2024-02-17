from enum import StrEnum, auto
from app.domain.task.schema.base_result import BaseTaskResult


class SquashState(StrEnum):
    SQUASHED = auto()
    NOT_SQUASHED = auto()


class SpecificTypoClusterTaskResult(BaseTaskResult):
    suspicious_indices: list[int] | None
    sguash_state: SquashState
    sorted_cluster: str | None
    not_sorted_cluster: str | None
    items_amount: int | None
