from typing import Literal, Annotated
from pydantic import Field
from internal.domain.common import OptionalModel
from internal.domain.task.value_objects.dd.algo_name import DdAlgoName
from internal.domain.task.value_objects.dd.algo_descriptions import descriptions


class BaseDdConfig(OptionalModel):
    __non_optional_fields__ = {
        "algo_name",
    }


class SplitConfig(BaseDdConfig):
    algo_name: Literal[DdAlgoName.Split]

    num_rows: Annotated[int, Field(ge=1, description=descriptions["num_rows"])]
    num_columns: Annotated[int, Field(ge=1, description=descriptions["num_columns"])]
    # TODO: diff table is not string
    difference_table: Annotated[
        str, Field(description=descriptions["difference_table"])
    ]


OneOfDdAlgoConfig = Annotated[
    SplitConfig,
    Field(discriminator="algo_name"),
]
