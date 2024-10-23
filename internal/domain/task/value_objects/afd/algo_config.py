from typing import Literal, Annotated, Union
from pydantic import Field

from internal.domain.common import OptionalModel
from internal.domain.task.value_objects.afd.algo_name import AfdAlgoName
from internal.domain.task.value_objects.afd.algo_descriptions import descriptions


class BaseAfdConfig(OptionalModel):
    __non_optional_fields__ = {
        "algo_name",
    }


class PyroConfig(BaseAfdConfig):
    algo_name: Literal[AfdAlgoName.Pyro]

    max_lhs: Annotated[int, Field(ge=1, le=10, description=descriptions["max_lhs"])]
    is_null_equal_null: Annotated[
        bool, Field(description=descriptions["is_null_equal_null"])
    ]
    error: Annotated[float, Field(ge=0, le=1, description=descriptions["error"])]
    threads: Annotated[int, Field(ge=1, le=8, description=descriptions["threads"])]
    seed: Annotated[int, Field(description=descriptions["seed"])]


class TaneConfig(BaseAfdConfig):
    algo_name: Literal[AfdAlgoName.Tane]

    max_lhs: Annotated[int, Field(ge=1, le=10, description=descriptions["max_lhs"])]
    is_null_equal_null: Annotated[
        bool, Field(description=descriptions["is_null_equal_null"])
    ]
    error: Annotated[float, Field(ge=0, le=1, description=descriptions["error"])]


OneOfAfdConfig = Annotated[
    Union[
        PyroConfig,
        TaneConfig,
    ],
    Field(discriminator="algo_name"),
]
