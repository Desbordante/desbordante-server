from typing import Literal, Annotated, Union
from pydantic import Field

from internal.domain.common import OptionalModel
from internal.domain.task.value_objects.afd.algo_name import AfdAlgoName


class BaseAfdConfig(OptionalModel):
    __non_optional_fields__ = {
        "algo_name",
    }


class PyroConfig(BaseAfdConfig):
    algo_name: Literal[AfdAlgoName.Pyro]

    is_null_equal_null: bool
    error: Annotated[float, Field(ge=0, le=1)]
    max_lhs: Annotated[int, Field(ge=1, le=10)]
    threads: Annotated[int, Field(ge=1, le=8)]
    seed: int


class TaneConfig(BaseAfdConfig):
    algo_name: Literal[AfdAlgoName.Tane]

    is_null_equal_null: bool
    error: Annotated[float, Field(ge=0, le=1)]
    max_lhs: Annotated[int, Field(ge=1, le=10)]


OneOfAfdConfig = Annotated[
    Union[
        PyroConfig,
        TaneConfig,
    ],
    Field(discriminator="algo_name"),
]
