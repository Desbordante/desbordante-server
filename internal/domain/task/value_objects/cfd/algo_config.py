from typing import Literal, Annotated
from pydantic import Field
from internal.domain.common import OptionalModel
from internal.domain.task.value_objects.cfd.algo_name import CfdAlgoName
from internal.domain.task.value_objects.cfd.algo_descriptions import descriptions


class BaseCfdConfig(OptionalModel):
    __non_optional_fields__ = {
        "algo_name",
    }


class FDFirstConfig(BaseCfdConfig):
    algo_name: Literal[CfdAlgoName.FDFirst]

    columns_number: Annotated[
        int, Field(ge=1, description=descriptions["columns_number"])
    ]
    cfd_minsup: Annotated[int, Field(ge=1, description=descriptions["cfd_minsup"])]
    cfd_minconf: Annotated[
        float, Field(ge=0, le=1, description=descriptions["cfd_minconf"])
    ]
    tuples_number: Annotated[
        int, Field(ge=1, description=descriptions["tuples_number"])
    ]
    cfd_max_lhs: Annotated[int, Field(ge=1, description=descriptions["cfd_max_lhs"])]
    cfd_substrategy: Annotated[
        str,
        Literal["dfs", "bfs"],
        Field(description=descriptions["cfd_substrategy"]),
    ]


OneOfCfdAlgoConfig = Annotated[
    FDFirstConfig,
    Field(discriminator="algo_name"),
]
