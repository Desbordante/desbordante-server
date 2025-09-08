from typing import Annotated, Literal, Union

from pydantic import Field

from src.schemas.base_schemas import BaseSchema
from src.schemas.task_schemas.primitives.mfd_verification.types import (
    MfdVerificationMetricAlgorithm,
    MfdVerificationMetrics,
)

from .algo_name import MfdVerificationAlgoName

LHS_INDICES = "LHS column indices"
RHS_INDICES = "RHS column indices"
PARAMETER = "Metric FD parameter"
DIST_FROM_NULL_IS_INFINITY = "Specify whether distance from NULL value is infinity"
NULL_EQUAL_DESC = "Whether two NULL values should be considered equal"

METRIC = ""
METRIC_ALGORITHM = ""
Q = ""


class BaseMfdVerificationConfig(BaseSchema):
    algo_name: Literal[MfdVerificationAlgoName.MetricVerifier]
    lhs_indices: list[int] = Field(..., description=LHS_INDICES)
    rhs_indices: list[int] = Field(..., description=RHS_INDICES)
    parameter: float = Field(1, ge=0, description="Parameter for the metric algorithm")
    dist_from_null_is_infinity: bool = Field(
        False,
        description=DIST_FROM_NULL_IS_INFINITY,
    )
    is_null_equal_null: bool = Field(False, description=NULL_EQUAL_DESC)
    metric_algorithm: MfdVerificationMetricAlgorithm = Field(
        ..., description=METRIC_ALGORITHM
    )


class MfdVerificationEuclideanConfig(BaseMfdVerificationConfig):
    metric: Literal[MfdVerificationMetrics.Euclidean] = Field(..., description=METRIC)


class MfdVerificationCosineConfig(BaseMfdVerificationConfig):
    metric: Literal[MfdVerificationMetrics.Cosine] = Field(..., description=METRIC)
    q: float = Field(1, ge=0, description=Q)


class MfdVerificationLevenshteinConfig(BaseMfdVerificationConfig):
    metric: Literal[MfdVerificationMetrics.Levenshtein] = Field(..., description=METRIC)


OneOfMfdVerificationAlgoConfig = Annotated[
    Union[
        MfdVerificationEuclideanConfig,
        MfdVerificationCosineConfig,
        MfdVerificationLevenshteinConfig,
    ],
    Field(discriminator="metric"),
]
