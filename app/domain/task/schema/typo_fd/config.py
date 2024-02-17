from enum import StrEnum, auto
from typing import Annotated
from pydantic import Field
from app.domain.task.schema.base_config import BaseTaskConfig


class MetricType(StrEnum):
    LEVENSHTEIN = auto()
    MODULUS_OF_DIFFERENCE = auto()


class TypoFDTaskConfig(BaseTaskConfig):
    error_threshold: Annotated[float, Field(ge=0, le=1)]
    max_lhs: Annotated[int, Field(ge=1, le=9)]
    threads_count: Annotated[int, Field(ge=1, le=8)]
    precise_algorithm: str
    approximate_algorithm: str
    type_of_metric: MetricType
    default_radius: Annotated[float, Field(ge=1, le=10)]
    default_ratio: Annotated[float, Field(ge=0, le=1)]
