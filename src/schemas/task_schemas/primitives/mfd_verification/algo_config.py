from typing import Annotated, Literal, Union

from pydantic import Field

from src.schemas.base_schemas import BaseSchema
from src.schemas.task_schemas.primitives.mfd_verification.types import (
    MfdVerificationMetric,
    MfdVerificationMetricAlgorithm,
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


class MetricVerifierConfig(BaseSchema):
    algo_name: Literal[MfdVerificationAlgoName.MetricVerifier]
    lhs_indices: list[int] = Field(default=[0], description=LHS_INDICES)
    rhs_indices: list[int] = Field(default=[1], description=RHS_INDICES)
    parameter: float = Field(
        default=1, ge=0, description="Parameter for the metric algorithm"
    )
    dist_from_null_is_infinity: bool | None = Field(
        default=None,
        description=DIST_FROM_NULL_IS_INFINITY,
    )
    is_null_equal_null: bool | None = Field(default=None, description=NULL_EQUAL_DESC)
    metric_algorithm: MfdVerificationMetricAlgorithm = Field(
        default=MfdVerificationMetricAlgorithm.Brute, description=METRIC_ALGORITHM
    )
    metric: Literal[MfdVerificationMetric.Euclidean] = Field(
        default=MfdVerificationMetric.Euclidean, description=METRIC
    )


OneOfMfdVerificationAlgoConfig = Annotated[
    Union[MetricVerifierConfig],
    Field(discriminator="algo_name"),
]
