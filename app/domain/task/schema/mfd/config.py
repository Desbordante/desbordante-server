from enum import StrEnum, auto
from app.domain.task.schema.base_config import BaseTaskConfig


class MFDMetrics(StrEnum):
    EUCLIDEAN = auto()
    LEVENSHTEIN = auto()
    MODULUS_OF_DIFFERENCE = auto()


class MFDMetricAlgorithm(StrEnum):
    BRUTE = auto()
    APPROX = auto()
    CALIPERS = auto()


class MFDTaskConfig(BaseTaskConfig):
    tolerance_parametr: float
    lhs_indices: list[int]
    rhs_indices: list[int]
    distance_to_null_is_infinity: bool
    type_of_metric: MFDMetrics
    q_gram_length: int
    metric_algorithm: MFDMetricAlgorithm
